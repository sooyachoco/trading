import httpx

class KRXClient:
    """KRX stock daily-trading API; AUTH_KEY is an HTTP request header."""
    BASE_URL = "https://data-dbg.krx.co.kr"
    ENDPOINTS = {"KOSPI": "/svc/apis/sto/stk_bydd_trd", "KOSDAQ": "/svc/apis/sto/ksq_bydd_trd"}

    def __init__(self, auth_key: str, base_url: str = BASE_URL):
        self.auth_key = auth_key.strip()
        self.base_url = base_url.rstrip("/")

    def daily_trading(self, market: str, base_date: str):
        market = market.strip().upper()
        if market not in self.ENDPOINTS:
            raise ValueError("market must be KOSPI or KOSDAQ")
        if not (base_date.isdigit() and len(base_date) == 8):
            raise ValueError("base_date must use YYYYMMDD")
        if not self.auth_key:
            raise RuntimeError("KRX_AUTH_KEY is required")
        response = httpx.get(self.base_url + self.ENDPOINTS[market],
            headers={"AUTH_KEY": self.auth_key, "Accept": "application/json"},
            params={"basDd": base_date}, timeout=30)
        response.raise_for_status()
        return response.json()

    def kospi_daily(self, base_date: str):
        return self.daily_trading("KOSPI", base_date)

    def kosdaq_daily(self, base_date: str):
        return self.daily_trading("KOSDAQ", base_date)
