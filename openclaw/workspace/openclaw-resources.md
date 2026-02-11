# OpenClaw Resources

Source: https://github.com/SamurAIGPT/awesome-openclaw

## Quick Reference

### Official
- **Website:** https://openclaw.ai/
- **GitHub:** https://github.com/openclaw/openclaw
- **Docs:** https://docs.openclaw.ai/
- **ClawHub:** https://clawhub.ai/ (700+ skills)
- **Showcase:** https://openclaw.ai/showcase

### Key Resources
- **AGENTS.md:** Agent configuration guide
- **Plugin Development:** https://docs.openclaw.ai/plugin
- **Dashboard:** http://localhost:18789/

## Installation

```bash
# Install globally
npm install -g openclaw@latest

# Run onboarding
openclaw onboard --install-daemon
```

## Skills & Plugins

### Skill Registries
- [ClawHub](https://clawhub.ai/) - Official (700+ skills)
- [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) - Community curated
- [openclaw/skills](https://github.com/openclaw/skills) - Official repo

### Installing Skills
```bash
# From ClawHub
openclaw skills install <skill-name>

# From npm
openclaw plugins install <npm-package>
```

### Notable Skills
- **ClawdTalk** - Phone calling & SMS (Telnyx)
- **AgentFund** - Crowdfunding for AI agents (Base blockchain)

## Integrations

### Messaging (12+)
WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Microsoft Teams, Google Chat, Matrix, BlueBubbles, Zalo, WebChat

### External Services (50+)
GitHub, Gmail, Spotify, Obsidian, Hue, Twitter/X, Browser, Calendar, File System, Shell, Cron

## Community Projects

### Deployment
- **moltworker** - Run on Cloudflare Workers (7.9k stars)
- **OpenClawInstaller** - One-click deployment (1.3k stars)
- **MimiClaw** - Run on $5 ESP32-S3 chip
- **PhoneClaw** - Automate Android apps

### Web Clients
- **webclaw** - Fast, minimal web client (155+ stars)
- **clawterm** - Terminal-based client

### Memory & Storage
- **memU** - Persistent memory layer (8k stars)
- **clawmem** - Vector-based memory

### Chinese IM Integrations
- DingTalk (500+ stars)
- WeChat (600+ stars)
- Feishu/Lark (400+ stars)
- QQ (300+ stars)
- WeCom (200+ stars)

### Enterprise
- **archestra** - Enterprise RBAC (2.8k stars)
- **openclaw-saml** - SAML authentication

### Monitoring
- **crabwalk** - Real-time monitoring (683 stars)
- **clawmetrics** - Prometheus exporter

### Dev Workflows
- **FTW** - First Try Works (PIV: Plan-Implement-Validate)

## MCP Support

OpenClaw supports Model Context Protocol (MCP):
- [MCP Adapter Plugin](https://github.com/androidStern-personal/openclaw-mcp-adapter)
- Native MCP support in progress

### MCP Servers
- ecap-security-auditor (vulnerability scanning)
- glin-profanity-mcp (profanity detection)
- AnChain.AI Data MCP (AML compliance)

## Security Best Practices

- Run in sandboxed environment
- Limit file system access
- Use environment variables for API keys
- Update regularly
- Review skills before installing
- **Don't expose to public internet**

### Known Risks
- Exposed instances can be commandeered
- Malicious instructions in ingested data
- Misconfigured setups may leak data

**Resource:** [CrowdStrike Security Guide](https://www.crowdstrike.com/en-us/blog/what-security-teams-need-to-know-about-openclaw-ai-super-agent/)

## Tutorials

### Beginner
- [What is OpenClaw?](https://medium.com/@gemQueenx/what-is-openclaw-open-source-ai-agent-in-2026-setup-features-8e020db20e5e)
- [Complete Installation Guide](https://www.aifreeapi.com/en/posts/openclaw-installation-guide)

### Advanced
- [GitHub PR Review Automation](https://zenvanriel.nl/ai-engineer-blog/openclaw-github-pr-review-automation-guide/)
- [Creating AI Agent Workforce](https://o-mega.ai/articles/openclaw-creating-the-ai-agent-workforce-ultimate-guide-2026)

## Alternatives

- **Claude Code** - Developer coding assistant (Anthropic)
- **Manus AI** - General agent framework (proprietary)
- **OpenManus** - Open-source Manus alternative
- **Jan.ai** - Privacy-focused, offline
- **eesel AI** - Business customer service

## Community

- **GitHub Discussions:** https://github.com/openclaw/openclaw/discussions
- **GitHub Issues:** https://github.com/openclaw/openclaw/issues
- **ClawCon:** First meetup Feb 4, 2026 (SF)
- **Creator:** Peter Steinberger (Austrian engineer)

## History

Originally "Clawdbot" → renamed to "Moltbot" → now "OpenClaw"

Last updated: February 2026
