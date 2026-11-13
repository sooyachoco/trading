import time
import httpx

class KISClient:
    # Read-only KIS REST client. Defaults to the paper-trading host.
    def __init__(self, app_key: str, app_secret: str, base_url: str):
        self.app_key, self.app_secret = app_key, app_secret
        self.base_url = base_url.rstrip("/")
        self._token, self._token_expiry = None, 0

    def _access_token(self):
        if self._token and time.time() < self._token_expiry - 60:
            return self._token
        if not self.app_key or not self.app_secret:
            raise RuntimeError("KIS_APP_KEY and KIS_APP_SECRET are required.")
        r = httpx.post(f"{self.base_url}/oauth2/tokenP",
            json={"grant_type":"client_credentials","appkey":self.app_key,"appsecret":self.app_secret}, timeout=20)
        r.raise_for_status()
        data = r.json()
        self._token = data["access_token"]
        self._token_expiry = time.time() + int(data.get("expires_in", 86400))
        return self._token

    def _get(self, path, tr_id, params):
        headers = {"authorization":f"Bearer {self._access_token()}","appkey":self.app_key,
                   "appsecret":self.app_secret,"tr_id":tr_id,"custtype":"P"}
        r = httpx.get(f"{self.base_url}{path}", headers=headers, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        if data.get("rt_cd") not in (None, "0"):
            raise RuntimeError(f"KIS API error: {data.get('msg_cd')} {data.get('msg1')}")
        return data

    def quote(self, symbol):
        return self._get("/uapi/domestic-stock/v1/quotations/inquire-price", "FHKST01010100",
            {"FID_COND_MRKT_DIV_CODE":"J","FID_INPUT_ISCD":symbol.zfill(6)})

    def daily_prices(self, symbol, start_date, end_date, period="D"):
        if period not in {"D","W","M"}:
            raise ValueError("period must be D, W, or M")
        return self._get("/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice", "FHKST03010100",
            {"FID_COND_MRKT_DIV_CODE":"J","FID_INPUT_ISCD":symbol.zfill(6),
             "FID_INPUT_DATE_1":start_date,"FID_INPUT_DATE_2":end_date,
             "FID_PERIOD_DIV_CODE":period,"FID_ORG_ADJ_PRC":"0"})
