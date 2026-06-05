from __future__ import annotations

from academic_tracker.storage.models import Paper


def deduplicate_papers(papers: list[Paper]) -> list[Paper]:
    merged: dict[str, Paper] = {}
    for paper in papers:
        key = paper.stable_key
        existing = merged.get(key)
        if not existing:
            merged[key] = paper
            continue
        if paper.citation_count > existing.citation_count:
            paper.extra = {**existing.extra, **paper.extra, "merged_sources": _sources(existing, paper)}
            merged[key] = paper
        else:
            existing.citation_count = max(existing.citation_count, paper.citation_count)
            existing.extra["merged_sources"] = _sources(existing, paper)
            if not existing.abstract and paper.abstract:
                existing.abstract = paper.abstract
            if not existing.url and paper.url:
                existing.url = paper.url
    return list(merged.values())


def _sources(a: Paper, b: Paper) -> list[str]:
    sources = set(a.extra.get("merged_sources", []))
    sources.add(a.source)
    sources.add(b.source)
    return sorted(sources)
