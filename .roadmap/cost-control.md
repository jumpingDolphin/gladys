# Ops & Cost Control

> Applied alongside all phases.

## Overview

Gladys uses multiple pay-per-token APIs (Anthropic, Google, Deepseek, OpenAI Whisper). Without monitoring and guardrails, costs can grow silently — especially with concurrent sub-agents or long-running sessions. This doc covers quota monitoring, cost guardrails, model routing, and gateway health.

References: [openclaw-runbook/guide.md](https://github.com/digitalknk/openclaw-runbook/blob/main/guide.md), [check-quotas.sh](https://github.com/digitalknk/openclaw-runbook/blob/main/examples/check-quotas.sh).

## API Quota Monitoring

Adapt the runbook's `check-quotas.sh` for Linux/VPS (strip macOS Keychain, read from `openclaw/credentials/`). Run via systemd timer (daily). Have Gladys report daily spend via Telegram, alert when approaching limits.

- [ ] `scripts/check-quotas.sh` adapted and working
- [ ] Systemd timer runs daily
- [ ] Gladys reports spend via Telegram

## Cost Guardrails

Configure concurrency limits to prevent runaway costs:
```json
"maxConcurrent": 4,
"subagents": { "maxConcurrent": 8 }
```

Enable session compaction at 40k tokens to flush to daily memory files (saves token costs on long conversations).

- [ ] Concurrency limits set in `openclaw.json`
- [ ] Session compaction configured

## Model Routing Optimization

Already using Sonnet 4.5 (primary) with Gemini 3 Flash + Deepseek v3.2 as fallbacks. Consider further optimization: route simple classification/routing tasks to the cheapest fallback model, reserving Sonnet for reasoning-heavy work. Per the [runbook guide](https://github.com/digitalknk/openclaw-runbook/blob/main/guide.md): "Route expensive models away from default coordinator loops."

- [ ] Coordinator model configured (cheapest model for routing)
- [ ] Verified Sonnet only invoked for reasoning tasks

## Gateway Health Monitoring

Lightweight systemd timer that pings gateway, alerts via Telegram if unresponsive.

- [ ] Health check script at `scripts/health-check.sh`
- [ ] Systemd timer runs every 5 min
- [ ] Alerts arrive in Telegram on failure

## Built-in Diagnostics & OpenTelemetry

**OpenClaw has native cost/usage telemetry via OpenTelemetry.** Every model run emits structured diagnostics events with tokens, cost, duration, and context size. These can be exported to any OTLP-compatible collector/backend (Prometheus, Grafana, Jaeger, etc.).

### What's Tracked

**Metrics (counters + histograms):**
- `openclaw.tokens` — token usage by type (input/output/cache_read/cache_write/total)
- `openclaw.cost.usd` — cost per run (channel/provider/model)
- `openclaw.run.duration_ms` — model run latency
- `openclaw.context.tokens` — context size distribution
- Message flow: webhooks received/processed/errors, queue depth/wait time, session state transitions

**Traces (spans):**
- `openclaw.model.usage` — full token breakdown + cost per model invocation
- `openclaw.webhook.processed` — webhook processing spans
- `openclaw.message.processed` — message handling spans with outcome/session/channel

**Logs (optional OTLP export):**
- Structured JSON logs can be exported via OTLP alongside metrics/traces

### How to Enable

1. **Enable diagnostics:**
```json
{
  "diagnostics": {
    "enabled": true
  }
}
```

2. **Enable OTLP exporter plugin:**
```json
{
  "plugins": {
    "allow": ["diagnostics-otel"],
    "entries": {
      "diagnostics-otel": {
        "enabled": true
      }
    }
  },
  "diagnostics": {
    "enabled": true,
    "otel": {
      "enabled": true,
      "endpoint": "http://localhost:4318",
      "protocol": "http/protobuf",
      "serviceName": "openclaw-gateway",
      "traces": true,
      "metrics": true,
      "logs": false,
      "sampleRate": 1.0,
      "flushIntervalMs": 60000
    }
  }
}
```

3. **Set up OTLP collector** (e.g., Prometheus + Grafana for metrics, Jaeger for traces)

### Actionable Insights

With diagnostics enabled, you can:
- **Track daily/weekly spend** by model, channel, or session
- **Alert on cost spikes** (e.g., >$5 in one hour)
- **Identify expensive sessions** (long-running contexts, repeated tool calls)
- **Optimize model routing** (if Sonnet costs spike, route more to Gemini/Deepseek)
- **Monitor queue/webhook health** for gateway stability

### Tasks

- [ ] Enable diagnostics in `openclaw.json`
- [ ] Set up local OTLP collector (Docker Compose with Prometheus + Grafana)
- [ ] Create Grafana dashboards for cost/tokens/latency
- [ ] Set up alerting for cost thresholds (e.g., >$2/day)
- [ ] Document dashboard setup in `docs/monitoring.md`

See: `/usr/lib/node_modules/openclaw/docs/logging.md` (Diagnostics + OpenTelemetry section)

## Lightweight Monitoring Alternatives

**For simpler setups without full observability infrastructure:**

### OpenClaw Cost Monitor (Open Source)
**Repo:** https://github.com/bokonon23/clawdbot-cost-monitor  
**License:** MIT  
**Type:** Local dashboard (no external servers)

**What it does:**
- Parses local JSONL session files (`~/.openclaw/agents/main/sessions/*.jsonl`)
- Beautiful web dashboard at http://localhost:3939
- Shows lifetime costs, token usage, prompt caching savings
- Per-model cost breakdown, 7-day history charts
- Real-time updates every 30 seconds

**Security:**
- Fully local, no telemetry or data exfiltration
- Only dependencies: Express (web server) + ws (WebSocket)
- Read-only access to session files

**Setup:** `git clone` + `npm install` + `npm start` (30 seconds)

**Status:** Reviewed 2026-02-11, code audited — safe to use

### Built-in `/usage` Commands
- `/status` — shows session tokens + estimated cost for last reply
- `/usage full` — appends token+cost footer to every reply
- `/usage tokens` — token counts only
- `openclaw status --usage` — CLI provider quota snapshots

**Decision:** Use built-in `/usage full` for immediate visibility, evaluate OpenClaw Cost Monitor for historical analysis when needed.

## Open Questions

- What monthly budget threshold should trigger alerts? (e.g., 80% of a $50/month cap)
- How often should spend reports go to Telegram? (daily summary vs. real-time alerts on spikes)
- Should per-model spend be tracked separately, or just aggregate API cost?
