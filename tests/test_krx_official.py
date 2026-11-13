import pytest
from unittest.mock import Mock
from collective_alpha.providers.krx import KRXClient

def test_krx_kospi_official_request(monkeypatch):
    calls=[]
    def fake_get(url, headers, params, timeout):
        calls.append((url, headers, params))
        r=Mock(); r.raise_for_status.return_value=None
        r.json.return_value={"OutBlock_1":[{"ISU_SRT_CD":"011790"}]}
        return r
    monkeypatch.setattr("collective_alpha.providers.krx.httpx.get", fake_get)
    result=KRXClient("secret").kospi_daily("20261113")
    assert result["OutBlock_1"][0]["ISU_SRT_CD"]=="011790"
    assert calls[0][0]=="https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd"
    assert calls[0][1]["AUTH_KEY"]=="secret"
    assert calls[0][2]=={"basDd":"20261113"}

def test_krx_kosdaq_endpoint(monkeypatch):
    urls=[]
    def fake_get(url, headers, params, timeout):
        urls.append(url)
        r=Mock(); r.raise_for_status.return_value=None; r.json.return_value={"OutBlock_1":[]}
        return r
    monkeypatch.setattr("collective_alpha.providers.krx.httpx.get", fake_get)
    KRXClient("secret").kosdaq_daily("20261113")
    assert urls[0].endswith("/svc/apis/sto/ksq_bydd_trd")

def test_krx_validation():
    with pytest.raises(ValueError): KRXClient("secret").daily_trading("KONEX","20261113")
    with pytest.raises(ValueError): KRXClient("secret").daily_trading("KOSPI","2026-11-13")
    with pytest.raises(RuntimeError): KRXClient("").daily_trading("KOSPI","20261113")
