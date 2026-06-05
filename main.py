from __future__ import annotations

import argparse
import asyncio
import os
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from academic_tracker.storage.database import get_database
from academic_tracker.storage.models import TaskConfig
from academic_tracker.utils.formatting import save_markdown_report

console = Console()


async def run_once(user_text: str, assume_yes: bool = False) -> None:
    from academic_tracker.agent.graph import AcademicTrackerAgent

    agent = AcademicTrackerAgent()
    config = await agent.parse_task(user_text)
    console.print(Panel.fit(config.model_dump_json(indent=2), title="解析得到的任务配置"))
    if not assume_yes and not Confirm.ask("是否按该配置立即获取论文并生成简报？", default=True):
        console.print("已取消执行。")
        return
    with console.status("正在获取论文、排序并生成简报..."):
        report = await agent.run(config)
    path = save_markdown_report(report.markdown, config.research_direction)
    console.print(Panel(report.markdown[:4000] + ("\n\n..." if len(report.markdown) > 4000 else ""), title="报告预览"))
    console.print(f"完整报告已保存到：[bold]{path}[/bold]")


async def add_scheduled_task(user_text: str | None = None, assume_yes: bool = False) -> None:
    from academic_tracker.agent.graph import AcademicTrackerAgent
    from academic_tracker.scheduler.task_scheduler import TaskScheduler

    agent = AcademicTrackerAgent()
    scheduler = TaskScheduler(agent=agent, db=agent.db)
    query = user_text or Prompt.ask("请输入你的周期论文追踪需求")
    config = await agent.parse_task(query)
    config = _ensure_schedulable_config(config)
    console.print(Panel.fit(config.model_dump_json(indent=2), title="将保存的定时任务配置"))
    if not assume_yes and not Confirm.ask("是否保存该定时任务？", default=True):
        console.print("已取消保存。")
        return
    task_id = scheduler.create_task(config)
    from academic_tracker.scheduler.task_scheduler import schedule_to_trigger

    trigger = schedule_to_trigger(config.schedule)
    console.print(f"已保存任务 [bold]#{task_id}[/bold]：{config.research_direction}")
    if trigger:
        console.print(f"调度规则：{trigger}")
    console.print("运行 `python main.py scheduler` 可启动常驻调度服务。")


def _ensure_schedulable_config(config: TaskConfig) -> TaskConfig:
    from academic_tracker.scheduler.task_scheduler import schedule_to_trigger

    if config.schedule and config.schedule.lower() != "manual" and schedule_to_trigger(config.schedule):
        return config
    console.print("当前任务未包含可识别的周期规则。示例：weekly mon 08:00、每天 09:00、cron: 0 8 * * mon")
    schedule = Prompt.ask("请输入定时规则", default="weekly mon 08:00")
    return config.model_copy(update={"schedule": schedule})


def run_task_now(task_id: int) -> None:
    from academic_tracker.scheduler.task_scheduler import TaskScheduler

    scheduler = TaskScheduler()
    with console.status(f"正在手动触发任务 #{task_id}..."):
        result = scheduler.run_now(task_id)
    console.print(Panel(result.report.markdown[:4000] + ("\n\n..." if len(result.report.markdown) > 4000 else ""), title="报告预览"))
    console.print(f"完整报告已保存到：[bold]{result.report_path}[/bold]")


def start_scheduler_service() -> None:
    from academic_tracker.scheduler.task_scheduler import TaskScheduler

    scheduler = TaskScheduler()
    restored = scheduler.restore_persisted_tasks()
    scheduler.start()
    console.print(f"已启动定时调度服务，恢复 [bold]{restored}[/bold] 个周期任务。按 Ctrl+C 退出。")
    _print_scheduler_jobs(scheduler)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()
        console.print("调度服务已停止。")


def open_interactive_ui() -> None:
    _print_agent_banner()
    _print_agent_help(compact=True)
    while True:
        try:
            user_text = Prompt.ask("[bold cyan]tracker[/bold cyan] [dim]›[/dim]", default="").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n会话已结束。")
            return

        if not user_text:
            continue

        should_exit = _handle_agent_command(user_text)
        if should_exit:
            return


def _print_agent_banner() -> None:
    banner = "\n".join(
        [
            "[bold white]Academic Tracker Agent[/bold white]",
            "[dim]Natural-language paper intelligence console[/dim]",
        ]
    )
    console.print(Panel.fit(banner, border_style="cyan", padding=(1, 4)))


