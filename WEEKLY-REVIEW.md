# WEEKLY-REVIEW.md — weekly performance reviews (append-only)

Written by the Friday 3 PM run. Append at the BOTTOM.

## Template

```
## Week of YYYY-MM-DD
- Closed trades: n | winners: n | win rate: X%
- Avg winner: +X.XR | avg loser: -X.XR | expectancy: X.XR/trade
- Equity: start $X → end $X (X.X%)
- Rule violations: none | list them honestly
- What worked / what didn't:
- One change to test next week:
```

---

## Week of 2026-07-15 (Mon–Fri, 7/15–7/20)
- Closed trades: 0 | winners: n/a | win rate: n/a (no closes, all positions remain open)
- Open positions: 7 total (1 infra-test AAPL from 7/8, 6 Quy manual adds from 7/16 pre-open). Unrealized P&L: +$5.76 / +0.41%.
- Equity: start $100,010.72 (Mon 7/15 9:39 AM) → close $99,994.05 (Fri 7/20 4:00 PM) = **-$16.67 / -0.017%**
- Rule violations: position-count guardrail exceeded (7 open vs strategy's 4-max), weekly entry cap exceeded (6 new entries vs 5 allowed, all Quy's manual trades 7/16). Agent-driven entries this week: **0** (no research ideas survived the gate all five days). Confessed honestly; position-count/entry-cap breaches are Quy's manual trades, not agent-driven.
- What worked: guardrail discipline on the agent side — four consecutive no-trade days kept dry powder and risk small despite zero qualifying setups (position-count/weekly-entry caps now force "observe mode"). AAPL system-test position still profitable (+$16.34 / +5.26%). BTC/ETH/SOL crypto positions showing small gains (+$0.99 combined / +0.22%) despite BEAR regime and tight -7% stops.
- What didn't: crypto sleeve regime gate (BEAR, BTC < SMA200) correctly blocked entries all week, but Quy's manual BTC/ETH/SOL adds 7/16 contradicted the regime call — flagged honestly. No equities research ideas found all week (five premarket scans = 0 watchlist tickers cumulative) — low-activity week on "no gap + catalyst" environment and macro uncertainty (Fed blackout, earnings season, Iran tension, AI-capex anxiety dragging chips).
- One change to test next week: clarify position-count guardrail scope — does the 4-max apply to agent-driven entries only (recommend: yes) or the account holistically? With 7 concurrent and Quy's manual flexibility, the rule effectively gates only the agent. Future refinement: track agent-entries vs manual separately and report guardrail utilization (e.g., "3 of 4 agent slots full this week").
