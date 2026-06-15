from __future__ import annotations

from pydantic import ValidationError

from academic_tracker.agent.deepseek_client import DeepSeekClient
from academic_tracker.storage.models import TaskConfig


class IntentParser:
    def __init__(self) -> None:
        self.llm = DeepSeekClient()

    async def parse(self, user_text: str) -> TaskConfig:
        if not self.llm.available:
            return self._fallback_parse(user_text)
        messages = [
            {
                "role": "system",
                "content": (
                    "你是学术论文追踪任务配置解析器。请把用户自然语言转换为严格 JSON，"
                    "字段包括：research_direction(str), keywords(list[str]), sources(list[str]), "
                    "time_range_days(int), schedule(str), categories(list[str]), "
                    "top_n_per_category(int), venues(list[str])。"
                    "你可以联想与用户直接提到的关键词相关但可能未被用户明确提到的其他重要技术术语或研究关键词，并把它们补充进 keywords 字段。"
                    "关键词需同时包含中文和英文版本，如果 keywords 字段只包含某个关键词的中文或英文，请补充其对应的翻译。"
                    "categories 只能从 latest、popular、relevant 三个英文值中选择。"
                    "如果用户说每类、三类或没有明确限制，就输出 "
                    "[\"latest\", \"popular\", \"relevant\"]。"
                    "不要把研究主题、技术方向或关键词放进 categories。"
                    "sources 可包含 arxiv、dblp、semantic_scholar、arxiv:cs.CL、"
                    "arxiv:cs.LG、dblp:KDD、dblp:WWW 等。"
                    "只输出 JSON，不要输出解释。"
                ),
            },
            {"role": "user", "content": user_text},
        ]
        try:
            data = await self.llm.json_chat(messages)
            return TaskConfig.model_validate(data)
        except Exception:
            return self._fallback_parse(user_text)

    def _fallback_parse(self, user_text: str) -> TaskConfig:
        keywords = []
        for sep in ["，", ",", "。", " "]:
            if sep in user_text:
                keywords = [item.strip() for item in user_text.split(sep) if 2 <= len(item.strip()) <= 40]
                break
        if not keywords:
            keywords = [user_text.strip()]

        sources = ["arxiv", "dblp", "semantic_scholar"]
        if "cs.CL" in user_text or "自然语言" in user_text or "NLP" in user_text.upper():
            sources.append("arxiv:cs.CL")
        if "cs.LG" in user_text or "机器学习" in user_text:
            sources.append("arxiv:cs.LG")
        days = 90 if "三个月" in user_text or "90" in user_text else 30
        schedule = "weekly" if "每周" in user_text or "周" in user_text else "manual"
        return TaskConfig(
            research_direction=keywords[0],
            keywords=keywords[:8],
            sources=sources,
            time_range_days=days,
            schedule=schedule,
        )
