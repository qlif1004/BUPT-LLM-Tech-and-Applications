from __future__ import annotations

import json
from typing import Any

import httpx

from academic_tracker.config.settings import get_settings


class DeepSeekClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def available(self) -> bool:
        return bool(self.settings.deepseek_api_key)

    async def chat(self, messages: list[dict[str, str]], temperature: float = 0.2) -> str:
        if not self.available:
            raise RuntimeError("未配置 DEEPSEEK_API_KEY，请在 .env 中设置或通过环境变量传入。")
        url = f"{self.settings.deepseek_base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.settings.deepseek_api_key}",
            "Content-Type": "application/json",
        }
        payload: dict[str, Any] = {
            "model": self.settings.deepseek_model,
            "messages": messages,
            "temperature": temperature,
        }
        async with httpx.AsyncClient(timeout=self.settings.request_timeout) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    async def json_chat(self, messages: list[dict[str, str]], temperature: float = 0.1) -> dict[str, Any]:
        content = await self.chat(messages, temperature=temperature)
        cleaned = content.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned.removeprefix("```json").removesuffix("```").strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned.removeprefix("```").removesuffix("```").strip()
        return json.loads(cleaned)
