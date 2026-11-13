from dataclasses import asdict, dataclass
from collective_alpha.config import settings

@dataclass(frozen=True)
class ProviderStatus:
    provider: str
    status: str
    missing: list[str]
    note: str

def provider_status() -> dict:
    providers = []
    kis_missing = [name for name, value in (("KIS_APP_KEY", settings.kis_app_key), ("KIS_APP_SECRET", settings.kis_app_secret)) if not value]
    providers.append(ProviderStatus("KIS", "UNAVAILABLE" if kis_missing else "CONFIGURED", kis_missing,
        "Read-only market data; configured host defaults to KIS paper environment."))
    krx_missing = [name for name, value in (("KRX_BASE_URL", settings.krx_base_url), ("KRX_ENDPOINT", settings.krx_endpoint), ("KRX_AUTH_KEY", settings.krx_auth_key)) if not value]
    providers.append(ProviderStatus("KRX", "UNAVAILABLE" if krx_missing else "CONFIGURED", krx_missing,
        "Endpoint and parameters must match the exact approved KRX service specification."))
    dart_missing = ["DART_API_KEY"] if not settings.dart_api_key else []
    providers.append(ProviderStatus("DART", "UNAVAILABLE" if dart_missing else "CONFIGURED", dart_missing,
        "OpenDART corp-code and disclosure endpoints."))
    return {"mode": "LIVE" if all(p.status == "CONFIGURED" for p in providers) else "DEVELOPMENT",
            "live_data_ready": all(p.status == "CONFIGURED" for p in providers),
            "providers": [asdict(p) for p in providers],
            "credentials_exposed": False}
