#!/usr/bin/env bash
#
# Gladys VPS Bootstrap Script
# Run as root on a fresh Ubuntu VPS.
# Each step is idempotent — safe to re-run.
#
set -euo pipefail

# ── Config ───────────────────────────────────────────────────────────
USERNAME="simon"
REPO_URL="git@github.com:jumpingDolphin/gladys.git"
REPO_DIR="/home/${USERNAME}/gladys"
NODE_MAJOR=22
# ─────────────────────────────────────────────────────────────────────

info()  { printf '\n\033[1;34m[INFO]\033[0m  %s\n' "$*"; }
ok()    { printf '\033[1;32m[OK]\033[0m    %s\n' "$*"; }
warn()  { printf '\033[1;33m[WARN]\033[0m  %s\n' "$*"; }
fatal() { printf '\033[1;31m[FATAL]\033[0m %s\n' "$*" >&2; exit 1; }

# ── 1. Pre-flight checks ────────────────────────────────────────────
info "Pre-flight checks"

[[ $EUID -eq 0 ]] || fatal "This script must be run as root."

if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    case "${ID:-}" in
        ubuntu|debian) ok "Detected $PRETTY_NAME" ;;
        *) fatal "Unsupported OS: ${ID:-unknown}. Expected Ubuntu or Debian." ;;
    esac
else
    fatal "/etc/os-release not found — cannot detect OS."
fi

# ── 2. System update ────────────────────────────────────────────────
info "Updating system packages"

export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get upgrade -y -qq
apt-get install -y -qq curl git ufw unattended-upgrades
ok "System packages up to date"

# ── 3. Create user ──────────────────────────────────────────────────
info "Setting up user: ${USERNAME}"

if id "${USERNAME}" &>/dev/null; then
    ok "User ${USERNAME} already exists"
else
    adduser --disabled-password --gecos "" "${USERNAME}"
    ok "Created user ${USERNAME}"
fi

# Ensure sudo group membership
if groups "${USERNAME}" | grep -qw sudo; then
    ok "${USERNAME} already in sudo group"
else
    usermod -aG sudo "${USERNAME}"
    ok "Added ${USERNAME} to sudo group"
fi

# Allow passwordless sudo
SUDOERS_FILE="/etc/sudoers.d/${USERNAME}"
if [[ -f "${SUDOERS_FILE}" ]]; then
    ok "Sudoers entry already exists"
else
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > "${SUDOERS_FILE}"
    chmod 440 "${SUDOERS_FILE}"
    ok "Created passwordless sudo entry"
fi

# Copy SSH authorized_keys from root
USER_SSH_DIR="/home/${USERNAME}/.ssh"
mkdir -p "${USER_SSH_DIR}"

if [[ -f /root/.ssh/authorized_keys ]]; then
    cp /root/.ssh/authorized_keys "${USER_SSH_DIR}/authorized_keys"
    chown -R "${USERNAME}:${USERNAME}" "${USER_SSH_DIR}"
    chmod 700 "${USER_SSH_DIR}"
    chmod 600 "${USER_SSH_DIR}/authorized_keys"
    ok "Copied SSH keys from root"
else
    warn "No /root/.ssh/authorized_keys found — add keys manually"
fi

# ── 4. Harden SSH ───────────────────────────────────────────────────
info "Hardening SSH configuration"

SSHD_DROPIN="/etc/ssh/sshd_config.d/99-gladys-hardening.conf"
SSHD_CONTENT="# Gladys SSH hardening — managed by scripts/setup.sh
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3"

if [[ -f "${SSHD_DROPIN}" ]] && [[ "$(cat "${SSHD_DROPIN}")" == "${SSHD_CONTENT}" ]]; then
    ok "SSH hardening already applied"
else
    echo "${SSHD_CONTENT}" > "${SSHD_DROPIN}"

    # Validate before restarting — prevents lockout
    if sshd -t; then
        systemctl restart ssh
        ok "SSH hardened and restarted"
    else
        rm -f "${SSHD_DROPIN}"
        fatal "sshd config validation failed — removed drop-in to prevent lockout"
    fi
