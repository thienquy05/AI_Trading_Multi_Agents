# 🧠 AI PREMARKET REPORT - Zenith

### Thursday, July 9, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Paper trading research, not financial advice.
> **Shakedown note**: this first report ran at 12:44 ET, not premarket, and
> the environment blocked yfinance and the econ feed. Gaps and levels are
> full-session reads, market caps are missing, so no name could clear the
> eligibility flags today. The format below is the daily blueprint.

## Summary

Tape read unavailable from the packet (snapshot blocked); the gapper set
skews hard to small speculative names, which usually means the big indexes
are quiet. The catch we're watching: every one of today's twelve movers
failed the day screen, mostly on the missing market cap field, so this is a
watch-only report. Rules-vs-discretion verdict: both passes agree there is
nothing here you'd size up on, and agreeing on "no" is still agreement.

## 📊 Pre-Market Gappers

- **VRAX +262.4% ($8.71)**: "Why Did Virax Biolabs Stock Triple In One Session?" (Benzinga). Also halted on an upside circuit breaker.
- **JLHL +109.5% ($6.81)**: only a sector wrap mention ("12 Industrials Stocks Moving In Thursday's Pre-Market Session", Benzinga). Thin catalyst.
- **LASC +53.9% ($28.40)**: no clean catalyst found. `catalyst_found: false`.
- **TRAX +43.8% ($29.84)**: "HC Wainwright Reiterates Buy on First Tracks, Maintains $30 Price Target" (Benzinga).
- **PTLE +39.7% ($10.10)**: only wrap mentions. Thin.
- **AEHG +30.7% ($8.00)**: "Aehr Test Systems Gets New 2X Leveraged ETF Amid AI Semiconductor Rally" (Benzinga). Note: headline is about AEHR the semi name; AEHG matched on the Aehr token. Treat as unverified.
- **LASR +27.9% ($74.98)**: "nLIGHT Secures $44M Initial U.S. Defense Laser Weapons Award" (Benzinga). Real catalyst, defense theme.
- **SDOT +26.6% ($25.31)**: "Sadot Group Stock Rises 17% After-Hours: Here's Why" (Benzinga).
- **LITU +25.6% ($17.69)**, **MRAL +24.1% ($64.51)**, **SNDG +23.0% ($16.97)**, **LITX +22.4% ($28.16)**: no clean catalyst found on any of them.

## ☀️ Day Trading Watchlist

Rule the flag encodes: gap > 3%, price > $3, market cap > $1B, premarket
RVOL > 1.5, price above prior-day high, prev close above the 200-day SMA.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|
| none | `day_eligible` came back false on all 12 | market caps unavailable this run | no day trades from this screen today | 🔴 |

## 📈 Notable Swing Watchlist

Rule the flag encodes: gap >= 8%, price > $3, open above prior-day high and
the 200-day SMA, market cap >= $800M, real catalyst. Starter ideas only.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| none eligible | closest miss: LASR, real defense award, price $74.98 above its 200-day ($51.60) and prior high ($58.70) | failed only the unavailable market-cap check | re-run the screen with market cap live before calling it | 🟡 |

## 📉 Market Trends of the Day

- Snapshot feed was blocked this run, so no index/VIX read from the packet.
- The gapper tape is all low-float speculation (bio, micro-industrial), no
  large-cap theme leadership visible in the mover set.
- One real theme: defense lasers (LASR $44M award), worth a note for the
  swing screen when data is complete.

### Crypto regime + extra watch (Zenith standing section)

- Supplied by the 7 AM workflow's crypto scan, not this packet. Not run in
  this shakedown.

## 📊 Technical Signals for Today

- VRAX printed a 122x premarket RVOL, the kind of number that always means
  halts, spreads, and pain. Spectacle, not a setup.
- SDOT gapped up but trades below its 200-day ($54.26) and below its prior
  day high; MRAL same story ($90.55 200-day). Gaps INTO downtrends, not out
  of bases.
- LASR is the only mover holding above both its prior high and 200-day.

## 💰 Economic Data, Rates & the Fed

- Econ feed unavailable this run (network policy blocked the calendar
  source). Not claiming a clear day; the calendar is simply unknown from
  the packet. Workflow fallback: one targeted search before trading.

### Guardrail status (Zenith standing section)

- Supplied by the live workflow from account data. Not run in this
  shakedown.

## 📅 Coming Up

- Econ: unknown this run (same feed note as above).
- Earnings among the gappers: none returned (earnings dates ride the
  blocked yfinance path).

## 🚫 Skips & Traps

- **LASC, LITU, MRAL, SNDG, LITX**: `catalyst_found: false`. Up big on
  nothing is somebody's exit.
- **VRAX**: +262% with halts, unknown float, unknown cap. Lottery ticket.
- **JLHL, PTLE**: only sector-wrap mentions, no company-specific story.
- **AEHG**: the headline is about AEHR and a new 2X leveraged ETF, and
  AEHG looks like that ETF. A leveraged wrapper riding someone else's
  catalyst is not a Trend Join candidate; verify before ever touching.
- **SDOT, MRAL**: below the 200-day. The screen would kill them even with
  market caps present.

---

## 🤖 Where rules and discretion landed

- **Agreement**: nothing tradeable today. The screen said no twelve times;
  the read agrees on all twelve.
- **Rules vs discretion**: the read likes LASR (real award, clean trend)
  but the screen could not confirm market cap, so it stays unranked.
  Respect the screen; keep the idea.
- **Sharp catches**: the rules caught SDOT and MRAL trading below their
  200-day, easy to miss when staring at +25% gaps. The read caught the
  AEHG/AEHR headline cross-match that no numeric filter would ever see.
- Trade where they agree; where they disagree, stand down or size down;
  never average.
