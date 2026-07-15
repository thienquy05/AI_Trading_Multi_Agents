# 🧠 AI PREMARKET REPORT - Zenith

### Wednesday, July 15, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

Round two of the CPI/Warsh story: PPI lands at 8:30 AM and Fed Chair
Warsh gives his second day of testimony (Senate Banking this time, after
House Financial Services yesterday) at 10:00 AM. Yesterday's cool CPI
rally came with hawkish Warsh commentary ("not mission accomplished") —
today could easily be a two-sided session. The catch we're watching: 8
gappers today, seven gapping down and two of those (SOXS, TZA) are almost
certainly leveraged-ETF reverse-split artifacts, not real moves. Rules
and discretion agree: nothing tradeable, and today is a blackout window
again anyway.

## 📊 Pre-Market Gappers

**SOXS (Direxion Daily Semiconductor Bear 3x)** — "gap" -90.1% to $4.28
(prev close $43.00). This is a leveraged inverse ETF with 2.4M
20-day-avg volume; a clean 90% single-session drop on a liquid product
like this is a reverse-split data artifact, not a real move. The
attached "catalyst" (a Direxion 2x fund filing headline) is unrelated
noise from the keyword matcher.

**TZA (Direxion Daily Small Cap Bear 3x)** — same story: -90.0% to $4.04
(prev close $40.35), 2.5M 20-day-avg volume, no catalyst attached. Also
a reverse-split artifact.

**CRMT (America's Car-Mart)** — gap -11.7% to $3.77 (prev close $4.27).
Real catalyst: Q4 2026 earnings call transcript — a post-earnings
selloff. Down-gap, never in contention.

**BMGL (Basel Medical Group)** — gap +8.8% to $8.32 (prev close $7.64).
Real catalyst ("Regains Nasdaq Compliance") and clears the 8% swing gap
threshold, but 20-day avg volume is just 162 shares/day — essentially
untradeable liquidity on a nano-cap, and price is still below its
200-day SMA ($10.26).

**VEEE (Twin Vee PowerCats)** — gap -7.7% to $38.06 (prev close $41.22),
continuing to give back Monday's merger-news spike (see Monday and
Tuesday's reports). The attached "catalyst" headline is actually about
Aehr Test Systems, an unrelated mismatch from a 20-stock roundup
article. Down-gap regardless.

**NXTC (NextCure/Avere)** — gap -5.5% to $6.17 (prev close $6.53). Real
catalyst (corporate rebrand, oral psoriasis therapy focus), but down-gap.

**BMNU** — gap -4.5% to $9.14 (prev close $9.57). No catalyst, down-gap.

**LCID (Lucid)** — gap -3.0% to $4.48 (prev close $4.62). Real catalyst:
reports the EV maker is weighing strategic options (negative framing).
Down-gap, never in contention, but a name Quy might see in headlines
today — worth knowing the driver is real, not noise.

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
names cleared it today** — table empty. BMGL is the closest (real
catalyst, gap size, above prior high) but fails on 200-day SMA and market
cap, and its 162-share daily volume makes it a non-starter regardless of
what the flags said.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **Today's calendar, round two**: June PPI at 8:30 AM ET (core forecast
  0.3% vs 0.4% prior, headline forecast 0.0% vs 1.1% prior — a much
  cooler read expected after May's spike), then Fed Chair Warsh's second
  day of testimony, this time before the Senate Banking Committee (10:00
  AM ET), following yesterday's House Financial Services appearance.
- **Cool CPI, hawkish Warsh**: yesterday's benign CPI (3.5% YoY vs ~3.8%
  expected) drove a relief rally (S&P +0.37%, Nasdaq +1%, chip-stock
  bounce), but Warsh told Congress the inflation improvement "isn't
  mission accomplished" — a hawkish tell that could cap today's rally if
  he repeats it, per multiple outlets characterizing this as a
  potential "two-stage" session again.
- Futures this morning are mixed: Dow/S&P futures +0.2%, Nasdaq-100
  futures +0.5% ahead of the print.
- IBM's -25% profit-warning selloff from Monday is still working through
  sentiment in software/infrastructure names; no update found today.
