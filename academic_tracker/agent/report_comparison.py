from __future__ import annotations

import json
from typing import Any

from academic_tracker.storage.models import Report, ReportComparison, TrendPaper


CATEGORY_NAMES = {
    "latest": "最新",
    "popular": "热门",
    "relevant": "相关",
}


def compare_with_previous_report(current: Report, previous_record: Any | None) -> ReportComparison:
    current_papers = _paper_index(current)
    comparison = ReportComparison(current_total=len(current_papers))
    if previous_record is None:
        comparison.new_papers = list(current_papers.values())
        return comparison

    previous = _load_report(previous_record)
    if previous is None:
        comparison.new_papers = list(current_papers.values())
        comparison.previous_report_id = getattr(previous_record, "id", None)
        comparison.previous_created_at = getattr(previous_record, "created_at", None)
        return comparison

    previous_papers = _paper_index(previous)
    current_keys = set(current_papers)
    previous_keys = set(previous_papers)

    comparison.previous_report_id = getattr(previous_record, "id", None)
    comparison.previous_created_at = getattr(previous_record, "created_at", previous.created_at)
    comparison.previous_total = len(previous_papers)
    comparison.new_papers = [current_papers[key] for key in sorted(current_keys - previous_keys)]
    comparison.continuing_papers = [current_papers[key] for key in sorted(current_keys & previous_keys)]
    comparison.dropped_papers = [previous_papers[key] for key in sorted(previous_keys - current_keys)]
    return comparison


def attach_comparison_section(report: Report, comparison: ReportComparison) -> Report:
    markdown = report.markdown.rstrip()
    section = _format_comparison_section(comparison)
    return report.model_copy(update={"comparison": comparison, "markdown": f"{markdown}\n\n{section}\n"})


def _load_report(record: Any) -> Report | None:
    payload = getattr(record, "payload", "")
    if not payload:
        return None
    try:
        return Report.model_validate(json.loads(payload))
    except (json.JSONDecodeError, ValueError, TypeError):
        return None


def _paper_index(report: Report) -> dict[str, TrendPaper]:
    indexed: dict[str, TrendPaper] = {}
    for category, summaries in [
        ("latest", report.latest),
        ("popular", report.popular),
        ("relevant", report.relevant),
    ]:
        for item in summaries:
            key = item.paper.stable_key
            if key not in indexed:
                indexed[key] = TrendPaper(
                    title=item.paper.title,
                    url=item.paper.url,
                    source=item.paper.source,
                    categories=[],
                    published_date=item.paper.published_date,
                )
            label = CATEGORY_NAMES.get(category, category)
            if label not in indexed[key].categories:
                indexed[key].categories.append(label)
    return indexed


def _format_comparison_section(comparison: ReportComparison) -> str:
    lines = ["## 五、历史增量追踪", ""]
    if comparison.has_previous:
        created_at = comparison.previous_created_at.strftime("%Y-%m-%d %H:%M") if comparison.previous_created_at else "未知时间"
        lines.append(f"对比上一期报告：#{comparison.previous_report_id or '-'}，生成时间：{created_at}。")
    else:
        lines.append("这是该研究方向的第一期可对比报告，本期结果将作为后续增量追踪基线。")
    lines.extend(
        [
            "",
            f"- 本期入选论文：{comparison.current_total} 篇",
            f"- 上期入选论文：{comparison.previous_total} 篇",
            f"- 本期新增：{len(comparison.new_papers)} 篇",
            f"- 延续关注：{len(comparison.continuing_papers)} 篇",
            f"- 本期退出：{len(comparison.dropped_papers)} 篇",
            "",
        ]
    )
    lines.extend(_paper_list("### 新增论文", comparison.new_papers))
    lines.extend(_paper_list("### 延续关注", comparison.continuing_papers))
    lines.extend(_paper_list("### 本期退出", comparison.dropped_papers))
    return "\n".join(lines)


def _paper_list(title: str, papers: list[TrendPaper], limit: int = 8) -> list[str]:
    lines = [title, ""]
    if not papers:
        return [*lines, "暂无。", ""]
    for paper in papers[:limit]:
        category_text = "、".join(paper.categories) or "未分类"
        link = paper.url or "#"
        lines.append(f"- [{paper.title}]({link})，来源：{paper.source}，命中榜单：{category_text}")
    if len(papers) > limit:
        lines.append(f"- 另有 {len(papers) - limit} 篇未展开。")
    lines.append("")
    return lines
