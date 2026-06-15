"""Web server providing REST API and static frontend for the Academic Tracker Agent."""

from __future__ import annotations

import asyncio
import json
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from academic_tracker.agent.graph import AcademicTrackerAgent
from academic_tracker.agent.nl_router import NLRouter, RouteResult
from academic_tracker.config.settings import get_settings
from academic_tracker.scheduler.task_scheduler import TaskScheduler, schedule_to_trigger
from academic_tracker.storage.database import get_database
from academic_tracker.storage.models import TaskConfig
from academic_tracker.utils.formatting import save_markdown_report

app = FastAPI(title="Academic Tracker Agent")

_agent = AcademicTrackerAgent()
_router = NLRouter()
_db = get_database()

_pending: dict[str, tuple[str, TaskConfig]] = {}

# ── request / response models ──

class ChatRequest(BaseModel):
    message: str
    session_id: str = ""

class ChatResponse(BaseModel):
    response: str
    intent: str
    type: str = "message"
    config: dict | None = None

class TaskItem(BaseModel):
    id: int
    research_direction: str
    schedule: str
    created_at: str

class ReportItem(BaseModel):
    id: int
    research_direction: str
    created_at: str
    preview: str

# ── chat ──

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    sid = req.session_id or str(uuid.uuid4())[:8]
    msg = req.message.strip()

    if msg == "__confirm__":
        return await _handle_confirm(sid)
    if msg == "__cancel__":
        _pending.pop(sid, None)
        return ChatResponse(response="已取消，配置未保存。", intent="cancel")
    if msg.startswith("__update_config__"):
        return await _handle_update_config(sid, msg)

    result = await _router.route(req.message)

    if result.intent in ("search", "schedule"):
        query = result.params.get("query", req.message)
        config = await _agent.parse_task(query)
        if result.intent == "schedule":
            config = _ensure_schedulable_web(config)
        _pending[sid] = (result.intent, config)
        return ChatResponse(
            response=_format_config_for_chat(config, result.intent),
            intent=result.intent,
            type="config_review",
            config=config.model_dump(),
        )

    response_text = await _execute_intent(result, req.message)
    return ChatResponse(response=response_text, intent=result.intent)


async def _handle_confirm(sid: str) -> ChatResponse:
    entry = _pending.pop(sid, None)
    if not entry:
        return ChatResponse(response="更新完成，未改变配置。", intent="unknown")
    intent, config = entry
    response_text = await _execute_config(intent, config)
    return ChatResponse(response=response_text, intent=intent)


async def _handle_update_config(sid: str, msg: str) -> ChatResponse:
    entry = _pending.get(sid)
    if not entry:
        return ChatResponse(response="更新完成，未改变配置。", intent="unknown")
    intent, _old = entry
    try:
        payload = json.loads(msg.removeprefix("__update_config__"))
        config = TaskConfig.model_validate(payload)
    except Exception:
        return ChatResponse(response="配置数据无效，请重新描述你的需求。", intent="unknown")
    _pending[sid] = (intent, config)
    return ChatResponse(
        response=_format_config_for_chat(config, intent),
        intent=intent,
        type="config_review",
        config=config.model_dump(),
    )


async def _execute_config(intent: str, config: TaskConfig) -> str:
    if intent == "search":
        report = await _agent.run(config, save_task_config=False)
        path = save_markdown_report(report.markdown, config.research_direction)
        excerpt = report.markdown[:3000]
        if len(report.markdown) > 3000:
            excerpt += "\n\n...(完整报告已保存)"
        return f"## 已生成简报\n\n报告已保存至 `{path}`\n\n{excerpt}"
    else:
        scheduler = TaskScheduler(agent=_agent, db=_db)
        task_id = scheduler.create_task(config)
        trigger = schedule_to_trigger(config.schedule)
        trigger_str = str(trigger) if trigger else "手动"
        return (f"## 已创建定时任务\n\n"
                f"- **任务 #{task_id}**\n"
                f"- 研究方向：{config.research_direction}\n"
                f"- 调度规则：{trigger_str}\n"
                f"- 数据源：{', '.join(config.sources)}\n"
                f"- 时间范围：近 {config.time_range_days} 天")


