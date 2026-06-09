from __future__ import annotations

import math
import re
from importlib.util import find_spec
from collections import Counter
from typing import Protocol

import httpx
import numpy as np

from academic_tracker.config.settings import get_settings
from academic_tracker.storage.models import Paper, TaskConfig

_TOKEN_RE = re.compile(r"[A-Za-z0-9_\-]+|[\u4e00-\u9fff]+")


class EmbeddingBackend(Protocol):
    name: str

    def embed(self, texts: list[str]) -> list[list[float]]:
        ...


class SentenceTransformerBackend:
    name = "sentence_transformers"

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model = None

    def embed(self, texts: list[str]) -> list[list[float]]:
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
        vectors = self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return vectors.tolist()


class OpenAICompatibleEmbeddingBackend:
    name = "openai_compatible"

    def __init__(self, api_key: str, base_url: str, model: str, timeout: float) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def embed(self, texts: list[str]) -> list[list[float]]:
        url = f"{self.base_url}/embeddings"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": self.model, "input": texts}
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
        data = sorted(response.json()["data"], key=lambda item: item["index"])
        return [item["embedding"] for item in data]


class RelevanceRanker:
    def __init__(self, embedding_backend: EmbeddingBackend | None = None) -> None:
        self.embedding_backend = embedding_backend

    def rank(self, papers: list[Paper], config: TaskConfig, top_n: int) -> list[Paper]:
        if not papers:
            return []

        query = " ".join(config.query_terms())
        lexical_scores = [self.lexical_score(query, paper) for paper in papers]
        semantic_scores = self._semantic_scores(query, papers)
        ranked_items = []

        for paper, lexical_score, semantic_score in zip(papers, lexical_scores, semantic_scores):
            if semantic_score is None:
                final_score = lexical_score
                method = "lexical_fallback"
            else:
                final_score = semantic_score * 0.85 + lexical_score * 0.15
                method = self._backend().name
            paper.relevance_score = final_score
            paper.extra = {
                **paper.extra,
                "relevance_ranker": method,
                "semantic_score": semantic_score,
                "lexical_score": lexical_score,
            }
            ranked_items.append((final_score, paper))

        return [paper for _, paper in sorted(ranked_items, key=lambda item: item[0], reverse=True)[:top_n]]

    def score(self, query: str, paper: Paper) -> float:
        semantic_scores = self._semantic_scores(query, [paper])
        lexical_score = self.lexical_score(query, paper)
        semantic_score = semantic_scores[0]
        if semantic_score is None:
            paper.relevance_score = lexical_score
        else:
            paper.relevance_score = semantic_score * 0.85 + lexical_score * 0.15
        return paper.relevance_score

    def lexical_score(self, query: str, paper: Paper) -> float:
        text = self._paper_text(paper)
        q_vec = self._tf(query)
        p_vec = self._tf(text)
        cosine = self._counter_cosine(q_vec, p_vec)
        keyword_bonus = sum(1 for token in q_vec if token in p_vec) / max(len(q_vec), 1)
        return cosine * 0.8 + keyword_bonus * 0.2

    def _semantic_scores(self, query: str, papers: list[Paper]) -> list[float | None]:
        backend = self._backend()
        if backend is None:
            return [None] * len(papers)

        texts = [query, *(self._paper_text(paper) for paper in papers)]
        try:
            vectors = backend.embed(texts)
        except Exception as exc:
            for paper in papers:
                paper.extra = {**paper.extra, "relevance_ranker_error": f"{type(exc).__name__}: {exc}"}
            return [None] * len(papers)

        query_vector = np.asarray(vectors[0], dtype=float)
        return [self._vector_cosine(query_vector, np.asarray(vector, dtype=float)) for vector in vectors[1:]]

    def _backend(self) -> EmbeddingBackend | None:
        if self.embedding_backend is not None:
            return self.embedding_backend

        settings = get_settings()
        provider = settings.embedding_provider.strip().lower()
        if provider in {"none", "off", "disabled"}:
            return None

        if provider in {"auto", "local", "sentence_transformers"}:
            if find_spec("sentence_transformers") is not None:
                self.embedding_backend = SentenceTransformerBackend(settings.local_embedding_model)
                return self.embedding_backend
            if provider != "auto":
                return None

        if provider in {"auto", "api", "openai", "openai_compatible"} and settings.embedding_api_key:
            self.embedding_backend = OpenAICompatibleEmbeddingBackend(
                api_key=settings.embedding_api_key,
                base_url=settings.embedding_base_url,
                model=settings.embedding_model,
                timeout=settings.request_timeout,
            )
            return self.embedding_backend

        return None

    def _paper_text(self, paper: Paper) -> str:
        return " ".join(
            item
            for item in [
                paper.title,
                paper.abstract,
                " ".join(paper.keywords),
                paper.venue or "",
            ]
            if item
        )

    def _tf(self, text: str) -> Counter[str]:
        return Counter(token.lower() for token in _TOKEN_RE.findall(text or ""))

    def _counter_cosine(self, a: Counter[str], b: Counter[str]) -> float:
        if not a or not b:
            return 0.0
        common = set(a) & set(b)
        numerator = sum(a[token] * b[token] for token in common)
        norm_a = math.sqrt(sum(value * value for value in a.values()))
        norm_b = math.sqrt(sum(value * value for value in b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return numerator / (norm_a * norm_b)

    def _vector_cosine(self, a: np.ndarray, b: np.ndarray) -> float:
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))
