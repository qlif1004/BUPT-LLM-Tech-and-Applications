from __future__ import annotations

import asyncio
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import httpx

from academic_tracker.config.settings import get_settings
from academic_tracker.fetchers.base import BaseFetcher
from academic_tracker.storage.models import Paper, TaskConfig


class DblpFetcher(BaseFetcher):
    name = "dblp"
    base_url = "https://dblp.org/search/publ/api"
    retry_wait_seconds = 8.0

    async def fetch(self, config: TaskConfig, max_results: int = 30) -> list[Paper]:
        params = {
            "q": self._build_query(config),
            "format": "json",
            "h": min(max_results, 1000),
            "f": 0,
        }
        cache_key = json.dumps(params, ensure_ascii=False, sort_keys=True)
        cached = self._read_cache(cache_key, ttl_seconds=6 * 60 * 60)
        if cached is not None:
            payload = cached
        else:
            settings = get_settings()
            headers = {"User-Agent": "academic-tracker-course-demo/1.0"}
            async with httpx.AsyncClient(timeout=settings.request_timeout, headers=headers, follow_redirects=True) as client:
                response = await self._get_with_retry(client, params)
                response.raise_for_status()
            payload = response.json()
            self._write_cache(cache_key, payload)
        return self._parse_payload(payload, config)

    def _build_query(self, config: TaskConfig) -> str:
        english_terms: list[str] = []
        for term in config.query_terms():
            ascii_part = " ".join(re.findall(r"[A-Za-z][A-Za-z0-9\-]*(?:\s+[A-Za-z][A-Za-z0-9\-]*)*", term))
            if ascii_part:
                english_terms.append(ascii_part.strip())
        if english_terms:
            return " ".join(dict.fromkeys(english_terms[:6]))
        return config.research_direction

    def _parse_payload(self, payload: dict[str, Any], config: TaskConfig) -> list[Paper]:
        hits = payload.get("result", {}).get("hits", {}).get("hit", [])
        if isinstance(hits, dict):
            items = [hits]
        elif isinstance(hits, list):
            items = hits
        else:
            items = []

        cutoff = datetime.now(timezone.utc) - timedelta(days=config.time_range_days)
        requested_venues = self._requested_venues(config)
        papers: list[Paper] = []
        for item in items:
            paper = self._paper_from_hit(item, config)
            if paper is None:
                continue
            if paper.published_date and paper.published_date < cutoff:
                continue
            if requested_venues and not self._matches_requested_venue(paper.venue, requested_venues):
                continue
            papers.append(paper)
        return papers

    def _paper_from_hit(self, item: dict[str, Any], config: TaskConfig) -> Paper | None:
        info = item.get("info") or {}
        title = str(info.get("title") or "").replace("\n", " ").strip()
        if not title:
            return None

        authors = self._parse_authors(info.get("authors"))
        venue = self._clean_text(info.get("venue"))
        doi = self._clean_text(info.get("doi"))
        ee = self._clean_text(info.get("ee"))
        dblp_url = self._clean_text(info.get("url"))
        external_id = self._clean_text(info.get("key")) or self._clean_text(item.get("@id"))

        return Paper(
            title=title,
            authors=authors,
            abstract="",
            published_date=self._parse_year(info.get("year")),
            url=ee or dblp_url or "",
            doi=doi,
            citation_count=0,
            source=self.name,
            keywords=config.keywords,
            venue=venue,
            external_id=external_id,
            extra={
                "dblp_key": self._clean_text(info.get("key")),
                "dblp_url": dblp_url,
                "ee": ee,
                "pages": self._clean_text(info.get("pages")),
                "type": self._clean_text(info.get("type")),
                "access": self._clean_text(info.get("access")),
            },
        )

    def _parse_authors(self, authors_info: Any) -> list[str]:
        authors = []
        entries = (authors_info or {}).get("author", [])
        if isinstance(entries, dict):
            entries = [entries]
        for entry in entries:
            if isinstance(entry, str):
                name = entry.strip()
            else:
                name = str(entry.get("text") or "").strip()
            if name:
                authors.append(name)
        return authors

    def _requested_venues(self, config: TaskConfig) -> list[str]:
        requested = [venue.strip() for venue in config.venues if venue and venue.strip()]
        for source in config.sources:
            if source.startswith("dblp:"):
                venue = source.split(":", 1)[1].strip()
                if venue:
                    requested.append(venue)
        return list(dict.fromkeys(requested))

    def _matches_requested_venue(self, venue: str | None, requested_venues: list[str]) -> bool:
        if not venue:
            return False
        normalized_venue = venue.casefold()
        for requested in requested_venues:
            normalized_requested = requested.casefold()
            if normalized_requested in normalized_venue or normalized_venue in normalized_requested:
                return True
        return False

    async def _get_with_retry(self, client: httpx.AsyncClient, params: dict[str, Any]) -> httpx.Response:
        last_error: Exception | None = None
        last_response: httpx.Response | None = None
        for attempt in range(5):
            try:
                response = await client.get(self.base_url, params=params)
            except httpx.TimeoutException as exc:
                last_error = exc
                wait_seconds = self.retry_wait_seconds
                print(f"[WARN] DBLP request timed out, retrying in {wait_seconds:.1f}s ({attempt + 1}/5)")
                await asyncio.sleep(wait_seconds)
                continue
            if response.status_code == 429:
                last_response = response
                retry_after = self._retry_after_seconds(response)
                print(f"[WARN] DBLP returned 429, retrying in {retry_after:.1f}s ({attempt + 1}/5)")
                await asyncio.sleep(retry_after)
                continue
            if response.status_code in {500, 502, 503, 504}:
                last_response = response
                wait_seconds = self.retry_wait_seconds
                print(f"[WARN] DBLP returned {response.status_code}, retrying in {wait_seconds:.1f}s ({attempt + 1}/5)")
                await asyncio.sleep(wait_seconds)
                continue
            return response
        if last_response is not None:
            return last_response
        if last_error is not None:
            raise last_error
        raise RuntimeError("DBLP request failed after retries")

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
        cache_dir = Path("data/cache/dblp")
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir / f"{digest}.json"

    def _read_cache(self, key: str, ttl_seconds: int) -> dict[str, Any] | None:
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
        print("[INFO] DBLP using local cache")
        return payload.get("data")

    def _write_cache(self, key: str, data: dict[str, Any]) -> None:
        payload = {"created_at": datetime.now(timezone.utc).isoformat(), "data": data}
        self._cache_path(key).write_text(json.dumps(payload), encoding="utf-8")

    def _parse_year(self, year: Any) -> datetime | None:
        if not year:
            return None
        try:
            return datetime(year=int(year), month=1, day=1, tzinfo=timezone.utc)
        except (TypeError, ValueError):
            return None

    def _clean_text(self, value: Any) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None
