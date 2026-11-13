from io import BytesIO
from zipfile import ZipFile
from unittest.mock import Mock
import pytest
from collective_alpha.providers.dart import DARTClient
from collective_alpha.providers.krx import KRXClient
from collective_alpha.providers.kis import KISClient

def response(payload=None,content=b"",headers=None):
    r=Mock(); r.json.return_value=payload or {}; r.content=content; r.headers=headers or {"content-type":"application/json"}; r.text="{}"; r.raise_for_status.return_value=None; return r

def test_kis_quote_uses_paper_host_and_expected_tr_id(monkeypatch):
    calls=[]
    monkeypatch.setattr("collective_alpha.providers.kis.httpx.post",lambda *a,**k:response({"access_token":"test-token","expires_in":3600}))
    def fake_get(url,headers,params,timeout): calls.append((url,headers,params)); return response({"rt_cd":"0","output":{"stck_prpr":"70000"}})
    monkeypatch.setattr("collective_alpha.providers.kis.httpx.get",fake_get)
    result=KISClient("paper-key","paper-secret","https://paper.example").quote("11790")
    assert result["output"]["stck_prpr"]=="70000" and calls[0][0].endswith("/inquire-price")
    assert calls[0][1]["tr_id"]=="FHKST01010100" and calls[0][1]["custtype"]=="P" and calls[0][2]["FID_INPUT_ISCD"]=="011790"

def test_kis_requires_credentials():
    with pytest.raises(RuntimeError,match="KIS_APP_KEY"): KISClient("","","https://paper.example").quote("011790")

def test_dart_resolves_skc_stock_code_from_corp_zip(monkeypatch):
    stream=BytesIO()
    with ZipFile(stream,"w") as z: z.writestr("CORPCODE.xml","<result><list><corp_code>00123456</corp_code><corp_name>SKC</corp_name><stock_code>011790</stock_code></list></result>")
    monkeypatch.setattr("collective_alpha.providers.dart.httpx.get",lambda *a,**k:response(content=stream.getvalue()))
    assert DARTClient("key").corp_code_for_stock_code("011790")=="00123456"

def test_dart_rejects_invalid_dates():
    with pytest.raises(ValueError,match="YYYYMMDD"): DARTClient("key").filings("00123456","2026-01-01","20261231")

def test_krx_requires_exact_service_configuration():
    with pytest.raises(RuntimeError,match="KRX_BASE_URL"): KRXClient("","","").dataset({"basDd":"20261113"})

def test_krx_passes_configured_auth_and_parameters(monkeypatch):
    calls=[]
    def fake_get(url,params,timeout): calls.append((url,params)); return response({"OutBlock_1":[]})
    monkeypatch.setattr("collective_alpha.providers.krx.httpx.get",fake_get)
    client=KRXClient("https://krx.example","/svc","secret","AUTH_KEY",market_param="market",market_value="KOSPI")
    assert client.dataset({"basDd":"20261113"})=={"OutBlock_1":[]}
    assert calls[0]==("https://krx.example/svc",{"basDd":"20261113","AUTH_KEY":"secret","market":"KOSPI"})
