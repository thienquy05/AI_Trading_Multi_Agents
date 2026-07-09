# REPORT_TEMPLATE.md - premarket report skeleton

Blueprint for the daily `reports/premarket_<date>.md`. The analyst prompt
(PROMPT-PREMARKET.md) fills this in from the day's packet. Section order is
fixed. Voice: casual Humbled Trader, witty but honest, zero em dashes.

Single-brain edition: Claude runs two passes over the same packet, a RULES
pass (what the deterministic flags say) and a DISCRETION pass (what a
trader's read says). Where the internet template had a second AI, we have
the screen vs the read. Same tension, cheaper seat.

Conviction key, used everywhere:
- 🟢 green = rules pass + clean catalyst + price in position. Trade the plan.
- 🟡 yellow = something is off (weak RVOL, mixed macro, stretched from levels). Size down or wait for confirmation.
- 🔴 red = rules or the read say no. Watch, do not touch.

---

# 🧠 AI PREMARKET REPORT - Zenith

### {Weekday, Month D, YYYY} · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

The tape in one line. The catch we're watching in one line (the thing most
likely to wreck the plan today). One-line rules-vs-discretion verdict: do
the screen and the read agree, and on what.

## 📊 Pre-Market Gappers

Every gapper that survived the scan filter, one block each: ticker, gap %,
price, and the FULL catalyst headline exactly as the packet has it (source
in parens). `catalyst_found: false` gets said out loud.

## ☀️ Day Trading Watchlist

Only `day_eligible: true` names. State the rule the flag encodes once above
the table.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|

Levels = price vs VWAP / PMH / prior HOD / prior day high. Plan = the 2b
execution: trigger over PMH + prior HOD in the 10:00 to 3:30 window, stop at
signal bar low (1R), 3R bracket, flat 3:55.

## 📈 Notable Swing Watchlist

Only `swing_eligible: true` names. Starter ideas only, management is still
being built, so no fake stops or targets.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|

Trend context = open vs 200-day SMA and prior day high. Idea = catalyst
type + theme + what would make it a real entry.

## 📉 Market Trends of the Day

Bullets: index tone from the snapshot, sector/theme rotation visible in the
gapper set, anything overnight that changes risk appetite.

### Crypto regime + extra watch (Zenith standing section)

- Crypto sleeve regime state (BTC vs daily SMA200) + BTC/ETH/SOL moves.
- One-liners on the extra-watch names Quy holds for real: BTC, ETH, SOL, NVDA, ORCL.

## 📊 Technical Signals for Today

Bullets: key index levels, VIX read, 10Y/3M from the snapshot, what the
gapper levels say collectively (are gaps holding above PMH or fading).

## 💰 Economic Data, Rates & the Fed

From `econ_calendar.today`: each event with time ET, forecast vs previous.
Rates read from the snapshot (^TNX, ^IRX). Empty list = "light data day,
no tier-1 prints". `econ_calendar.error` set = say the feed was unavailable
rather than pretending the calendar is clear.

### Guardrail status (Zenith standing section)

3b check: circuit breakers, event blackout windows in effect today (tier-1
prints from the calendar), names inside 24h of earnings, entries used this
week.

## 📅 Coming Up

From `econ_calendar.tomorrow` (time ET) plus notable earnings among the
gappers (next earnings dates from the packet).

## 🚫 Skips & Traps

Names that failed the screens or got flagged by either pass, each with the
why: no catalyst, up on bad news (dilution, offering, probe, miss), gap too
thin, below the 200-day, RVOL dead. Traps get named so we do not "discover"
them at 10:15.

---

## 🤖 Where rules and discretion landed

- **Agreement**: names both passes like. Trade the overlap.
- **Rules vs discretion**: names the read liked but the screen rejected, and
  which rule killed them (respect the screen, note the idea).
- **Sharp catches**: the one thing the rules caught that a human skims past,
  and the one thing the read caught that no filter can see.
- Closing line, always: trade where they agree; where they disagree, stand
  down or size down; never average.
