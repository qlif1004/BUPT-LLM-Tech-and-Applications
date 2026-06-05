from __future__ import annotations

from datetime import datetime, timezone

from academic_tracker.storage.models import Paper


class LatestRanker:
    def rank(self, papers: list[Paper], top_n: int) -> list[Paper]:
        return sorted(
            papers,
            key=lambda paper: paper.published_date or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )[:top_n]
