from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from sqlalchemy import DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, sessionmaker, mapped_column

from academic_tracker.config.settings import get_settings
from academic_tracker.storage.models import Paper, Report, TaskConfig


class Base(DeclarativeBase):
    pass


class TaskConfigRecord(Base):
    __tablename__ = "task_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    research_direction: Mapped[str] = mapped_column(String(255), index=True)
    payload: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class PaperRecord(Base):
    __tablename__ = "papers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stable_key: Mapped[str] = mapped_column(String(512), unique=True, index=True)
    title: Mapped[str] = mapped_column(Text)
    payload: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class ReportRecord(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    research_direction: Mapped[str] = mapped_column(String(255), index=True)
    markdown: Mapped[str] = mapped_column(Text)
    payload: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class TaskRunRecord(Base):
    __tablename__ = "task_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer, index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    message: Mapped[str] = mapped_column(Text, default="")
    report_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Database:
    def __init__(self) -> None:
        settings = get_settings()
        if settings.database_url.startswith("sqlite:///"):
            Path(settings.database_path).parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(settings.database_url, future=True)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False, future=True)

    def init_db(self) -> None:
        Base.metadata.create_all(self.engine)

    def save_task_config(self, config: TaskConfig) -> int:
        with self.SessionLocal() as session:
            record = TaskConfigRecord(
                research_direction=config.research_direction,
                payload=config.model_dump_json(),
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return record.id

    def get_task_config_record(self, task_id: int) -> TaskConfigRecord | None:
        with self.SessionLocal() as session:
            return session.get(TaskConfigRecord, task_id)

    def get_task_config(self, task_id: int) -> TaskConfig | None:
        record = self.get_task_config_record(task_id)
        if not record:
            return None
        return TaskConfig.model_validate(json.loads(record.payload))

    def list_task_configs(self, scheduled_only: bool = False, limit: int | None = None) -> list[TaskConfigRecord]:
        with self.SessionLocal() as session:
            query = session.query(TaskConfigRecord).order_by(TaskConfigRecord.created_at.desc())
            if limit:
                query = query.limit(limit)
            records = list(query)
        if not scheduled_only:
            return records
        scheduled_records: list[TaskConfigRecord] = []
        for record in records:
            try:
                config = TaskConfig.model_validate(json.loads(record.payload))
            except (json.JSONDecodeError, ValueError):
                continue
            if config.schedule and config.schedule.lower() != "manual":
                scheduled_records.append(record)
        return scheduled_records

    def delete_task_config(self, task_id: int) -> bool:
        with self.SessionLocal() as session:
            record = session.get(TaskConfigRecord, task_id)
            if not record:
                return False
            session.delete(record)
            session.commit()
            return True

    def save_papers(self, papers: list[Paper]) -> None:
        with self.SessionLocal() as session:
            for paper in papers:
                existing = session.query(PaperRecord).filter_by(stable_key=paper.stable_key).first()
                payload = paper.model_dump_json()
                if existing:
                    existing.title = paper.title
                    existing.payload = payload
                else:
                    session.add(PaperRecord(stable_key=paper.stable_key, title=paper.title, payload=payload))
            session.commit()

    def save_report(self, report: Report) -> int:
        with self.SessionLocal() as session:
            record = ReportRecord(
                research_direction=report.task_config.research_direction,
                markdown=report.markdown,
                payload=report.model_dump_json(),
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return record.id

    def get_report(self, report_id: int) -> ReportRecord | None:
        with self.SessionLocal() as session:
            return session.get(ReportRecord, report_id)

    def delete_report(self, report_id: int) -> bool:
        with self.SessionLocal() as session:
            record = session.get(ReportRecord, report_id)
            if not record:
                return False
            session.delete(record)
            session.commit()
            return True

    def list_reports(self, limit: int = 10) -> list[ReportRecord]:
        with self.SessionLocal() as session:
            return list(session.query(ReportRecord).order_by(ReportRecord.created_at.desc()).limit(limit))

    def get_report_record(self, report_id: int) -> ReportRecord | None:
        with self.SessionLocal() as session:
            return session.get(ReportRecord, report_id)

    def get_latest_report_by_direction(self, research_direction: str) -> ReportRecord | None:
        with self.SessionLocal() as session:
            return (
                session.query(ReportRecord)
                .filter_by(research_direction=research_direction)
                .order_by(ReportRecord.created_at.desc())
                .first()
            )

    def start_task_run(self, task_id: int) -> int:
        with self.SessionLocal() as session:
            record = TaskRunRecord(task_id=task_id, status="running")
            session.add(record)
            session.commit()
            session.refresh(record)
            return record.id

    def finish_task_run(self, run_id: int, status: str, message: str = "", report_id: int | None = None) -> None:
        with self.SessionLocal() as session:
            record = session.get(TaskRunRecord, run_id)
            if not record:
                return
            record.status = status
            record.message = message
            record.report_id = report_id
            record.finished_at = datetime.now()
            session.commit()

    def list_task_runs(self, task_id: int | None = None, limit: int = 10) -> list[TaskRunRecord]:
        with self.SessionLocal() as session:
            query = session.query(TaskRunRecord).order_by(TaskRunRecord.started_at.desc())
            if task_id is not None:
                query = query.filter_by(task_id=task_id)
            return list(query.limit(limit))


def get_database() -> Database:
    db = Database()
    db.init_db()
    return db
