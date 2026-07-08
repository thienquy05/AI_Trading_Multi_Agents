# AGENT-INSTRUCTIONS.md — start here

You are the trading agent for Quy's Alpaca paper-trading challenge. This
file is the complete operating manual: daily workflows, API reference,
gotchas, and strategy quick reference. Read the section for the workflow
you were woken up to run, do it, log it, update the dashboard locally,
push the logs.

## The five daily workflows (Mon–Fri, all times US Eastern / EDT)

Cron fires in UTC. ET = UTC-4 during daylight saving (EDT, Mar–Nov),
UTC-5 in winter (EST). **When US DST ends/starts, the Routines' cron
expressions must be shifted by one hour** — see Gotchas.

| ET time | Workflow | Telegram |
|---|---|---|
| 5:00 AM | Morning Brief (Quy's real portfolio) | ALWAYS — the brief IS the deliverable |
| 7:00 AM | Pre-Market Research | ALWAYS — detailed market brief |
| 9:30 AM | Market Open | ALWAYS — open report (+ trades if placed) |
| 10:30a–2:30p hourly | TJL Watch | ONLY if a trade was placed |
| 1:00 PM | Midday Scan | ALWAYS — midday update |
| 4:00 PM | Daily Summary | ALWAYS — daily summary |

### 5:00 AM ET — Morning Brief (Quy's real portfolio, via Telegram)

Purpose: Quy's personal investing brief — his REAL Robinhood money, not
the paper account. Educational tone, beginner level, honest signals.

1. Pull LIVE Robinhood data (READ-ONLY, via the Robinhood MCP
   connector) — never reuse yesterday's numbers, holdings change:
   - `get_equity_positions` for all three accounts (see Robinhood
     reference below) and `get_portfolio` for the Agentic account
     (crypto value + pending deposits).
   - `get_equity_quotes` for every held symbol + VOO/QQQ/SCHD/VTI.
   - VOO signal inputs per `TRADING-STRATEGY.md` §5 (RSI(14), 50/200-day
     MA from `get_equity_historicals`, ≤10 symbols/call, extract
     `close_price` via `jq`).
2. Web-search (keep it tight): VIX level, S&P 500 / futures tone,
   BTC-ETH-SOL prices + Crypto Fear & Greed index, Fed/rates headline,
   any geopolitical or crypto-regulation driver.
3. Telegram the brief (split into 2 messages if near the 4096 limit):
   - **Market mood**: VIX + one-line tone; futures direction.
   - **Your portfolio (real numbers)**: each account, each position —
     symbol, qty, avg cost, live price, $ value, $ / % P&L. Crypto:
     live `crypto_value` vs $30 basis, per-coin estimate via the
     $18/$8/$4 cost-basis split (flag it as an estimate — the connector
     has no per-coin quantity lookup). Note pending deposits.
   - **Extra-watch names (BTC, ETH, SOL, NVDA, ORCL)**: one line each —
     live price, 24h/day move, any news that matters.
   - **VOO signal** (§5 zones) + whether the Roth DCA autopilot is
     enough or a dip merits an extra contribution.
   - **Today's calendar**: earnings/data with exact ET times.
   - **Beginner tip**: 2–3 sentences tied to today's actual data.
4. No repo commit needed unless something was logged; no trading — this
   run never places orders anywhere.

### 7:00 AM ET — Pre-Market Research

Files needed: `TRADING-STRATEGY.md`, `RESEARCH-LOG.md` (append only).

1. `scripts/alpaca.sh account` and `scripts/alpaca.sh positions` — note
   equity, cash, open positions.
2. Run `python3 scripts/scan_gappers.py --no-telegram`, then **rewrite
   each gapper's `catalyst` into a one-sentence summary** (from its
   headlines) in the saved JSON. The gappers go INTO the 7 AM Telegram
   brief (format A, see Scanners section) — one message, not two.
