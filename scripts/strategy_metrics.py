#!/usr/bin/env python3
"""strategy_metrics.py — full performance metrics from a backtest JSON.

Usage: python3 scripts/strategy_metrics.py scans/backtest_<...>.json

Reads the per-trade R records saved by backtest_tjl.py (key `r_multiple`)
or backtest_crypto.py (key `net_r`) and prints the desk's standard metric
set: win rate, avg win/loss, profit factor, expectancy, max drawdown (R),
per-trade + annualized Sharpe, Sortino, and a 95% bootstrap CI on the
expectancy so small samples can't oversell themselves. Stdlib only.

Sharpe here is computed on R-multiples per trade, then annualized by
sqrt(trades/year) — an estimate that assumes independent trades. Treat
any Sharpe from <100 trades as a rough gauge, not a promise.
"""
import json
import math
import random
import statistics
import sys
from datetime import datetime


def trade_r(t):
    for k in ("net_r", "r_multiple", "gross_r"):
        if k in t:
            return float(t[k])
    raise KeyError(f"no R key in trade record: {list(t)}")


def trade_date(t):
    for k in ("exit_time", "entry_time", "date"):
        if k in t and t[k]:
            return datetime.fromisoformat(str(t[k]).replace("Z", "+00:00").split("+")[0])
    return None


def max_drawdown_r(rs):
    peak = equity = dd = 0.0
    for r in rs:
        equity += r
        peak = max(peak, equity)
        dd = max(dd, peak - equity)
    return dd


def bootstrap_ci(rs, n_iter=10000, seed=42):
    rng = random.Random(seed)
    n = len(rs)
    means = sorted(sum(rng.choices(rs, k=n)) / n for _ in range(n_iter))
    return means[int(0.025 * n_iter)], means[int(0.975 * n_iter)]


def main(path):
    with open(path) as f:
        data = json.load(f)
    trades = data["trades"]
    rs = [trade_r(t) for t in trades]
    n = len(rs)
    if n == 0:
        print("no trades in file")
        return

    wins = [r for r in rs if r > 0]
    losses = [r for r in rs if r <= 0]
    win_rate = len(wins) / n
    gross_win = sum(wins)
    gross_loss = -sum(losses)
    pf = gross_win / gross_loss if gross_loss else math.inf
    expectancy = sum(rs) / n

    mean = expectancy
    sd = statistics.stdev(rs) if n > 1 else float("nan")
    sharpe_trade = mean / sd if sd and sd > 0 else float("nan")

    downside = [min(r, 0.0) for r in rs]
    dsd = math.sqrt(sum(d * d for d in downside) / n)
    sortino_trade = mean / dsd if dsd > 0 else math.inf

    dates = [d for d in (trade_date(t) for t in trades) if d]
    years = None
    if len(dates) >= 2:
        span_days = (max(dates) - min(dates)).days
        years = max(span_days / 365.25, 1 / 365.25)
    tpy = n / years if years else None
    ann = math.sqrt(tpy) if tpy else None

    lo, hi = bootstrap_ci(rs)

    print(f"file:              {path}")
    print(f"trades:            {n}" + (f"  (~{tpy:.0f}/yr over {years:.1f}y)" if tpy else ""))
    print(f"win rate:          {win_rate * 100:.1f}%")
    print(f"avg win / loss:    +{(gross_win / len(wins)) if wins else 0:.2f}R / "
          f"{(sum(losses) / len(losses)) if losses else 0:.2f}R")
    print(f"profit factor:     {pf:.2f}")
    print(f"expectancy:        {expectancy:+.3f}R per trade  (net {sum(rs):+.2f}R)")
    print(f"expectancy 95% CI: [{lo:+.3f}R, {hi:+.3f}R] per trade (bootstrap)")
    print(f"max drawdown:      {max_drawdown_r(rs):.2f}R")
    print(f"Sharpe (per-trade):{sharpe_trade:.3f}")
    if ann:
        print(f"Sharpe (annualized ≈ per-trade × √{tpy:.0f}): {sharpe_trade * ann:.2f}")
    print(f"Sortino (per-trade): {sortino_trade:.3f}"
          + (f"  (annualized ≈ {sortino_trade * ann:.2f})" if ann else ""))
    if lo < 0 < hi:
        print("NOTE: expectancy CI includes 0 — the edge is NOT statistically "
              "confirmed at this sample size. Trade small; keep validating.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
