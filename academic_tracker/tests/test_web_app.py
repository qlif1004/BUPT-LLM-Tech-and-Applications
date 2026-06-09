from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from fastapi.testclient import TestClient

from academic_tracker.storage.models import Report, TaskConfig
from academic_tracker.web.app import create_app


@dataclass
class FakeTaskRecord:
    id: int
    payload: str
    created_at: datetime


@dataclass
class FakeReportRecord:
    id: int
    research_direction: str
    markdown: str
    created_at: datetime


@dataclass
class FakeLogRecord:
    id: int
    task_id: int
    status: str
    message: str
    started_at: datetime
    finished_at: datetime | None = None


class FakeDatabase:
    def __init__(self) -> None:
        self.saved_report: Report | None = None
        self.report_records = [
            FakeReportRecord(
                id=7,
                research_direction="graph foundation model",
                markdown="# Example Report\n\nHello world.",
                created_at=datetime(2026, 6, 8, 10, 0, 0),
            )
        ]
        self.task_records = [
            FakeTaskRecord(
                id=3,
                payload=TaskConfig(
                    research_direction="graph foundation model",
                    schedule="weekly mon 08:00",
                    keywords=["graph foundation model"],
                ).model_dump_json(),
                created_at=datetime(2026, 6, 8, 9, 0, 0),
            )
        ]
        self.log_records = [
            FakeLogRecord(
                id=11,
                task_id=3,
                status="success",
                message="saved",
                started_at=datetime(2026, 6, 8, 9, 30, 0),
                finished_at=datetime(2026, 6, 8, 9, 32, 0),
            )
        ]

    def list_task_configs(self, limit: int = 12):
        return self.task_records[:limit]

    def list_reports(self, limit: int = 12):
        return self.report_records[:limit]

    def list_task_runs(self, limit: int = 12, task_id: int | None = None):
        return self.log_records[:limit]

    def save_report(self, report: Report) -> int:
        self.saved_report = report
        return 99

    def get_report_record(self, report_id: int):
        for record in self.report_records:
            if record.id == report_id:
                return record
        return None


class FakeAgent:
    def __init__(self, db: FakeDatabase) -> None:
        self.db = db

    async def parse_task(self, user_text: str) -> TaskConfig:
        return TaskConfig(
            research_direction=user_text,
            keywords=["graph"],
            sources=["arxiv", "dblp"],
            schedule="manual",
        )

    async def run(self, config: TaskConfig, save_report_record: bool = False) -> Report:
        return Report(task_config=config, markdown="# Test Report\n\nRendered output.", overview="overview")


class FakeScheduler:
    def __init__(self) -> None:
        self.created_tasks: list[TaskConfig] = []
        self.started = False

    def restore_persisted_tasks(self) -> int:
        return 1

    def start(self) -> None:
        self.started = True

    def shutdown(self) -> None:
        self.started = False

    def list_jobs(self) -> list[dict[str, str]]:
        jobs = []
        for index, config in enumerate(self.created_tasks, start=1):
            jobs.append({"id": str(index), "next_run_time": "2026-06-09 08:00:00", "trigger": config.schedule})
        return jobs

    def create_task(self, config: TaskConfig) -> int:
        self.created_tasks.append(config)
        return len(self.created_tasks)

    def run_now(self, task_id: int):
        config = TaskConfig(research_direction=f"task-{task_id}", schedule="weekly mon 08:00")
        report = Report(task_config=config, markdown="# Task Report\n\nDone.", overview="overview")
        return type(
            "TaskExecutionResult",
            (),
            {
                "report_id": 55,
                "report_path": "reports/task_001.md",
                "report": report,
            },
        )()


def test_dashboard_renders_summary():
    db = FakeDatabase()
    app = create_app(agent=FakeAgent(db), db=db, scheduler=FakeScheduler(), report_saver=lambda *_: Path("reports/test.md"))

    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "Academic Tracker Agent" in response.text
    assert "graph foundation model" in response.text


def test_run_api_returns_report_payload():
    db = FakeDatabase()
    app = create_app(agent=FakeAgent(db), db=db, scheduler=FakeScheduler(), report_saver=lambda *_: Path("reports/test.md"))

    with TestClient(app) as client:
        response = client.post("/api/run", json={"query": "graph foundation model"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["report_id"] == 99
    assert payload["config"]["research_direction"] == "graph foundation model"
    assert "Test Report" in payload["report_html"]


def test_create_task_api_accepts_schedule_override():
    db = FakeDatabase()
    scheduler = FakeScheduler()
    app = create_app(agent=FakeAgent(db), db=db, scheduler=scheduler, report_saver=lambda *_: Path("reports/test.md"))

    with TestClient(app) as client:
        response = client.post(
            "/api/tasks",
            json={"query": "graph foundation model", "schedule_override": "weekly mon 08:00"},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["task_id"] == 1
    assert scheduler.created_tasks[0].schedule == "weekly mon 08:00"


def test_report_detail_page_uses_saved_markdown():
    db = FakeDatabase()
    app = create_app(agent=FakeAgent(db), db=db, scheduler=FakeScheduler(), report_saver=lambda *_: Path("reports/test.md"))

    with TestClient(app) as client:
        response = client.get("/reports/7")

    assert response.status_code == 200
    assert "Example Report" in response.text
