# Plan: Add Transcription Bot (Second OpenClaw Agent)

## Context

Add a dedicated Telegram transcription bot as a second OpenClaw agent. It receives voice messages, and returns clean transcribed text (grammar/punctuation corrected, no reformulation). Uses Gemini 3 Flash (cheap, fast) — Whisper STT handles the actual audio-to-text at the channel layer, Gemini just polishes the output.

## Architecture

```
Telegram Bot 1 (Gladys)          Telegram Bot 2 (Transcriber)
        |                                  |
        v                                  v
 OpenClaw Gateway (port 18789, single process)
        |                                  |
  Agent: main                        Agent: transcriber
  Claude Sonnet 4.5                  Gemini 3 Flash
  Full skills + memory               No skills, no memory
  Heartbeat: 60m                     Heartbeat: disabled
```

Same gateway process, same systemd service. Two Telegram polling connections (one per bot token).

## Steps

### 1. Update secrets

**`openclaw/.env`** — add:
```
TELEGRAM_BOT_TOKEN_TRANSCRIBER=<token>
```

**`.env.example`** — add template line:
```
# Transcriber bot token (second Telegram bot, from @BotFather)
TELEGRAM_BOT_TOKEN_TRANSCRIBER=
```

### 2. Create minimal workspace

```
mkdir -p /home/simon/gladys/openclaw/workspace-transcriber
```

Create `openclaw/workspace-transcriber/IDENTITY.md` with minimal identity + security rules. No SOUL.md, USER.md, AGENTS.md, MEMORY.md, skills/, etc.

### 3. Update `openclaw/openclaw.json`

Add `agents.entries.transcriber` alongside existing `agents.defaults`:

```json
"agents": {
  "defaults": { /* ... existing ... */ },
  "entries": {
    "transcriber": {
      "label": "Transcription Bot",
      "model": {
        "primary": "google/gemini-3-flash"
      },
      "workspace": "/home/simon/gladys/openclaw/workspace-transcriber",
      "systemPrompt": "Tu es un assistant de transcription. Ton seul rôle : transcrire l'audio reçu et corriger légèrement les erreurs (grammaire, ponctuation) sans reformuler. Output uniquement le texte corrigé, prêt à copier-coller.",
      "heartbeat": { "enabled": false },
      "channels": {
        "telegram": {
          "enabled": true,
          "botToken": "${TELEGRAM_BOT_TOKEN_TRANSCRIBER}",
          "dmPolicy": "allowlist",
          "allowFrom": ["7273735518"]
        }
      }
    }
  }
}
```

**Config format risk:** The exact shape (`agents.entries` with per-agent `channels`) hasn't been validated yet. We'll follow your proposed pattern, restart the gateway, and check the logs. If OpenClaw expects a different format (e.g. top-level channel accounts with routing bindings), we'll adapt based on the error output.

### 4. Model auth for the transcriber

Gemini 3 Flash auth (`google:manual` profile) is already configured for the main agent. Check if:
- Auth is resolved globally (shared) — no action needed
- Auth is per-agent dir — run `openclaw models auth --agent transcriber` or copy the Google token to `openclaw/agents/transcriber/agent/auth-profiles.json`

### 5. Restart and test

```bash
systemctl --user restart openclaw-gateway
journalctl --user -u openclaw-gateway --since "1 min ago" --no-pager
```

Test checklist:
- [ ] Voice message to transcriber bot → clean text back
- [ ] Text message to transcriber bot → minimal response
- [ ] Main Gladys bot unaffected
- [ ] DM from non-allowlisted user rejected by transcriber

### 6. Update docs

**`openclaw/workspace/roadmap/ROADMAP.md`** — add to integrations table and completed section

**`CLAUDE.md`** — update architecture diagram, secrets table, key decisions table

**`.env.example`** — already handled in step 2

## Files to modify

| File | Action |
|------|--------|
| `openclaw/.env` | Add `TELEGRAM_BOT_TOKEN_TRANSCRIBER` (manual) |
| `.env.example` | Add token template line |
| `openclaw/openclaw.json` | Add `agents.entries.transcriber` |
| `openclaw/workspace-transcriber/IDENTITY.md` | Create (minimal) |
| `openclaw/workspace/roadmap/ROADMAP.md` | Add integration + completed item |
| `openclaw/workspace/roadmap/transcriber-bot.md` | Create detailed reference doc |
| `CLAUDE.md` | Update architecture, secrets, decisions |
