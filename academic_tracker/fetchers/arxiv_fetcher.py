from __future__ import annotations

from datetime import datetime, timedelta, timezone
import asyncio
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import quote_plus

import feedparser
import httpx

from academic_tracker.config.settings import get_settings
from academic_tracker.fetchers.base import BaseFetcher
from academic_tracker.storage.models import Paper, TaskConfig


class ArxivFetcher(BaseFetcher):
    name = "arxiv"
    base_url = "https://export.arxiv.org/api/query"
    retry_wait_seconds = 8.0

    async def fetch(self, config: TaskConfig, max_results: int = 30) -> list[Paper]:
        query = self._build_query(config)
        url = f"{self.base_url}?search_query={quote_plus(query)}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
        settings = get_settings()
        cached = self._read_cache(url, ttl_seconds=6 * 60 * 60)
        if cached is not None:
            feed = feedparser.parse(cached)
        else:
            headers = {"User-Agent": "academic-tracker-course-demo/1.0 (mailto:example@example.com)"}
            async with httpx.AsyncClient(timeout=settings.request_timeout, follow_redirects=True, headers=headers) as client:
                response = await self._get_with_retry(client, url)
                response.raise_for_status()
            self._write_cache(url, response.text)
            feed = feedparser.parse(response.text)
        cutoff = datetime.now(timezone.utc) - timedelta(days=config.time_range_days)
        papers: list[Paper] = []
        for entry in feed.entries:
            published = self._parse_date(getattr(entry, "published", ""))
            if published and published < cutoff:
                continue
            doi = None
            for link in getattr(entry, "links", []):
                if link.get("title") == "doi":
                    doi = link.get("href")
            papers.append(
                Paper(
                    title=getattr(entry, "title", "").replace("\n", " ").strip(),
                    authors=[author.get("name", "") for author in getattr(entry, "authors", [])],
                    abstract=getattr(entry, "summary", "").replace("\n", " ").strip(),
                    published_date=published,
                    url=getattr(entry, "link", ""),
                    doi=doi,
                    source=self.name,
                    keywords=config.keywords,
                    venue="arXiv",
                    external_id=getattr(entry, "id", None),
                )
            )
        return papers

    def _build_query(self, config: TaskConfig) -> str:
        terms = self._english_terms(config.query_terms())
        if not terms:
            terms = [config.research_direction]
        term_query = " OR ".join(f'all:"{term}"' for term in terms[:6])
        arxiv_categories = [source.split(":", 1)[1] for source in config.sources if source.startswith("arxiv:")]
        if arxiv_categories:
            cat_query = " OR ".join(f"cat:{cat}" for cat in arxiv_categories)
            return f"({term_query}) AND ({cat_query})"
        return term_query

    def _english_terms(self, terms: list[str]) -> list[str]:
        english_terms = []
        for term in terms:
            cleaned = term.strip()
            if not cleaned:
                continue
            ascii_part = " ".join(re.findall(r"[A-Za-z][A-Za-z0-9\-]*(?:\s+[A-Za-z][A-Za-z0-9\-]*)*", cleaned))
            if ascii_part:
                english_terms.append(ascii_part.strip())
        return list(dict.fromkeys(english_terms))

    async def _get_with_retry(self, client: httpx.AsyncClient, url: str) -> httpx.Response:
        last_error: Exception | None = None
        for attempt in range(5):
            try:
                response = await client.get(url)
                if response.status_code in {429, 503}:
                    retry_after = self._retry_after_seconds(response)
                    print(f"[WARN] arXiv 返回 {response.status_code}，等待 {retry_after:.1f}s 后重试 ({attempt + 1}/5)")
                    await asyncio.sleep(retry_after)
                    continue
                return response
            except httpx.TimeoutException as exc:
                last_error = exc
                wait_seconds = self.retry_wait_seconds
                print(f"[WARN] arXiv 请求超时，等待 {wait_seconds:.1f}s 后重试 ({attempt + 1}/5)")
                await asyncio.sleep(wait_seconds)
        if last_error:
            raise last_error
        raise RuntimeError("arXiv request failed after retries")

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
        cache_dir = Path("data/cache/arxiv")
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir / f"{digest}.json"

    def _read_cache(self, key: str, ttl_seconds: int) -> str | None:
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
        print("[INFO] arXiv 使用本地缓存结果")
        return payload.get("text")

    def _write_cache(self, key: str, text: str) -> None:
        payload = {"created_at": datetime.now(timezone.utc).isoformat(), "text": text}
        self._cache_path(key).write_text(json.dumps(payload), encoding="utf-8")

    def _parse_date(self, raw: str) -> datetime | None:
        if not raw:
            return None
        try:
            return datetime.strptime(raw, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            return None
