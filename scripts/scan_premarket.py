#!/usr/bin/env python3
"""Premarket packet builder - data collection only, zero analysis.

Collects raw premarket data into scans/packet_YYYY-MM-DD.json. No
conviction, no buckets, no opinions: all judgment happens later in the
analyst pass (PROMPT-PREMARKET.md). The deterministic watchlist flags
(day_eligible, swing_eligible) encode WATCHLIST_CRITERIA.md in code,
not in an AI's mood.

Data policy (revised 2026-07-16, yfinance removed):
  - Alpaca (keys via .env or env vars) is the sole source of truth for
    candidates, premarket gaps, premarket volume, TRUE premarket RVOL,
    and live intraday levels. There is no keyless fallback candidate
    path anymore: without Alpaca credentials this packet has no
    gappers.
  - yfinance previously filled what the free Alpaca tier lacks (market
    cap, the index/VIX/rates/oil/dollar snapshot, earnings dates, a
    keyless screener fallback) but was removed 2026-07-16: Yahoo's
    edge rate-limits (HTTP 429 "Too Many Requests") this sandbox's
    shared egress IP, so every yfinance call failed every single run
    since 2026-07-09 (confirmed via direct curl: real 429 responses,
    not a network/firewall block). Dead, misleading code, not a real
    fallback. market_cap, next_earnings, and market_snapshot are now
    ALWAYS None/empty from this script; see gaps_to_fill. That means
    the mcap_gt_1b / mcap_ge_800m WATCHLIST_CRITERIA.md gates can never
    pass until a replacement market-cap source is wired in (SEC EDGAR's
    keyless company-facts API is a candidate; ask before adding a new
    paid data source).
  - feedparser RSS + the ForexFactory weekly JSON replace token-costly
    web searches for market news and the econ calendar.

Every network call is wrapped: one bad ticker or dead feed never kills
the run. Progress prints to stdout. No em dashes in this file.

Usage: scan_premarket.py [--no-alpaca]
Output: scans/packet_YYYY-MM-DD.json
"""
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta

from alpaca_common import (DATA, ET, SCANS, get, get_bars, latest_trades,
                           load_env, save_json)

try:
    import feedparser
except ImportError:
    feedparser = None

GAP_MIN, PRICE_MIN, TOP_N, CAND_CAP = 3.0, 3.0, 12, 60

SNAPSHOT_SYMBOLS = {
    "S&P 500": "^GSPC", "Dow": "^DJI", "Nasdaq": "^IXIC",
    "Russell 2000": "^RUT", "VIX": "^VIX", "US 10Y": "^TNX",
    "US 3M": "^IRX", "WTI Oil": "CL=F", "Dollar (DXY)": "DX-Y.NYB",
}

RSS_FEEDS = [
    ("MarketWatch Top", "https://feeds.content.dowjones.io/public/rss/mw_topstories"),
    ("MarketWatch RealTime", "https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines"),
    ("CNBC", "https://www.cnbc.com/id/100003114/device/rss/rss.html"),
    ("Yahoo Finance", "https://finance.yahoo.com/news/rssindex"),
    ("Google News Markets",
     "https://news.google.com/rss/search?q=stock+market+OR+earnings+when:1d&hl=en-US&gl=US&ceid=US:en"),
]
# Obvious SEO spam: crypto price prediction mills and "NVDA 2025-2030" bait.
SPAM_RE = re.compile(r"price prediction|20\d\d\s*-\s*20\d\d", re.I)
TAG_RE = re.compile(r"<[^>]+>")

PRIMARY_PUBS = ["bloomberg", "reuters", "cnbc", "marketwatch", "barron",
                "wsj", "wall street journal", "dow jones", "yahoo finance",
                "financial times", "benzinga", "associated press"]

# Generic company-name words that must NEVER match a company on their own.
# Without this, a headline saying "Applied Materials beats" would count as
# a catalyst for Applied Digital and Applied Optoelectronics too; same for
# "Digital", "Holdings", "Strategy" and friends. A name token only counts
# as distinctive if it is 4+ letters AND not in this set.
NAME_STOP = {"the", "inc", "corp", "corporation", "company", "co", "plc",
             "ltd", "llc", "holdings", "holding", "group", "technologies",
             "technology", "tech", "digital", "applied", "advanced",
             "strategy", "strategies", "motors", "motor", "energy",
             "platforms", "platform", "systems", "solutions", "sciences",
             "science", "industries", "industrial", "global",
             "international", "enterprises", "enterprise", "financial",
             "capital", "partners", "resources", "materials", "media",
             "communications", "networks", "labs", "pharmaceuticals",
             "pharma", "therapeutics", "bancorp", "airlines", "brands",
             "acquisition", "trust", "fund", "first", "united", "american",
             "national", "new", "class", "series"}

