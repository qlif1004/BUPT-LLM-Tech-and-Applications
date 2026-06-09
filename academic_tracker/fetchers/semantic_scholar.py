from __future__ import annotations

import asyncio
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx

from academic_tracker.config.settings import get_settings
from academic_tracker.fetchers.base import BaseFetcher
from academic_tracker.storage.models import Paper, TaskConfig


class SemanticScholarFetcher(BaseFetcher):
    name = "semantic_scholar"
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    retry_wait_seconds = 8.0
    max_retry_times = 3

    async def fetch(self, config: TaskConfig, max_results: int = 30) -> list[Paper]:
        query = self._build_query(config)
        params = {
            "query": query,
            "limit": min(max_results, 100),
            "fields": "title,authors,year,citationCount,url,externalIds,venue,publicationDate",
        }
        settings = get_settings()
        cache_key = json.dumps(params, ensure_ascii=False, sort_keys=True)
        cached = self._read_cache(cache_key, ttl_seconds=6 * 60 * 60)
        if cached is not None:
            data = cached.get("data", [])
        else:
            headers = {"User-Agent": "academic-tracker-course-demo/1.0"}
            if settings.semantic_scholar_api_key:
                headers["x-api-key"] = settings.semantic_scholar_api_key
            async with httpx.AsyncClient(timeout=settings.request_timeout, headers=headers) as client:
                response = await self._get_with_retry(client, params)
                response.raise_for_status()
            payload = response.json()
            self._write_cache(cache_key, payload)
            data = payload.get("data", [])
        cutoff = datetime.now(timezone.utc) - timedelta(days=config.time_range_days)
        papers: list[Paper] = []
        for item in data:
            published = self._parse_date(item.get("publicationDate"), item.get("year"))
            if published and published < cutoff:
                continue
            external_ids = item.get("externalIds") or {}
            papers.append(
                Paper(
                    title=item.get("title") or "Untitled",
                    authors=[author.get("name", "") for author in item.get("authors", [])],
                    abstract=item.get("abstract") or "",
                    published_date=published,
                    url=item.get("url") or "",
                    doi=external_ids.get("DOI"),
                    citation_count=item.get("citationCount") or 0,
                    source=self.name,
                    keywords=config.keywords,
                    venue=item.get("venue"),
                    external_id=item.get("paperId"),
                    extra={"external_ids": external_ids},
                )
            )
        return papers

    def _build_query(self, config: TaskConfig) -> str:
        english_terms: list[str] = []
        for term in config.query_terms():
            ascii_part = " ".join(re.findall(r"[A-Za-z][A-Za-z0-9\-]*(?:\s+[A-Za-z][A-Za-z0-9\-]*)*", term))
            if ascii_part:
                english_terms.append(ascii_part.strip())
        if english_terms:
            return " ".join(dict.fromkeys(english_terms[:4]))
        return config.research_direction

    async def _get_with_retry(self, client: httpx.AsyncClient, params: dict[str, object]) -> httpx.Response:
        last_error: Exception | None = None
        last_response: httpx.Response | None = None
        for attempt in range(self.max_retry_times):
            try:
                response = await client.get(self.base_url, params=params)
            except httpx.TimeoutException as exc:
                last_error = exc
                wait_seconds = self.retry_wait_seconds
                print(f"[WARN] Semantic Scholar 请求超时，等待 {wait_seconds:.1f}s 后重试 ({attempt + 1}/5)")
                await asyncio.sleep(wait_seconds)
                continue
            if response.status_code == 429:
                last_response = response
                retry_after = self._retry_after_seconds(response)
                print(f"[WARN] Semantic Scholar 返回 429，等待 {retry_after:.1f}s 后重试 ({attempt + 1}/5)")
                await asyncio.sleep(retry_after)
                continue
            if response.status_code in {500, 502, 503, 504}:
                last_response = response
                wait_seconds = self.retry_wait_seconds
                print(f"[WARN] Semantic Scholar 返回 {response.status_code}，等待 {wait_seconds:.1f}s 后重试 ({attempt + 1}/5)")
                await asyncio.sleep(wait_seconds)
                continue
            return response
        if last_response is not None:
            return last_response
        if last_error is not None:
            raise last_error
        raise RuntimeError("Semantic Scholar request failed after retries")

    def _retry_after_seconds(self, response: httpx.Response) -> float:
        value = response.headers.get("retry-after")
        if value:
            try:
                return min(float(value), self.retry_wait_seconds)
            except ValueError:
                return self.retry_wait_seconds
        return self.retry_wait_seconds

    def _cache_path(self, key: str) -> Path:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        cache_dir = Path("data/cache/semantic_scholar")
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir / f"{digest}.json"

    def _read_cache(self, key: str, ttl_seconds: int) -> dict[str, object] | None:
        path = self._cache_path(key)
        if not path.exists():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
        created_at = datetime.fromisoformat(payload["created_at"])
        if datetime.now(timezone.utc) - created_at > timedelta(seconds=ttl_seconds):
            return None
        print("[INFO] Semantic Scholar 使用本地缓存结果")
        return payload.get("data")

    def _write_cache(self, key: str, data: dict[str, object]) -> None:
        payload = {"created_at": datetime.now(timezone.utc).isoformat(), "data": data}
        self._cache_path(key).write_text(json.dumps(payload), encoding="utf-8")

    def _parse_date(self, date_text: str | None, year: int | None) -> datetime | None:
        if date_text:
            try:
                return datetime.strptime(date_text, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except ValueError:
                pass
        if year:
            return datetime(year=int(year), month=1, day=1, tzinfo=timezone.utc)
        return None
