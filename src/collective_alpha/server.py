import json, os
from mcp.server.fastmcp import FastMCP
from collective_alpha.config import settings
from collective_alpha.providers.kis import KISClient
from collective_alpha.providers.krx import KRXClient
from collective_alpha.providers.dart import DARTClient
from collective_alpha.paper import PaperBroker
from collective_alpha.status import provider_status
from collective_alpha.providers.mock import MockMarketData

mcp = FastMCP("collective-alpha-korea")
kis = KISClient(settings.kis_app_key, settings.kis_app_secret, settings.kis_base_url)
krx = KRXClient(settings.krx_base_url, settings.krx_endpoint, settings.krx_auth_key, settings.krx_auth_param,
                settings.krx_date_param, settings.krx_market_param, settings.krx_market_value)
dart = DARTClient(settings.dart_api_key)
paper = PaperBroker(settings.db_path)

@mcp.tool()
def provider_status() -> str:
    """Show whether KIS, KRX and DART are configured; never returns secret values."""
    return json.dumps(provider_status(), ensure_ascii=False)

@mcp.tool()
def mock_skc_snapshot() -> str:
    """Return schema-only SKC demo data. This contains no real market prices."""
    return json.dumps(MockMarketData().snapshot("011790"), ensure_ascii=False)

@mcp.tool()
def kis_quote(symbol: str) -> str:
    """Read a domestic KRX stock quote. Uses the configured KIS paper host by default."""
    return json.dumps(kis.quote(symbol), ensure_ascii=False)

@mcp.tool()
def kis_daily_prices(symbol: str, start_date: str, end_date: str, period: str = "D") -> str:
    """Read daily/weekly/monthly bars. Dates use YYYYMMDD."""
    return json.dumps(kis.daily_prices(symbol, start_date, end_date, period), ensure_ascii=False)

@mcp.tool()
def dart_corp_code(stock_code: str) -> str:
    """Resolve a six-digit stock code to its 8-digit OpenDART corporation code."""
    return dart.corp_code_for_stock_code(stock_code)

@mcp.tool()
def dart_filings(corp_code: str, start_date: str, end_date: str, page_no: int = 1, page_count: int = 20) -> str:
    return json.dumps(dart.filings(corp_code, start_date, end_date, page_no, page_count), ensure_ascii=False)

@mcp.tool()
def dart_filings_by_stock_code(stock_code: str, start_date: str, end_date: str, page_no: int = 1, page_count: int = 20) -> str:
    corp_code = dart.corp_code_for_stock_code(stock_code)
    return json.dumps({"corp_code":corp_code,"filings":dart.filings(corp_code,start_date,end_date,page_no,page_count)},ensure_ascii=False)

@mcp.tool()
def krx_dataset(params_json: str) -> str:
    params = json.loads(params_json or "{}")
    if not isinstance(params,dict): raise ValueError("params_json must encode a JSON object")
    return json.dumps(krx.dataset(params),ensure_ascii=False)

@mcp.tool()
def paper_portfolio() -> str:
    return json.dumps(paper.portfolio(),ensure_ascii=False)

@mcp.tool()
def paper_order(symbol: str, side: str, quantity: int, price: float) -> str:
    """Simulated local order only; never routes to KIS or any broker."""
    return json.dumps(paper.order(symbol,side,quantity,price),ensure_ascii=False)

@mcp.tool()
def paper_reset(confirm: bool = False) -> str:
    if not confirm: return "Not reset. confirm=true is required to erase the virtual ledger."
    if os.path.exists(settings.db_path): os.remove(settings.db_path)
    global paper
    paper = PaperBroker(settings.db_path)
    return "Paper ledger reset. PAPER_ONLY."

def main(): mcp.run()
if __name__ == "__main__": main()