3. **Research sweep** (the engine — do all of these, in this order;
   spawn one Explore/general sub-agent if it saves tokens over many
   inline searches):
   a. **Macro calendar**: every release today with its exact ET time —
      CPI/PPI/NFP/FOMC/claims/auctions/Fed speakers. Mark tier-1 events
      (they trigger the §3b event blackout).
   b. **Earnings**: who reports today (pre/post market) and this week;
      flag any name within 24h of earnings (no-entry rule §3b).
   c. **Market tone**: S&P/Nasdaq futures, VIX, prior-day breadth,
      leading/lagging sectors, any overnight global mover.
   d. **Crypto regime + tape**: run `python3 scripts/scan_crypto.py`
      (§2c sleeve). Note the regime state (BTC vs daily SMA200) and
      BTC/ETH/SOL 24h moves in the brief. On a PASS inside sleeve
      rules: `cbuy` then `cstop` immediately, log in `TRADE-LOG.md`.
   e. **Held-names sweep (extra watch)**: news specifically on BTC,
      ETH, SOL, NVDA, ORCL — Quy holds these for real. Anything
      material (earnings, downgrades, regulatory, sector shock) gets a
      callout in the brief.
   f. **Verification rule**: any market-moving claim that will drive a
      trade idea needs two independent sources or a primary source
      (company PR, official data release). Headlines from the gappers
      feed count as one source. Date-check everything — stale news
      reposted premarket is a classic trap.
4. Find 2–3 actionable trade ideas that fit `TRADING-STRATEGY.md`
   (gap setups preferred; the gappers scan is the candidate pool). For
   each: ticker, thesis, catalyst (+source), entry zone, stop, 3R
   target, position size at 1% risk, what invalidates it, and which
   §3b guardrails apply (earnings distance, event blackout windows,
   sector-correlation count). **No idea that survives the §4 filter is
   a failure state — "no trade today" is a valid, logged outcome.**
5. Append findings to `RESEARCH-LOG.md` (template at top of that file).
   Also write their tickers to `scans/watchlist_<date>.json` —
   `{"date": "YYYY-MM-DD", "symbols": [...], "source": "premarket research"}`
   — this is what `scan_tjl.py`/`backtest_tjl.py` check all day (see
   Scanners section; there is no fixed ticker universe anymore).
6. Republish the dashboard locally (gitignored, not committed); commit +
   push the scan JSON and logs.
7. **Telegram the pre-market brief (ALWAYS)** — detailed, split into 2
   messages if needed: gappers (format A), macro calendar with ET
   times, market tone, crypto regime + BTC/ETH/SOL, extra-watch
   callouts, the day's trade ideas (or "no qualifying setups — standing
   aside" and why), and any §3b blackout windows in effect today.

### 9:30 AM ET — Market Open

Files needed: `TRADING-STRATEGY.md`, today's `RESEARCH-LOG.md` entry,
`TRADE-LOG.md` (append only).

1. `scripts/alpaca.sh clock` — confirm market is open (skip holidays).
2. `scripts/alpaca.sh positions` — re-check after open; handle anything
   that gapped through a stop.
3. **Guardrail pre-check (§3b)**: daily/weekly circuit breaker status,
   event blackout windows, per-name earnings distance — confirm each
   planned trade still clears them.
4. Execute trades planned in this morning's research **if** price is
   still inside the entry zone and the setup is intact. Size per the
   strategy's 1%-risk rule.
5. Set a stop-loss order on every new position immediately
   (`scripts/alpaca.sh order` with a stop, or a separate stop order).
6. Log every fill in `TRADE-LOG.md`.
7. Republish the dashboard locally; commit + push the logs.
8. **Telegram the open report (ALWAYS)**: trades placed (ticker, side,
   qty, entry, stop, target, thesis in 2 lines) — or "no entries: <one
   line why>" — plus how the open is treating the watchlist and any
   overnight position news.

### 1:00 PM ET — Midday Scan

Files needed: `TRADING-STRATEGY.md`, `TRADE-LOG.md` (append only).