fi

# ── 5. Configure UFW ────────────────────────────────────────────────
info "Configuring UFW firewall"

ufw --force reset >/dev/null 2>&1
ufw default deny incoming >/dev/null
ufw default allow outgoing >/dev/null
ufw limit 22/tcp >/dev/null
ufw --force enable >/dev/null
ok "UFW enabled: SSH rate-limited, all other inbound denied"

# ── 6. Install Node.js ──────────────────────────────────────────────
info "Installing Node.js ${NODE_MAJOR}.x"

if command -v node &>/dev/null && node --version | grep -q "^v${NODE_MAJOR}\."; then
    ok "Node.js $(node --version) already installed"
else
    # NodeSource setup
    curl -fsSL "https://deb.nodesource.com/setup_${NODE_MAJOR}.x" | bash -
    apt-get install -y -qq nodejs
    ok "Installed Node.js $(node --version)"
fi

# ── 7. Install OpenClaw ─────────────────────────────────────────────
info "Installing OpenClaw"

if command -v openclaw &>/dev/null; then
    ok "OpenClaw already installed: $(openclaw --version 2>/dev/null || echo 'version unknown')"
else
    npm install -g openclaw@latest
    ok "Installed OpenClaw"
fi

# ── 8. Install Claude Code ──────────────────────────────────────────
info "Installing Claude Code"

if command -v claude &>/dev/null; then
    ok "Claude Code already installed: $(claude --version 2>/dev/null || echo 'version unknown')"
else
    npm install -g @anthropic-ai/claude-code
    ok "Installed Claude Code"
fi

# ── 9. Generate SSH deploy key ──────────────────────────────────────
info "Setting up SSH deploy key for GitHub"

DEPLOY_KEY="${USER_SSH_DIR}/id_ed25519"
if [[ -f "${DEPLOY_KEY}" ]]; then
    ok "Deploy key already exists"
else
    sudo -u "${USERNAME}" ssh-keygen -t ed25519 -f "${DEPLOY_KEY}" -N "" -C "${USERNAME}@gladys"
    ok "Generated deploy key"
fi

# Only prompt for deploy key if repo hasn't been cloned yet
if [[ ! -d "${REPO_DIR}/.git" ]]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Add this public key as a GitHub deploy key (with write access):"
    echo "  https://github.com/jumpingDolphin/gladys/settings/keys"
    echo ""
    cat "${DEPLOY_KEY}.pub"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    read -rp "Press Enter after adding the deploy key to GitHub... "
fi

# Add GitHub to known_hosts (idempotent — grep before appending)
if ! grep -q "github.com" "${USER_SSH_DIR}/known_hosts" 2>/dev/null; then
    sudo -u "${USERNAME}" bash -c "ssh-keyscan -t ed25519 github.com >> ${USER_SSH_DIR}/known_hosts 2>/dev/null"
    ok "Added github.com to known_hosts"
else
    ok "github.com already in known_hosts"
fi

# ── 10. Clone repo ──────────────────────────────────────────────────
info "Cloning repository"

if [[ -d "${REPO_DIR}/.git" ]]; then
    sudo -u "${USERNAME}" git -C "${REPO_DIR}" pull --ff-only
    ok "Repository already exists — pulled latest"
else
    sudo -u "${USERNAME}" git clone "${REPO_URL}" "${REPO_DIR}"
    ok "Cloned repository to ${REPO_DIR}"
fi

# ── 11. Create .env ─────────────────────────────────────────────────
info "Setting up .env"

ENV_FILE="${REPO_DIR}/.env"
ENV_EXAMPLE="${REPO_DIR}/.env.example"

if [[ -f "${ENV_FILE}" ]]; then
    ok ".env already exists — not overwriting"
