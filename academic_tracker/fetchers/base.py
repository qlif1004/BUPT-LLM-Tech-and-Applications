from __future__ import annotations

from abc import ABC, abstractmethod

from academic_tracker.storage.models import Paper, TaskConfig


class BaseFetcher(ABC):
    name: str

    @abstractmethod
    async def fetch(self, config: TaskConfig, max_results: int = 30) -> list[Paper]:
        raise NotImplementedError