FF_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
FF_CACHE = SCANS / ".ff_calendar_cache.json"
FF_TTL_HOURS = 4


def step(msg):
    print(f"[scan_premarket] {msg}", flush=True)


# ---------------------------------------------------------------- snapshot

def market_snapshot():
    """Index/VIX/rates/oil/dollar snapshot. No keyless source is wired in
    (yfinance removed 2026-07-16, see module docstring) - the agent fills
    this gap via Robinhood get_index_quotes or one web search per the
    7:00 AM workflow step 3a."""
    out = {name: {"symbol": sym, "error": "no market-snapshot source configured"}
           for name, sym in SNAPSHOT_SYMBOLS.items()}
    step("market snapshot: no source configured, skipped (agent fills via Robinhood/web search)")
    return out


# -------------------------------------------------------------- candidates

def candidates_alpaca(now, today):
    """Alpaca screener gainers + most-actives, gap from real premarket
    trades vs previous daily close. Returns (rows, label) or (None, why)."""
    syms, seen = [], set()
    for url, key in ((f"{DATA}/v1beta1/screener/stocks/movers?top=50", "gainers"),
                     (f"{DATA}/v1beta1/screener/stocks/most-actives?by=volume&top=50",
                      "most_actives")):
        try:
            for row in get(url).get(key, []):
                s = row["symbol"]
                if s not in seen and s.isalpha():
                    seen.add(s)
                    syms.append(s)
        except Exception as e:
            step(f"alpaca screener {key} failed: {e}")
    syms = syms[:CAND_CAP]
    if not syms:
        return None, "alpaca screeners returned nothing"

    daily = get_bars(syms, "1Day", now - timedelta(days=10))
    prev_close = {}
    for s, bars in daily.items():
        done = [b for b in bars if b["t"].date() < today]
        if done:
            prev_close[s] = done[-1]["c"]

    pm_start = now.replace(hour=4, minute=0, second=0, microsecond=0)
    pm_end = min(now, now.replace(hour=9, minute=30, second=0, microsecond=0))
    pm = (get_bars(list(prev_close), "1Min", pm_start, pm_end)
          if now >= pm_start else {})
    try:
        live = latest_trades(list(prev_close))
    except Exception:
        live = {}

    rows = []
    for s, pc in prev_close.items():
        bars = [b for b in pm.get(s, []) if pm_start <= b["t"] < pm_end]
        pm_last = bars[-1]["c"] if bars else None
        px = live.get(s) or pm_last
        ref = pm_last or px
        if not px or not ref:
            continue
        rows.append({"symbol": s, "price": round(px, 2),
                     "prev_close": round(pc, 2),
                     "gap_pct": round((ref / pc - 1) * 100, 2),
                     "premarket_volume": int(sum(b["v"] for b in bars)),
                     "market_cap": None, "volume": None, "name": None})
    return rows, "alpaca_screener_premarket"


# ------------------------------------------------------------------- news

def fetch_rss():
    """Market-wide headlines from free RSS, HTML-stripped, spam-dropped."""
    if feedparser is None:
        return [], "feedparser not installed"
    items = []
    for src, url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:25]:
                title = TAG_RE.sub("", e.get("title", "")).strip()
                if not title or SPAM_RE.search(title):
                    continue
                summary = TAG_RE.sub(" ", e.get("summary", ""))
                summary = re.sub(r"\s+", " ", summary).strip()[:280]
                items.append({"title": title, "summary": summary,
                              "source": src,
                              "published": e.get("published", "")})
            step(f"rss {src}: {len(feed.entries)} entries")
        except Exception as e:
            step(f"rss {src} failed: {e}")
    return items, None


