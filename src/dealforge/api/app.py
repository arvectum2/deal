"""Foundational HTTP API with no external side effects."""

from fastapi import FastAPI

from dealforge import __version__
from dealforge.adapters.data_platform import DataPlatformDiscovery


def create_app() -> FastAPI:
    app = FastAPI(
        title="Arvectum DealForge",
        version=__version__,
        description="Buyer-centric sourcing. External outreach requires approval (not built).",
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "dealforge", "version": __version__}

    @app.get("/health/data-platform")
    def data_platform_health() -> dict[str, object]:
        return DataPlatformDiscovery().connector_health()

    return app


app = create_app()
