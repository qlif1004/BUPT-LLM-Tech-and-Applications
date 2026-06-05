from __future__ import annotations

from datetime import datetime, timezone

from academic_tracker.storage.models import Paper


class PopularRanker:
    def rank(self, papers: list[Paper], top_n: int) -> list[Paper]:
        return sorted(papers, key=self._score, reverse=True)[:top_n]

    def _score(self, paper: Paper) -> float:
        age_bonus = 0.0
        if paper.published_date:
            days = max((datetime.now(timezone.utc) - paper.published_date).days, 1)
            age_bonus = 30.0 / days
        return paper.citation_count * 0.8 + age_bonus * 20.0