def name_matchers(sym, company):
    """Regexes that decide whether a headline is about this company: the
    ticker on a word boundary (case sensitive, headlines print tickers
    uppercase) OR a DISTINCTIVE company-name token, 4+ letters and not in
    NAME_STOP. See the NAME_STOP comment for the Applied/Digital
    cross-match bug this prevents."""
    tick_re = re.compile(rf"\b{re.escape(sym)}\b")
    tokens = []
    for tok in re.split(r"[^A-Za-z]+", company or ""):
        t = tok.lower()
        if len(t) >= 4 and t not in NAME_STOP:
            tokens.append(re.compile(rf"\b{re.escape(t)}\b", re.I))
    return tick_re, tokens


def mentions(title, tick_re, tokens):
    return bool(tick_re.search(title) or any(t.search(title) for t in tokens))


def match_headlines(rss_items, tick_re, tokens):
    return [it for it in rss_items if mentions(it["title"], tick_re, tokens)]


def rank_headlines(headlines, tick_re, tokens):
    """Headlines that actually name the company first (the Alpaca feed
    tags market wraps with every symbol they brush past), then primary
    publishers, then the rest, order preserved."""
    def key(h):
        named = 0 if mentions(h.get("title", ""), tick_re, tokens) else 1
        # an Alpaca item tagged with 3+ symbols is almost always a wrap
        wrap = 1 if h.get("n_symbols", 1) >= 3 else 0
        src = (h.get("source") or "").lower()
        for i, pub in enumerate(PRIMARY_PUBS):
            if pub in src:
                return (named, wrap, 0, i)
        return (named, wrap, 1, 0)
    return sorted(headlines, key=key)


# ---------------------------------------------------------- econ calendar

