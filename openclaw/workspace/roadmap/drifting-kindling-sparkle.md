# Plan: Cost Monitoring for Gladys

## Context

Gladys uses multiple pay-per-token APIs (Anthropic, Google/Deepseek via OpenRouter, OpenAI for Whisper/DALL-E). There's no visibility into actual spend today — costs grow silently. The roadmap lists this as **#2 priority** but nothing is implemented beyond basic guardrails (concurrency limits, context pruning). Budget target: **$50/month**.

## What Exists Today

| Layer | Status |
|-------|--------|
| Concurrency limits (`maxConcurrent: 4`, subagents: 8) | Active |
| Context pruning (cache-ttl 60m, safeguard compaction) | Active |
| `/usage` commands (`/usage full`, `/status`) | Available, not enabled |
| OpenTelemetry support (built into OpenClaw) | Not needed — skip Prometheus/Grafana |
| Cost Monitor dashboard (parses session JSONL) | Audited safe, not installed |
| Session JSONL data (8MB across multiple sessions) | Exists, ready to parse |

## Phase 1: Visibility (implement now)

### 1. Install OpenClaw Cost Monitor dashboard

- Clone `bokonon23/clawdbot-cost-monitor` to `~/gladys/tools/cost-monitor/`
- `npm install`
- Configure to read from `~/gladys/openclaw/agents/main/sessions/`
- Create systemd user service, bind to `127.0.0.1:3939`
- Enable and start

**Files created:**
- `~/.config/systemd/user/cost-monitor.service`

**Verification:** `curl http://localhost:3939` returns dashboard, `systemctl --user status cost-monitor` shows active

### 2. Write `scripts/check-quotas.sh`

Adapt from the [openclaw-runbook example](https://github.com/digitalknk/openclaw-runbook/blob/main/examples/check-quotas.sh). Query API usage endpoints:

- **Anthropic:** `GET https://api.anthropic.com/v1/usage` (API key from `.env`)
- **OpenRouter:** `GET https://openrouter.ai/api/v1/auth/key` (returns credits/usage)
- **OpenAI:** `GET https://api.openai.com/v1/usage` (Whisper + DALL-E)

Output: today's spend, month-to-date total, per-provider breakdown, % of $50 budget used.

**File:** `scripts/check-quotas.sh`

**Verification:** Run manually, confirm it outputs spend data

### 3. Enable `/usage full` for Gladys

Add a note to `openclaw/workspace/TOOLS.md` documenting the `/usage` commands so Gladys knows to report costs when asked. (The `/usage full` toggle is a per-session runtime command — Gladys can enable it when a user asks about costs.)

**File:** `openclaw/workspace/TOOLS.md` (minor addition)

## Phase 2: Automated Alerts (implement after Phase 1 is verified)

### 4. Systemd timer for daily spend report

- Create `~/.config/systemd/user/check-quotas.timer` — runs `check-quotas.sh` daily at 08:00
- Script sends summary to Telegram via the gateway API (or writes to a file Gladys reads)

**Files created:**
- `~/.config/systemd/user/check-quotas.service`
- `~/.config/systemd/user/check-quotas.timer`

### 5. Budget threshold alerts in check-quotas.sh

Add percentage-based thresholds to the script:
- **50%** ($25): info message to Telegram ("halfway through monthly budget")
- **80%** ($40): warning ("approaching budget limit")
- **100%** ($50): alert ("budget exceeded")

Track month-to-date spend in a simple state file (`/tmp/openclaw/spend-state.json`) to avoid duplicate alerts for the same threshold.

### 6. Add cost check to Gladys's heartbeat

Update `openclaw/workspace/HEARTBEAT.md` — add daily cost report to the morning proactive task list so Gladys includes spend in her morning routine.

**File:** `openclaw/workspace/HEARTBEAT.md`

## Housekeeping

- Update `openclaw/workspace/roadmap/cost-control.md` — check off completed items
- Update `openclaw/workspace/TOOLS.md` — document Cost Monitor dashboard

## Files Summary

| File | Action |
|------|--------|
| `scripts/check-quotas.sh` | Create |
| `~/.config/systemd/user/cost-monitor.service` | Create |
| `~/.config/systemd/user/check-quotas.service` | Create (Phase 2) |
| `~/.config/systemd/user/check-quotas.timer` | Create (Phase 2) |
| `openclaw/workspace/TOOLS.md` | Edit (add cost monitoring docs) |
| `openclaw/workspace/HEARTBEAT.md` | Edit (add cost check task, Phase 2) |
| `openclaw/workspace/roadmap/cost-control.md` | Edit (update status) |
