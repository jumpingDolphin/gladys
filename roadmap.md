# Gladys — Personal AI Assistant Roadmap

> An OpenClaw-based personal AI assistant accessed via Telegram (text + voice),
> with Claude as the primary reasoning model, Notion for structured state,
> and Google Docs for narrative memory and artifacts.
>
> **VPS:** Hetzner, bare metal (no Docker), domain: `gladys.simonschenker.com`

---

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Docker vs. bare metal | **Bare metal** | Single user, less overhead, simpler debugging on small VPS |
| Repo structure | **Repo = OpenClaw state dir** | `OPENCLAW_STATE_DIR=~/gladys` — one place for everything |
| Backup strategy | **Git** | `.gitignore` excludes secrets/sessions; `git push` = backup |
| VPS access | **SSH** (Tailscale later if needed) | Telegram bot only needs outbound; dashboard access via SSH tunnel |
| VPS provider | **Hetzner** | — |

---

## Repository & State Directory Layout

This repo (`~/gladys`) doubles as the OpenClaw state directory
(`OPENCLAW_STATE_DIR=~/gladys`). OpenClaw writes its runtime state here;
git tracks the parts worth backing up.

```
~/gladys/                              # git repo AND OPENCLAW_STATE_DIR
├── .env.example                       # secret template (no values)
├── .env                               # actual secrets (gitignored)
├── .gitignore
├── roadmap.md                         # this file
├── openclaw.json                      # config (uses ${ENV_VARS}, no secrets)
├── scripts/
│   └── setup.sh                       # VPS bootstrap: node, openclaw, systemd, ufw
├── agents/
│   └── main/
│       ├── agent/
│       │   ├── IDENTITY.md            # backed up (personality/system prompt)
│       │   └── MEMORY.md              # backed up (durable memory)
│       ├── memory/
│       │   ├── *.md                   # backed up (daily context)
│       │   └── *.sqlite              # gitignored (binary, rebuilt)
│       └── sessions/                  # gitignored (private transcripts)
├── credentials/                       # gitignored (secrets)
├── sandboxes/                         # gitignored (tool sandbox workspaces)
└── extensions/                        # gitignored (installed plugins)
```

### .gitignore

```
.env
credentials/
agents/*/sessions/
**/*.sqlite
sandboxes/
extensions/
```

---

## Prerequisites & API Key Inventory

All secrets live in `.env`, never in config files. OpenClaw's config supports
`${VAR_NAME}` references that resolve from the environment.

| Env Variable | Service | Purpose | Required by |
|--------------|---------|---------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic | Claude Opus 4.6 — primary reasoning model | Phase 1 |
| `TELEGRAM_BOT_TOKEN` | Telegram (via @BotFather) | Chat interface for text + voice | Phase 1 |
| `OPENAI_API_KEY` | OpenAI | Whisper STT (voice transcription), image generation | Phase 2 |
| `NOTION_API_TOKEN` | Notion | Structured state: tasks, projects, priorities | Phase 3 |
| `GOOGLE_APPLICATION_CREDENTIALS` | Google | Google Docs read/write for artifacts | Phase 3 |

> **Decision needed:** For Google integration, OpenClaw recommends creating a
> *separate Google account* so the agent never touches personal files. Decide
> before Phase 3.

---

## Principles

1. **No silent side effects** — every action the agent takes is reported back.
2. **Clear separation** — models by capability, state vs. memory, local vs. deployed.
3. **Each phase is independently testable** with explicit validation criteria.
4. **Context survives across days.**

---

## Architecture Overview

```
Telegram (text/voice)
        |
        v
 OpenClaw Gateway (port 18789, loopback only)
        |
        |-- Channel layer: Telegram adapter
        |     \-- Whisper STT (voice -> text, handled here)
        |
        |-- Agent: Claude Opus 4.6 (all reasoning)
        |     |-- Notion skill (tasks, projects, state)
        |     \-- Google Docs skill (logs, drafts, artifacts)
        |
        \-- Memory subsystem
              |-- MEMORY.md (durable facts)
              |-- memory/YYYY-MM-DD.md (daily context)
              \-- SQLite vector index (semantic search)
```

