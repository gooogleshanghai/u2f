from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DiscoveryOutput:
    core_problem: str
    baseline_solution: str
    critical_defects: str


@dataclass
class ExplorationOutput:
    analysis: str
    validated_uus: str
    requires_discovery_reset: bool = False
    requires_more_validation: bool = False


@dataclass
class IntegrationOutput:
    synthesis: str
    callback: str | None = None


@dataclass
class ConversationContext:
    enabler_story: str
    potential_fix: str
    human_preferences: str | None = None
    discovery: DiscoveryOutput | None = None
    exploration: ExplorationOutput | None = None
    integration: IntegrationOutput | None = None
    search_log: list[str] = field(default_factory=list)

    def append_search(self, query: str, results: str) -> None:
        self.search_log.append(f"Query: {query}\n{results}")