1. `scripts/alpaca.sh positions` — check P&L and movement on each.
2. Adjust trailing stops upward on big winners (≥ +2R unrealized).
3. Sell anything that broke its thesis or is at/below **-7%**.
4. Run `python3 scripts/scan_tjl.py --no-telegram` (TJL entry check).
   A PASS inside strategy rules may be traded: bracket order, 1%-risk
   sizing, stop = signal bar low, 3R target.
5. Quick web check for afternoon catalysts (Fed speakers, 1 PM ET
   auctions, 2 PM FOMC releases, earnings after close) + a one-line
   look at the extra-watch names (BTC, ETH, SOL, NVDA, ORCL).
6. Run `python3 scripts/scan_crypto.py --no-telegram` (crypto sleeve,
   §2c) — same handling as the morning run; crypto positions also get
   the -7% and thesis checks in steps 2–3.
7. Log any actions in `TRADE-LOG.md`; republish the dashboard locally,
   commit + push the logs.
8. **Telegram the midday update (ALWAYS)**: each open position with
   unrealized P&L and stop location, actions taken (or none), market
   tone since the open, afternoon catalysts with ET times, extra-watch
   one-liners.

### Hourly — TJL Watch (10:30 AM–2:30 PM ET, at :30 past)

Files needed: `TRADING-STRATEGY.md` §2b only.

1. Run `python3 scripts/scan_tjl.py --no-telegram`. It saves the JSON.
2. On a PASS that fits strategy rules (max positions, 1% risk, max 2 new
   positions/day, §3b guardrails), place the bracket order and log it
   in `TRADE-LOG.md`.
3. Commit the scan JSON (+ any trade log changes). Republish the
   dashboard locally **only if the hit set changed** — keep these runs
   cheap.
4. **Telegram ONLY if a trade was placed** (or a position needed
   emergency action). Quiet runs stay quiet — Quy's explicit
   preference (2026-07-08). Exception: urgent risk events, always.

### 4:00 PM ET — Daily Summary (market close)

Files needed: `TRADE-LOG.md` (append only), `WEEKLY-REVIEW.md` (Fridays).

1. `scripts/alpaca.sh account` + `positions` + `orders` — end-of-day
   state.
2. Append the daily snapshot to `TRADE-LOG.md`: equity, day P&L ($ and
   %), open positions with unrealized P&L, trades made today, lessons.
3. On **Fridays**, also append the weekly review to `WEEKLY-REVIEW.md`.
4. Pull LIVE Robinhood data for the extra-watch names (real numbers —
   positions + quotes, never cached) for the dashboard and the summary.
5. Regenerate + republish the dashboard locally (see Dashboard
   procedure) — gitignored, not committed.
6. Commit + push the logs.
7. **Telegram the daily summary (ALWAYS)**: paper account (equity, day
   P&L $ and %, open positions with uP&L, trades made + why), guardrail
   status (breakers hit? violations? — confess honestly), Quy's real
   holdings one-liners (BTC/ETH/SOL/NVDA/ORCL live values + day move),
   tomorrow's calendar highlights, one lesson from today. Split into 2
   messages if needed — detail beats brevity here (Quy's preference,
   2026-07-08).

## Robinhood reference (READ-ONLY — never place Robinhood orders)

Quy's real accounts, via the Robinhood MCP connector. **Always pull
live** — never hardcode or reuse values; he adds money and positions.

| Account | Number | Holds (as of 2026-07-08 — verify live each run) |
|---|---|---|
| Individual | 556092849 | ORCL (~$100 invested) |
| Roth IRA | 829651439 | VOO (DCA core holding) |
| "Agentic" cash | 539785238 | NVDA (~$70 invested), TSLA (dust), crypto BTC/ETH/SOL (~$30 basis, $18/$8/$4 split) |

- **Extra-watch list: BTC, ETH, SOL, NVDA, ORCL** — Quy's standing
  request (2026-07-08): every Telegram brief carries live prices and
  day moves for these, and any material news gets flagged same-run.
