from collective_alpha.status import provider_status
from collective_alpha.providers.mock import MockMarketData

def test_all_providers_report_unavailable_without_credentials(monkeypatch):
    from collective_alpha import config
    for key in ("kis_app_key", "kis_app_secret", "krx_base_url", "krx_endpoint", "krx_auth_key", "dart_api_key"):
        monkeypatch.setattr(config.settings, key, "")
    result = provider_status()
    assert result["mode"] == "DEVELOPMENT"
    assert result["live_data_ready"] is False
    assert [p["status"] for p in result["providers"]] == ["UNAVAILABLE"] * 3
    assert result["credentials_exposed"] is False

def test_mock_snapshot_never_claims_live_price():
    result = MockMarketData().snapshot("11790")
    assert result["mode"] == "MOCK"
    assert result["is_real_market_data"] is False
    assert result["symbol"] == "011790"
    assert result["quote"]["current_price"] is None
    assert result["missing_live_sources"] == ["KIS", "KRX", "DART"]
