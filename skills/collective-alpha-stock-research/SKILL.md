---
name: collective-alpha-stock-research
description: Research KOSPI/KOSDAQ equities using KIS, KRX, OpenDART, six specialist agents, independent risk gates and paper-trading validation.
---

# COLLECTIVE ALPHA — Korean Equity Research

## Non-negotiable rules
- V1.0 is research and paper trading only. Never place real brokerage orders.
- Separate verified facts, calculations, hypotheses and forecasts.
- State source, timestamp, freshness, missing fields and market session.
- Never invent quotes, flows, filings, analyst targets or API responses.
- If a provider is unavailable, disclose the gap; do not silently substitute stale data.
- Simulations must include fees, taxes, slippage, liquidity and trading halts.
- Do not promote a model based on one profitable period.

## Six specialist agents
1. TREND: OHLCV, moving averages, RSI, MACD, volatility, relative strength and drawdown.
2. FLOW: foreign/institution/retail flows, program trading, short-sale and lending data when licensed.
3. VALUE: revenue, operating profit, margins, debt, cash flow, valuation and dilution.
4. SENTIMENT: dated news and disclosures; distinguish confirmed facts from rumor.
5. GUARDIAN: independent veto for liquidity, drawdown, concentration, event and data-quality risk.
6. RESEARCH: hypotheses, ablation tests, walk-forward experiments and failure analysis.

## Workflow
1. Resolve ticker, security type and point-in-time universe membership.
2. Fetch KIS quote and historical bars; record timestamp and adjustment mode.
3. Fetch KRX data only through the exact configured service schema.
4. Fetch OpenDART filings using the correct 8-digit corporation code; inspect original filing before material conclusions.
5. Compute returns, trend, volatility, volume anomalies, drawdown and investor-flow features where available.
6. Each agent returns stance, horizon, confidence, evidence, invalidations, timestamp and model version.
7. Learn consensus weights only from out-of-sample track records. Guardian remains a separate veto.
8. Produce 5/10/20-trading-day bull/base/bear scenarios, not certainty or guaranteed target prices.
9. Calculate paper position size from risk budget and stop distance. Never average down solely to lower cost basis.
10. Record predictions before outcomes; score after each horizon closes against a benchmark and after costs.
11. Evaluate daily; retrain only on a schedule or validated drift trigger.

## Required report
- Snapshot and data freshness
- Company and sector thesis
- TREND / FLOW / VALUE / SENTIMENT / RESEARCH opinions
- GUARDIAN risk gate
- Consensus: STRONG_BUY_CANDIDATE / BUY_CANDIDATE / WATCH / HOLD / AVOID / BLOCKED_BY_RISK
- Bull/base/bear scenarios and invalidation levels
- Paper trade proposal or explicit no-trade, with sizing and cost assumptions
- Uncertainties and missing data

## Model promotion
Use chronological walk-forward validation, purging/embargo for overlapping labels, survivorship-bias-aware universes, corporate-action adjustments, realistic costs, paper trading, versioned artifacts and reproducible tests. Compare with buy-and-hold and simple baselines.
