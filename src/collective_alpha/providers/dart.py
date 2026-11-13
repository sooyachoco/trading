from __future__ import annotations
from io import BytesIO
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import httpx

class DARTClient:
    BASE_URL = "https://opendart.fss.or.kr/api"
    def __init__(self, api_key: str): self.api_key = api_key
    def _require_key(self):
        if not self.api_key: raise RuntimeError("DART_API_KEY is required.")
    def corp_code_for_stock_code(self, stock_code: str) -> str:
        self._require_key()
        stock_code = stock_code.strip().zfill(6)
        if not stock_code.isdigit() or len(stock_code) != 6: raise ValueError("stock_code must be a six-digit numeric code.")
        response = httpx.get(f"{self.BASE_URL}/corpCode.xml", params={"crtfc_key":self.api_key}, timeout=30)
        response.raise_for_status()
        with ZipFile(BytesIO(response.content)) as archive:
            xml_name = next((n for n in archive.namelist() if n.lower().endswith(".xml")), None)
            if not xml_name: raise RuntimeError("DART corpCode.zip did not contain an XML file.")
            root = ET.fromstring(archive.read(xml_name))
        for item in root.findall("list"):
            if (item.findtext("stock_code") or "").strip() == stock_code:
                corp_code = (item.findtext("corp_code") or "").strip()
                if len(corp_code) == 8 and corp_code.isdigit(): return corp_code
        raise LookupError(f"No DART corporation code found for stock code {stock_code}.")
    def filings(self, corp_code: str, start_date: str, end_date: str, page_no: int = 1, page_count: int = 20):
        self._require_key()
        if not (corp_code.isdigit() and len(corp_code) == 8): raise ValueError("corp_code must be an 8-digit numeric DART corporation code.")
        for label, value in (("start_date", start_date), ("end_date", end_date)):
            if not (value.isdigit() and len(value) == 8): raise ValueError(f"{label} must use YYYYMMDD.")
        if start_date > end_date: raise ValueError("start_date must not be later than end_date.")
        if page_no < 1 or not 1 <= page_count <= 100: raise ValueError("page_no must be >= 1 and page_count must be between 1 and 100.")
        response = httpx.get(f"{self.BASE_URL}/list.json", params={"crtfc_key":self.api_key,"corp_code":corp_code,
            "bgn_de":start_date,"end_de":end_date,"page_no":page_no,"page_count":page_count,
            "sort":"date","sort_mth":"desc"}, timeout=25)
        response.raise_for_status()
        data = response.json()
        if data.get("status") not in {"000","013"}: raise RuntimeError(f"DART API error: {data.get('status')} {data.get('message')}")
        return data
