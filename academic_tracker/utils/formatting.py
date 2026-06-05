from __future__ import annotations

from pathlib import Path

from academic_tracker.config.settings import get_settings


def save_markdown_report(markdown: str, research_direction: str) -> Path:
    settings = get_settings()
    report_dir = Path(settings.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(ch if ch.isalnum() else "_" for ch in research_direction).strip("_")[:60] or "report"
    existing = len(list(report_dir.glob(f"{safe_name}_*.md"))) + 1
    path = report_dir / f"{safe_name}_{existing:03d}.md"
    path.write_text(markdown, encoding="utf-8")
    return path
