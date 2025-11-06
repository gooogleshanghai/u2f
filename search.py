from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Iterable

from .settings import settings


@dataclass
class SearchResult:
    title: str
    link: str
    snippet: str


class SearchAugmentor:
    def __init__(self):
        self.api_key = settings.search_api_key
        self.engine_id = settings.search_engine_id

    def enabled(self) -> bool:
        return bool(self.api_key and self.engine_id)

    def search(self, query: str, *, max_results: int = 3) -> list[SearchResult]:
        if not self.enabled():
            return []

        base = "https://www.googleapis.com/customsearch/v1"
        params = urllib.parse.urlencode(
            {
                "key": self.api_key,
                "cx": self.engine_id,
                "q": query,
                "num": max_results,
            }
        )

        with urllib.request.urlopen(f"{base}?{params}", timeout=10) as response:
            payload = json.loads(response.read())

        items = payload.get("items", [])
        results: list[SearchResult] = []
        for item in items:
            results.append(
                SearchResult(
                    title=item.get("title", ""),
                    link=item.get("link", ""),
                    snippet=item.get("snippet", ""),
                )
            )
        return results

    def render_results(self, results: Iterable[SearchResult]) -> str:
        lines: list[str] = []
        for index, result in enumerate(results, start=1):
            lines.append(
                f"[{index}] {result.title}\nURL: {result.link}\nSummary: {result.snippet}"
            )
        return "\n\n".join(lines)
