# Phase 0 — VPS Bootstrap Setup

**Status: COMPLETE**

## Context

Phase 0 of the Gladys roadmap requires a bootstrap script to provision a fresh Hetzner VPS.
The VPS infrastructure is already provisioned (Hetzner, DNS, firewall), but the software setup
(user, Node.js, OpenClaw, systemd, UFW) is TODO.

Write the script locally, commit, push, then clone on the VPS and run it.

## Files

| File | Purpose |
|------|---------|
| `scripts/setup.sh` | VPS bootstrap script (run as root on fresh Ubuntu) |
| `.gitignore` | Exclude secrets, sessions, SQLite, sandboxes, extensions |
| `.env.example` | Reference for required API keys (secrets managed by OpenClaw) |
| `README.md` | Project overview and Phase 0 setup instructions |

## setup.sh Steps

1. **Pre-flight checks** — verify root, verify Ubuntu/Debian
2. **System update** — `apt-get update/upgrade`, install `curl git ufw unattended-upgrades`
3. **Create user `simon`** — with sudo, copy SSH keys from root
4. **Harden SSH** — drop-in config, validate with `sshd -t` before restarting
5. **Configure UFW** — `ufw limit 22/tcp`, deny all other inbound
6. **Install Node.js 22.x** — via NodeSource
7. **Install OpenClaw** — `npm install -g openclaw@latest`
8. **Install Claude Code** — `npm install -g @anthropic-ai/claude-code`
9. **Generate SSH deploy key** — pause for user to add as GitHub deploy key
10. **Clone repo** — via SSH to `/home/simon/gladys`
11. **Configure user environment** — `.bashrc` sourcing (`OPENCLAW_STATE_DIR=~/gladys/openclaw`)
12. **Set permissions** — repo dir 700
13. **Install systemd service** — user-level unit, enable but don't start
14. **Print next steps** — run `openclaw onboard`, commit config, start service

## Security

- SSH: key-only, root login disabled, MaxAuthTries 3
- UFW: limit 22/tcp, deny all other inbound
- Gateway: loopback bind, token auth, mDNS off
- Systemd: NoNewPrivileges, PrivateTmp, ProtectSystem=strict
- File permissions: state dir 700

## Verification

1. `ssh simon@gladys.simonschenker.com` works, `ssh root@...` rejected
2. `ufw status` shows only SSH rate-limited
3. `node --version` → v22.x, `openclaw --version`, `claude --version` installed
4. `/home/simon/gladys/` contains repo
5. `git -C /home/simon/gladys remote -v` shows SSH remote
6. `systemctl --user status openclaw-gateway` shows enabled (inactive)
7. After running `openclaw onboard`: `systemctl --user start openclaw-gateway` works
