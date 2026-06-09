from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Callable

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markdown import markdown
from pydantic import BaseModel, Field

from academic_tracker.agent.graph import AcademicTrackerAgent
from academic_tracker.scheduler.task_scheduler import TaskExecutionResult, TaskScheduler, schedule_to_trigger
from academic_tracker.storage.database import Database, ReportRecord, get_database
from academic_tracker.storage.models import Report, TaskConfig
from academic_tracker.utils.formatting import save_markdown_report

BASE_DIR = Path(__file__).resolve().parent


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)


class TaskRequest(BaseModel):
    query: str = Field(..., min_length=1)
    schedule_override: str | None = None


def create_app(
    agent: AcademicTrackerAgent | None = None,
    db: Database | None = None,
    scheduler: TaskScheduler | None = None,
    report_saver: Callable[[str, str], Path] = save_markdown_report,
) -> FastAPI:
    agent = agent or AcademicTrackerAgent()
    db = db or agent.db or get_database()
    scheduler = scheduler or TaskScheduler(agent=agent, db=db)
    templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        restored_jobs = scheduler.restore_persisted_tasks()
        scheduler.start()
        app.state.restored_jobs = restored_jobs
        try:
            yield
        finally:
            scheduler.shutdown()

    app = FastAPI(title="Academic Tracker Web UI", lifespan=lifespan)
    app.state.agent = agent
    app.state.db = db
    app.state.scheduler = scheduler
    app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def dashboard(request: Request) -> HTMLResponse:
        tasks = _serialize_tasks(db.list_task_configs(limit=12))
        reports = _serialize_reports(db.list_reports(limit=12))
        logs = _serialize_logs(db.list_task_runs(limit=12))
        jobs = scheduler.list_jobs()
        return templates.TemplateResponse(
            request,
            "dashboard.html",
            {
                "tasks": tasks,
                "reports": reports,
                "logs": logs,
                "jobs": jobs,
                "restored_jobs": getattr(request.app.state, "restored_jobs", 0),
            },
        )

    @app.get("/reports/{report_id}", response_class=HTMLResponse)
    async def report_detail(request: Request, report_id: int) -> HTMLResponse:
        record = db.get_report_record(report_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Report not found")
        return templates.TemplateResponse(
            request,
            "report.html",
            {
                "report_id": report_id,
                "research_direction": record.research_direction,
                "created_at": record.created_at.strftime("%Y-%m-%d %H:%M"),
                "report_html": _render_markdown(record.markdown),
                "markdown": record.markdown,
            },
        )

    @app.post("/api/run")
    async def run_query(payload: QueryRequest) -> dict[str, Any]:
        query = payload.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        config = await agent.parse_task(query)
        report = await agent.run(config, save_report_record=False)
        report_path = report_saver(report.markdown, config.research_direction)
        report_id = db.save_report(report)
        return {
            "config": config.model_dump(),
            "report_id": report_id,
            "report_path": str(report_path),
            "report_markdown": report.markdown,
            "report_html": _render_markdown(report.markdown),
        }

    @app.post("/api/tasks")
    async def create_task(payload: TaskRequest) -> dict[str, Any]:
        query = payload.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        config = await agent.parse_task(query)
        if payload.schedule_override and payload.schedule_override.strip():
            config = config.model_copy(update={"schedule": payload.schedule_override.strip()})
        if schedule_to_trigger(config.schedule) is None:
            raise HTTPException(
                status_code=400,
                detail="A valid schedule is required. Example: weekly mon 08:00 or cron: 0 8 * * mon",
            )

        task_id = scheduler.create_task(config)
        job = next((item for item in scheduler.list_jobs() if item["id"] == str(task_id)), None)
        return {
            "task_id": task_id,
            "config": config.model_dump(),
            "job": job,
        }

    @app.post("/api/tasks/{task_id}/run")
    async def run_task(task_id: int) -> dict[str, Any]:
        try:
            result = await asyncio.to_thread(scheduler.run_now, task_id)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return _serialize_execution_result(result)

    return app


def _serialize_tasks(records: list[Any]) -> list[dict[str, Any]]:
    serialized: list[dict[str, Any]] = []
    for record in records:
        try:
            config = TaskConfig.model_validate_json(record.payload)
        except ValueError:
            continue
        serialized.append(
            {
                "id": record.id,
                "research_direction": config.research_direction,
                "schedule": config.schedule,
                "sources": ", ".join(config.sources),
                "categories": ", ".join(config.categories),
                "created_at": record.created_at.strftime("%Y-%m-%d %H:%M"),
            }
        )
    return serialized


def _serialize_reports(records: list[ReportRecord]) -> list[dict[str, Any]]:
    serialized: list[dict[str, Any]] = []
    for record in records:
        first_heading = next((line.strip("# ").strip() for line in record.markdown.splitlines() if line.startswith("#")), "Report")
        serialized.append(
            {
                "id": record.id,
                "research_direction": record.research_direction,
                "created_at": record.created_at.strftime("%Y-%m-%d %H:%M"),
                "heading": first_heading[:80],
            }
        )
    return serialized


def _serialize_logs(records: list[Any]) -> list[dict[str, Any]]:
    serialized: list[dict[str, Any]] = []
    for record in records:
        serialized.append(
            {
                "id": record.id,
                "task_id": record.task_id,
                "status": record.status,
                "started_at": record.started_at.strftime("%Y-%m-%d %H:%M:%S"),
                "finished_at": record.finished_at.strftime("%Y-%m-%d %H:%M:%S") if record.finished_at else "-",
                "message": record.message[:120],
            }
        )
    return serialized


def _serialize_execution_result(result: TaskExecutionResult) -> dict[str, Any]:
    return {
        "report_id": result.report_id,
        "report_path": result.report_path,
        "report_markdown": result.report.markdown,
        "report_html": _render_markdown(result.report.markdown),
        "config": result.report.task_config.model_dump(),
    }


def _render_markdown(text: str) -> str:
    return markdown(text, extensions=["extra", "nl2br", "sane_lists"])