- Gapper set is mostly down-gaps plus two leveraged-ETF data artifacts —
  no tradeable sector signal in it.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $64,993.47 vs daily SMA200
  $73,633.01 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-15_1119UTC.json`).
- **BTC** $64,717 (live), essentially flat vs today's session open
  ($65,014, -0.5%) after touching above $65,000 overnight; still firm
  after yesterday's CPI-relief bounce (+3.6% on a 24h basis per market
  coverage).
- **ETH** $1,880.6 (live), -0.6% vs today's open ($1,891.35), also firm
  after a strong 24h move (+4.9%) — ETF inflows (~$58M) and Morgan
  Stanley's Ethereum/Solana ETF filing naming Coinbase as
  custodian/staking provider cited as tailwinds.
- **SOL** $77.51 (live), -0.4% vs today's open ($77.83).
- **NVDA** $211.68 (live premarket) vs prior close $211.80, roughly flat
  — no specific headline found today.
- **ORCL** $129.11 (live premarket) vs prior close $127.94, +0.9% — a
  small bounce after Monday/Tuesday's slide; no new company-specific
  news found today.

## 📊 Technical Signals for Today

- SPX 7,543.59 · NDX 29,586.29 · RUT 2,964.76 (Robinhood index feed,
  yesterday's regular-session close — yfinance snapshot path blocked
  again this run — levels are up across the board on the CPI relief
  rally).
- VIX 16.38, down from Tuesday's 17.49 — cooling off as the CPI scare
  passed, though Warsh's hawkish tone is a reason it hasn't dropped
  further.
- 10Y yield: no live print again (yfinance ^TNX/^IRX blocked).
- The gapper set's quality is poor today: two artifacts, five real-news
  down-gaps, one illiquid nano-cap up-gap. No collective read to draw.

## 💰 Economic Data, Rates & the Fed

**Another live data day** — 3 US high-impact events today (ForexFactory
live fetch, confirmed via web search):
- 8:30 AM ET: Core PPI m/m (forecast 0.3%, previous 0.4%)
- 8:30 AM ET: PPI m/m (forecast 0.0%, previous 1.1%)
- 10:00 AM ET: Fed Chairman Warsh testifies (Senate Banking Committee,
  day 2)

All tier-1, putting today inside a §3b event blackout window around
8:30–10:00 AM ET again, same as yesterday.

### Guardrail status (Zenith standing section)

- Daily/weekly circuit breakers: not tripped. Equity $100,006.32 vs
  $100,000 baseline — flat.
- Weekly entry cap: 0 of 5 used this week.
- **§3b blackout window IN EFFECT today**: PPI (8:30 AM) + Fed Chair
  Warsh testimony (10:00 AM) — no new entries until this clears and
  price action confirms.
- No names within 24h of earnings on today's gappers (`next_earnings`
  null across the board — unknown, not a confirmed clear).
- No sector cap conflicts, no open crypto positions, no consecutive
  same-day stop-outs.

## 📅 Coming Up

- No high-impact US events surfaced for tomorrow (7/16) in this run's
  calendar pull yet — will confirm at the next run.
- No specific earnings dates surfaced for today's gappers (`next_earnings`
  null across the board — data gap, not a confirmed "none").

## 🚫 Skips & Traps

- **SOXS / TZA** — both -90% "gaps" are leveraged-ETF reverse-split data
  artifacts, not real market moves. Not tradeable, not even a real
  signal — flagged so nobody double-takes on these later today.
- **BMGL** — real catalyst and a real gap-up, but 162 shares/day average
  volume makes any position effectively unfillable at size. Skip
  regardless of what the rules said.
- **CRMT, VEEE, NXTC, LCID, BMNU** — all down-gaps (some on real news,
  some not), mechanically excluded from a long-only gap-up strategy.

---

## 🤖 Where rules and discretion landed

- **Agreement**: full agreement — nothing here is tradeable. The rules
  reject everything on gap direction, trend, mcap, or RVOL; discretion
  independently flags the two ETF "gaps" as data artifacts the rules
  can't distinguish from real moves (a case where the read adds value
  the screen can't).
- **Rules vs discretion**: no ticker-level disagreement today.
- **Sharp catches**: discretion caught that SOXS/TZA aren't real gaps at
  all — the rules correctly rejected them anyway (on trend/mcap
  criteria) but for the wrong reason, which matters if this pattern ever
  produces a false positive on a less obviously-artifactual leveraged
  product. Worth a future rule tweak: flag any gap where prev_close is
  wildly inconsistent with sma200 (here $43 vs $417.68) as a likely
  split artifact before it even reaches the enrichment step.
- Nothing agrees to trade, so nothing gets traded. Same playbook as
  yesterday: stay out of the way of PPI and Warsh's testimony, reassess
  after 10:00 AM ET.