def _format_config_for_chat(config: TaskConfig, intent: str) -> str:
    action = "立即检索论文并生成简报" if intent == "search" else "保存定时任务"
    lines = [
        f"## 已解析任务配置（{action}）",
        "",
        "| 字段 | 值 |",
        "|------|-----|",
        f"| 研究方向 | {config.research_direction} |",
        f"| 关键词 | {', '.join(config.keywords) or '(无)'} |",
        f"| 数据源 | {', '.join(config.sources)} |",
        f"| 时间范围 | 近 {config.time_range_days} 天 |",
        f"| 排序类别 | {', '.join(config.categories)} |",
        f"| 每类篇数 | {config.top_n_per_category} |",
    ]
    if intent == "schedule":
        lines.append(f"| 定时规则 | {config.schedule} |")
    if config.venues:
        lines.append(f"| 会议/期刊 | {', '.join(config.venues)} |")
    lines.append("")
    lines.append("请选择：**确认执行** / **修改配置** / **取消**")
    return "\n".join(lines)

async def _execute_intent(result: RouteResult, user_text: str) -> str:
    intent = result.intent

    if intent == "search":
        query = result.params.get("query", user_text)
        config = await _agent.parse_task(query)
        with console_status("正在获取论文、排序并生成简报...") as _status:
            report = await _agent.run(config, save_task_config=False)
        path = save_markdown_report(report.markdown, config.research_direction)
        excerpt = report.markdown[:3000]
        if len(report.markdown) > 3000:
            excerpt += "\n\n…(完整报告已保存)"
        return f"## 已生成简报\n\n报告已保存至 `{path}`\n\n{excerpt}"

    elif intent == "schedule":
        query = result.params.get("query", user_text)
        config = await _agent.parse_task(query)
        config = _ensure_schedulable_web(config)
        scheduler = TaskScheduler(agent=_agent, db=_db)
        task_id = scheduler.create_task(config)
        trigger = schedule_to_trigger(config.schedule)
        trigger_str = str(trigger) if trigger else "手动"
        return f"## 已创建定时任务\n\n- **任务 #{task_id}**\n- 研究方向：{config.research_direction}\n- 调度规则：{trigger_str}\n- 数据源：{', '.join(config.sources)}\n- 时间范围：近 {config.time_range_days} 天"

    elif intent == "list_tasks":
        records = _db.list_task_configs(limit=50)
        if not records:
            return "当前没有已保存的追踪任务。"
        lines = ["## 任务列表\n"]
        for r in records:
            try:
                cfg = TaskConfig.model_validate_json(r.payload)
            except Exception:
                continue
            lines.append(f"- **#{r.id}** {cfg.research_direction} — 调度: {cfg.schedule} | 创建于 {r.created_at.strftime('%Y-%m-%d %H:%M')}")
        return "\n".join(lines)

    elif intent == "trigger_task":
        task_id = result.params.get("task_id")
        if task_id is None:
            return "请指定要触发的任务编号，例如：触发任务 #3"
        scheduler = TaskScheduler()
        try:
            exec_result = scheduler.run_now(int(task_id))
            path = exec_result.report_path
            excerpt = exec_result.report.markdown[:3000]
            if len(exec_result.report.markdown) > 3000:
                excerpt += "\n\n…(完整报告已保存)"
            return f"## 任务 #{task_id} 执行完成\n\n报告已保存至 `{path}`\n\n{excerpt}"
        except ValueError as e:
            return f"任务 #{task_id} 不存在。"
        except Exception as e:
            return f"执行任务 #{task_id} 时出错：{e}"

    elif intent == "view_logs":
        task_id = result.params.get("task_id")
        records = _db.list_task_runs(task_id=task_id, limit=20)
        if not records:
            return "暂无运行日志。"
        lines = ["## 最近运行日志\n"]
        for r in records:
            status_icon = "✅" if r.status == "success" else "❌" if r.status == "failed" else "⏳"
            lines.append(f"- {status_icon} **#{r.id}** (任务 #{r.task_id}) — {r.status} | {r.started_at.strftime('%m-%d %H:%M')} | {r.message[:60]}")
        return "\n".join(lines)

    elif intent == "view_reports":
        limit = result.params.get("limit") or 10
        records = _db.list_reports(limit=int(limit))
        if not records:
            return "暂无历史报告。"
        lines = ["## 历史报告\n"]
        for r in records:
            first_heading = next((line.strip("# ") for line in r.markdown.splitlines() if line.startswith("#")), "报告")
            lines.append(f"- **#{r.id}** {r.research_direction} — {r.created_at.strftime('%Y-%m-%d %H:%M')}\n  {first_heading[:80]}")
        return "\n".join(lines)

    elif intent == "start_scheduler":
        scheduler = TaskScheduler()
        restored = scheduler.restore_persisted_tasks()
        scheduler.start()
        return f"## 调度服务已启动\n\n已恢复 {restored} 个周期任务。服务将在后台持续运行。"

    elif intent == "help":
        return (
            "## Academic Tracker Agent\n\n"
            "我是一个学术论文自动追踪与简报生成助手。你可以用自然语言：\n\n"
            "- **搜索论文**：告诉我研究方向，我会从 arXiv 和 Semantic Scholar 获取最新论文并生成简报\n"
            "- **创建定时任务**：设置定期自动追踪，如「每周一早上追踪 RAG 方向的最新论文」\n"
            "- **查看任务**：查看已保存的追踪任务\n"
            "- **查看报告**：浏览历史生成的简报\n"
            "- **查看日志**：了解任务执行记录\n\n"
            "示例：「追踪最近一个月多模态大语言模型推理优化的高影响论文」"
        )

    elif intent == "unrelated":
        return (
            "## 系统功能简介\n\n"
            "我是一个**学术论文自动追踪与简报生成 Agent**，专注于帮助研究人员高效获取学术前沿信息。\n\n"
            "**我能做的事：**\n"
            "- 🔍 论文检索：描述研究方向，从 arXiv、Semantic Scholar 获取论文\n"
            "- ⏰ 定时追踪：创建定期任务，自动关注最新进展\n"
            "- 📊 简报生成：自动生成中文摘要与研究进展综述\n"
            "- 📋 任务管理：查看与管理已保存的追踪任务\n\n"
            "如果你有论文追踪相关的需求，随时告诉我！"
        )

    else:
        # fallback: treat as search
        return await _execute_intent(RouteResult(intent="search", params={"query": user_text}), user_text)


