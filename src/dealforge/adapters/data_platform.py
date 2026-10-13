"""Anti-corruption boundary to the version-pinned Arvectum Data Platform SDK.

This adapter discovers *candidate public URLs*, not verified deals or discounts.
No external supplier communication or automatic purchasing is performed here.
"""

from dataclasses import dataclass
from typing import Protocol

from arvectum_data.connectors import (
    ConnectorHealth,
    DiscoveryPage,
    ManualURLConnector,
)


@dataclass(frozen=True, slots=True)
class SourceCandidate:
    url: str
    source: str
    source_type: str
    title: str | None
    rank: int | None


class URLDiscoverer(Protocol):
    """Minimal supported Data Platform discovery surface."""

    name: str

    def discover(
        self, query: str, *, cursor: str | None = None, limit: int = 10
    ) -> DiscoveryPage: ...

    def health(self) -> ConnectorHealth: ...


class DataPlatformDiscovery:
    """Translate a generic Data Platform resource into a DealForge candidate."""

    def __init__(self, connector: URLDiscoverer | None = None) -> None:
        self._connector = connector if connector is not None else ManualURLConnector()

    def connector_health(self) -> dict[str, object]:
        health = self._connector.health()
        return {
            "name": health.name,
            "state": str(health.state.value),
            "capabilities": list(health.capabilities),
        }

    def discover_url(self, url: str) -> tuple[SourceCandidate, ...]:
        page = self._connector.discover(url, limit=1)
        return tuple(
            SourceCandidate(
                url=item.canonical_uri,
                source=item.provider,
                source_type=item.source_type,
                title=item.title,
                rank=item.rank,
            )
            for item in page.resources
        )
