from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class TaskConfig(BaseModel):
    research_direction: str = Field(..., description="用户关注的研究方向")
    keywords: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=lambda: ["arxiv", "semantic_scholar"])
    time_range_days: int = 30
    schedule: str = "manual"
    categories: list[str] = Field(default_factory=lambda: ["latest", "popular", "relevant"])
    top_n_per_category: int = 5
    venues: list[str] = Field(default_factory=list)

    @field_validator("categories", mode="before")
    @classmethod
    def normalize_categories(cls, value: Any) -> list[str]:
        if not value:
            return ["latest", "popular", "relevant"]
        if isinstance(value, str):
            raw_categories = [value]
        else:
            raw_categories = list(value)

        mapping = {
            "latest": "latest",
            "new": "latest",
            "recent": "latest",
            "最新": "latest",
            "新": "latest",
            "popular": "popular",
            "hot": "popular",
            "trending": "popular",
            "热门": "popular",
            "热度": "popular",
            "最热门": "popular",
            "relevant": "relevant",
            "related": "relevant",
            "relevance": "relevant",
            "相关": "relevant",
            "最相关": "relevant",
            "匹配": "relevant",
        }
        normalized: list[str] = []
        for category in raw_categories:
            text = str(category).strip().lower()
            matched = None
            for key, standard in mapping.items():
                if key.lower() in text:
                    matched = standard
                    break
            if matched and matched not in normalized:
                normalized.append(matched)

        return normalized or ["latest", "popular", "relevant"]

    def query_terms(self) -> list[str]:
        terms = [self.research_direction, *self.keywords]
        return [term.strip() for term in terms if term and term.strip()]


class Paper(BaseModel):
    title: str
    authors: list[str] = Field(default_factory=list)
    abstract: str = ""
    published_date: datetime | None = None
    url: str = ""
    doi: str | None = None
    citation_count: int = 0
    source: str = "unknown"
    keywords: list[str] = Field(default_factory=list)
    venue: str | None = None
    external_id: str | None = None
    relevance_score: float = 0.0
    extra: dict[str, Any] = Field(default_factory=dict)

    @property
    def stable_key(self) -> str:
        if self.doi:
            return self.doi.lower().strip()
        if self.external_id:
            return self.external_id.lower().strip()
        return self.title.lower().strip()


class PaperSummary(BaseModel):
    paper: Paper
    summary: str
    category_labels: list[str] = Field(default_factory=list)


class Report(BaseModel):
    task_config: TaskConfig
    latest: list[PaperSummary] = Field(default_factory=list)
    popular: list[PaperSummary] = Field(default_factory=list)
    relevant: list[PaperSummary] = Field(default_factory=list)
    overview: str = ""
    markdown: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