else
    if [[ -f "${ENV_EXAMPLE}" ]]; then
        cp "${ENV_EXAMPLE}" "${ENV_FILE}"
        chown "${USERNAME}:${USERNAME}" "${ENV_FILE}"
        chmod 600 "${ENV_FILE}"
        ok "Created .env from .env.example"
    else
        warn ".env.example not found in repo — create .env manually"
    fi
fi

# ── 12. Configure user environment ──────────────────────────────────
info "Configuring user environment"

BASHRC="/home/${USERNAME}/.bashrc"
MARKER="# Gladys environment"

if grep -qF "${MARKER}" "${BASHRC}" 2>/dev/null; then
    ok "Bashrc already configured"
else
    cat >> "${BASHRC}" << 'BASHRC_BLOCK'

# Gladys environment
export OPENCLAW_STATE_DIR=~/gladys/openclaw
if [[ -f ~/gladys/.env ]]; then
    set -a
    source ~/gladys/.env
    set +a
fi
BASHRC_BLOCK
    ok "Added Gladys environment to .bashrc"
fi

# ── 13. Set permissions ─────────────────────────────────────────────
info "Setting file permissions"

chown -R "${USERNAME}:${USERNAME}" "${REPO_DIR}"
chmod 700 "${REPO_DIR}"
[[ -f "${REPO_DIR}/.env" ]] && chmod 600 "${REPO_DIR}/.env"
ok "Permissions set: repo dir 700, .env 600"

# ── 14. Install systemd service ─────────────────────────────────────
info "Installing systemd user service"

SERVICE_DIR="/home/${USERNAME}/.config/systemd/user"
SERVICE_FILE="${SERVICE_DIR}/openclaw-gateway.service"

mkdir -p "${SERVICE_DIR}"

cat > "${SERVICE_FILE}" << EOF
[Unit]
Description=OpenClaw Gateway
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=$(command -v openclaw) gateway start
Restart=on-failure
RestartSec=5
EnvironmentFile=${REPO_DIR}/.env
Environment=OPENCLAW_STATE_DIR=${REPO_DIR}/openclaw

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=${REPO_DIR}

[Install]
WantedBy=default.target
EOF

chown -R "${USERNAME}:${USERNAME}" "/home/${USERNAME}/.config"

# Enable lingering so user services run without active login
loginctl enable-linger "${USERNAME}"

# Enable the service (as the user)
# The user's D-Bus session may not exist yet (first provision), so try
# machinectl shell first, then fall back to advising manual enable.
USER_UID="$(id -u "${USERNAME}")"
RUNTIME_DIR="/run/user/${USER_UID}"

if [[ -S "${RUNTIME_DIR}/bus" ]]; then
    sudo -u "${USERNAME}" XDG_RUNTIME_DIR="${RUNTIME_DIR}" \
        systemctl --user daemon-reload
    sudo -u "${USERNAME}" XDG_RUNTIME_DIR="${RUNTIME_DIR}" \
        systemctl --user enable openclaw-gateway.service
    ok "Systemd service installed and enabled (not started — fill .env first)"
else
    ok "Systemd service file installed"
    warn "User session not available — after first login as ${USERNAME}, run:"
    warn "  systemctl --user daemon-reload && systemctl --user enable openclaw-gateway.service"
fi

# ── 15. Next steps ──────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Setup complete! Next steps:"
echo ""
echo "  1. Log in as ${USERNAME}:"
echo "     ssh ${USERNAME}@gladys.simonschenker.com"
echo ""
echo "  2. Fill in your API keys:"
echo "     nano ${REPO_DIR}/.env"
echo ""
echo "  3. Run the OpenClaw onboard wizard (do NOT use --install-daemon):"
echo "     openclaw onboard"
echo ""
echo "  4. Review and commit the generated config:"
echo "     git add openclaw/ && git diff --cached && git commit -m 'Add OpenClaw config via wizard'"
echo ""
echo "  5. Start the gateway:"
echo "     systemctl --user start openclaw-gateway"
echo ""
echo "  6. Verify everything works:"
echo "     openclaw doctor"
echo "     systemctl --user status openclaw-gateway"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
