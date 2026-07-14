# 🧠 AI PREMARKET REPORT - Zenith

### Tuesday, July 14, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

A loaded macro Tuesday: CPI lands at 8:30 AM, Fed Chair Warsh gives his
congressional debut at 10:00 AM, and the US starts enforcing a Strait of
Hormuz blockade (20% cargo fee) this afternoon. The catch we're watching:
today is a live blackout window, not a day to lean into new risk even if
something looked tempting. Our one real catalyst gapper (VEEE, a genuine
merger/spinoff) already faded from a 600%+ spike to +19% and is still
underwater vs its own trend — a trap dressed as an opportunity. Rules and
discretion agree: stand aside, let the macro prints clear first.

## 📊 Pre-Market Gappers

**VEEE (Twin Vee PowerCats)** — gap +19.4% to $29.70 (prev close $24.87).
Real catalyst, verified: announced a merger with USFM Corp plus a
privatization/spinoff of its core boat-building business (confirmed via
the company's own IR release and multiple outlets). Shares spiked over
600% intraday yesterday on the news and have given back most of that
already — today's premarket print is +19.4% off yesterday's close, still
below the prior-day high ($35.45) and well below its 200-day SMA
($41.56). Real news, but the stock is bleeding out the pop, not building
on it.

**AGEN (Agenus)** — gap -3.4% to $5.89 (prev close $6.10). "Catalyst" is
a multi-symbol roundup headline ("5 Stocks on Investors' Radars") with no
AGEN-specific driver. Down-gap, never in contention for either list.

## ☀️ Day Trading Watchlist

Rule: `day_eligible: true` requires gap >3% (up), price >$3, market cap
>$1B, premarket RVOL >1.5x, price above prior-day high, and prior close
above the 200-day SMA (WATCHLIST_CRITERIA.md). **No names cleared it
today** — table empty.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📈 Notable Swing Watchlist

Rule: `swing_eligible: true` requires gap ≥8% (up), price >$3, open above
prior high and 200-day SMA, market cap ≥$800M, confirmed catalyst. **No
names cleared it today** — table empty. VEEE has the catalyst and the gap
size, but fails on both trend checks (below prior-day high, below
200-day SMA) and market cap is unconfirmed (data feed blocked) — exactly
the profile WATCHLIST_CRITERIA.md's trend filters exist to catch: real
news bouncing a stock that's still structurally broken.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **Today's calendar is the whole story**: June CPI at 8:30 AM ET (core
  m/m forecast 0.2%, core y/y 2.8% vs 2.9% prior, still well above the
  Fed's 2% target), then Fed Chair Kevin Warsh's first-ever congressional
  testimony at 10:00 AM ET as part of the semiannual monetary policy
  report. Both are tier-1 events.
- **Strait of Hormuz escalation, separate from the econ calendar**: the
  US begins enforcing a blockade on Iranian shipping through the Strait
  of Hormuz this afternoon, with a 20% fee on all cargo crossing —
  reviving energy-shock-into-inflation concerns. Confirmed via
  Yahoo Finance and Bloomberg. Monday's session saw a broad selloff on
  the announcement (chips especially hard hit); today's futures are
  described as mixed/steadier heading into the prints.
- Big bank earnings (Citigroup, Goldman Sachs, Wells Fargo, JPMorgan,
  Bank of America) also land this week, adding to the event density.
- Gapper set: one real catalyst (VEEE) that's already faded hard, one
  non-catalyst (AGEN) — no tradeable sector signal in either.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $62,274.38 vs daily SMA200
  $73,744.48 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-14_1113UTC.json`).
- **BTC** $62,691 (live), +0.7% vs today's session open ($62,284) — a
  modest bounce after yesterday's slide, still well under the SMA200
  regime line.
- **ETH** $1,796 (live), +1.3% vs today's session open ($1,774).
- **SOL** $75.46 (live), +0.8% vs today's session open ($74.87).
- **NVDA** $205.10 (live premarket) vs prior close $203.53, +0.8% — a
  small bounce, no NVDA-specific headline found today.
- **ORCL** $128.80 (live premarket) vs prior close $131.54, -2.1% —
  continuing a sharp slide: ORCL beat Q4/FY26 earnings (record cloud
  revenue +47%, IaaS +93%) but fell ~6% Monday and is now near a
  14-month low on investor concern over margin compression as the
  business mix shifts to lower-margin IaaS, ~$16.5B in quarterly capex,
  rising debt to fund AI buildout, and a 21,000-job restructuring.
  Verified via FX Leaders and TradingKey. **Note: the Individual
  Robinhood account (556092849) shows no ORCL position and $0 equity
  value for the second consecutive check (first flagged yesterday's
  midday run)** — appears Quy sold the position manually; flagging again
  since it's now confirmed twice, not a one-off data glitch.

## 📊 Technical Signals for Today

- SPX 7,515.34 · NDX 29,264.10 · RUT 2,953.17 (Robinhood index feed —
  yfinance market-snapshot path blocked again this run; these reflect
  yesterday's regular-session levels, down across the board after
  Monday's Hormuz-driven selloff).
- VIX 17.49, up from 16.30 Monday and 15.86 Friday — a steady climb in
  hedging demand across three sessions, still not panic-level but the
  trend is worth watching into today's prints.
- 10Y yield: no live print again (yfinance ^TNX/^IRX blocked).
- VEEE's fade from a 600%+ spike to +19% by this morning is the one
  gap-quality signal today: even real news isn't holding in this tape.

## 💰 Economic Data, Rates & the Fed

**Heavy data day** — 5 US high-impact events today (ForexFactory live
fetch, confirmed via web search):
- 8:30 AM ET: Core CPI m/m (forecast 0.2%, previous 0.2%)
- 8:30 AM ET: Core CPI y/y (forecast 2.8%, previous 2.9%)
- 8:30 AM ET: CPI m/m (forecast -0.1%, previous 0.5%)
- 8:30 AM ET: CPI y/y (forecast 3.8%, previous 4.2%)
- 10:00 AM ET: Fed Chairman Warsh testifies (his congressional debut)

All five are tier-1 and put today squarely inside a §3b event blackout
window around 8:30–10:00 AM ET at minimum; treat the whole morning as
elevated-volatility given Warsh's testimony risk on top of the print.

### Guardrail status (Zenith standing section)

- Daily/weekly circuit breakers: not tripped. Equity $100,004.41 vs
  $100,000 baseline — flat.
- Weekly entry cap: 0 of 5 used this week (no trades since the reset).
- **§3b blackout window IN EFFECT today**: CPI (8:30 AM) + Fed Chair
  Warsh's testimony (10:00 AM) — no new entries until the dust settles
  and price action confirms, per strategy rules.
- No names within 24h of earnings on today's two gappers (`next_earnings`
  null for both — unknown, not a confirmed clear).
- Elevated geopolitical/energy risk (Hormuz blockade enforcement starts
  this afternoon) is an additional risk-awareness flag for the existing
  AAPL position and any potential new entries later today, on top of the
  scheduled blackout.
- No sector cap conflicts, no open crypto positions, no consecutive
  same-day stop-outs.

## 📅 Coming Up

- No high-impact events surfaced for tomorrow (7/15) in the packet's
  calendar pull yet — will confirm at the next run.
- No specific earnings dates surfaced for VEEE/AGEN (`next_earnings`
  null on both — data gap, not a confirmed "none").
- Big bank earnings (C, GS, WFC, JPM, BAC) continue rolling out this
  week — watch for sector volatility even without a direct setup today.

## 🚫 Skips & Traps

- **VEEE** — real catalyst (merger + spinoff, verified), but the move is
  already 97% faded from its intraday spike and the stock remains below
  both its prior-day high and 200-day SMA. This is the textbook "news is
  real, trend isn't" trap — don't chase the bounce.
- **AGEN** — no company-specific catalyst, just a roundup mention. Skip.

---

## 🤖 Where rules and discretion landed

- **Agreement**: full agreement — nothing here is tradeable, and today
  isn't a day to force one even if something had looked close. The rules
  reject both gappers on trend/mcap/RVOL checks; discretion independently
  flags VEEE's catalyst as real but the tape as already having priced (and
  un-priced) it.
- **Rules vs discretion**: no disagreement on tickers today.
- **Sharp catches**: discretion caught that VEEE is the more interesting
  trap of the two — a legitimate catalyst can still be a bad trade if
  you're buying the exhausted tail of a spike. The rules caught it too,
  mechanically, via the trend filters — good example of the screen and
  the read reinforcing each other from different angles.
- Nothing agrees to trade, so nothing gets traded. Today's real job is
  staying out of the way of CPI, Warsh's testimony, and the Hormuz
  blockade enforcement — reassess after 10:00 AM ET once the prints and
  the testimony are behind us.
