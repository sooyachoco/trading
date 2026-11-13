from datetime import datetime, timezone

class MockMarketData:
    """Schema-only demo fixtures. No fabricated market price is presented as real data."""
    def snapshot(self, symbol: str = "011790") -> dict:
        symbol = symbol.strip().zfill(6)
        if not (symbol.isdigit() and len(symbol) == 6):
            raise ValueError("symbol must be a six-digit numeric stock code")
        now = datetime.now(timezone.utc).isoformat()
        return {
            "mode": "MOCK",
            "is_real_market_data": False,
            "symbol": symbol,
            "as_of": now,
            "quote": {"current_price": None, "change": None, "volume": None, "source": "MOCK_SCHEMA_ONLY"},
            "daily_prices": [],
            "disclosures": [],
            "missing_live_sources": ["KIS", "KRX", "DART"],
            "notice": "This is a schema/demo response only. No current or historical market values are included."
        }
