# Gladys — Roadmap

## High Priority

1. **Security hardening** — restrict DM policy, remove wildcard allowlists, systemd hardening, tool policies → [`.roadmap/security.md`](.roadmap/security.md)
2. **Cost monitoring & guardrails** — API quota tracking, spend alerts, model routing optimization → [`.roadmap/cost-control.md`](.roadmap/cost-control.md)
3. **Backup & restore** — differential backup of `openclaw/` to Google Drive (15 GB free on bot account) → [`.roadmap/backup.md`](.roadmap/backup.md)
4. ~~**Secrets management**~~ — **Done.** Secrets in `openclaw/.env` with `${VAR}` substitution; `.gitignore` organized with secrets map; gitleaks clean on git history
5. **Evaluate OpenRouter** — model routing alternative for cost/flexibility
6. **Document skills & tools** — audit available but unconfigured skills (`openclaw skills list`), document active ones

## Medium Priority

- **Daily brief** — morning Telegram summary (tasks, yesterday recap, Swiss news) → [`.roadmap/daily-brief.md`](.roadmap/daily-brief.md)

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

## Open Decisions

| # | Decision | Status |
|---|----------|--------|
| 1 | ~~Media backup strategy~~ | **Decided:** Google Drive differential backup (see `.roadmap/backup.md`) |
| 2 | Tool exec policy | Deny `exec` globally vs. allow for trusted agent only |
| 3 | OpenRouter evaluation | Pending — assess cost savings and model routing benefits |

## Principles

1. **No silent side effects** — every action the agent takes is reported back.
2. **Clear separation** — models by capability, state vs. memory, local vs. deployed.
3. **Context survives across days.**
