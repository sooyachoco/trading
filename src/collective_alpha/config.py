import os
from dataclasses import dataclass
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

@dataclass(frozen=True)
class Settings:
    kis_app_key: str = os.getenv("KIS_APP_KEY", "")
    kis_app_secret: str = os.getenv("KIS_APP_SECRET", "")
    kis_base_url: str = os.getenv("KIS_BASE_URL", "https://openapivts.koreainvestment.com:29443")
    krx_base_url: str = os.getenv("KRX_BASE_URL", "")
    krx_endpoint: str = os.getenv("KRX_ENDPOINT", "")
    krx_auth_key: str = os.getenv("KRX_AUTH_KEY", "")
    krx_auth_param: str = os.getenv("KRX_AUTH_PARAM", "AUTH_KEY")
    krx_date_param: str = os.getenv("KRX_DATE_PARAM", "basDd").strip()
    krx_market_param: str = os.getenv("KRX_MARKET_PARAM", "")
    krx_market_value: str = os.getenv("KRX_MARKET_VALUE", "")
    dart_api_key: str = os.getenv("DART_API_KEY", "")
    db_path: str = os.getenv("COLLECTIVE_ALPHA_DB", "./data/collective_alpha.sqlite3")

settings = Settings()
