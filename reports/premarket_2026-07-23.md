# 🧠 AI PREMARKET REPORT - Zenith

### Thursday, July 23, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

A rough 24 hours: Wednesday's session sold off hard on the Iran/oil
headlines (SPX -1.4%, NDX -2.4%), and this morning Tesla is down ~6.7%
premarket after its earnings print — real pain for Quy's real dust
position. On the scan side, one gapper (NOK) is a genuine, verified
earnings beat that nearly clears the day screen but gets blocked purely
by missing market-cap/RVOL data — a real near-miss worth naming, even
though it stays off the watchlist per the rules. None of it matters for
new entries regardless: the account is still at 7 concurrent positions,
sixth-plus straight day at the cap. Rules and discretion agree: stand
aside, watch the book, note TSLA's real-money hit.

## 📊 Pre-Market Gappers

**NOK (Nokia)** — gap +4.4% to $10.75 (prev close $10.30). Real,
verified beat: comparable operating profit +18% to €434M (vs €382M
est.), non-GAAP EPS €0.07 (vs €0.06 est.), revenue €4.82B (+8.3% YoY,
narrowly missed by €10M). AI/cloud sales reportedly doubled; CEO cited
strong demand with supply as the constraint, reaffirmed FY guidance.
Confirmed via Nokia's own IR release, Business Recorder, and Euronext.
This clears 4 of 6 day-eligibility checks (gap size, price, above
prior-day high, above 200-day SMA) — it's blocked only by market cap
and RVOL data being unavailable (yfinance blocked this run), not by any
real disqualifier. A large, liquid, real company (6M+ shares/day avg
volume) — this is the closest thing to a real setup this week, and it's
sitting out only because of a data gap and the position-count lock.

**ZCMD** — gap -22.8% to $3.32 (prev close $4.30). Fading a
circuit-breaker halt from a +351% spike yesterday — pump-and-dump
aftermath, down-gap regardless.

## ☀️ Day Trading Watchlist

Rule: `day_eligible: true` requires gap >3% (up), price >$3, market cap
>$1B, premarket RVOL >1.5x, price above prior-day high, and prior close
above the 200-day SMA (WATCHLIST_CRITERIA.md). **No names cleared it
today** — table empty. NOK passes 4 of 6 checks and fails only on
data-unavailable fields (mcap, RVOL); per the rule, an unflagged ticker
never gets promoted regardless of how likely it'd pass with live data —
noted in Skips & Traps instead.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📈 Notable Swing Watchlist

Rule: `swing_eligible: true` requires gap ≥8% (up), price >$3, open above
prior high and 200-day SMA, market cap ≥$800M, confirmed catalyst. **No
names cleared it today** — table empty. NOK's gap is only 4.4%, short of
the 8% swing threshold regardless of the mcap/RVOL data gap.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **Wednesday sold off**: the oil/Iran headline risk flagged in
  yesterday's premarket report played out through the session — SPX
  fell to 7,407.20 (-1.4%), NDX to 28,455.10 (-2.4%), RUT to 2,937.08.
  VIX has climbed to 19.48 this morning, the highest live read of the
  week, reflecting both the ongoing Iran situation and today's
  earnings-driven volatility.
- **Tesla missed and it's showing**: TSLA is down ~6.7% premarket
  ($349.03 vs $374.01 prior close) after last night's earnings — Quy's
  real (dust) Robinhood position takes a real hit here, even at a
  fractional-share size.
- Alphabet also reported last night alongside Tesla; no confirmed
  reaction data captured this run — worth checking GOOGL's move for
  broader Big Tech sentiment context once the open confirms it.
