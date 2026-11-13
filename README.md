# COLLECTIVE ALPHA V1.0 — Korean Equity Research + Paper Trading

A Python MCP server for KOSPI/KOSDAQ research using KIS market data, KRX Open API datasets and OpenDART disclosures. Includes a local SQLite **paper-only** broker. No live-order endpoint exists.

## Local setup

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# Fill credentials locally; never commit .env.
pytest -q
collective-alpha-mcp
```

## Credentials
- KIS: create a paper-trading app and set `KIS_APP_KEY`, `KIS_APP_SECRET`. Default host is the KIS paper host.
- KRX: apply for a key and the required dataset. Configure the exact `KRX_BASE_URL`, `KRX_ENDPOINT`, auth parameter and query parameters from that dataset's service specification. KRX services do not all share one schema.
- OpenDART: set `DART_API_KEY`. `dart_corp_code("011790")` resolves SKC's eight-digit corporation code from the official corp-code ZIP.

## MCP tools
`kis_quote`, `kis_daily_prices`, `dart_corp_code`, `dart_filings`, `dart_filings_by_stock_code`, `krx_dataset`, `paper_portfolio`, `paper_order`, `paper_reset`.

## Scope and controls
- V1.0 has no live brokerage order capability. `paper_order` writes only to a local SQLite ledger.
- Simulated fills include configurable fee and sell-tax basis points. Slippage is not yet modeled and must be added before strategy performance is interpreted.
- Never commit `.env`; rotate credentials immediately if exposed.
- Verify API quotas, permitted storage/redistribution and commercial-use terms with each provider.
- KIS portal lists notices dated 2026-10-27 and 2026-10-29; check current endpoint status before deployment. The starter uses quote/history endpoints and OpenDART/KRX for disclosures and exchange datasets.
- Daily evaluation is not daily retraining. Use walk-forward validation, realistic costs, survivorship-bias-aware universes, corporate-action adjustments and versioned models.

## Sprint 01 validation

Unit tests mock provider HTTP responses and verify URL/parameters, symbol normalization, DART corporation-code lookup, KRX service configuration and paper-ledger accounting. Real provider connectivity still requires the user's keys and a selected KRX dataset.