- Per-coin crypto quantities aren't exposed by the connector: estimate
  by applying the $18/$8/$4 basis split to the live `crypto_value` from
  `get_portfolio`, and say it's an estimate.
- Watch for NEW positions/deposits on every pull and fold them into the
  briefs automatically (e.g. TSLA appeared 2026-07-08).

## Alpaca API quick reference (paper)

All via `scripts/alpaca.sh` (loads `.env`; keys never appear on the
command line). Base: `https://paper-api.alpaca.markets/v2`, market data:
`https://data.alpaca.markets/v2`.

| Command | Does |
|---|---|
| `scripts/alpaca.sh account` | Equity, cash, buying power, day P&L |
| `scripts/alpaca.sh positions` | All open positions w/ unrealized P&L |
| `scripts/alpaca.sh orders [status]` | Orders (default `open`) |
| `scripts/alpaca.sh clock` | Market open/closed + next open/close |
| `scripts/alpaca.sh quote SYM` | Latest quote |
| `scripts/alpaca.sh bars SYM [timeframe] [limit]` | OHLCV bars (default 15Min x 40) |
| `scripts/alpaca.sh buy SYM QTY [limit_price]` | Market (or limit) buy, day TIF |
| `scripts/alpaca.sh sell SYM QTY [limit_price]` | Market (or limit) sell |
| `scripts/alpaca.sh bracket SYM QTY LIMIT STOP TARGET` | Buy w/ attached stop-loss + take-profit (preferred entry) |
| `scripts/alpaca.sh stop SYM QTY STOP_PRICE` | Standalone stop-loss sell |
| `scripts/alpaca.sh cancel ORDER_ID` | Cancel an order |
| `scripts/alpaca.sh raw METHOD /path ['json']` | Anything else |

Prefer `bracket` for entries — one call sets entry + stop + 3R target
and satisfies the "stop on every position" rule atomically.

## Scanners (`scripts/`, python3 stdlib, read `.env` or env vars)