def econ_calendar(now):
    """US High-impact events today + tomorrow (ET) from the ForexFactory
    data-partner weekly JSON. Cached to a dotfile with a ~4h TTL because
    the feed rate-limits (429) on rapid calls. Fully defensive: any
    failure returns an empty calendar with an error note, never raises."""
    today = now.date()
    tomorrow = today + timedelta(days=1)
    result = {"source": FF_URL, "filter": "country=USD, impact=High",
              "today_date": str(today), "tomorrow_date": str(tomorrow),
              "today": [], "tomorrow": []}
    raw, note = None, None

    cached = None
    try:
        if FF_CACHE.exists():
            cached = json.loads(FF_CACHE.read_text())
    except Exception:
        cached = None
    if cached:
        age_h = (now.timestamp() - cached.get("fetched_at_ts", 0)) / 3600
        if age_h < FF_TTL_HOURS:
            raw, note = cached["data"], f"cache hit ({age_h:.1f}h old)"

    if raw is None:
        try:
            req = urllib.request.Request(FF_URL, headers={
                "User-Agent": "Mozilla/5.0 (zenith premarket scan)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = json.load(r)
            SCANS.mkdir(exist_ok=True)
            FF_CACHE.write_text(json.dumps(
                {"fetched_at": now.isoformat(),
                 "fetched_at_ts": now.timestamp(), "data": raw}))
            note = "live fetch"
        except Exception as e:
            if cached:
                raw = cached["data"]
                note = (f"live fetch failed ({str(e)[:80]}); using stale "
                        f"cache from {cached.get('fetched_at', '?')}")
            else:
                result["error"] = f"feed unavailable: {str(e)[:120]}"
                step(f"econ calendar FAILED: {result['error']}")
                return result

    try:
        for ev in raw:
            if ev.get("country") != "USD" or ev.get("impact") != "High":
                continue
            try:
                dt = datetime.fromisoformat(ev["date"]).astimezone(ET)
            except Exception:
                continue
            rec = {"time_et": dt.strftime("%I:%M %p").lstrip("0"),
                   "title": ev.get("title", ""),
                   "forecast": ev.get("forecast", ""),
                   "previous": ev.get("previous", ""), "_dt": dt}
            if dt.date() == today:
                result["today"].append(rec)
            elif dt.date() == tomorrow:
                result["tomorrow"].append(rec)
        for k in ("today", "tomorrow"):
            result[k].sort(key=lambda r: r.pop("_dt"))
        result["note"] = note
    except Exception as e:
        result["error"] = f"parse failed: {str(e)[:120]}"
    step(f"econ calendar: {len(result['today'])} today, "
         f"{len(result['tomorrow'])} tomorrow ({note})")
    return result


# ------------------------------------------------------------- enrichment

def alpaca_levels(syms, now, today):
    """Live intraday levels from Alpaca 5-min bars (premarket included):
    VWAP, HOD, LOD, premarket high, premarket volume, today's open."""
    out = {s: {} for s in syms}
    try:
        start = now.replace(hour=4, minute=0, second=0, microsecond=0)
        bars = get_bars(syms, "5Min", start)
        open_t = now.replace(hour=9, minute=30, second=0, microsecond=0)
        for s in syms:
            bs = [b for b in bars.get(s, []) if b["t"].date() == today]
            if not bs:
                continue
            pmb = [b for b in bs if b["t"] < open_t]
            reg = [b for b in bs if b["t"] >= open_t]
            vol = sum(b["v"] for b in bs)
            out[s] = {
                "vwap": round(sum(b.get("vw", b["c"]) * b["v"] for b in bs)
                              / vol, 2) if vol else None,
                "premarket_high": round(max(b["h"] for b in pmb), 2) if pmb else None,
                "premarket_volume": int(sum(b["v"] for b in pmb)),
                "hod": round(max(b["h"] for b in reg), 2) if reg else None,
                "lod": round(min(b["l"] for b in reg), 2) if reg else None,
                "today_open": round(reg[0]["o"], 2) if reg else None,
            }
    except Exception as e:
        step(f"intraday levels failed: {e}")
    return out


def alpaca_daily(syms, now, today):
    """Daily metrics from 1y of bars, excluding today's partial bar:
    SMA200, prior-day high, prior close, 20-day average volume."""
    out = {s: {} for s in syms}
    try:
        daily = get_bars(syms, "1Day", now - timedelta(days=380))
        for s in syms:
            done = [b for b in daily.get(s, []) if b["t"].date() < today]
            if not done:
                continue
            closes = [b["c"] for b in done]
            out[s] = {
                "sma200": round(sum(closes[-200:]) / 200, 2)
                          if len(closes) >= 200 else None,
                "prior_day_high": round(done[-1]["h"], 2),
                "prior_close": round(done[-1]["c"], 2),
                "avg_vol_20d": int(sum(b["v"] for b in done[-20:])
                                   / min(20, len(done))),
                "today_volume_daily": None,
            }
        # today's partial daily bar gives full-day volume so far
        for s, bs in daily.items():
            todays = [b for b in bs if b["t"].date() == today]
            if todays and s in out and out[s]:
                out[s]["today_volume_daily"] = int(todays[-1]["v"])
    except Exception as e:
        step(f"daily metrics failed: {e}")
    return out


def alpaca_pm_rvol(syms, now, today):
    """TRUE premarket RVOL: today's premarket volume so far vs the 20-day
    average premarket volume at the same clock time, from 15-min bars.
    A true premarket RVOL needs a premarket feed; Alpaca is the only one
    wired in here now."""
    out = {s: None for s in syms}
    try:
        clock_cap = min(now.time(),
                        now.replace(hour=9, minute=30).time())
        pm_open = now.replace(hour=4, minute=0).time()
        if clock_cap <= pm_open:
            return out  # before 04:00 ET there is no premarket volume yet
        bars = get_bars(syms, "15Min", now - timedelta(days=30))
        for s in syms:
            per_day = {}
            for b in bars.get(s, []):
                bt = b["t"]
                if pm_open <= bt.time() < clock_cap:
                    per_day[bt.date()] = per_day.get(bt.date(), 0) + b["v"]
            hist = [v for d, v in sorted(per_day.items()) if d < today][-20:]
            today_v = per_day.get(today, 0)
            if hist and sum(hist):
                out[s] = round(today_v / (sum(hist) / len(hist)), 2)
    except Exception as e:
        step(f"premarket rvol failed: {e}")
    return out


def alpaca_news(syms):
    """Per-ticker headlines from Alpaca news (Benzinga), already
    ticker-tagged by the feed so no name matching needed."""
    out = {s: [] for s in syms}
    try:
        news = get(f"{DATA}/v1beta1/news",
                   {"symbols": ",".join(syms), "limit": 50})
        for item in news.get("news", []):
            for s in item.get("symbols", []):
                if s in out and len(out[s]) < 4:
                    out[s].append({"title": item.get("headline", ""),
                                   "source": item.get("source", "benzinga"),
                                   "published": item.get("created_at", ""),
                                   "n_symbols": len(item.get("symbols", []))})
    except Exception as e:
        step(f"alpaca news failed: {e}")
    return out


# ------------------------------------------------------------------- main

def main():
    now = datetime.now(ET)
    today = now.date()
    use_alpaca = "--no-alpaca" not in sys.argv
    if use_alpaca:
        try:
            load_env()
        except SystemExit as e:
            step(f"alpaca unavailable ({e}); falling back to keyless path")
            use_alpaca = False

    gaps_to_fill = [
        "market_snapshot: no source configured (yfinance removed "
        "2026-07-16, permanently rate-limited on this sandbox) - agent "
        "fills via Robinhood get_index_quotes or one web search",
        "market_cap: no source configured (yfinance removed 2026-07-16) "
        "- mcap_gt_1b / mcap_ge_800m day/swing gates can never pass "
        "until a replacement source is wired in",
        "market-wide earnings calendar is only partial: no per-gapper "
        "next_earnings source either (yfinance removed) - use "
        "get_earnings_calendar/get_earnings_results for gappers that "
        "clear the other gates",
        "intraday levels (VWAP/HOD/LOD/PMH) need intraday bars and are "
        "only available on the Alpaca path",
        "candidates have no keyless fallback anymore (yfinance removed "
        "2026-07-16): without Alpaca credentials this packet has zero "
        "gappers",
    ]

    step("1/6 market snapshot")
    snapshot = market_snapshot()

    step("2/6 candidates")
    rows, source = (None, "alpaca disabled")
    if use_alpaca:
        try:
            rows, source = candidates_alpaca(now, today)
        except Exception as e:
            rows, source = None, f"alpaca candidates failed: {e}"
            step(source)
    rows = rows or []
    step(f"candidates: {len(rows)} from {source}")

    # gap filter: abs gap >= 3 (day rule needs >3, so do not starve it),
    # price >= $3, top 12 by absolute gap
    movers = [r for r in rows
              if abs(r["gap_pct"]) >= GAP_MIN and r["price"] >= PRICE_MIN]
    movers.sort(key=lambda r: -abs(r["gap_pct"]))
    movers = movers[:TOP_N]
    syms = [r["symbol"] for r in movers]
    step(f"gap filter: {len(movers)} gappers kept: {', '.join(syms) or 'none'}")

    step("3/6 market news (rss)")
    rss_items, rss_err = fetch_rss()
    if rss_err:
        gaps_to_fill.append(f"market news unavailable: {rss_err}")

    step("4/6 econ calendar")
    econ = econ_calendar(now)

    step("5/6 per-gapper enrichment")
    levels = alpaca_levels(syms, now, today) if (use_alpaca and syms) else {}
    dailym = alpaca_daily(syms, now, today) if (use_alpaca and syms) else {}
    pm_rvol = alpaca_pm_rvol(syms, now, today) if (use_alpaca and syms) else {}
    a_news = alpaca_news(syms) if (use_alpaca and syms) else {}

    gappers = []
    for i, r in enumerate(movers):
        s = r["symbol"]
        cap, earn = r.get("market_cap"), None
        name = r.get("name")
        lv = levels.get(s) or {}
        dm = dailym.get(s) or {}

        tick_re, tokens = name_matchers(s, name)
        headlines = list(a_news.get(s) or [])
        headlines += match_headlines(rss_items, tick_re, tokens)
        headlines = rank_headlines(headlines, tick_re, tokens)[:5]
        catalyst_found = bool(headlines)

        pm_vol = lv.get("premarket_volume")
        if pm_vol is None:
            pm_vol = r.get("premarket_volume")
        today_vol = dm.get("today_volume_daily") or r.get("volume")
        rvol_full = (round(today_vol / dm["avg_vol_20d"], 2)
                     if today_vol and dm.get("avg_vol_20d") else None)
        rvol_pm = pm_rvol.get(s)
        rvol_used = rvol_pm if rvol_pm is not None else rvol_full

        # before 09:30 there is no official open: the latest premarket
        # price stands in for it (noted in scan_params)
        open_proxy = lv.get("today_open") or r["price"]
        prior_high = dm.get("prior_day_high")
        sma200 = dm.get("sma200")
        gap = r["gap_pct"]

        day_checks = {
            "gap_gt_3": gap > 3,
            "price_gt_3": r["price"] > 3,
            "mcap_gt_1b": bool(cap and cap > 1_000_000_000),
            "rvol_gt_1.5": bool(rvol_used and rvol_used > 1.5),
            "price_above_prior_high": bool(prior_high and r["price"] > prior_high),
            "prev_close_above_sma200": bool(sma200 and dm.get("prior_close")
                                            and dm["prior_close"] > sma200),
        }
        swing_checks = {
            "gap_ge_8": gap >= 8,
            "price_gt_3": r["price"] > 3,
            "open_above_prior_high": bool(prior_high and open_proxy > prior_high),
            "open_above_sma200": bool(sma200 and open_proxy > sma200),
            "mcap_ge_800m": bool(cap and cap >= 800_000_000),
            "catalyst_found": catalyst_found,
        }

        gappers.append({
            "rank": i + 1, "symbol": s, "name": name,
            "price": r["price"], "prev_close": r["prev_close"],
            "gap_pct": gap, "market_cap": cap,
            "premarket_volume": pm_vol, "today_volume": today_vol,
            "rvol_premarket": rvol_pm, "rvol_fullday": rvol_full,
            "vwap": lv.get("vwap"), "premarket_high": lv.get("premarket_high"),
            "hod": lv.get("hod"), "lod": lv.get("lod"),
            "today_open": lv.get("today_open"),
            "sma200": sma200, "prior_day_high": prior_high,
            "prior_close": dm.get("prior_close"),
            "avg_vol_20d": dm.get("avg_vol_20d"),
            "next_earnings": earn,
            "catalyst_found": catalyst_found,
            "catalyst": headlines[0]["title"] if headlines else None,
            "headlines": headlines,
            "day_checks": day_checks,
            "day_eligible": all(day_checks.values()),
            "swing_checks": swing_checks,
            "swing_eligible": all(swing_checks.values()),
        })
        step(f"  {s}: gap {gap:+.1f}%  day={all(day_checks.values())} "
             f"swing={all(swing_checks.values())} catalyst={catalyst_found}")

    step("6/6 writing packet")
    in_premarket = (now.replace(hour=4, minute=0) <= now
                    < now.replace(hour=9, minute=30))
    packet = {
        "generated_at": now.isoformat(),
        "candidate_source": source,
        "trading_day_note": (
            f"{now:%A %Y-%m-%d %H:%M} ET; "
            + ("inside the 04:00-09:30 premarket window"
               if in_premarket else
               "OUTSIDE the premarket window: levels and gaps reflect "
               "the full session so far, not a live premarket read")
            + ("; weekend, stale data" if now.weekday() >= 5 else "")),
        "scan_params": {
            "gap_filter_abs_pct": GAP_MIN, "price_min": PRICE_MIN,
            "top_n": TOP_N,
            "open_note": "before 09:30 ET the latest premarket price "
                         "stands in for the official open in swing checks",
        },
        "criteria": {
            "day_trading": "Trend Join Long selection: gap > 3% vs prev "
                           "close, price > $3, market cap > $1B, premarket "
                           "RVOL > 1.5, price above prior-day high, prev "
                           "close above 200-day SMA. Execution per "
                           "TRADING-STRATEGY.md 2b: trigger over PMH + "
                           "prior HOD 10:00-15:30 ET, stop = signal bar "
                           "low, 3R bracket, flat 15:55.",
            "swing": "Gap >= 8%, price > $3, open above prior-day high, "
                     "open above 200-day SMA, market cap >= $800M, and a "
                     "real catalyst (earnings on gap day, or news with no "
                     "earnings). Starter ideas only, swing management is "
                     "still being built.",
        },
        "market_snapshot": snapshot,
        "econ_calendar": econ,
        "gappers": gappers,
        "market_news": rss_items[:20],
        "gaps_to_fill": gaps_to_fill,
    }
    save_json(SCANS / f"packet_{today}.json", packet)
    step(f"done: {len(gappers)} gappers, "
         f"{len(econ.get('today', []))} econ events today, "
         f"{len(rss_items[:20])} market headlines")


if __name__ == "__main__":
    main()
