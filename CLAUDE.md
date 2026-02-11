# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Gladys is a personal AI assistant built on [OpenClaw](https://openclaw.dev), accessed via Telegram (text + voice), with Claude Sonnet 4.5 as the primary reasoning model (Gemini 3 Flash and Deepseek v3.2 as fallbacks). It runs on a bare metal Hetzner VPS (no Docker) at `gladys.simonschenker.com`.

## Key Architectural Concept

This repo (`~/gladys`) contains project files at the root. OpenClaw state lives in the `openclaw/` subfolder (`OPENCLAW_STATE_DIR=~/gladys/openclaw`), keeping a clear separation between project files (scripts, docs, config) and OpenClaw-generated files (agents, sessions, credentials).

## How OpenClaw Works

OpenClaw is an open-source AI agent framework. The **gateway** is a Node.js process that:
1. Receives messages from **channels** (Telegram, Discord, etc.)
2. Routes them to an **agent** (Claude Sonnet 4.5) with access to **skills** (tools)
3. Maintains **memory** across sessions via workspace files and SQLite vector search
4. Runs as a systemd user service, configured via `openclaw.json`

Key concepts:
- **Skills** are tool plugins (Todoist, Notion, Gmail, etc.) installed via `openclaw skills install` or ClawHub
- **Heartbeats** are periodic polls that let the agent do proactive work (check email, calendar, etc.)
- **Memory** persists via markdown files (`MEMORY.md` for long-term, `memory/YYYY-MM-DD.md` for daily)
- **Config** uses `${VAR}` substitution — secrets live in `openclaw/.env`, not in `openclaw.json`

For the full OpenClaw ecosystem (skills, plugins, community projects, deployment options), see `openclaw/workspace/openclaw-resources.md`.

## Architecture

```
Telegram (text/voice)
        |
        v
 OpenClaw Gateway (port 18789, loopback only, token auth)
        |
        |-- Channel layer: Telegram adapter
        |     \-- Whisper STT (voice -> text)
        |
        |-- Agent: Claude Sonnet 4.5 (primary reasoning)
        |     |-- Todoist skill (tasks)
        |     |-- Notion skill (databases, projects)
        |     |-- Google skill (Docs, Drive, Gmail, Calendar, Sheets, Places)
        |     |-- Web search (Brave)
        |     \-- Image generation (OpenAI DALL-E)
        |
        |-- Fallback models: Gemini 3 Flash, Deepseek v3.2
        |
        \-- Memory subsystem
              |-- MEMORY.md (durable facts, curated)
              |-- memory/YYYY-MM-DD.md (daily context, raw)
              \-- SQLite vector index (semantic search)
```

## OpenClaw Workspace Files

The agent's personality, behavior, and knowledge are defined by markdown files in `openclaw/workspace/`. These are read by the agent at session start and define who Gladys is:

| File | Purpose |
|------|---------|
| `IDENTITY.md` | Name, persona (GlaDOS-inspired dry wit), security rules |
| `SOUL.md` | Personality guide — Pratchett-dry humor, opinionated, competent-not-cheerful |
| `AGENTS.md` | Session boot sequence, memory protocol, safety rules, heartbeat behavior, group chat etiquette |
| `USER.md` | Simon's profile (timezone, preferences, professional background) |
| `MEMORY.md` | Curated long-term memory (distilled from daily notes) |
| `CONTACTS.md` | Known people directory |
| `TOOLS.md` | Environment-specific tool notes (API project IDs, OAuth setup, Todoist config) |
| `HEARTBEAT.md` | Proactive task checklist (calendar checks, etc.) |
| `openclaw-resources.md` | OpenClaw ecosystem reference (docs, skills, community projects) |

Skills live in `openclaw/workspace/skills/<skill-name>/` with their own `SKILL.md`, `scripts/`, and `references/`.

## Secrets Management

Secrets are centralized in `openclaw/.env` (chmod 600), loaded via `${VAR}` substitution in `openclaw.json` and via systemd `EnvironmentFile` drop-in. See `.env.example` for the full template and a map of all secret file locations.

| Secret type | Location | Managed by |
|-------------|----------|------------|
| API keys (gateway, Telegram, Brave, Notion, OpenAI, Google Maps, Todoist) | `openclaw/.env` | Manual edit + gateway restart |
| Backup passphrase | `openclaw/.env` (`BACKUP_PASSPHRASE`) | Manual edit + gateway restart |
| Model keys (Anthropic, Gemini) | `openclaw/agents/main/agent/auth-profiles.json` | `openclaw models auth` |
| Google OAuth (client creds + tokens) | `openclaw/workspace/google_credentials.json`, `google_token.json` | Google OAuth flow |
| Device identity | `openclaw/identity/`, `openclaw/devices/` | OpenClaw internal |

All secret files are gitignored. See `.gitignore` for the full organized inventory.

## OpenClaw Commands

