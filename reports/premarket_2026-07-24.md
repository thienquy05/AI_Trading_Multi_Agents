# 🧠 AI PREMARKET REPORT - Zenith

### Friday, July 24, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

Second straight day with a real, verified setup blocked purely by a data
gap: INTC clears 5 of 6 checks for BOTH the day and swing screens on a
genuine earnings blowout, and only fails on market cap (unavailable —
yfinance blocked again). Same pattern as yesterday's NOK, but stronger —
this one clears the 8% swing gap threshold outright. Doesn't matter for
action either way: the account is still at 7 concurrent positions,
seventh-plus straight day pinned at the cap. Rules and discretion agree:
stand aside, but this is the second consecutive day worth flagging the
data-gap pattern explicitly.

## 📊 Pre-Market Gappers

**INTC (Intel)** — gap +9.8% to $109.86 (prev close $100.05). Real,
substantial catalyst: Intel's Q2 revenue growth was its fastest in
almost 15 years, and Q3 guidance ($15.8–16.8B) shattered the $15.1B
analyst estimate, driven by data center/AI demand. CEO Lip-Bu Tan made
bullish comments on AI inference demand for CPUs specifically (beyond
the GPU training story). Confirmed via Bloomberg and Benzinga. Clears
gap size, price, above-prior-day-high, and above-200-day-SMA checks for
both day and swing eligibility — blocked only by market cap (unknown,
defaults to fail with yfinance down) and RVOL (same issue). Intel is
obviously a real, liquid, multi-billion-dollar company (3.2M+ shares/day
avg volume) — this is a legitimate near-miss, not a name to chase blind,
but one where the "no" is about data availability, not the setup itself.
Worth noting: Mizuho stayed Neutral today with a $109 price target
(essentially today's price) — not every desk is chasing this, and the
stock is still down net for July despite the +170% YTD run and today's
pop, so there's real two-sided debate on valuation here (HSBC $200 vs.
"bubble risk" framing from others per market coverage).

## ☀️ Day Trading Watchlist

Rule: `day_eligible: true` requires gap >3% (up), price >$3, market cap
>$1B, premarket RVOL >1.5x, price above prior-day high, and prior close
above the 200-day SMA (WATCHLIST_CRITERIA.md). **No names cleared it
today** — table empty. INTC passes gap size, price, above-prior-high, and
above-SMA200 (4 of 6) — held back only by the mcap/RVOL data gap, not a
real disqualifier.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📈 Notable Swing Watchlist

Rule: `swing_eligible: true` requires gap ≥8% (up), price >$3, open above
prior high and 200-day SMA, market cap ≥$800M, confirmed catalyst. **No
names cleared it today** — table empty. INTC passes 5 of 6 checks here
(gap size, price, above prior high, above SMA200, real catalyst) — the
strongest near-miss either watchlist has seen this week, blocked only by
the missing market-cap field.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **Two days running, a real setup blocked by data availability, not
  substance**: yesterday it was NOK's earnings beat (4/6 day checks);
  today it's INTC's earnings blowout (5/6 swing checks, would clear the
  8% swing bar outright). Both times the mcap/RVOL fields were the only
  failures, both times because yfinance's connection was blocked this
  run. Worth a note for future maintenance: if this pattern continues,
  the packet builder's Alpaca-only fallback path might need a market-cap
  source that doesn't depend on the currently-blocked yfinance route.
- Broader tape: SPX 7,408.30, NDX 28,454.81, RUT 2,940.16 — essentially
  flat vs. Thursday's close. VIX 18.84 this morning, down from
  Thursday's 19.48, a modest cooling.
