# Plan: Cost Monitoring Skill

## Context

Gladys uses multiple pay-per-token APIs (Anthropic, Deepseek via OpenRouter, OpenAI for Whisper/DALL-E) with no visibility into actual spend. Budget target: **$50/month**. The session JSONL files already contain per-message cost breakdowns in USD — we just need a skill that lets Gladys parse and report them.

**Approach:** Build a native OpenClaw skill (no external dashboards or tools to install). Gladys can query her own costs on demand and report via Telegram.

## What Already Exists

- **Session JSONL files** (`openclaw/agents/main/sessions/*.jsonl`) — each assistant message includes `usage.cost.total` in USD, plus per-type breakdown (input/output/cacheRead/cacheWrite), provider, and model
- **8MB of session data** across multiple files, ready to parse
- **OpenRouter `/api/v1/key`** endpoint — returns credits remaining for the current key (uses existing API key, no admin key needed)
- **Concurrency limits + context pruning** — already active in `openclaw.json`
- **Built-in `/usage full`** — per-session runtime toggle, already available

**Not viable without extra setup:** Anthropic's Usage API requires a separate Admin API key (sk-ant-admin). Not worth it — JSONL already has Anthropic costs.

## Skill: `cost-monitoring`

### Structure

```
openclaw/workspace/skills/cost-monitoring/
├── SKILL.md
└── scripts/
    └── cost_report.py
```

### `scripts/cost_report.py`

Single Python script that parses session JSONL files and outputs a cost report.

**What it does:**
1. Scans all `*.jsonl` files in `openclaw/agents/main/sessions/`
2. Extracts `usage.cost.total`, `provider`, `model`, and timestamp from each assistant message
3. Aggregates by time period (today, this week, this month) and by provider/model
4. Compares month-to-date spend against $50 budget (configurable via env var or argument)
5. Outputs a formatted text report suitable for Telegram

**Arguments:**
- `--period today|week|month|all` (default: month)
- `--budget 50` (default: $50, overridable)
- `--json` flag for machine-readable output

**Output example:**
```
Cost Report — February 2026

Month-to-date: $12.45 / $50.00 (24.9%)
Today: $1.82

By provider:
  Anthropic (claude-sonnet-4-5): $11.20
  OpenRouter (deepseek-v3.2):    $0.85
  OpenRouter (gemini-3-flash):   $0.40

Budget status: ✓ On track
```

**Budget alerts** — when Gladys runs this (via heartbeat or on demand), the output includes clear threshold warnings:
- <50%: "On track"
- 50-79%: "Halfway through budget"
- 80-99%: "Approaching budget limit"
- ≥100%: "Budget exceeded"

### `SKILL.md`

Following the pattern from backup-restore and todoist-task-manager:
- YAML frontmatter (name, description)
- Quick start with script path and example usage
- Describes when to use it (on demand, during heartbeat)
- Documents output format

### Heartbeat integration

Add a cost check to `openclaw/workspace/HEARTBEAT.md` so Gladys runs the report during her morning routine and proactively warns if spend is high.

## Files to Create/Edit

| File | Action |
|------|--------|
| `openclaw/workspace/skills/cost-monitoring/SKILL.md` | Create |
| `openclaw/workspace/skills/cost-monitoring/scripts/cost_report.py` | Create |
| `openclaw/workspace/HEARTBEAT.md` | Edit — add daily cost check |
| `openclaw/workspace/roadmap/cost-control.md` | Edit — update status |

## Verification

1. Run `python3 openclaw/workspace/skills/cost-monitoring/scripts/cost_report.py` — confirm it outputs spend data from existing sessions
2. Run with `--period today` and `--json` to verify both modes
3. Ask Gladys via Telegram "how much have you cost me this month?" — she should use the skill
4. Check heartbeat picks up the cost check on next cycle
