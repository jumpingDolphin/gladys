# Gladys — Roadmap

## High Priority

1. **Security hardening** — restrict DM policy, remove wildcard allowlists, systemd hardening, tool policies → [`security.md`](security.md)
2. **Cost monitoring & guardrails** — API quota tracking, spend alerts, model routing optimization → [`cost-control.md`](cost-control.md)
3. **Backup & restore** — differential backup of `openclaw/` to Google Drive (15 GB free on bot account) → [`backup.md`](backup.md)
4. ~~**Secrets management**~~ — **Done.** Secrets in `openclaw/.env` with `${VAR}` substitution; `.gitignore` organized with secrets map; gitleaks clean on git history
5. **Evaluate OpenRouter** — model routing alternative for cost/flexibility
6. **Document skills & tools** — audit available but unconfigured skills (`openclaw skills list`), document active ones

## Medium Priority

- **Daily brief** — morning Telegram summary (tasks, yesterday recap, Swiss news) → [`daily-brief.md`](daily-brief.md)

## Low Priority

### Restic Backups
**Status:** Documented, not implemented
**Why:** Space-efficient incremental backups via deduplication
**Current:** Full tar backups every 2 days (~32MB, works fine)
**With restic:** Only upload changed data, snapshot-based restore, better for frequent backups
**Setup:** Install restic, configure rclone for Google Drive backend, migrate from tar script
**Worth it when:** Workspace grows significantly (100MB+) or backup frequency increases

## Integrations

| Integration | Status | Notes |
|-------------|--------|-------|
| Telegram (text + voice) | Active | Primary interface |
| Claude Sonnet 4.5 | Active | Primary reasoning model |
| Gemini 3 Flash | Active | Fallback model |
| Deepseek v3.2 | Active | Fallback model |
| Whisper (OpenAI) | Active | Voice transcription at channel layer |
| Todoist | Active | Task management |
| Notion | Active | Structured databases, projects |
| Google Docs | Active | Narrative artifacts |
| Google Drive | Active | File storage |
| Gmail | Active | Email |
| Google Calendar | Untested | OAuth configured, not yet validated |
| Google Sheets | Untested | OAuth configured, not yet validated |
| Brave Search | Active | Web search |
| DALL-E (OpenAI) | Active | Image generation |
| Transcription Bot | Active | Second agent — Claude Sonnet 4.5, dedicated Telegram bot for voice→text (transcribe skill) |

## Open Decisions

| # | Decision | Status |
|---|----------|--------|
| 1 | ~~Media backup strategy~~ | **Decided:** Google Drive differential backup (see [`backup.md`](backup.md)) |
| 2 | Tool exec policy | Deny `exec` globally vs. allow for trusted agent only |
| 3 | OpenRouter evaluation | Pending — assess cost savings and model routing benefits |

## Principles

1. **No silent side effects** — every action the agent takes is reported back.
2. **Clear separation** — models by capability, state vs. memory, local vs. deployed.
3. **Context survives across days.**

---

## Completed

### Encrypted Backups to Google Drive
**Completed:** 2026-02-11
Full encrypted tar backups every 2 days, uploaded to Google Drive, automated via cron.

### Transcription Bot (Second Agent)
**Completed:** 2026-02-12
Dedicated Telegram bot for voice transcription. Second OpenClaw agent using Claude Sonnet 4.5 with the `transcribe` skill — Whisper STT handles audio-to-text at channel layer, Sonnet outputs clean copy-ready text + enhanced reformulation. No memory, no heartbeat.

### Credentials Audit
**Completed:** 2026-02-11
Verified all API keys and OAuth tokens after .env reorganization.
