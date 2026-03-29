# Shengwang Skills

[![中文](https://img.shields.io/badge/lang-中文-red.svg)](README_CN.md)

Reusable skills for AI coding agents building with the [Shengwang](https://shengwang.cn/) platform. These skills help agents accurately integrate, configure, and debug Shengwang products.

## Available Skills

| Skill | Product | Description |
|-------|---------|-------------|
| [conversational-ai](skills/voice-ai-integration/references/conversational-ai/README.md) | ConvoAI | AI voice agent lifecycle: create/stop/update/query. Supports Go, Java, Python |
| [rtc](skills/voice-ai-integration/references/rtc/README.md) | RTC SDK | Real-time audio/video calls. Web, Android, iOS, Flutter, and more |
| [rtm](skills/voice-ai-integration/references/rtm/README.md) | RTM | Real-time messaging, signaling, presence |
| [cloud-recording](skills/voice-ai-integration/references/cloud-recording/README.md) | Cloud Recording | Server-side recording of RTC sessions |
| [token-server](skills/voice-ai-integration/references/token-server/README.md) | Token Server | Server-side token generation (AccessToken2) |
| [general](skills/voice-ai-integration/references/general/credentials-and-auth.md) | General | Credential management, REST auth patterns |

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

### 2. Use the bundled doc indexes

The skill ships with prebuilt doc indexes:

- `skills/voice-ai-integration/references/doc-index/docs.index.md` — product catalog with URIs for focus products
- `skills/voice-ai-integration/references/doc-index/shards/{product}.json` — per-product records for selective loading
- `skills/voice-ai-integration/references/doc-index/shards/api-ref/{product}-{platform}.json` — SDK class docs

These are fallback lookup aids. Agents should start from the routed product module first, then use these indexes only when that module still needs external documentation lookup.

To refresh the indexes (maintainer only):
```bash
bash scripts/fetch-docs.sh
```

### 3. Start Using

Describe your needs to the agent — skills trigger automatically:

- "I want to build an AI voice assistant" → ConvoAI + RTC integration
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
   ├─ Clear request → Route directly to product module
   │
   └─ Vague request → Ask one clarifying question, then route
```

The entry point (`skills/voice-ai-integration/SKILL.md`) matches the request to a product module:
- Clear and actionable → route directly to the matching product module
- Vague or multi-product → ask one clarifying question, then route

Each product module follows a consistent workflow: confirm credentials → fetch latest docs → generate code → validate.

## Repository Structure

```
shengwang-skills/
├── README.md                  # This file
├── AGENTS.md                  # Agent entry point instructions
├── CLAUDE.md                  # → AGENTS.md
├── CONTRIBUTING.md            # Contribution guidelines
├── scripts/
│   ├── fetch-docs.sh          # Download sitemap + rebuild doc-index
│   ├── build-doc-index.py     # Generate all index files from sitemap
│   ├── ab-test-doc-index.py   # Token-based benchmark (56 cases)
│   ├── llm-eval-doc-index.py  # LLM end-to-end eval (72 cases)
│   └── validate-skills.sh     # Link and frontmatter validation
├── tests/
│   ├── eval-cases.md          # Evaluation test cases
│   └── doc-index-benchmark.md # Doc-index benchmark results
└── skills/
    └── voice-ai-integration/     # The skill (agentskills.io standard)
        ├── SKILL.md               # Entry point and router (only SKILL.md)
        └── references/            # All product modules and shared knowledge
            ├── doc-fetching.md        # Doc fetching guide
            ├── doc-index/             # Prebuilt doc indexes
            │   ├── docs.index.md      # Agent-readable product catalog
            │   ├── docs.index.json    # Full machine-readable index
            │   ├── api-reference.json # SDK class docs (separate)
            │   └── shards/            # Per-product shards
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
# Validate skill structure and links
bash scripts/validate-skills.sh

# Run doc-index token benchmark (no API key needed)
python3 scripts/ab-test-doc-index.py

# Run doc-index LLM evaluation (needs OPENAI_API_KEY)
export OPENAI_API_KEY=sk-...
python3 scripts/llm-eval-doc-index.py

# Rebuild doc-index from fresh sitemap (maintainer only)
bash scripts/fetch-docs.sh
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Key requirements:

- The root skill has a `SKILL.md` with YAML frontmatter (name, description, metadata.author, metadata.version)
- Sub-modules use `README.md` (no frontmatter needed)
- Directory names use kebab-case
- Detailed docs go in `references/`; keep SKILL.md and README.md concise
- Run `bash scripts/validate-skills.sh` before submitting

## Links

- [Shengwang Console](https://console.shengwang.cn/)
- [Shengwang Docs (CN)](https://doc.shengwang.cn/)
- [GitHub](https://github.com/Shengwang-Community)
