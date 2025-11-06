from __future__ import annotations

from typing import Optional

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from .settings import settings


class LLMClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or settings.openai_api_key)
        self.model = model or settings.model_name
        self.temperature = settings.temperature
        self.top_p = settings.top_p

    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    def complete(self, messages: list[dict[str, str]]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p,
        )
        return response.choices[0].message.content
