# Shengwang (Agora) Skills

[![中文](https://img.shields.io/badge/lang-中文-red.svg)](README_CN.md)

Reusable skills for AI coding agents building with the [Shengwang (Agora)](https://www.agora.io/) platform. These skills help agents accurately integrate, configure, and debug Agora products.

## Available Skills

| Skill | Product | Description |
|-------|---------|-------------|
| [integrate-shengwang-conversational-ai](skills/shengwang-integration/integrate-shengwang-conversational-ai/SKILL.md) | ConvoAI | AI voice agent lifecycle: create/stop/update/query. Supports Go, Java, Python |
| [integrate-shengwang-rtc](skills/shengwang-integration/integrate-shengwang-rtc/SKILL.md) | RTC SDK | Real-time audio/video calls. Web, Android, iOS, Flutter, and more |
| [integrate-shengwang-rtm](skills/shengwang-integration/integrate-shengwang-rtm/SKILL.md) | RTM | Real-time messaging, signaling, presence |
| [integrate-shengwang-cloud-recording](skills/shengwang-integration/integrate-shengwang-cloud-recording/SKILL.md) | Cloud Recording | Server-side recording of RTC sessions |
| [implement-shengwang-token-on-server](skills/shengwang-integration/implement-shengwang-token-on-server/SKILL.md) | Token Server | Server-side token generation (AccessToken2) |
| [general](skills/shengwang-integration/general/SKILL.md) | General | Credential management, REST auth patterns |
| [resource-downloader](skills/shengwang-integration/resource-downloader/SKILL.md) | Tooling | Download SDKs, sample projects, Token Builder |
| [intake](skills/shengwang-integration/intake/SKILL.md) | Routing | Needs analysis → product recommendation → route to product skill |

## Quick Start

## Installation

### Option A: Skills CLI (agentskills.io standard)

```bash
npx skills add AgoraIO-Community/shengwang-skills
```

### Option B: Git clone

Clone to your AI coding agent's skills directory:

```bash
# Claude Code
git clone https://github.com/AgoraIO-Community/shengwang-skills.git .claude/skills/shengwang-skills

# Kiro
git clone https://github.com/AgoraIO-Community/shengwang-skills.git .kiro/skills/shengwang-skills
```

Skills activate automatically when the agent detects relevant tasks (e.g., "build a voice agent", "integrate Agora RTC", "generate a token").

### 2. Configure MCP (Recommended)

These skills are designed to work alongside the [Agora Doc MCP Server](https://doc-mcp.shengwang.cn). Skills provide behavioral guidance and workflow; MCP provides up-to-date API documentation.

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "agora-docs": {
      "type": "sse",
      "url": "https://doc-mcp.shengwang.cn/mcp"
    }
  }
}
```

> Skills work without MCP too — they fall back to local OpenAPI specs and external doc links.

### 3. Start Using

Describe your needs to the agent — skills trigger automatically:

- "I want to build an AI voice assistant" → intake analysis → ConvoAI + RTC integration
- "Generate an RTC token in Go" → Token Server skill
- "How to implement video calls on Web" → RTC SDK skill
- "Download the ConvoAI Go SDK" → Resource Downloader

## How It Works

```
User Request
   │
   ▼
skills/shengwang-integration/SKILL.md (entry point)
   │
   ├─ Vague request → intake (needs analysis → product recommendation)
   │                      │
   │                      ▼
   │                 Product module (code generation)
   │
   └─ Clear request → Route directly to product module
```

The entry point (`skills/shengwang-integration/SKILL.md`) determines whether the request is specific enough:
- Clear and actionable → route directly to the matching product skill
- Vague or missing details → run intake to collect requirements first, then route

Each product skill follows a consistent workflow: confirm credentials → fetch latest docs via MCP → generate code → validate.

## Repository Structure

```
shengwang-skills/
├── README.md                  # This file
├── AGENTS.md                  # Agent entry point instructions
├── CLAUDE.md                  # → AGENTS.md
├── CONTRIBUTING.md            # Contribution guidelines
├── scripts/
│   └── validate-skills.sh     # Link and frontmatter validation
├── tests/
│   └── eval-cases.md          # Evaluation test cases
└── skills/
    └── shengwang-integration/     # The skill (agentskills.io standard)
        ├── SKILL.md               # Entry point and router
        ├── mcp-tools.md           # MCP tool usage guide
        ├── intake/                # Needs analysis and product routing
        ├── general/               # Credentials, REST auth
        ├── integrate-shengwang-conversational-ai/  # ConvoAI
        ├── integrate-shengwang-rtc/               # RTC SDK
        ├── integrate-shengwang-rtm/               # RTM
        ├── integrate-shengwang-cloud-recording/   # Cloud Recording
        ├── implement-shengwang-token-on-server/   # Token generation
        └── resource-downloader/                   # SDK/sample downloads
```

## Design Philosophy

- Behavior over knowledge: skills teach agents *how to approach* integration; MCP provides *specific APIs*
- Single responsibility: each skill does one thing
- Progressive disclosure: SKILL.md serves as navigation; detailed content lives in `references/`
- Explicit failure paths: every skill defines error handling
- Eval-driven iteration: validate changes against `tests/eval-cases.md`

## Validation

```bash
bash scripts/validate-skills.sh
```

Checks all SKILL.md frontmatter format and markdown link validity.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Key requirements:

- Every skill directory must have a `SKILL.md` with YAML frontmatter (name, description, metadata.author, metadata.version)
- Directory names use kebab-case
- Detailed docs go in `references/`; keep SKILL.md concise
- Run `bash scripts/validate-skills.sh` before submitting

## Links

- [Agora Console](https://console.agora.io/)
- [Agora Docs (CN)](https://doc.shengwang.cn/)
- [Agora Docs (Global)](https://docs.agora.io/)
- [GitHub](https://github.com/AgoraIO-Community)
