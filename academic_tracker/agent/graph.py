from __future__ import annotations

import asyncio

from academic_tracker.agent.intent_parser import IntentParser
from academic_tracker.agent.report_generator import ReportGenerator
from academic_tracker.config.settings import get_settings
from academic_tracker.fetchers.arxiv_fetcher import ArxivFetcher
from academic_tracker.fetchers.semantic_scholar import SemanticScholarFetcher
from academic_tracker.rankers.latest import LatestRanker
from academic_tracker.rankers.popular import PopularRanker
from academic_tracker.rankers.relevant import RelevanceRanker
from academic_tracker.storage.database import get_database
from academic_tracker.storage.models import Paper, PaperSummary, Report, TaskConfig
from academic_tracker.utils.deduplication import deduplicate_papers


class AcademicTrackerAgent:
    def __init__(self) -> None:
        self.intent_parser = IntentParser()
        self.report_generator = ReportGenerator()
        self.fetchers = {
            "arxiv": ArxivFetcher(),
            "semantic_scholar": SemanticScholarFetcher(),
        }
        self.db = get_database()

    async def parse_task(self, user_text: str) -> TaskConfig:
        return await self.intent_parser.parse(user_text)

    async def run(self, config: TaskConfig, save_task_config: bool = True, save_report_record: bool = True) -> Report:
        settings = get_settings()
        papers = await self.fetch_papers(config, settings.default_max_results)
        if save_task_config:
            self.db.save_task_config(config)
        self.db.save_papers(papers)

        top_n = config.top_n_per_category
        latest_papers = LatestRanker().rank(papers, top_n) if "latest" in config.categories else []
        popular_papers = PopularRanker().rank(papers, top_n) if "popular" in config.categories else []
        relevant_papers = RelevanceRanker().rank(papers, config, top_n) if "relevant" in config.categories else []

        latest = await self._summarize_group(latest_papers, "最新")
        popular = await self._summarize_group(popular_papers, "热门")
        relevant = await self._summarize_group(relevant_papers, "相关")
        all_summaries = self._merge_summaries([latest, popular, relevant])
        overview = await self.report_generator.generate_overview(config, all_summaries)
        report = self.report_generator.format_report(config, latest, popular, relevant, overview)
        if save_report_record:
            self.db.save_report(report)
        return report

    async def run_from_text(self, user_text: str) -> tuple[TaskConfig, Report]:
        config = await self.parse_task(user_text)
        report = await self.run(config)
        return config, report

    async def fetch_papers(self, config: TaskConfig, max_results: int) -> list[Paper]:
        active_fetchers = []
        for source in config.sources:
            source_name = source.split(":", 1)[0]
            fetcher = self.fetchers.get(source_name)
            if fetcher and fetcher not in active_fetchers:
                active_fetchers.append(fetcher)
        if not active_fetchers:
            active_fetchers = list(self.fetchers.values())

        papers: list[Paper] = []
        for index, fetcher in enumerate(active_fetchers):
            if index > 0:
                await asyncio.sleep(2.0)
            try:
                result = await fetcher.fetch(config, max_results=max_results)
            except Exception as exc:
                print(f"[WARN] 数据源 {fetcher.name} 获取失败：{type(exc).__name__}: {exc}")
                continue
            print(f"[INFO] 数据源 {fetcher.name} 获取到 {len(result)} 篇候选论文")
            papers.extend(result)
        deduplicated = deduplicate_papers(papers)
        print(f"[INFO] 去重后共有 {len(deduplicated)} 篇候选论文")
        return deduplicated

    async def _summarize_group(self, papers: list[Paper], label: str) -> list[PaperSummary]:
        summaries = await asyncio.gather(*(self.report_generator.summarize_paper(paper) for paper in papers))
        return [PaperSummary(paper=paper, summary=summary, category_labels=[label]) for paper, summary in zip(papers, summaries)]

    def _merge_summaries(self, groups: list[list[PaperSummary]]) -> list[PaperSummary]:
        merged: dict[str, PaperSummary] = {}
        for group in groups:
            for item in group:
                key = item.paper.stable_key
                if key not in merged:
                    merged[key] = item
                else:
                    merged[key].category_labels.extend(item.category_labels)
        return list(merged.values())
