from datetime import datetime, timezone

from academic_tracker.fetchers.dblp_fetcher import DblpFetcher
from academic_tracker.rankers.relevant import RelevanceRanker
from academic_tracker.storage.models import Paper, TaskConfig
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