- Nokia's beat is the one bright, verified spot on the tape today,
  though it's not actionable here per the rules and the position cap.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $66,081.59 vs daily SMA200
  $72,691.42 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-23_1145UTC.json`).
- **BTC** $65,562 (live), -0.8% vs today's session open ($66,086) —
  pulling back slightly, tracking the broader risk-off tone from
  Wednesday's selloff.
- **ETH** $1,926 (live), -0.5% vs today's open ($1,935).
- **SOL** $77.80 (live), -0.2% vs today's open ($77.98).
- **NVDA** $209.99 (live premarket) vs prior close $212.06, -1.0% —
  no company-specific headline found today.
- **ORCL** $125.65 (live premarket) vs prior close $125.84, roughly
  flat — no new company-specific news found today.

## 📊 Technical Signals for Today

- SPX 7,407.20 · NDX 28,455.10 · RUT 2,937.08 (Wednesday's regular-
  session close per the Robinhood index feed — yfinance snapshot path
  blocked again this run — down meaningfully across the board on
  Wednesday's Iran/oil-driven selloff).
- VIX 19.48 (live), the week's highest read, up from Wednesday's 17.45
  — both the geopolitical overhang and today's earnings volatility
  (TSLA's miss especially) are feeding into it.
- 10Y yield: no live print again (yfinance ^TNX/^IRX blocked).
- NOK's clean 4-of-6 pass is the one gap-quality signal worth noting
  today, even though it doesn't clear the bar.

## 💰 Economic Data, Rates & the Fed

Light data day by our tier-1 standard — 0 US high-impact events on
today's calendar (ForexFactory live fetch). No tier-1 print, no §3b
event blackout window today.

### Guardrail status (Zenith standing section)

- **Position count: still 7 open (AAPL, NVDA, ORCL, VOO, BTC, ETH, SOL)
  vs the strategy's 4-concurrent max.** No new agent entry is permitted
  today regardless of scan results — pinned since 7/18, now the sixth
  straight trading day at the ceiling. This is the binding constraint
  today even more than usual, given NOK's near-miss.
- Daily/weekly circuit breakers: not tripped. Equity $100,006.80 vs
  $100,000 baseline — flat. **Note**: today's Alpaca account snapshot
  showed some unusual fields (multiplier reset to 1, `last_equity`/`sma`
  reading 0) — likely a paper-account day-rollover artifact, not a real
  issue; all position values and unrealized P&L checked out normal.
  Worth a light re-check at the next run.
- **Position health check** (informational, full management happens at
  9:30/1:00/4:00): all 7 positions healthy, none near their stops.
  AAPL leads at +4.3%; ORCL and NVDA both recovering toward flat.
- Elevated geopolitical risk remains a standing flag; today adds
  earnings-driven volatility (TSLA) on top of it.
- No names within 24h of earnings on today's gappers (`next_earnings`
  null across the board — unknown, not a confirmed clear). TSLA (held,
  dust position) already reported last night — past its earnings event
  now, not a forward-looking flag anymore.

## 📅 Coming Up

- No US high-impact events surfaced for tomorrow (7/24) in this run's
  calendar pull yet.
- Watch GOOGL's post-earnings reaction and broader Big Tech follow-
  through into Friday.
- FOMC decision July 29 — six days out.

## 🚫 Skips & Traps

- **NOK** — not a trap, a genuine near-miss: real verified earnings
  beat, passes most day-eligibility checks, blocked by a data gap
  (mcap/RVOL unavailable) and the position-count cap. Not promoted per
  the rules (never promote an unflagged ticker), but worth remembering
  if the data feed recovers and this pattern repeats.
- **ZCMD** — fading a +351% pump from yesterday's halt. Don't touch.

---

## 🤖 Where rules and discretion landed

- **Agreement**: the screen and the read agree there's nothing to
  action today, though for the first time this week there's real
  tension worth naming: NOK is a legitimately good setup that the rules
  correctly hold back only because of a data gap, not because the
  underlying thesis is weak.
- **Rules vs discretion**: NOK is the case to watch — if this were a day
  with an open position slot and live mcap/RVOL data, this is exactly
  the kind of name that should be on the day list. Today it's held back
  by data availability and the position cap, both legitimate reasons,
  but worth flagging so it doesn't read as "nothing interesting
  happened."
- **Sharp catches**: discretion's other job today is connecting TSLA's
  premarket earnings drop to Quy's real Robinhood position — small
  dollar amount, but a real loss worth being aware of, not just an
  abstract line in a table.
- Nothing to trade here regardless of the near-miss — the position cap
  blocks it. Stand aside; monitor the 7 open positions at the scheduled
  checkpoints, and watch for GOOGL's reaction and any TSLA follow-
  through today.
