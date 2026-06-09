from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from academic_tracker.agent.deepseek_client import DeepSeekClient


@dataclass
class RouteResult:
    intent: str
    params: dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    message: str = ""


class NLRouter:
    """自然语言指令路由器：将任意用户输入分类到系统功能并提取参数。"""

    INTENTS = [
        "search",           # 单次论文检索
        "schedule",         # 创建定时任务
        "list_tasks",       # 查看任务列表
        "trigger_task",     # 触发指定任务
        "view_logs",        # 查看运行日志
        "view_reports",     # 查看历史报告
        "start_scheduler",  # 启动调度服务
        "help",             # 查看帮助/了解系统功能
        "exit",             # 退出
        "unrelated",        # 与本系统无关的请求
    ]

    def __init__(self) -> None:
        self.llm = DeepSeekClient()

    async def route(self, user_text: str) -> RouteResult:
        if not self.llm.available:
            return self._fallback_route(user_text)

        system_prompt = (
            "你是一个学术论文追踪系统的意图路由器。请分析用户输入，判断意图并提取参数。\n\n"
            "系统功能：\n"
            "1. search - 单次论文检索：用户描述研究方向，系统立即搜索论文并生成简报\n"
            "2. schedule - 创建定时任务：用户描述研究方向和周期，系统定期自动追踪\n"
            "3. list_tasks - 查看任务列表：查看已保存的追踪任务\n"
            "4. trigger_task - 触发指定任务：手动执行某个已保存的任务\n"
            "5. view_logs - 查看运行日志：查看任务执行历史\n"
            "6. view_reports - 查看历史报告：查看已生成的简报\n"
            "7. start_scheduler - 启动调度服务：启动后台定时任务调度\n"
            "8. help - 查看帮助：了解系统功能和使用方法\n"
            "9. exit - 退出：退出系统\n"
            "10. unrelated - 无关请求：与论文追踪完全无关的对话\n\n"
            "输出格式（严格JSON）：\n"
            '{"intent": "意图名", "params": {}, "message": "简短确认信息"}\n\n'
            "params说明：\n"
            "- search/schedule: params包含 query（用户的研究需求原文或提炼）\n"
            "- trigger_task: params包含 task_id（任务编号，可为null）\n"
            "- view_logs: params包含 task_id（可为null表示查看全部）\n"
            "- view_reports: params包含 limit（整数，可为null表示默认）\n"
            "- 其他意图: params为空对象 {}\n\n"
            "判断规则：\n"
            "- 用户描述研究内容（不论多详细），没有提到定时/周期/每周/每天等词 → search\n"
            "- 用户描述研究内容，同时提到定时/周期/每周/每天/创建任务等 → schedule\n"
            "- 用户说查看/显示/列出 任务 → list_tasks\n"
            "- 用户说执行/运行/触发 任务X（含数字） → trigger_task\n"
            "- 用户说查看/显示 日志/运行记录 → view_logs\n"
            "- 用户说查看/显示 报告/简报/历史 → view_reports\n"
            "- 用户说启动/开始 调度/服务 → start_scheduler\n"
            "- 用户问你能做什么/功能/帮助/介绍 → help\n"
            "- 用户说退出/结束/再见 → exit\n"
            "- 其他（如闲聊、问天气、写代码等）→ unrelated\n"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ]

        try:
            data = await self.llm.json_chat(messages, temperature=0.1)
            intent = data.get("intent", "search")
            if intent not in self.INTENTS:
                intent = "search"
            return RouteResult(
                intent=intent,
                params=data.get("params", {}),
                confidence=0.9,
                message=data.get("message", ""),
            )
        except Exception:
            return self._fallback_route(user_text)

    # ── rule-based fallback when DeepSeek is unavailable ──

    def _fallback_route(self, user_text: str) -> RouteResult:
        text = user_text.strip()

        # exit
        if text.lower() in {"exit", "quit", "q", "退出", "结束", "再见"}:
            return RouteResult(intent="exit")

        # help
        if text.lower() in {"help", "h", "?", "帮助"}:
            return RouteResult(intent="help")
        if any(kw in text for kw in ["你能做什么", "功能", "介绍", "帮助", "怎么用", "用途"]):
            return RouteResult(intent="help")

        # list_tasks
        task_kw = ["查看任务", "任务列表", "列出任务", "我的任务", "显示任务", "有哪些任务", "所有任务"]
        if any(kw in text for kw in task_kw):
            return RouteResult(intent="list_tasks")

        # view_logs
        log_kw = ["查看日志", "运行日志", "执行记录", "显示日志", "最近运行"]
        if any(kw in text for kw in log_kw):
            return RouteResult(intent="view_logs")

        # view_reports
        report_kw = ["查看报告", "历史报告", "我的简报", "显示报告", "我的报告", "生成的报告"]
        if any(kw in text for kw in report_kw):
            return RouteResult(intent="view_reports")

        # trigger_task — extract numeric id
        trigger_match = re.search(r"(?:执行|运行|触发|run)\s*(?:任务)?\s*#?\s*(\d+)", text)
        if trigger_match:
            return RouteResult(intent="trigger_task", params={"task_id": int(trigger_match.group(1))})

        # start_scheduler
        sched_kw = ["启动调度", "开始调度", "开启服务", "启动服务", "后台运行"]
        if any(kw in text for kw in sched_kw):
            return RouteResult(intent="start_scheduler")

        # schedule (periodic keywords)
        period_kw = ["定时", "周期", "每周", "每天", "每月", "创建任务", "schedule", "定期"]
        if any(kw in text for kw in period_kw):
            return RouteResult(intent="schedule", params={"query": text})

        # default: one-shot search
        return RouteResult(intent="search", params={"query": text})
