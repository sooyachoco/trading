import httpx
from urllib.parse import urljoin

class KRXClient:
    # Endpoint and parameter schema must come from the exact KRX service specification.
    def __init__(self, base_url, endpoint, auth_key, auth_param="AUTH_KEY", date_param="basDd", market_param="", market_value=""):
        self.base_url, self.endpoint, self.auth_key = base_url, endpoint, auth_key
        self.auth_param, self.date_param = auth_param, date_param
        self.market_param, self.market_value = market_param, market_value
    def dataset(self, params):
        if not (self.base_url and self.endpoint and self.auth_key):
            raise RuntimeError("Configure KRX_BASE_URL, KRX_ENDPOINT and KRX_AUTH_KEY from the selected service specification.")
        query = dict(params)
        query.setdefault(self.auth_param, self.auth_key)
        if self.market_param and self.market_value: query.setdefault(self.market_param, self.market_value)
        url = urljoin(self.base_url.rstrip("/") + "/", self.endpoint.lstrip("/"))
        r = httpx.get(url, params=query, timeout=30)
        r.raise_for_status()
        if "json" in r.headers.get("content-type",""): return r.json()
        return {"content_type":r.headers.get("content-type",""),"text":r.text[:200000]}