def _print_agent_help(compact: bool = False) -> None:
    table = Table(show_header=True, header_style="bold cyan", box=None, pad_edge=False)
    table.add_column("输入方式", style="bold white", no_wrap=True)
    table.add_column("作用", style="dim")
    rows = [
        ("直接输入研究需求", "立即解析需求、抓取论文并生成简报"),
        ("task <周期追踪需求>", "创建持久化定时追踪任务"),
        ("tasks", "查看已保存任务"),
        ("run-task <id>", "立即触发一个已有任务"),
        ("logs [task_id]", "查看最近运行日志，可按任务过滤"),
        ("reports [limit]", "查看历史报告"),
        ("scheduler", "启动常驻调度服务"),
        ("help / exit", "查看帮助或退出会话"),
    ]
    for command, description in rows:
        table.add_row(command, description)
    title = "可用指令" if not compact else "试着输入：追踪最近 30 天 RAG 与长上下文推理的高影响论文"
    console.print(Panel(table, title=title, border_style="bright_black"))


def _handle_agent_command(user_text: str) -> bool:
    normalized = user_text.strip()
    command = normalized.lower()

    if command in {"exit", "quit", "q", ":q", "bye", "退出"}:
        console.print("会话已结束。")
        return True

    if command in {"help", "h", "?", "帮助"}:
        _print_agent_help()
        return False

    if command in {"tasks", "task list", "list-tasks", "任务", "任务列表"}:
        print_task_list()
        return False

    if command == "logs" or command.startswith("logs "):
        print_run_logs(_optional_int_arg(normalized, "logs"))
        return False

    if command == "reports" or command.startswith("reports "):
        print_reports(_optional_int_arg(normalized, "reports") or 10)
        return False

    if command in {"scheduler", "serve", "service", "调度", "启动调度"}:
        start_scheduler_service()
        return False

    task_text = _strip_command_prefix(normalized, ["task", "schedule", "定时", "周期"])
    if task_text is not None:
        if not task_text:
            task_text = Prompt.ask("请输入你的周期论文追踪需求")
        asyncio.run(add_scheduled_task(task_text))
        return False

    task_id = _task_id_from_run_command(normalized)
    if task_id is not None:
        run_task_now(task_id)
        return False

    asyncio.run(run_once(normalized))
    return False


def _strip_command_prefix(text: str, prefixes: list[str]) -> str | None:
    lowered = text.lower()
    for prefix in prefixes:
        if lowered == prefix:
            return ""
        marker = f"{prefix} "
        if lowered.startswith(marker):
            return text[len(marker) :].strip()
    return None


def _optional_int_arg(text: str, command: str) -> int | None:
    tail = text[len(command) :].strip()
    if not tail:
        return None
    if tail.startswith("#"):
        tail = tail[1:].strip()
    try:
        return int(tail)
    except ValueError:
        console.print(f"[yellow]无法识别参数：{tail}。将显示默认范围。[/yellow]")
        return None


def _task_id_from_run_command(text: str) -> int | None:
    lowered = text.lower()
    for prefix in ["run-task", "run task", "run", "触发", "运行"]:
        if lowered == prefix:
            return IntPrompt.ask("请输入任务 ID")
        marker = f"{prefix} "
        if lowered.startswith(marker):
            candidate = text[len(marker) :].strip().lstrip("#")
            if candidate.isdigit():
                return int(candidate)
    return None


def print_task_list() -> None:
    db = get_database()
    records = db.list_task_configs(limit=50)
    table = Table(title="任务列表", show_header=True, header_style="bold cyan")
    table.add_column("ID", justify="right")
    table.add_column("研究方向")
    table.add_column("定时规则")
    table.add_column("创建时间")
    for record in records:
        config = TaskConfig.model_validate_json(record.payload)
        table.add_row(str(record.id), config.research_direction, config.schedule, record.created_at.strftime("%Y-%m-%d %H:%M"))
    console.print(table if records else "暂无任务。")


