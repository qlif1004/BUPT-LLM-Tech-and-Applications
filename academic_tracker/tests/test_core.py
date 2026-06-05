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
