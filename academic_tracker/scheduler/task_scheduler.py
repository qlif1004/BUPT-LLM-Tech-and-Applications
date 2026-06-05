from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.base import BaseTrigger

from academic_tracker.storage.database import Database, get_database
from academic_tracker.storage.models import Report, TaskConfig
from academic_tracker.utils.formatting import save_markdown_report

if TYPE_CHECKING:
    from academic_tracker.agent.graph import AcademicTrackerAgent


@dataclass
class ScheduledTask:
    task_id: str
    config: TaskConfig


@dataclass
class TaskExecutionResult:
    report: Report
    report_path: str
    report_id: int | None = None


class TaskScheduler:
    def __init__(self, agent: AcademicTrackerAgent | None = None, db: Database | None = None) -> None:
        if agent is None:
            from academic_tracker.agent.graph import AcademicTrackerAgent

            agent = AcademicTrackerAgent()
        self.agent = agent
        self.db = db or get_database()
        self.scheduler = BackgroundScheduler(timezone="Asia/Shanghai")

    def start(self) -> None:
        if not self.scheduler.running:
            self.scheduler.start()

    def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown()

    def restore_persisted_tasks(self) -> int:
        count = 0
        for record in self.db.list_task_configs(scheduled_only=True):
            config = TaskConfig.model_validate_json(record.payload)
            if self.add_task(str(record.id), config):
                count += 1
        return count

    def create_task(self, config: TaskConfig) -> int:
        task_id = self.db.save_task_config(config)
        self.add_task(str(task_id), config)
        return task_id

    def add_task(self, task_id: str, config: TaskConfig) -> bool:
        trigger = schedule_to_trigger(config.schedule)
        if not trigger:
            return False
        self.scheduler.add_job(
            self._run_config,
            trigger=trigger,
            args=[int(task_id), config],
            id=task_id,
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        return True

    def add_weekly_task(self, task_id: str, config: TaskConfig, day_of_week: str = "mon", hour: int = 8) -> None:
        self.scheduler.add_job(
            self._run_config,
            trigger=CronTrigger(day_of_week=day_of_week, hour=hour, minute=0, timezone="Asia/Shanghai"),
            args=[int(task_id), config],
            id=task_id,
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )

    def add_daily_task(self, task_id: str, config: TaskConfig, hour: int = 8) -> None:
        self.scheduler.add_job(
            self._run_config,
            trigger=CronTrigger(hour=hour, minute=0, timezone="Asia/Shanghai"),
            args=[int(task_id), config],
            id=task_id,
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )

    def list_jobs(self) -> list[dict[str, str]]:
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append(
                {
                    "id": job.id,
                    "next_run_time": job.next_run_time.strftime("%Y-%m-%d %H:%M:%S") if job.next_run_time else "未启动",
                    "trigger": str(job.trigger),
                }
            )
        return jobs

    def remove_task(self, task_id: str) -> None:
        if self.scheduler.get_job(task_id):
            self.scheduler.remove_job(task_id)

    def run_now(self, task_id: int) -> TaskExecutionResult:
        config = self.db.get_task_config(task_id)
        if not config:
            raise ValueError(f"任务 {task_id} 不存在")
        return self._execute(task_id, config)

    def _run_config(self, task_id: int, config: TaskConfig) -> None:
        self._execute(task_id, config)

    def _execute(self, task_id: int, config: TaskConfig) -> TaskExecutionResult:
        run_id = self.db.start_task_run(task_id)
        try:
            report = asyncio.run(self.agent.run(config, save_task_config=False, save_report_record=False))
            report_path = save_markdown_report(report.markdown, config.research_direction)
            report_id = self.db.save_report(report)
            self.db.finish_task_run(run_id, "success", f"报告已保存到 {report_path}", report_id=report_id)
            return TaskExecutionResult(report=report, report_path=str(report_path), report_id=report_id)
        except Exception as exc:
            self.db.finish_task_run(run_id, "failed", f"{type(exc).__name__}: {exc}")
            raise


def schedule_to_trigger(schedule: str) -> BaseTrigger | None:
    text = (schedule or "").strip().lower()
    if not text or text == "manual":
        return None
    if text.startswith("cron:"):
        return _cron_expr_to_trigger(text.removeprefix("cron:").strip())
    if text.startswith("weekly") or "每周" in text:
        day = _extract_weekday(text)
        hour, minute = _extract_time(text, default_hour=8)
        return CronTrigger(day_of_week=day, hour=hour, minute=minute, timezone="Asia/Shanghai")
    if text.startswith("daily") or "每天" in text or "每日" in text:
        hour, minute = _extract_time(text, default_hour=8)
        return CronTrigger(hour=hour, minute=minute, timezone="Asia/Shanghai")
    if text.startswith("monthly") or "每月" in text:
        day = _extract_month_day(text)
        hour, minute = _extract_time(text, default_hour=8)
        return CronTrigger(day=day, hour=hour, minute=minute, timezone="Asia/Shanghai")
    return None


def _cron_expr_to_trigger(expr: str) -> CronTrigger:
    parts = expr.split()
    if len(parts) != 5:
        raise ValueError("cron 表达式需要 5 段：minute hour day month day_of_week")
    minute, hour, day, month, day_of_week = parts
    return CronTrigger(
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=day_of_week,
        timezone="Asia/Shanghai",
    )


def _extract_time(text: str, default_hour: int = 8) -> tuple[int, int]:
    match = re.search(r"(\d{1,2})[:：](\d{1,2})", text)
    if match:
        return _clamp_int(match.group(1), 0, 23), _clamp_int(match.group(2), 0, 59)

    match = re.search(r"(\d{1,2})\s*(点|时|am|pm)", text)
    if match:
        hour = _clamp_int(match.group(1), 0, 23)
        if match.group(2) == "pm" and hour < 12:
            hour += 12
        return hour, 0

    if "下午" in text or "晚上" in text:
        return 18, 0
    if "中午" in text:
        return 12, 0
    if "早" in text or "上午" in text:
        return default_hour, 0
    return default_hour, 0


def _extract_weekday(text: str) -> str:
    mapping = {
        "mon": ["mon", "monday", "周一", "星期一", "礼拜一", "一"],
        "tue": ["tue", "tuesday", "周二", "星期二", "礼拜二", "二"],
        "wed": ["wed", "wednesday", "周三", "星期三", "礼拜三", "三"],
        "thu": ["thu", "thursday", "周四", "星期四", "礼拜四", "四"],
        "fri": ["fri", "friday", "周五", "星期五", "礼拜五", "五"],
        "sat": ["sat", "saturday", "周六", "星期六", "礼拜六", "六"],
        "sun": ["sun", "sunday", "周日", "周天", "星期日", "星期天", "礼拜日", "日", "天"],
    }
    for day, aliases in mapping.items():
        if any(alias in text for alias in aliases):
            return day
    return "mon"


def _extract_month_day(text: str) -> int:
    match = re.search(r"(\d{1,2})\s*(日|号)", text)
    if match:
        return _clamp_int(match.group(1), 1, 31)
    return 1


def _clamp_int(value: str, low: int, high: int) -> int:
    return max(low, min(high, int(value)))
