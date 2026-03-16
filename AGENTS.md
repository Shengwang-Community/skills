# AGENTS.md

This repository contains AI agent skills for Shengwang platform integration,
following the [Agent Skills](https://agentskills.io) open standard.

## How to Use

> **CRITICAL FIRST STEP:** Before doing ANY work, run `bash skills/voice-ai-integration/scripts/fetch-docs.sh`
> to download the doc index (`references/docs.txt`). All doc lookups depend on this file.
> Skip this only if the file already exists.

1. Download doc index (see above) — this MUST happen before anything else
2. Start from [skills/voice-ai-integration/SKILL.md](skills/voice-ai-integration/SKILL.md) — it is the root entry point
3. The root skill decides whether to run intake (needs analysis) or route directly to a sub-module
4. Each sub-module has a `README.md` with its workflow: confirm credentials → fetch docs → generate code → validate

## Repository Structure

```
skills/
└── voice-ai-integration/         # The skill (start here)
    ├── SKILL.md                   # Entry point and router (only SKILL.md in the repo)
    ├── intake/                    # Needs analysis → product routing
    └── references/                # All product modules and shared knowledge
        ├── doc-fetching.md            # Doc fetching guide
        ├── general/               # Credentials, REST auth (shared)
        ├── conversational-ai/     # ConvoAI
        ├── rtc/                   # RTC SDK
        ├── rtm/                   # RTM
        ├── cloud-recording/       # Cloud Recording
        └── token-server/          # Token generation
```

## Documentation Access

Skills provide behavioral guidance and workflow. Up-to-date API documentation is fetched
directly via HTTP from `doc-mcp.shengwang.cn` — no MCP server setup required.
See [references/doc-fetching.md](skills/voice-ai-integration/references/doc-fetching.md) for doc fetching patterns.

## Rules

- **FIRST ACTION on every session:** check if `skills/voice-ai-integration/references/docs.txt` exists; if not, run `bash skills/voice-ai-integration/scripts/fetch-docs.sh` before doing anything else
- Always start from `skills/voice-ai-integration/SKILL.md`
- Never hardcode credentials — use environment variables
- Download `docs.txt` first, then fetch quick start docs before generating code
- When fetch fails, use local references + fallback URLs, and tell the user to verify
