# Security Roadmap

> Prioritized security hardening checklist for the Gladys/OpenClaw deployment.
> Companion to [`roadmap.md`](../roadmap.md).

---

## Baseline Audit (2026-02-11)

Initial `openclaw security audit --deep` results:

| Severity | Count | Key findings |
|----------|-------|--------------|
| Critical | 4 | Open group policy with elevated tools, open DM policy, open group sender allowlist (wildcard `*`), elevated tools exposure |
| Warning | 2 | Missing trusted proxies config, DM sessions share main session (context leaking) |
| Info | 1 | Attack surface: browser control enabled, hooks disabled |

After `openclaw security audit --fix`:

| Severity | Count | Key findings |
|----------|-------|--------------|
| Critical | 2 | Open DM policy, wildcard in group allowFrom |
| Warning | 2 | Missing trusted proxies config, DM sessions share main session |
| Info | 1 | Attack surface: browser control enabled |

**Auto-fixed by `--fix`:**
- `groupPolicy` changed from `open` to `allowlist`
- Sessions directory permissions set to `700`
- All other file permissions already correct

After P0 hardening (2026-02-11):

| Severity | Count | Key findings |
|----------|-------|--------------|
| Critical | 1 | Wildcard in groupAllowFrom (intentional — see P0 notes) |
| Warning | 1 | Missing trusted proxies config |
| Info | 1 | Attack surface: browser control enabled |

**P0 fixes applied:**
- `dmPolicy` changed from `open` to `allowlist`
- `allowFrom` changed from `["*"]` to `["7273735518"]`
- Systemd hardening drop-in: `NoNewPrivileges`, `PrivateTmp`, `ProtectSystem=strict`

---

## P0 — Critical (fix now)

- [x] Run `openclaw security audit --deep` — baseline captured above
- [x] Run `openclaw security audit --fix` — auto-fixed group policy + session dir permissions
- [x] Restrict Telegram DM policy: `open` → `allowlist` (allowFrom set to Simon's user ID)
- [x] Keep `groupAllowFrom` wildcard — appropriate since `groupPolicy` is `allowlist` (only explicitly configured groups can interact; within those groups, all members can talk)
- [x] Add systemd hardening directives via drop-in override (`~/.config/systemd/user/openclaw-gateway.service.d/hardening.conf`):
  - `NoNewPrivileges=yes`
  - `PrivateTmp=yes`
  - `ProtectSystem=strict`
  - `ReadWritePaths=` (limit to `~/gladys/openclaw`)

## P1 — High (this week)

- [x] Migrate env vars to **systemd drop-in override**: `EnvironmentFile=` in `~/.config/systemd/user/openclaw-gateway.service.d/env.conf` pointing to `openclaw/.env` (600 perms). 9 secrets in `openclaw.json` replaced with `${VAR}` refs. Gitleaks scan: git history clean, all findings in expected gitignored files.
- [ ] Configure tool policies: create restrictive tool profile, deny `exec` globally
  ```json
  "tools": { "profile": "full", "deny": ["exec"] }
  ```
- [ ] Restrict elevated tools: set `tools.elevated.allowFrom` to trusted user ID only
- [ ] Set up plugin allowlist (empty by default)
- [ ] Disable browser control: `gateway.nodes.browser.mode: "off"` — not needed for Telegram bot
- [ ] Configure logging redaction: `logging.redactSensitive: "tools"` + custom `redactPatterns` for internal hostnames

## P2 — Medium (this sprint)

- [ ] Configure DM session isolation: `session.dmScope="per-channel-peer"` to prevent context leaking across users
- [ ] Test prompt injection defenses against IDENTITY.md rules (manual red-team)
- [ ] Verify full-disk encryption on Hetzner VPS
- [ ] Set up device auth / pairing for Telegram
- [ ] Document token rotation procedure (gateway auth token, API keys, Telegram bot token)

## P3 — Ongoing

- [ ] Run `openclaw security audit --deep` after each deploy and config change
- [ ] Review session transcripts for leaked credentials periodically
- [ ] Keep OpenClaw updated and re-audit after upgrades

---

## Reference

- [OpenClaw Security Docs](https://docs.openclaw.ai/gateway/security)
- [Security Patterns (runbook)](https://github.com/digitalknk/openclaw-runbook/blob/main/examples/security-patterns.md)
- [`roadmap.md`](../roadmap.md)
