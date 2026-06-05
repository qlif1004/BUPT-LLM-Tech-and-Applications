from __future__ import annotations

import math
import re
from collections import Counter

from academic_tracker.storage.models import Paper, TaskConfig

_TOKEN_RE = re.compile(r"[A-Za-z0-9_\-]+|[\u4e00-\u9fff]+")


class RelevanceRanker:
    def rank(self, papers: list[Paper], config: TaskConfig, top_n: int) -> list[Paper]:
        query = " ".join(config.query_terms())
        ranked = sorted(papers, key=lambda paper: self.score(query, paper), reverse=True)
        return ranked[:top_n]

    def score(self, query: str, paper: Paper) -> float:
        text = f"{paper.title} {paper.abstract} {' '.join(paper.keywords)}"
        q_vec = self._tf(query)
        p_vec = self._tf(text)
        cosine = self._cosine(q_vec, p_vec)
        keyword_bonus = sum(1 for token in q_vec if token in p_vec) / max(len(q_vec), 1)
        paper.relevance_score = cosine * 0.8 + keyword_bonus * 0.2
        return paper.relevance_score

    def _tf(self, text: str) -> Counter[str]:
        return Counter(token.lower() for token in _TOKEN_RE.findall(text or ""))

    def _cosine(self, a: Counter[str], b: Counter[str]) -> float:
        if not a or not b:
            return 0.0
        common = set(a) & set(b)
        numerator = sum(a[token] * b[token] for token in common)
        norm_a = math.sqrt(sum(value * value for value in a.values()))
        norm_b = math.sqrt(sum(value * value for value in b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return numerator / (norm_a * norm_b)