def print_run_logs(task_id: int | None = None) -> None:
    db = get_database()
    records = db.list_task_runs(task_id=task_id, limit=20)
    table = Table(title="最近运行日志", show_header=True, header_style="bold cyan")
    table.add_column("ID", justify="right")
    table.add_column("任务", justify="right")
    table.add_column("状态")
    table.add_column("开始时间")
    table.add_column("结束时间")
    table.add_column("信息")
    for record in records:
        table.add_row(
            str(record.id),
            str(record.task_id),
            record.status,
            record.started_at.strftime("%Y-%m-%d %H:%M:%S"),
            record.finished_at.strftime("%Y-%m-%d %H:%M:%S") if record.finished_at else "-",
            record.message[:80],
        )
    console.print(table if records else "暂无运行日志。")


def print_reports(limit: int = 10) -> None:
    db = get_database()
    records = db.list_reports(limit=limit)
    table = Table(title="历史报告", show_header=True, header_style="bold cyan")
    table.add_column("ID", justify="right")
    table.add_column("研究方向")
    table.add_column("生成时间")
    table.add_column("预览")
    for record in records:
        first_heading = next((line.strip("# ") for line in record.markdown.splitlines() if line.startswith("#")), "报告")
        table.add_row(str(record.id), record.research_direction, record.created_at.strftime("%Y-%m-%d %H:%M"), first_heading[:60])
    console.print(table if records else "暂无历史报告。")


def _print_scheduler_jobs(scheduler: TaskScheduler) -> None:
    jobs = scheduler.list_jobs()
    table = Table(title="已注册调度任务", show_header=True, header_style="bold cyan")
    table.add_column("任务 ID", justify="right")
    table.add_column("下次运行")
    table.add_column("触发器")
    for job in jobs:
        table.add_row(job["id"], job["next_run_time"], job["trigger"])
    console.print(table if jobs else "没有可调度任务。")


def init_env_file(api_key: str | None = None) -> None:
    env_path = Path(".env")
    if env_path.exists():
        console.print(".env 已存在，不会覆盖。")
        return
    key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
    env_path.write_text(
        "\n".join(
            [
                f"DEEPSEEK_API_KEY={key}",
                "DEEPSEEK_BASE_URL=https://api.deepseek.com",
                "DEEPSEEK_MODEL=deepseek-chat",
                "SEMANTIC_SCHOLAR_API_KEY=",
                "DATABASE_URL=sqlite:///data/academic_tracker.db",
                "REPORT_DIR=reports",
                "DEFAULT_MAX_RESULTS=30",
                "",
            ]
        ),
        encoding="utf-8",
    )
    console.print("已创建 .env。请确认其中的 DEEPSEEK_API_KEY。")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="学术论文自动追踪与简报生成 Agent")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="按自然语言任务立即生成一份简报")
    run_parser.add_argument("query", nargs="?", help="自然语言研究追踪任务")
    run_parser.add_argument("-y", "--yes", action="store_true", help="跳过配置确认")

    task_parser = subparsers.add_parser("task", help="新增一个持久化定时任务")
    task_parser.add_argument("query", nargs="?", help="自然语言周期追踪任务")
    task_parser.add_argument("-y", "--yes", action="store_true", help="跳过配置确认")

    run_task_parser = subparsers.add_parser("run-task", help="立即触发一个已保存任务")
    run_task_parser.add_argument("task_id", type=int, help="任务 ID")

    subparsers.add_parser("list-tasks", help="查看已保存任务")
    subparsers.add_parser("logs", help="查看任务运行日志")
    subparsers.add_parser("reports", help="查看历史报告")
    subparsers.add_parser("scheduler", help="启动常驻定时调度服务")
    subparsers.add_parser("ui", help="打开 Agent Console，自然语言和命令式混合交互")

    init_parser = subparsers.add_parser("init-env", help="创建 .env 配置文件")
    init_parser.add_argument("--api-key", default=None, help="DeepSeek API Key，不建议在共享终端历史中使用")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "init-env":
        init_env_file(args.api_key)
        return
    if args.command == "run":
        query = args.query or Prompt.ask("请输入你的论文追踪需求")
        asyncio.run(run_once(query, assume_yes=args.yes))
        return
    if args.command == "task":
        asyncio.run(add_scheduled_task(args.query, assume_yes=args.yes))
        return
    if args.command == "run-task":
        run_task_now(args.task_id)
        return
    if args.command == "list-tasks":
        print_task_list()
        return
    if args.command == "logs":
        print_run_logs()
        return
    if args.command == "reports":
        print_reports()
        return
    if args.command == "scheduler":
        start_scheduler_service()
        return
    if args.command == "ui":
        open_interactive_ui()
        return
    parser.print_help()


if __name__ == "__main__":
    main()