---

## Phase 0 — VPS Setup

**Goal:** Hetzner VPS is provisioned, secured, and ready for OpenClaw.

### Infrastructure (done)

- [x] Hetzner VPS provisioned
- [x] DNS: `gladys.simonschenker.com` pointed to VPS
- [x] Hetzner Cloud Firewall configured

### Firewall rules (Hetzner Cloud Firewall)

Inbound:

| Protocol | Port | Source | Description |
|----------|------|--------|-------------|
| TCP | 22 | 0.0.0.0/0, ::/0 | SSH |

Outbound: allow all (or explicitly: TCP 443, TCP 80, TCP/UDP 53, ICMP).

If Tailscale is added later: inbound UDP 41641 from 0.0.0.0/0, ::/0.

### VPS bootstrap (TODO)

1. SSH in, create non-root user, disable root login, enable SSH key-only auth.
2. Install Node.js (LTS) and npm.
3. Install OpenClaw: `npm install -g openclaw` (or per OpenClaw install docs).
4. Clone this repo: `git clone <repo-url> ~/gladys`
5. Create `.env` from `.env.example`, fill in API keys.
6. Set environment: `export OPENCLAW_STATE_DIR=~/gladys`
7. Symlink or configure OpenClaw to use `~/gladys/openclaw.json`.
8. Create systemd unit for `openclaw gateway start`.
9. Enable UFW as additional local firewall (`ufw limit 22/tcp && ufw enable`).
10. Verify gateway starts: `openclaw doctor`.

---

## Phase 1 — OpenClaw Baseline

**Goal:** OpenClaw runs on VPS, Telegram text messages work, Claude responds.

### Steps

1. Configure the provider/model section in `openclaw.json`:
   ```json5
   {
     provider: {
       anthropic: { apiKey: "${ANTHROPIC_API_KEY}" }
     },
     agents: {
       defaults: {
         model: { primary: "anthropic/claude-opus-4-6" }
       }
     }
   }
   ```
2. Configure the Telegram channel with bot token.
3. Start the gateway via systemd.
4. Send a text message to the Telegram bot.

### Validate

- [ ] Gateway starts without errors (`openclaw doctor` passes).
- [ ] Telegram text message gets a Claude-generated reply.
- [ ] `openclaw models status` confirms Claude Opus 4.6 is active.

---

## Phase 2 — Voice Transcription

**Goal:** Telegram voice messages are transcribed and processed by Claude.

Voice transcription is handled at the **channel level** — Telegram voice
messages are transcribed to text *before* they reach the Claude agent.
No custom model-routing code is needed.

| STT Option | Pros | Cons |
|------------|------|------|
| **OpenAI Whisper API** | Highest accuracy, no local GPU needed | Requires OpenAI API key, audio leaves machine |
| **Local faster-whisper** | Runs offline, audio stays local | Needs capable hardware, slightly lower accuracy |

> **Decision needed:** Choose STT backend before starting this phase.

### Steps

1. Add the OpenAI API key to config (if using Whisper API).
2. Enable voice transcription in the Telegram channel config.
3. Send a voice message to the bot.

### Validate

- [ ] Voice message is transcribed accurately.
- [ ] Bot confirms what it heard (the transcribed text) before responding.
- [ ] Claude receives and reasons over the transcribed text, not raw audio.

---

## Phase 3 — Memory & State Split

**Goal:** Notion holds structured state; Google Docs holds narrative artifacts.

OpenClaw already handles persistent memory natively. Notion and Google Docs
serve as *external artifact stores*, not as the agent's core memory:

| System | Role | Examples |
|--------|------|----------|
| OpenClaw memory (built-in) | Agent's working memory & recall | What was discussed, preferences, session history |
| Notion | Structured external state | Tasks, projects, reminders, priorities, statuses |
| Google Docs | Narrative external artifacts | Voice logs, notes, drafts, generated documents |