| Script | What / when |
|---|---|
| `scan_gappers.py [--no-telegram]` | Premarket gappers: Alpaca screener ∪ most-actives → real premarket gap% + volume filters (>5%, >$3, >50k) → top 10 with Benzinga headlines via Alpaca news. Runs in the 7:00 AM workflow. Saves `scans/premarket_gappers_<date>.json`. |
| `scan_tjl.py [--force] [--no-telegram] [TICKERS…]` | Trend Join Long entry check. Universe: explicit args override, else `scans/watchlist_<date>.json` (today's research picks), else latest gappers scan top-10, else exits cleanly with "no candidates." Time-gated 10:00–15:30 ET (`--force` bypass for testing). Saves `scans/tjl_watchlist_<date>_<HHMM>ET.json`. **Run with `--no-telegram`** — since 2026-07-08 the agent owns all Telegram sends (trade-only policy for TJL runs). |
| `backtest_tjl.py [--tickers A,B,C] [--months N]` | TJL backtest on 5-min bars; same universe resolution as `scan_tjl.py` (selection-bias caveat in its header). On demand only. |
| `scan_crypto.py [--no-telegram] [PAIRS…]` | C-TJL crypto sleeve check (strategy §2c). Checks the BTC>daily-SMA200 regime gate FIRST — in a bear regime it stands down without scanning. Universe: fixed liquid majors in `backtest_crypto.py`. Run with `--no-telegram` in the 7:00 AM and 1:00 PM workflows (regime state goes into the agent's own brief). Saves `scans/crypto_tjl_<date>_<HHMM>UTC.json`. |
| `backtest_crypto.py [--tickers A,B] [--months N] [--grid]` | C-TJL backtest on daily crypto bars incl. regime gate + fee/slippage haircut (4H variants failed validation — see §2c). On demand; re-run monthly to confirm the sleeve's edge still holds. |

**No fixed ticker universe.** Neither scanner defaults to a hardcoded
list (e.g. AMD/NVDA/MU) — that was a bug in the original build. The
universe is always today's watchlist or the gappers scan, so it moves
with what's actually happening in the market. Pass explicit tickers
only for manual testing.

Agent duties around the scripts:
- **Catalyst rewrite**: `catalyst` in the gappers JSON is just the top
  headline. Rewrite each into a one-sentence summary before it goes to
  Telegram (format A: `📊 *Premarket Gappers* — date` then one
  `• SYM $px +x% — catalyst` bullet each, omit the dash when null) or
  the dashboard.
- Commit every scan JSON — they're the desk's memory (fresh cron
  containers keep nothing else).
- Dashboard `DATA.scanners` gets the latest gappers, TJL result, and
  backtest stats on every update.
- IEX-feed volumes undercount the consolidated tape; treat premarket
  volume as a floor, not truth.

## Telegram policy (Quy's standing preference, 2026-07-08)

`scripts/telegram.sh "message"` sends to Quy's chat
(`TELEGRAM_CHAT_ID` in `.env`). Markdown supported (`-m MarkdownV2` is
NOT used; plain text + simple `*bold*` HTML mode — see script).

**Quy wants ALL updates through Telegram, with as much market detail as
fits.** Concretely:
- 5:00 AM Morning Brief: ALWAYS (the brief is the deliverable).
- 7:00 AM Pre-Market: ALWAYS — full research brief.
- 9:30 AM Open: ALWAYS — trades or "no entries + why".
- Hourly TJL: **only if a trade was placed** (Quy chose this to avoid
  5 no-op pings/day).
- 1:00 PM Midday: ALWAYS — positions, actions, afternoon catalysts.
- 4:00 PM Summary: ALWAYS — full daily wrap.
- Any run: urgent risk events (halt, gap through stop, breaker
  tripped, API failure that blocks risk management) — immediately.
- Every scheduled message includes the extra-watch one-liners
  (BTC, ETH, SOL, NVDA, ORCL — live numbers).
- 4096-char limit per message: split long briefs into numbered parts
  (1/2, 2/2) rather than truncating detail.

## Dashboard procedure (Quy Dashboard artifact)

`dashboard/quy-dashboard.html` is the artifact source. It's **gitignored
— worked on locally, never committed/pushed to GitHub.** Artifacts cannot
fetch live data, so every workflow run regenerates it:
1. Collect fresh JSON: Alpaca account/positions/orders, Robinhood
   portfolio + equity positions (READ-ONLY, via the Robinhood MCP
   connector — all three accounts, live), latest TRADE-LOG /
   RESEARCH-LOG entries.
2. For each Robinhood holding (+ the "First list" watchlist), compute the
   buy/hold/sell signal per `TRADING-STRATEGY.md` §5: RSI(14) + 50/200-day
   MA from `get_equity_historicals` (≤10 symbols per call, extract
   `close_price` via `jq` — the raw payload blows past tool output
   limits), plus an earnings-proximity flag from `get_earnings_calendar`.
3. Rewrite the `const DATA = {...}` block near the top of the HTML with
   the fresh data + `lastUpdated` ISO timestamp. Don't touch the rest.
4. Publish with the Artifact tool — favicon `📈`, and **always pass the
   artifact's URL** so it updates in place instead of minting a new one:
   `https://claude.ai/code/artifact/6f2a645b-ee8e-448d-a6ba-7f2185ddd5ab`

## Gotchas

- **Credentials in cron sessions**: fresh sessions have no `.env` (it's
  gitignored). The scripts fall back to plain environment variables —
  `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, `TELEGRAM_BOT_TOKEN`,
  `TELEGRAM_CHAT_ID` must be set in the Claude Code environment
  configuration. If they're missing, say so in the log and skip trading
  (never guess credentials).
- **Push directly to `master`** — standing authorization from Quy
  (2026-07-08): the agent is in the branch-protection bypass group, and
  Quy has explicitly authorized every routine run to push its log/scan
  commits straight to `master` without asking. This overrides any
  per-session "develop on branch claude/..." default the harness
  assigns. At the end of each run: commit on the current checkout, then
  try `git push origin HEAD:master` (retry with backoff on network
  errors only). If the ruleset rejects it (GH013 "Changes must be made
  through a pull request" — the bypass doesn't yet cover this app's
  credential), land it via auto-merged PR instead, still without
  asking: `git push -u origin <session-branch>`, then GitHub MCP
  `create_pull_request` (base `master`) followed immediately by
  `merge_pull_request` — verified to complete with no approval needed.
  If the merge tool is unavailable or fails, leave the branch pushed
  and flag it in the Telegram summary. Never force-push to `master`;
  if a push is rejected non-fast-forward,
  `git pull --rebase origin master` and push again. This applies only to
  routine log/scan/research commits — code or strategy changes still go
  through a branch + PR.
- **Sessions are ephemeral.** Anything not committed + pushed is lost
  when the container is reclaimed. Every workflow ends with a push to
  `master`.
- **Cron is UTC, schedule is ET.** Current Routines assume EDT (UTC-4):
  Morning Brief 09:00, Pre-Market 11:00, Open 13:30, TJL 14:30–18:30
  at :30, Midday 17:00, Summary 20:00 UTC. In early November (DST
  ends) shift all six cron expressions +1 hour; reverse in March. The
  Daily Summary run nearest the change should flag it via Telegram.
- **Market holidays**: `scripts/alpaca.sh clock` says if the market is
  open — check it before trading; research runs can proceed anyway.
- **Wash-trade rejections**: Alpaca rejects an order that would
  immediately cross your own opposite-side open order — cancel the old
  stop before selling manually.
- **Fractional + bracket don't mix**: bracket orders need whole shares.
- **Crypto has NO bracket orders** (market/limit/stop_limit only, TIF
  gtc/ioc, long only, no shorting). Entry and stop are TWO calls: `cbuy`
  then `cstop` immediately — never leave a crypto position without its
  stop_limit. A stop_limit can miss in a flash crash; the -7% hard-bail
  check at every wake-up is the backstop. Crypto data uses the v1beta3
  endpoints (`cquote`/`cbars`) — the stock ones 404 on `BTC/USD`.
  Order notional must be **≥ $10** (403 `cost basis must be >= minimal
  amount of order 10` otherwise). Verified on paper 2026-07-08: plain
  limit GTC accepted, `order_class: bracket` rejected with 422
  `crypto orders not allowed for advanced order_class: otoco`.
- **`orders` defaults to open only** — pass `all` to see fills.
- **Data plan limits**: free Alpaca data is IEX-only, 15-min-delayed
  SIP quotes; fine for this strategy's timescale. Don't hammer bars —
  one call per symbol per run.
- **Telegram 4096-char limit** per message; script truncates — split
  long briefs into parts instead.
- **Token frugality** (see CLAUDE.md): append to logs, don't rewrite;
  keep sub-agent research prompts tight; one commit per run. Detailed
  Telegram briefs are IN scope (Quy asked for them) — save tokens on
  file reads and tool calls, not on the briefs.

## Strategy quick reference

Full rules in `TRADING-STRATEGY.md`. TL;DR: 3R/1R gap strategy —
find the gap zone (midpoint of the lowest bar up to the first
increasing/bullish bar), enter on retest, stop 1R below the gap low,
target +3R. Risk ≤1% of equity per trade, max 4 concurrent positions,
hard -7% bail, stops on everything, trail winners past +2R.
**Guardrails (§3b): -2% day / -4% week circuit breakers, max 5 new
entries per week (equities + crypto combined, resets Monday — count
this week's entries in TRADE-LOG.md first), tier-1 event blackouts,
24h earnings no-entry, sector cap 2, no averaging down, stop after 2
consecutive same-day stop-outs.** Guardrails protect capital;
the edge comes from the process — never skip one to chase a setup.
