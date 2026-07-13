# 🧠 AI PREMARKET REPORT - Zenith

### Monday, July 13, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

Risk-off Monday: a fresh round of US-Iran strikes over the weekend broke
the ceasefire again and is dragging chip stocks lower premarket. The catch
we're watching: this is a geopolitical shock, not a stock-specific setup,
and our one gapper (SUNE) is gapping down on a generic roundup headline,
not a real catalyst. Rules and discretion agree: nothing to trade here,
stand aside. Tomorrow brings CPI + a Fed testimony, worth flagging now.

## 📊 Pre-Market Gappers

**SUNE** — gap -7.3% to $3.56 (prev close $3.84). "Catalyst": "12
Industrials Stocks Moving In Friday's After-Market Session" (Benzinga,
2026-07-10 21:05 ET) — a 12-symbol roundup article, not a company-specific
driver. `catalyst_found: true` on the packet's keyword match, but there's
no real explanation for the move. Gap is also down, not up, so it never
had a shot at the day/swing screens (both require a gap UP).

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
names cleared it today** — table empty. SUNE gapped down, not up, so it
was never in contention regardless of catalyst quality.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **Dominant driver: US-Iran escalation.** CENTCOM launched a fifth round
  of strikes against Iran Sunday evening (140 targets, first use of
  one-way attack sea drones), aimed at protecting Strait of Hormuz
  shipping; Iran retaliated against Gulf US bases. The June ceasefire is
  effectively unraveling. Confirmed via CNN, Al Jazeera, and CBS in
  addition to the CENTCOM release.
- **Chips leading the selloff**: SK Hynix -8%, Micron -5.2%, Sandisk
  -6.3% premarket per CNBC, tracking international chip peers lower.
  NVDA following the sector down (~-1.2% premarket, see extra-watch).
- Futures reads are noisy this morning: some sources show S&P futures
  -0.3% / Nasdaq-100 -0.9% (geopolitics-driven), others show E-mini S&P
  +0.4% (on cooling global inflation prints). Treat the tape as genuinely
  unsettled rather than picking a side.
- Week ahead: big bank earnings start Tuesday (Citigroup, Goldman Sachs,
  Wells Fargo, JPMorgan, Bank of America) — not actionable today but
  sets up sector volatility this week.
- Gapper set is a single illiquid small-cap gapping down on a non-catalyst
  — no tradeable sector/theme signal in it.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $63,745.49 vs daily SMA200
  $73,868.96 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-13_1112UTC.json`).
- **BTC** $63,049 (live), -1.1% vs today's session open ($63,740) —
  slipped in an Asian-session leverage flush per CoinDesk, tracking the
  weekend's risk-off tone.
- **ETH** $1,783 (live), -1.2% vs today's session open ($1,804).
- **SOL** $76.50 (live), -0.4% vs today's session open ($76.83), still
  struggling to reclaim $80.
- **NVDA** $208.44 (live premarket) vs prior close $210.96, -1.2% —
  dragged down with the broader chip selloff (SK Hynix/Micron/Sandisk all
  down sharply), no NVDA-specific headline found.
- **ORCL** $140.45 (live) vs prior close $140.64, roughly flat — quiet,
  no specific news today.

## 📊 Technical Signals for Today

- SPX 7,575.39 · NDX 29,825.11 · RUT 2,977.81 (Robinhood index feed, as
  of Friday 7/10's close — yfinance market-snapshot path was blocked
  again this run, so these are the latest settled levels, not live
  futures).
- VIX 16.30 — ticked up from Friday's 15.86, consistent with the
  weekend's Iran-strike risk-off tone, still well off panic levels.
- 10Y yield: no live print today either (yfinance ^TNX/^IRX blocked) —
  treat rates as an unknown this morning.
- SUNE is the only gapper and it's gapping down on a non-catalyst — no
  collective read on gap quality today.

## 💰 Economic Data, Rates & the Fed

Light data day — 0 US high-impact events on today's calendar
(ForexFactory live fetch). No tier-1 print today, no §3b event blackout
window in effect today.

### Guardrail status (Zenith standing section)

- Daily/weekly circuit breakers: not tripped. Equity $100,005.71 vs
  $100,000 baseline — flat.
- Weekly entry cap: 0 of 5 used this week (fresh week starting 7/13;
  last week's 1 AAPL test entry doesn't carry over).
- No names within 24h of earnings on today's one gapper (`next_earnings`
  null for SUNE — unknown, not a confirmed clear).
- No sector cap conflicts, no open crypto positions to average down on,
  no consecutive same-day stop-outs.
- No tier-1 blackout window today. **Heads up for tomorrow** (see Coming
  Up) — CPI prints + a Fed testimony land inside the 3b framework.
- Elevated geopolitical risk (US-Iran strikes, Strait of Hormuz) is a
  risk-awareness flag, not a scheduled-event blackout — noted for
  position sizing and gap-risk awareness on the existing AAPL position,
  not an automatic stand-down.

## 📅 Coming Up

- **Tuesday 7/14, 8:30 AM ET**: Core CPI m/m (forecast 0.2%, prev 0.2%),
  Core CPI y/y (forecast 2.8%, prev 2.9%), headline CPI m/m (forecast
  -0.1%, prev 0.5%), headline CPI y/y (forecast 3.8%, prev 4.2%) — tier-1
  prints, trigger the §3b event blackout window around that time.
- **Tuesday 7/14, 10:00 AM ET**: Fed Chairman Warsh testifies — also
  tier-1, treat as a blackout window.
- No specific earnings date surfaced for SUNE (`next_earnings` null —
  data gap, not a confirmed "none").

## 🚫 Skips & Traps

- **SUNE** — the only "catalyst" is a 12-stock roundup headline with no
  SUNE-specific explanation, and the gap is down, not up. Nothing here
  supports a long thesis; skip. Don't chase the bounce on a name with no
  real story either.

---

## 🤖 Where rules and discretion landed

- **Agreement**: full agreement — nothing here is tradeable. The rules
  reject SUNE mechanically (gap direction alone kills it for both lists);
  discretion independently rejects it on catalyst quality (a roundup
  headline isn't a catalyst).
- **Rules vs discretion**: no disagreement — nothing borderline today.
- **Sharp catches**: discretion caught that today's real story isn't in
  the gappers at all, it's macro — the Iran strikes and the chip-sector
  selloff are doing more to the tape than anything on the scan. The rules
  correctly stayed silent on a macro event they're not built to screen for
  — that's on the analyst pass, and it's flagged above.
- Nothing agrees to trade, so nothing gets traded. Stand aside on
  equities and crypto both; watch the AAPL position for weekend-gap-risk
  follow-through and keep an eye on the chip complex intraday in case
  the selloff creates a real setup later.
