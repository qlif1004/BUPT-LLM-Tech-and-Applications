from __future__ import annotations

from datetime import datetime

from academic_tracker.agent.deepseek_client import DeepSeekClient
from academic_tracker.storage.models import Paper, PaperSummary, Report, TaskConfig


class ReportGenerator:
    def __init__(self) -> None:
        self.llm = DeepSeekClient()

    async def summarize_paper(self, paper: Paper) -> str:
        if not self.llm.available:
            return self._fallback_summary(paper)
        messages = [
            {
                "role": "system",
                "content": "你是资深学术助手。根据论文标题和摘要，用中文输出 3-5 句话，说明研究问题、核心方法、主要贡献和适用场景。不要捏造信息。",
            },
            {
                "role": "user",
                "content": f"标题：{paper.title}\n摘要：{paper.abstract}\n来源：{paper.source}\n链接：{paper.url}",
            },
        ]
        try:
            return await self.llm.chat(messages, temperature=0.2)
        except Exception:
            return self._fallback_summary(paper)

    async def generate_overview(self, config: TaskConfig, summaries: list[PaperSummary]) -> str:
        if not summaries:
            return "本次未检索到足够相关的论文，建议扩大时间范围、增加英文关键词或放宽会议/期刊限制。"
        summary_text = "\n".join(f"- {item.paper.title}: {item.summary}" for item in summaries[:20])
        if not self.llm.available:
            return self._fallback_overview(config, summaries)
        messages = [
            {
                "role": "system",
                "content": "你是研究生的学术简报助手。请基于论文简报总结该方向近期进展，包含主要趋势、代表工作、技术路线和潜在研究空白，中文 500 字以内。",
            },
            {"role": "user", "content": f"研究方向：{config.research_direction}\n论文简报：\n{summary_text}"},
        ]
        try:
            return await self.llm.chat(messages, temperature=0.3)
        except Exception:
            return self._fallback_overview(config, summaries)

    def format_report(
        self,
        config: TaskConfig,
        latest: list[PaperSummary],
        popular: list[PaperSummary],
        relevant: list[PaperSummary],
        overview: str,
    ) -> Report:
        created_at = datetime.now()
        lines = [
            f"# 学术简报：{config.research_direction} 方向近期进展",
            "",
            f"生成时间：{created_at:%Y-%m-%d %H:%M}",
            f"覆盖来源：{', '.join(config.sources)}",
            f"时间窗口：近 {config.time_range_days} 天",
            "",
            "---",
            "",
        ]
        lines.extend(self._section("一、最新论文", latest, "latest"))
        lines.extend(self._section("二、最热门论文", popular, "popular"))
        lines.extend(self._section("三、最相关论文", relevant, "relevant"))
        lines.extend(["## 四、近期研究进展综述", "", overview, ""])
        markdown = "\n".join(lines)
        return Report(task_config=config, latest=latest, popular=popular, relevant=relevant, overview=overview, markdown=markdown, created_at=created_at)

    def _section(self, title: str, items: list[PaperSummary], category: str) -> list[str]:
        lines = [f"## {title}", ""]
        if not items:
            return [*lines, "本类别暂无结果。", ""]
        for idx, item in enumerate(items, start=1):
            paper = item.paper
            date_text = paper.published_date.strftime("%Y-%m-%d") if paper.published_date else "未知日期"
            link = paper.url or "#"
            lines.extend(
                [
                    f"### {idx}. [{paper.title}]({link})",
                    f"**作者：** {', '.join(paper.authors[:6]) or '未知'}",
                    f"**发表：** {date_text} | **来源：** {paper.source} | **引用数：** {paper.citation_count}",
                    f"**会议/期刊：** {paper.venue or '未知'}",
                    f"**相关度：** {paper.relevance_score:.3f}" if category == "relevant" else "",
                    f"**核心贡献：** {item.summary}",
                    "",
                ]
            )
        return lines

    def _fallback_summary(self, paper: Paper) -> str:
        abstract = paper.abstract.strip()
        if len(abstract) > 260:
            abstract = abstract[:260] + "..."
        if not abstract:
            abstract = "该论文暂无可用摘要。"
        return f"该论文题为《{paper.title}》。根据已有摘要信息，论文主要内容为：{abstract}"

    def _fallback_overview(self, config: TaskConfig, summaries: list[PaperSummary]) -> str:
        titles = "、".join(item.paper.title for item in summaries[:5])
        return f"围绕 {config.research_direction}，本次检索结果显示近期工作主要集中在方法改进、应用扩展和性能评估等方面。代表性论文包括 {titles}。建议后续重点关注这些论文中的实验设置、数据集选择和开放问题。"
