"""Defaults must be local-only; deployment config cannot open the port publicly by accident."""

from dealforge.settings import Settings


def test_default_binding_is_loopback(monkeypatch) -> None:
    monkeypatch.delenv("DEAL_HOST", raising=False)
    monkeypatch.delenv("DEAL_PORT", raising=False)
    cfg = Settings(_env_file=None)
    assert cfg.host == "127.0.0.1"
    assert cfg.port == 8767
