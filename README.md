# Shengwang (Agora) Skills

[![中文](https://img.shields.io/badge/lang-中文-red.svg)](README_CN.md)

Reusable skills for AI coding agents building with the [Shengwang (Agora)](https://shengwang.cn/) platform. These skills help agents accurately integrate, configure, and debug Agora products.

## Available Skills

| Skill | Product | Description |
|-------|---------|-------------|
| [conversational-ai](skills/voice-ai-integration/references/conversational-ai/README.md) | ConvoAI | AI voice agent lifecycle: create/stop/update/query. Supports Go, Java, Python |
| [rtc](skills/voice-ai-integration/references/rtc/README.md) | RTC SDK | Real-time audio/video calls. Web, Android, iOS, Flutter, and more |
| [rtm](skills/voice-ai-integration/references/rtm/README.md) | RTM | Real-time messaging, signaling, presence |
| [cloud-recording](skills/voice-ai-integration/references/cloud-recording/README.md) | Cloud Recording | Server-side recording of RTC sessions |
| [token-server](skills/voice-ai-integration/references/token-server/README.md) | Token Server | Server-side token generation (AccessToken2) |
| [general](skills/voice-ai-integration/references/general/credentials-and-auth.md) | General | Credential management, REST auth patterns |
| [intake](skills/voice-ai-integration/intake/README.md) | Routing | Needs analysis → product recommendation → route to product module |

## Quick Start

### Installation Methods

#### Skills CLI

Install with CLI:

```bash
npx skills add Shengwang-Community/skills
```

This is the most direct installation method. After installation, restart the session or refresh the skills list according to your coding agent's instructions.

#### Claude Code Plugin Marketplace

Run the following command in Claude Code:

```bash
plugin marketplace add Shengwang-Community/skills
```
#### OpenClaw

Install via `ClawHub`. Use `install` for the initial installation and `update` for subsequent updates.

```bash
clawhub install voice-ai-integration
clawhub update voice-ai-integration
```

### 2. Download Doc Index (Recommended)

Download the documentation index for fetching latest API docs during development:

```bash
bash skills/voice-ai-integration/scripts/fetch-docs.sh
```

This saves the doc index to `skills/voice-ai-integration/references/docs.txt`. Skills use it to look up and fetch documentation directly via HTTP — no external server process needed.

> Skills work without the doc index too — they fall back to local reference docs and external doc links.

### 3. Start Using

Describe your needs to the agent — skills trigger automatically:

- "I want to build an AI voice assistant" → intake analysis → ConvoAI + RTC integration
- "Generate an RTC token in Go" → Token Server module
- "How to implement video calls on Web" → RTC SDK module
- "Download the ConvoAI Go SDK" → Resource Downloader

## How It Works

```
User Request
   │
   ▼
skills/voice-ai-integration/SKILL.md (entry point)
   │
   ├─ Vague request → intake (needs analysis → product recommendation)
   │                      │
   │                      ▼
   │                 Product module (code generation)
   │
   └─ Clear request → Route directly to product module
```

The entry point (`skills/voice-ai-integration/SKILL.md`) determines whether the request is specific enough:
- Clear and actionable → route directly to the matching product module
- Vague or missing details → run intake to collect requirements first, then route

Each product module follows a consistent workflow: confirm credentials → fetch latest docs → generate code → validate.

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
    └── voice-ai-integration/     # The skill (agentskills.io standard)
        ├── SKILL.md               # Entry point and router (only SKILL.md)
        ├── intake/                # Needs analysis and product routing
        └── references/            # All product modules and shared knowledge
            ├── doc-fetching.md        # Doc fetching guide
            ├── docs.txt               # Local doc index
            ├── general/               # Credentials, REST auth
            ├── conversational-ai/     # ConvoAI
            ├── rtc/                   # RTC SDK
            ├── rtm/                   # RTM
            ├── cloud-recording/       # Cloud Recording
            └── token-server/          # Token generation
```

## Design Philosophy

- Behavior over knowledge: skills teach agents *how to approach* integration; doc fetching provides *specific APIs*
- Single responsibility: each module does one thing
- Progressive disclosure: SKILL.md serves as navigation; detailed content lives in `references/` and module `README.md` files
- Explicit failure paths: every module defines error handling
- Eval-driven iteration: validate changes against `tests/eval-cases.md`

## Validation

```bash
bash scripts/validate-skills.sh
```

Checks all SKILL.md frontmatter format and markdown link validity.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Key requirements:

- The root skill has a `SKILL.md` with YAML frontmatter (name, description, metadata.author, metadata.version)
- Sub-modules use `README.md` (no frontmatter needed)
- Directory names use kebab-case
- Detailed docs go in `references/`; keep SKILL.md and README.md concise
- Run `bash scripts/validate-skills.sh` before submitting

## Links

- [Shengwang Console](https://console.shengwang.cn/)
- [Agora Docs (CN)](https://doc.shengwang.cn/)
- [GitHub](https://github.com/Shengwang-Community)
