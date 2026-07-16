# WATCHLIST_CRITERIA.md - the rules that pick the watchlists

This file is the source of truth for what makes the premarket watchlists.
`scripts/scan_premarket.py` encodes these rules in code and stamps every
gapper with `day_eligible` and `swing_eligible` flags. The AI never decides
membership. Rules pick the list, judgment ranks the quality. That split is
the whole point: no hand-waving a ticker onto the list because the story
sounds sexy at 7 AM.

No em dashes in this file, and none in the scanner either. House style.

## 1. DAY TRADING WATCHLIST - "Trend Join Long" (TJL)

The idea: don't predict, join. A large-cap that gaps up, holds the gap, and
breaks yesterday's high with real relative volume is already telling you
which way the crowd is leaning. We get in when the trend proves itself
intraday, not before.

### Premarket selection (ALL required -> `day_eligible: true`)

| # | Rule | Why |
|---|---|---|
| 1 | Gap % vs prev close > 3% | Needs a real move, not noise |
| 2 | Price > $3 | No sub-penny lottery tickets |
| 3 | Market cap > $1B | Liquidity, tighter spreads, less manipulation |
| 4 | Premarket RVOL > 1.5 | Stock has to be "in play", volume is the tell |
| 5 | Price breaking above yesterday's high | The breakout is already happening |
| 6 | Prev close > 200-day SMA | Zenith house rule, only join uptrends. Kept from the validated TJL spec (TRADING-STRATEGY.md 2b) |

RVOL note: with Alpaca premarket bars we compute TRUE premarket RVOL
(today's premarket volume vs the 20-day average premarket volume at the
same clock time).

Market cap note (2026-07-16): yfinance, the only market-cap source this
scanner had, was removed — it was permanently rate-limited (HTTP 429)
on this sandbox's shared egress IP, not a real fallback. Rule 3 (day)
and rule 5 (swing) can never pass on their own until a replacement
source is wired in; `scan_premarket.py`'s `gaps_to_fill` says so on
every run. Until then, treat a gapper that clears every other gate as
"would qualify but for market cap" on discretion, and say so explicitly
in the report rather than silently waving it onto the list.

### Intraday plan (execution stays per TRADING-STRATEGY.md 2b, the validated ruleset)

- Window: entries 10:00 AM to 3:30 PM ET only. Skip the open chop.
- Trigger: price > premarket high AND price > prior high-of-day.
- Stop: signal bar low = 1R.
- Target: +3R via bracket order. Flat by 3:55 PM ET. One trade per ticker per day.
- Size: 1% of equity risk, all the 3b guardrails apply.

### Pending validation: the "scale-out" exit variant

An alternative exit style is on the bench, NOT live:
stop 1% below premarket high or LOD (whichever is lower) = 1R, scale 1/3 at
+1R, 1/3 at +2R, trail the last 1/3 on the 21-EMA, flat by 3:51 PM.

Honesty box on the stats:
- The scale-out variant arrived with claimed numbers of 54.6% win rate,
  profit factor 1.59, 280 trades. Those are EXTERNAL claims from outside
  this repo and we do not trade on them.
- We backtested it ourselves on 2026-07-09 (`backtest_tjl.py --exits pmh`,
  2026-01-10 to 2026-07-09, AMD/NVDA/MU, 5-min bars, same 84 signals for
  both exit styles):
  - Bracket baseline: 33.3% win rate, +11.04R total, PF 1.20, avg win 2.37R
  - Scale-out variant: 56.0% win rate, +4.35R total, PF 1.42, avg win 0.31R
- Read: the variant's win rate matches the internet claim almost exactly,
  and it FEELS nicer to trade. It also made less than half the R. Win rate
  is not profit. At 1% risk per trade, total R is the money, so brackets
  stay live. Re-test on dynamic watchlist names before ever revisiting.

## 2. SWING WATCHLIST - gap-up plus a real catalyst

The idea: a big gap over resistance, above the 200-day, with an actual
reason behind it, tends to keep working for days. No catalyst, no trade.
A stock up 9% on nothing is somebody's exit, not your entry.

### Premarket selection (ALL required -> `swing_eligible: true`)

| # | Rule | Why |
|---|---|---|
| 1 | Gap % >= 8% | Swing moves need a violent repricing |
| 2 | Price > $3 | Same junk filter |
| 3 | Open > yesterday's high | Gap must clear resistance, not fill into it |
| 4 | Open > 200-day SMA | Only swing longs in long-term uptrends |
| 5 | Market cap >= $800M | Institutions can actually follow through |
| 6 | Real catalyst exists | Earnings on the gap day, or news with no earnings. `catalyst_found: false` kills it |

Reference stats (external claims, same honesty rule as above, not yet
reproduced in this repo): 57.6% win rate / PF 5.34 on news catalysts,
44.7% / PF 2.57 on earnings catalysts.

### Management

Swing entry and exit management is still being built. Swing names are
STARTER IDEAS ONLY: the report gives the catalyst, the theme, and the trend
context, and that is it. No fake stops, no fake targets, no live swing
entries on the paper account until the management rules are written and
backtested. A watchlist is not a position.

## 3. What both lists always respect

- Paper trading only, stops on everything, -7% hard bail.
- All TRADING-STRATEGY.md 3b guardrails: circuit breakers, event
  blackouts, 24h earnings no-entry (day trades), sector cap, max entries
  per week.
- Up on BAD news (dilution, offering, probe, guidance cut) is a TRAP, not
  a candidate, no matter what the flags say.
- "No qualifying setups today" is a valid output, not a failure.