### 3a — Notion Integration

1. Create a Notion integration at <https://www.notion.so/my-integrations>.
2. Share target databases/pages with the integration.
3. Add the API token (use env var, never commit).
4. Test: ask Claude to create a task, verify it appears in Notion.

### 3b — Google Docs Integration

1. Set up a dedicated Google account (recommended) or use personal OAuth.
2. Share specific Docs/Sheets/Drive files with the agent's account.
3. Configure the Google Docs skill in OpenClaw.
4. Test: ask Claude to append a note, verify it appears in the doc.

### Validate

- [ ] Tasks created by Claude appear in Notion.
- [ ] Claude can query current task status from Notion.
- [ ] Text appended by Claude appears cleanly in Google Docs.
- [ ] No schema confusion between Notion (structured) and Docs (narrative).

---

## Phase 4 — Combined Workflow

**Goal:** One input triggers multiple correct outputs across systems.

```
Voice note via Telegram
    |
    v
Whisper STT (channel layer)
    |
    v
Claude receives transcribed text
    |
    |-- Appends full text to Google Docs (voice log)
    |-- Extracts tasks -> creates them in Notion
    \-- Reports all actions taken back to Telegram
```

### Error handling

| Failure | Behavior |
|---------|----------|
| Notion API unreachable | Report failure, retry once, store task in MEMORY.md as fallback |
| Google Docs write fails | Report failure, include text in Telegram reply (nothing lost) |
| STT produces garbled text | Ask user to confirm transcription before taking actions |
| Claude rate-limited | Queue the message, notify user of delay |

> **Decision needed:** Confirm or adjust these failure behaviors.

### Validate

- [ ] Voice note -> transcription + Docs append + Notion task extraction all succeed.
- [ ] Claude reports every action it took (no silent side effects).
- [ ] Failures are surfaced to the user with the affected content preserved.
- [ ] Works across multiple inputs in sequence without state corruption.

---

## VPS Security Checklist

Applied throughout all phases:

- [ ] Gateway binds to **loopback only** (`gateway.bind: "loopback"`)
- [ ] `allowInsecureAuth` is **not set**
- [ ] `trustedProxies` is **not set** (unless using a reverse proxy)
- [ ] Gateway auth token is set (`gateway.auth.mode: "token"`)
- [ ] mDNS discovery disabled (`discovery.mdns.mode: "off"`)
- [ ] DM policy: `pairing` (default)
- [ ] File permissions: `~/.openclaw` 700, config 600
- [ ] SSH: key-only, root login disabled
- [ ] Hetzner firewall: only port 22 inbound
- [ ] UFW on VPS: `limit 22/tcp`, deny all other inbound
- [ ] `openclaw security audit` passes

---

## Open Decisions

| # | Decision | Phase | Options |
|---|----------|-------|---------|
| 1 | STT backend | 2 | OpenAI Whisper API vs. local faster-whisper |
| 2 | Google account strategy | 3 | Dedicated agent account (recommended) vs. personal OAuth |
| 3 | Failure behavior | 4 | Confirm proposed error handling table above |
| 4 | Gemini integration | Future | Add as comparison/fallback model, not on critical path |

---

## Success Criteria

- Model routing works as intended (Claude for reasoning, Whisper for STT).
- Voice -> text -> action is reliable.
- Tasks live in Notion.
- Text lives in Docs.
- Context survives across days.

---

## Tool Roles

| Tool | Role |
|------|------|
| **OpenClaw** | Orchestration, gateway, built-in persistent memory |
| **Claude Opus 4.6** | All reasoning: thinking, writing, planning, task extraction |
| **OpenAI Whisper** | Voice transcription (STT only) |
| **Telegram** | User interface (text + voice) |
| **Notion** | External structured state (tasks, projects, priorities) |
| **Google Docs** | External narrative artifacts (logs, notes, drafts) |
| **Gemini** | Future: optional comparison/fallback model |
