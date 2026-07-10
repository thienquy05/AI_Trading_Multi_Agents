# 🧠 AI PREMARKET REPORT - Zenith

### Friday, July 10, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

Quiet premarket, both eligible watchlists are empty today. The catch we're
watching: yields are still sticky (10Y near 4.6%) capping any rally attempt,
and neither gapper on the tape has a mcap/RVOL profile that clears the
screen. Rules and discretion agree: stand aside on equities, sleeve stays
flat on crypto too.

## 📊 Pre-Market Gappers

**JLHL (Julong Holding)** — gap +75.8% to $22.35 (prev close $12.71).
Catalyst: "Why Is Julong Holding Stock Trending Overnight?" (Benzinga,
2026-07-10 03:21 ET). `catalyst_found: true` but the headline itself is a
question, not an answer — no confirmed driver in the packet. Thin float
(20d avg vol ~11.6k), market cap unavailable (data feed blocked).

**VRAX (Virax Biolabs)** — gap -12.4% to $5.60 (prev close $6.39). Catalyst:
"Virax Biolabs Shares Resume Trade" (Benzinga, 2026-07-09 17:48 ET), after
yesterday's circuit-breaker halt (+150.6%) on news of an "Immediate
Exercise Of 548K Shares At $6/Share For ~$3.3M" — a dilutive raise.
`catalyst_found: true`, fading hard the morning after.

## ☀️ Day Trading Watchlist

Rule: `day_eligible: true` requires gap >3%, price >$3, market cap >$1B,
premarket RVOL >1.5x, price above prior-day high, and prior close above the
200-day SMA (WATCHLIST_CRITERIA.md). **No names cleared it today** — table
empty.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📈 Notable Swing Watchlist

Rule: `swing_eligible: true` requires gap ≥8%, price >$3, open above prior
high and 200-day SMA, market cap ≥$800M, confirmed catalyst. **No names
cleared it today** — table empty. Both gappers failed on market cap (data
unavailable, defaults to fail) and RVOL; JLHL and VRAX would likely have
been demoted to Skips & Traps on quality grounds anyway (see below).

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- Index tone is mixed-to-flat: some premarket reads have S&P futures
  fractionally green, others (Benzinga/Polymarket) show futures down
  ~0.2% with only a 20% implied odds of a green open, reflecting a pause
  after this week's rally.
- Sticky yields are the drag: 10Y holding near 4.6% keeps one-more-hike
  chatter alive; May consumer credit came in soft (-$0.2B), a mild
  pullback-in-borrowing signal.
- SK Hynix's US listing debut and Delta's earnings beat (record revenue,
  profit beat despite fuel cost pressure) are the session's headline
  events — chip/semi sentiment and airline/travel read-through worth
  watching even though nothing here clears our screens.
- Gapper set is two illiquid small caps with no clean, confirmed
  catalyst between them — no sector/theme signal to read into it.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $63,162.31 vs daily SMA200
  $74,228.84 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-10_1112UTC.json`).
- **BTC** $64,442 (live), +2.0% vs prior close — bouncing back toward
  $64k after erasing Iran-headline losses, per CoinDesk (chip rally +
  yen strength cited as drivers, not crypto-specific news).
- **ETH** $1,799 (live), +2.6% on the day per market coverage.
- **SOL** $79.53 (live), +2.6% on the day, still carrying a ~2.1% weekly
  loss — the one major that hasn't clawed back to green this week.
- **NVDA** $202.76 (live), essentially flat vs prior close ($202.78) —
  no material headline found today.
- **ORCL** $144.26 last / $145.84 late non-reg (live) vs prior close
  $144.22 — roughly flat, quiet on news today.

## 📊 Technical Signals for Today

- SPX 7,543.64 · NDX 29,727.10 · RUT 2,992.54 (Robinhood index feed,
  yfinance market-snapshot path was blocked this run — see gap note
  below).
- VIX 15.86 — calm, no fear premium priced in despite the yield/rate
  overhang.
- 10Y yield ~4.6% per market coverage (yfinance ^TNX/^IRX pull failed,
  no live print in the packet — treat as directional only).
- Both gappers are small/illiquid with unknown market cap and RVOL
  (data feed blocked) — no collective read on gap quality possible
  beyond the headline-level catalyst check above.

## 💰 Economic Data, Rates & the Fed

Light data day — 0 US high-impact events on today's calendar
(ForexFactory live fetch, confirmed by a second web search: no
CPI/jobs/FOMC scheduled for 7/10, FOMC minutes already dropped
Wednesday 7/8). No tier-1 print, no §3b event blackout window today.

### Guardrail status (Zenith standing section)

- Daily/weekly circuit breakers: not tripped. Equity $100,004.46 vs
  $100,000 baseline — flat.
- Weekly entry cap: 1 of 5 used this week (AAPL, still the week of
  7/6-7/10).
- No names within 24h of earnings on today's gappers (`next_earnings`
  null for both — unknown, not a confirmed clear).
- No sector cap conflicts, no open crypto positions to average down on,
  no consecutive same-day stop-outs.
- No tier-1 blackout window in effect today (calendar is empty).

## 📅 Coming Up

- No US high-impact events flagged for tomorrow (7/11) in the packet's
  calendar pull either — Saturday, markets closed anyway.
- No specific earnings dates surfaced for JLHL/VRAX (`next_earnings`
  null on both in the packet — data feed gap, not a confirmed "none").

## 🚫 Skips & Traps

- **JLHL** — catalyst headline is a question, not an answer ("Why Is
  Julong Holding Stock Trending Overnight?"); no confirmed driver, thin
  20d avg volume (~11.6k shares), market cap unknown. Classic pump
  pattern on an illiquid name — skip.
- **VRAX** — up +150% yesterday on a halt, now fading -12.4% the morning
  after a dilutive share-exercise agreement ($3.3M raise at $6/share).
  Textbook post-spike dilution fade — skip, do not fade-buy the dip
  either without a defined level.

---

## 🤖 Where rules and discretion landed

- **Agreement**: both passes agree — nothing here is tradeable. The
  screen kills both gappers on market cap/RVOL data gaps, and the read
  independently kills them on catalyst quality (vague headline / active
  dilution).
- **Rules vs discretion**: no disagreement today — there was nothing
  borderline to argue about.
- **Sharp catches**: the rules caught the RVOL/mcap data gap
  mechanically (defaults both to fail when data's missing, which is the
  right conservative bias); the read caught that VRAX's "catalyst" is
  actually a dilution event dressed as a resume-trade headline, the kind
  of thing that looks like news but is actually the reason to stay away.
- Nothing agrees to trade, so nothing gets traded. Stand aside on
  equities and crypto both; revisit at 9:30 with fresh premarket levels
  in case something new gaps in.
