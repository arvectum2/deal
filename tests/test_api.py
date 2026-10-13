"""The API can start without secrets, database or live sites."""

from fastapi.testclient import TestClient

from dealforge import __version__
from dealforge.api.app import create_app


def test_health_has_stable_contract() -> None:
    with TestClient(create_app()) as client:
        result = client.get("/health")
        assert result.status_code == 200
        assert result.json() == {
            "status": "ok", "service": "dealforge", "version": __version__
        }


def test_real_data_platform_connector_is_available_offline() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/health/data-platform")
        assert response.status_code == 200
        assert response.json()["name"] == "manual_url"
        assert response.json()["state"] == "ready"
        assert "discover" in response.json()["capabilities"]
