"""Test the public connector DTO contract, with no outbound HTTP calls."""

from dataclasses import dataclass

from arvectum_data.connectors import (
    ConnectorHealth,
    ConnectorState,
    DiscoveredResource,
    DiscoveryPage,
)

from dealforge.adapters.data_platform import DataPlatformDiscovery


@dataclass
class FakeDiscoverer:
    name: str = "fake_test"

    def discover(
        self, query: str, *, cursor: str | None = None, limit: int = 10
    ) -> DiscoveryPage:
        assert cursor is None
        assert limit == 1
        return DiscoveryPage(resources=(DiscoveredResource(
            canonical_uri=query,
            provider=self.name,
            source_type="url",
            title="Source, not a confirmed offer",
            rank=1,
        ),))

    def health(self) -> ConnectorHealth:
        return ConnectorHealth(
            name=self.name,
            state=ConnectorState.READY,
            capabilities=("discover",),
        )


def test_discover_adapts_stable_data_platform_contract() -> None:
    adapter = DataPlatformDiscovery(FakeDiscoverer())
    results = adapter.discover_url("https://example.com/offer")
    assert len(results) == 1
    item = results[0]
    assert item.url == "https://example.com/offer"
    assert item.source == "fake_test"
    assert item.title == "Source, not a confirmed offer"
    assert item.source_type == "url"
    assert adapter.connector_health()["state"] == "ready"


def test_no_auto_offers_or_supplier_communications_in_boundary() -> None:
    item = DataPlatformDiscovery(FakeDiscoverer()).discover_url(
        "https://example.com/unverified"
    )[0]
    assert not hasattr(item, "discount_percent")
    assert not hasattr(item, "verified")
    assert not hasattr(item, "send_to_supplier")
