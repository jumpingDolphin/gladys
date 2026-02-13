#!/usr/bin/env python3
"""
OpenClaw Cost Analyzer
Parses session JSONL files, prints a text summary, and generates a PNG chart.

Usage:
  python3 cost-analyzer.py              # last 30 days
  python3 cost-analyzer.py --days 7     # last 7 days
  python3 cost-analyzer.py --png        # also generate PNG chart
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import argparse

AGENTS_DIR = Path.home() / "gladys" / "openclaw" / "agents"
OUTPUT_DIR = Path.home() / "gladys" / "openclaw" / "workspace" / "output"


def parse_sessions(days):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    daily = defaultdict(lambda: {"cost": 0.0, "input": 0, "output": 0, "cache_read": 0})
    by_model = defaultdict(float)
    by_agent = defaultdict(float)

    for agent_dir in AGENTS_DIR.iterdir():
        if not agent_dir.is_dir():
            continue
        agent_name = agent_dir.name
        sessions_dir = agent_dir / "sessions"
        if not sessions_dir.exists():
            continue

        for jsonl_file in sessions_dir.glob("*.jsonl"):
            with open(jsonl_file) as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    if entry.get("type") != "message":
                        continue

                    ts = entry.get("timestamp")
                    msg = entry.get("message", {})
                    usage = msg.get("usage")
                    model = msg.get("model")

                    if not ts or not usage or not model or model == "delivery-mirror":
                        continue

                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    if dt < cutoff:
                        continue

                    cost = 0.0
                    if isinstance(usage.get("cost"), dict):
                        cost = usage["cost"].get("total", 0.0) or 0.0

                    date_str = dt.strftime("%Y-%m-%d")
                    daily[date_str]["cost"] += cost
                    daily[date_str]["input"] += usage.get("input", 0) or 0
                    daily[date_str]["output"] += usage.get("output", 0) or 0
                    daily[date_str]["cache_read"] += usage.get("cacheRead", 0) or 0
                    by_model[model] += cost
                    by_agent[agent_name] += cost

    return daily, by_model, by_agent


def print_summary(daily, by_model, by_agent, days):
    if not daily:
        print("No usage data found.")
        return

    dates = sorted(daily.keys())
    total = sum(d["cost"] for d in daily.values())
    avg = total / len(dates) if dates else 0

    print(f"Cost summary (last {days} days)")
    print(f"{'=' * 40}")
    print(f"Total:   ${total:.2f}")
    print(f"Daily avg: ${avg:.2f}")
    print(f"Period:  {dates[0]} to {dates[-1]}")
    print()

    print("By model:")
    for model, cost in sorted(by_model.items(), key=lambda x: -x[1]):
        print(f"  {model:40s} ${cost:.2f}")
    print()

    if len(by_agent) > 1:
        print("By agent:")
        for agent, cost in sorted(by_agent.items(), key=lambda x: -x[1]):
            print(f"  {agent:40s} ${cost:.2f}")
        print()

    print("Daily breakdown:")
    for date in dates:
        d = daily[date]
        tokens = d["input"] + d["output"] + d["cache_read"]
        print(f"  {date}  ${d['cost']:7.2f}  ({tokens:,} tokens)")


def generate_png(daily, by_model, days):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    dates = sorted(daily.keys())
    if not dates:
        return None

    date_objs = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
    costs = [daily[d]["cost"] for d in dates]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={"width_ratios": [2, 1]})
    fig.suptitle(f"OpenClaw costs — last {days} days (total: ${sum(costs):.2f})", fontsize=13, fontweight="bold")

    # Daily cost bars
    ax1.bar(date_objs, costs, color="#4a90d9", alpha=0.85, width=0.8)
    ax1.set_ylabel("USD")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax1.tick_params(axis="x", rotation=45)
    ax1.set_xlim(date_objs[0] - timedelta(hours=12), date_objs[-1] + timedelta(hours=12))

    # Model breakdown donut
    models = sorted(by_model.items(), key=lambda x: -x[1])
    labels = [m.replace("claude-", "").replace("-20250929", "") for m, _ in models]
    values = [c for _, c in models]
    colors = ["#4a90d9", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c"]
    wedges, texts, autotexts = ax2.pie(
        values, labels=labels, autopct=lambda p: f"${p * sum(values) / 100:.2f}",
        colors=colors[: len(values)], startangle=90, textprops={"fontsize": 9},
    )
    for t in autotexts:
        t.set_fontsize(8)
    ax2.set_title("By model", fontsize=11)

    plt.tight_layout()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "cost-report.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    return out_path


def main():
    parser = argparse.ArgumentParser(description="OpenClaw cost analyzer")
    parser.add_argument("--days", type=int, default=30, help="Number of days to analyze (default: 30)")
    parser.add_argument("--png", action="store_true", help="Generate a PNG chart")
    args = parser.parse_args()

    daily, by_model, by_agent = parse_sessions(args.days)
    print_summary(daily, by_model, by_agent, args.days)

    if args.png:
        path = generate_png(daily, by_model, args.days)
        if path:
            print(f"\nChart saved to: {path}")


if __name__ == "__main__":
    main()