def _ensure_schedulable_web(config: TaskConfig) -> TaskConfig:
    """Web version: auto-assign a default schedule instead of prompting."""
    if config.schedule and config.schedule.lower() != "manual" and schedule_to_trigger(config.schedule):
        return config
    default = "weekly mon 08:00"
    return config.model_copy(update={"schedule": default})


# ── reports ──

@app.get("/api/reports", response_model=list[ReportItem])
async def list_reports(limit: int = 30):
    records = _db.list_reports(limit=limit)
    return [
        ReportItem(
            id=r.id,
            research_direction=r.research_direction,
            created_at=r.created_at.strftime("%Y-%m-%d %H:%M"),
            preview=next(
                (line.strip("# ") for line in r.markdown.splitlines() if line.startswith("#")), "报告"
            )[:80],
        )
        for r in records
    ]


@app.get("/api/reports/{report_id}")
async def get_report(report_id: int):
    record = _db.get_report(report_id)
    if not record:
        raise HTTPException(status_code=404, detail="报告不存在")
    return {
        "id": record.id,
        "research_direction": record.research_direction,
        "markdown": record.markdown,
        "created_at": record.created_at.strftime("%Y-%m-%d %H:%M"),
    }


@app.delete("/api/reports/{report_id}")
async def delete_report(report_id: int):
    deleted = _db.delete_report(report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="报告不存在")
    return {"ok": True, "deleted_id": report_id}


# ── tasks ──

@app.get("/api/tasks", response_model=list[TaskItem])
async def list_tasks():
    records = _db.list_task_configs(limit=100)
    items: list[TaskItem] = []
    for r in records:
        try:
            cfg = TaskConfig.model_validate_json(r.payload)
        except Exception:
            continue
        items.append(
            TaskItem(
                id=r.id,
                research_direction=cfg.research_direction,
                schedule=cfg.schedule,
                created_at=r.created_at.strftime("%Y-%m-%d %H:%M"),
            )
        )
    return items


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):
    scheduler = TaskScheduler()
    scheduler.remove_task(str(task_id))
    deleted = _db.delete_task_config(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="任务不存在")
    return {"ok": True, "deleted_id": task_id}


# ── static frontend ──

@app.get("/")
async def root():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


def console_status(msg: str):
    """Dummy context manager that just yields — used in web context where console isn't shown."""
    class _DummyStatus:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
    return _DummyStatus()