```bash
openclaw onboard          # Interactive config wizard (generates openclaw.json)
openclaw doctor           # Health check (reports issues, doesn't fix all)
openclaw doctor --repair  # Apply recommended fixes (config, service unit)
openclaw gateway start    # Launch gateway server
openclaw gateway install --force  # Reinstall systemd unit with correct paths
openclaw models status    # Verify active models
openclaw models auth      # Manage model API keys (writes auth-profiles.json)
openclaw skills list      # List installed skills
openclaw security audit   # Verify security settings
```

The gateway runs as a systemd user service (`openclaw-gateway.service`). Manage with:
```bash
systemctl --user start openclaw-gateway
systemctl --user status openclaw-gateway
systemctl --user restart openclaw-gateway
journalctl --user -u openclaw-gateway --since "5 min ago" --no-pager  # check logs
```

### Doctor caveats

Doctor does **not** auto-fix: state dir permissions (`chmod 700 openclaw/`), missing `credentials/` dir (`mkdir openclaw/credentials`), or stale `~/.openclaw` dir. Also, `doctor --repair` and `gateway install --force` regenerate the main systemd unit file, but **not** drop-in overrides (which is where `EnvironmentFile` and hardening directives live — by design).

## Configuration Management

**Always check OpenClaw documentation for configuration wizards before directly editing config files.** OpenClaw provides CLI commands (`openclaw onboard`, `openclaw doctor --repair`, etc.) that properly handle configuration with validation, templating, and secret management. Direct edits to `openclaw.json` or `auth-profiles.json` bypass these safeguards and may introduce errors or security issues.

When configuration changes are needed:
1. First check `openclaw --help` and relevant subcommand help for built-in wizards
2. Use the official OpenClaw commands when available
3. Only edit config files directly as a last resort, and document why

## VPS Deployment

`scripts/setup.sh` is an idempotent bootstrap script (safe to re-run) that provisions the VPS: creates user, hardens SSH, configures UFW, installs Node.js 22.x + OpenClaw + Claude Code, clones the repo, sets up systemd service. See README.md for the full setup workflow.

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Docker vs. bare metal | **Bare metal** | Single user, less overhead, simpler debugging on small VPS |
| Repo structure | **OpenClaw state in subfolder** | `OPENCLAW_STATE_DIR=~/gladys/openclaw` — clear separation between project files and OpenClaw-generated files |
| Google account strategy | **Dedicated agent account** (`simons.gladys.bot@gmail.com`) | Single OAuth flow for Gmail API, Drive, and Docs; isolates agent from personal files |
| Task management | **Todoist** + **Notion** | Todoist for quick tasks; Notion for structured databases and projects |
| STT backend | **Built-in OpenClaw Whisper** | Handled at the channel layer, no custom setup needed |
| Primary model | **Claude Sonnet 4.5** with Gemini 3 Flash + Deepseek v3.2 fallbacks | Cost/speed tradeoff; Opus 4.6 unnecessary for most interactions |
| Secrets strategy | **`openclaw/.env`** with `${VAR}` substitution | Centralized, gitignored, systemd drop-in survives config regeneration |

## Current Priorities

See `openclaw/workspace/roadmap/` for the full priority-based roadmap. Top items:

1. Security hardening (P1 items remaining) → `openclaw/workspace/roadmap/security.md`
2. Cost monitoring & guardrails → `openclaw/workspace/roadmap/cost-control.md`
3. Backup & restore (Google Drive) → `openclaw/workspace/roadmap/backup.md`
4. Document skills & tools

## Git Conventions

- **Never add `Co-Authored-By` lines to commit messages.**

## Design Principles

1. **No silent side effects** — every agent action is reported back to the user.
2. **Clear separation** — models by capability, state vs. memory, local vs. deployed.
3. **Context survives across days.**

## Security Model

- Gateway binds to loopback only with token auth, mDNS disabled
- SSH key-only auth, root login disabled, UFW rate-limits port 22
- Systemd hardening drop-ins: NoNewPrivileges, PrivateTmp, ProtectSystem=strict
- Secrets in `openclaw/.env` (600 perms), `openclaw/` dir 700
- Telegram DM restricted to allowlist (Simon's user ID only)
- Git history clean (verified by gitleaks); all secret files gitignored

## Key Files

| File | Purpose |
|------|---------|
| `openclaw/workspace/roadmap/` | Roadmap index + detailed planning docs (security, cost control, backup, daily brief, integrations) |
| `.env.example` | Secrets template + map of all secret file locations |
| `.gitignore` | Organized inventory: secrets, runtime state, workspace (with comments) |
| `scripts/setup.sh` | VPS bootstrap script (idempotent) |
| `openclaw/` | OpenClaw state dir (`OPENCLAW_STATE_DIR`), generated by `openclaw onboard` |
| `openclaw/openclaw.json` | OpenClaw config (uses `${VAR}` refs, gitignored) |
| `openclaw/.env` | Central secrets file (gitignored, 600 perms) |
| `openclaw/workspace/` | Agent definition files (see "OpenClaw Workspace Files" above) |
| `openclaw/workspace/openclaw-resources.md` | OpenClaw ecosystem reference |