- Earnings season continues: Intel's blowout print is the session's
  headline story; watch for read-through into the broader semiconductor
  complex (including NVDA, held here).

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $65,068.40 vs daily SMA200
  $72,559.27 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-24_1133UTC.json`).
- **BTC** $65,016 (live), roughly flat vs today's session open
  ($65,062).
- **ETH** $1,881 (live), +0.2% vs today's open ($1,878).
- **SOL** $75.32 (live), -0.6% vs today's open ($75.78).
- **NVDA** $208.30 (live premarket) vs prior close $208.76, roughly
  flat — no company-specific headline found today, but INTC's AI-demand
  commentary is adjacent sector context worth knowing.
- **ORCL** $122.47 (live premarket) vs prior close $120.04, +2.0% —
  bouncing back after Wednesday's slide, no new company-specific news
  found today.

## 📊 Technical Signals for Today

- SPX 7,408.30 · NDX 28,454.81 · RUT 2,940.16 (Thursday's regular-
  session close per the Robinhood index feed — yfinance snapshot path
  blocked again this run — essentially unchanged from Wednesday).
- VIX 18.84 (live), down slightly from Thursday's 19.48 but still
  elevated relative to two weeks ago.
- 10Y yield: no live print again (yfinance ^TNX/^IRX blocked).
- INTC's 5-of-6 pass is the clearest gap-quality signal of the week —
  a real, sizeable, liquid name moving on real news, just not
  confirmable against the mcap/RVOL thresholds today.

## 💰 Economic Data, Rates & the Fed

Light data day by our tier-1 standard — 0 US high-impact events on
today's calendar (ForexFactory live fetch). No tier-1 print, no §3b
event blackout window today. FOMC meets Monday-Tuesday (7/28-29) with
the rate decision Wednesday 2:00 PM ET — five days out, not yet a
blackout concern but getting closer.

### Guardrail status (Zenith standing section)

- **Position count: still 7 open (AAPL, NVDA, ORCL, VOO, BTC, ETH, SOL)
  vs the strategy's 4-concurrent max.** No new agent entry is permitted
  today regardless of scan results — pinned since 7/18, now the
  seventh-plus straight trading day. This is the binding constraint
  today, doubly so given INTC's strength.
- Daily/weekly circuit breakers: not tripped. Equity $99,994.35 vs
  $100,000 baseline — flat.
- **Position health check** (informational, full management happens at
  9:30/1:00/4:00): all 7 positions healthy. ORCL, which closed
  Wednesday at -6.04% (nearest the -7% hard bail), has bounced back to
  roughly -3.7% this morning — no longer at immediate risk. AAPL leads
  at +4.0%.
- No names within 24h of earnings on today's gapper (`next_earnings`
  null — unknown, not a confirmed clear; Intel already reported
  Wednesday night, so its earnings event is behind it, not forward-
  looking).

## 📅 Coming Up

- No US high-impact events surfaced for tomorrow (7/25) in this run's
  calendar pull yet.
- FOMC meets Monday-Tuesday next week (7/28-29), rate decision
  Wednesday 2:00 PM ET — a §3b blackout window will apply as that
  approaches.
- Watch for INTC follow-through and any read-through into the broader
  chip complex heading into next week.

## 🚫 Skips & Traps

- Nothing to flag as a trap today — the one gapper (INTC) is a
  legitimate near-miss, not a trap. No other candidates surfaced.

---

## 🤖 Where rules and discretion landed

- **Agreement**: the screen and the read agree there's nothing
  actionable today, and for the second straight day there's real
  tension worth naming — INTC is a strong, verified setup the rules
  correctly withhold only because of a data gap, not a weak thesis.
- **Rules vs discretion**: INTC is today's case, even more clear-cut
  than yesterday's NOK — 5 of 6 swing checks pass, the gap clears 8%
  outright, and the catalyst is about as strong as premarket news gets
  (guidance blowing past estimates, best revenue growth in 15 years).
  Held back by data availability and the position cap, both legitimate,
  but this is exactly the kind of day where "no qualifying setups"
  undersells what's actually happening on the tape.
- **Sharp catches**: discretion's added value today is the valuation
  nuance — Mizuho's Neutral rating with a $109 PT (essentially
  today's price) alongside HSBC's $200 target shows real analyst
  disagreement on how much further this run has, useful context if
  INTC ever does clear the screen on a future day with an open slot.
- Nothing to trade here regardless of the near-miss — the position cap
  blocks it. Stand aside; monitor the 7 open positions at the scheduled
  checkpoints, with ORCL worth a second look given how close it came to
  -7% Wednesday even though it's bounced back this morning.
