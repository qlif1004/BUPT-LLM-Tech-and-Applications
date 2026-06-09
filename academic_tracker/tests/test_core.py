from datetime import datetime, timezone

from academic_tracker.fetchers.dblp_fetcher import DblpFetcher
from academic_tracker.agent.report_comparison import compare_with_previous_report
from academic_tracker.rankers.relevant import RelevanceRanker
from academic_tracker.storage.models import Paper, PaperSummary, Report, TaskConfig
from academic_tracker.utils.deduplication import deduplicate_papers


def test_deduplicate_by_doi():
    papers = [
        Paper(title="A", doi="10.1/test", citation_count=1),
        Paper(title="A copy", doi="10.1/test", citation_count=5),
    ]
    result = deduplicate_papers(papers)
    assert len(result) == 1
    assert result[0].citation_count == 5


def test_relevance_ranker():
    config = TaskConfig(research_direction="retrieval augmented generation", keywords=["RAG"])
    papers = [
        Paper(title="Vision model", abstract="image classification"),
        Paper(title="RAG for question answering", abstract="retrieval augmented generation improves answers"),
    ]
    ranked = RelevanceRanker().rank(papers, config, top_n=1)
    assert ranked[0].title == "RAG for question answering"


def test_dblp_parse_payload_filters_by_requested_venue():
    fetcher = DblpFetcher()
    config = TaskConfig(
        research_direction="graph foundation model",
        keywords=["graph foundation model"],
        sources=["dblp:WWW"],
        time_range_days=3650,
    )
    payload = {
        "result": {
            "hits": {
                "hit": [
                    {
                        "info": {
                            "title": "GraphCLIP",
                            "authors": {"author": [{"text": "Alice"}, {"text": "Bob"}]},
                            "venue": "WWW",
                            "year": "2025",
                            "key": "conf/www/graphclip25",
                            "doi": "10.1/graphclip",
                            "ee": "https://doi.org/10.1/graphclip",
                            "url": "https://dblp.org/rec/conf/www/graphclip25",
                            "type": "Conference and Workshop Papers",
                        }
                    },
                    {
                        "info": {
                            "title": "Graphs for NLP",
                            "authors": {"author": {"text": "Carol"}},
                            "venue": "ACL",
                            "year": "2025",
                            "key": "conf/acl/graphs25",
                            "url": "https://dblp.org/rec/conf/acl/graphs25",
                        }
                    },
                ]
            }
        }
    }

    papers = fetcher._parse_payload(payload, config)

    assert len(papers) == 1
    assert papers[0].title == "GraphCLIP"
    assert papers[0].authors == ["Alice", "Bob"]
    assert papers[0].doi == "10.1/graphclip"
    assert papers[0].url == "https://doi.org/10.1/graphclip"
    assert papers[0].external_id == "conf/www/graphclip25"
    assert papers[0].published_date == datetime(2025, 1, 1, tzinfo=timezone.utc)


def test_dblp_requested_venues_merge_sources_and_config():
    fetcher = DblpFetcher()
    config = TaskConfig(
        research_direction="retrieval",
        sources=["dblp", "dblp:SIGIR"],
        venues=["CIKM", "SIGIR"],
    )

    venues = fetcher._requested_venues(config)

    assert venues == ["CIKM", "SIGIR"]


def test_report_comparison_marks_first_report_as_new():
    report = Report(
        task_config=TaskConfig(research_direction="RAG"),
        latest=[PaperSummary(paper=Paper(title="New RAG Paper", external_id="paper-1"), summary="summary")],
    )

    comparison = compare_with_previous_report(report, None)

    assert comparison.previous_total == 0
    assert comparison.current_total == 1
    assert [paper.title for paper in comparison.new_papers] == ["New RAG Paper"]
    assert comparison.continuing_papers == []
    assert comparison.dropped_papers == []


def test_report_comparison_splits_new_continuing_and_dropped():
    previous = Report(
        task_config=TaskConfig(research_direction="RAG"),
        latest=[
            PaperSummary(paper=Paper(title="Kept Paper", external_id="kept"), summary="summary"),
            PaperSummary(paper=Paper(title="Dropped Paper", external_id="dropped"), summary="summary"),
        ],
    )
    current = Report(
        task_config=TaskConfig(research_direction="RAG"),
        latest=[
            PaperSummary(paper=Paper(title="Kept Paper", external_id="kept"), summary="summary"),
            PaperSummary(paper=Paper(title="New Paper", external_id="new"), summary="summary"),
        ],
    )
    previous_record = type(
        "PreviousReportRecord",
        (),
        {"id": 3, "payload": previous.model_dump_json(), "created_at": previous.created_at},
    )()

    comparison = compare_with_previous_report(current, previous_record)

    assert comparison.previous_report_id == 3
    assert comparison.previous_total == 2
    assert comparison.current_total == 2
    assert [paper.title for paper in comparison.new_papers] == ["New Paper"]
    assert [paper.title for paper in comparison.continuing_papers] == ["Kept Paper"]
    assert [paper.title for paper in comparison.dropped_papers] == ["Dropped Paper"]
