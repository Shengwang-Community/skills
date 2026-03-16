---
name: voice-ai-integration
description: |
  Integrate Shengwang products: ConvoAI voice agents, RTC audio/video,
  RTM messaging, Cloud Recording, and token generation. Use when the user
  mentions Shengwang, 声网, ConvoAI, RTC, RTM, voice agent, AI agent,
  video call, live streaming, recording, token, or any Shengwang product task.
license: MIT
metadata:
  author: shengwang
  version: "1.0.0"
---

# Shengwang Integration

## Workflow

### Step 0: Ensure doc index exists (MANDATORY)

> **⚠️ This step is NON-NEGOTIABLE. Execute it BEFORE any routing, intake, or code generation.**

Check if `references/docs.txt` exists. If not (or if this is a fresh project), download it immediately:
```bash
bash skills/voice-ai-integration/scripts/fetch-docs.sh
```
This file is the documentation index — all doc lookups depend on it.
Do NOT proceed to Step 1 until this file exists or the download has been attempted.
If download fails, proceed with local reference docs and fallback URLs.

### Step 1: Collect kickoff information

Use [intake](intake/README.md) to collect kickoff information.
Ask only for details the user has not already provided.

Collect only the details needed to remove implementation blockers:
- User's use case / target solution
- Main Shengwang product
- Platform or client stack
- Backend language if relevant
- Any key technical details already known that affect routing or implementation

Use a conversational flow:
- Infer obvious context from the user's request when it is safe to do so
- Ask only for missing details that block routing or implementation
- Stop asking as soon as there is enough information to continue

ConvoAI has a special intake mode:
- If ConvoAI is clearly the primary product, switch to the consolidated ConvoAI intake in [intake/convoai.md](intake/convoai.md)
- Ask for all unresolved kickoff fields plus unresolved ConvoAI provider/config fields in one message
- Show numbered choices for each unresolved field and ask for a one-line numeric reply
- Do not repeat fields the user already answered

For ConvoAI, the user must still explicitly answer or confirm any unresolved `Other` follow-up value before implementation.

For unresolved ConvoAI fields with defaults, keep them visible and treat omission as an explicit default confirmation. This includes `Platform = Web` and `Backend = Python`.
If the first consolidated reply is incomplete, ask only a narrow follow-up for the unresolved mandatory blocker.

If the user already gave enough information, do not repeat questions.
Produce a lightweight kickoff recap, then continue automatically unless a required detail is still missing.

### Step 2: Start with local references

Use the kickoff summary plus the route table below to select the correct local reference module.
If the available information is sufficient, begin implementation using the existing local docs under
`references/`.

| Purpose | Route to |
|-------------|----------|
| New request, vague, or missing details | [intake](intake/README.md) |
| Credentials, AppID, REST auth | [general](references/general/credentials-and-auth.md) |
| Download SDK, sample project, Token Builder, GitHub repo | Route to the relevant product module |
| Generate Token, token server, AccessToken2, RTC/RTM auth | [token-server](references/token-server/README.md) |
| ConvoAI operation (with details already known) | [conversational-ai](references/conversational-ai/README.md) |
| RTC SDK integration | [rtc](references/rtc/README.md) |
| RTM messaging / signaling | [rtm](references/rtm/README.md) |
| Cloud Recording | [cloud-recording](references/cloud-recording/README.md) |

If Step 2 provides enough information for implementation, proceed.
If essential information is still missing or the local references are not enough, continue to Step 3.

### Step 3: Research with doc fetching

Use [references/doc-fetching.md](references/doc-fetching.md) to fetch more comprehensive documentation.
Do this only after Step 2, when the local references are insufficient for the requested implementation.

Research order:
1. Local references in this skill
2. Fetched docs via the doc-fetching workflow
3. Fallback web search only if needed after doc fetching

Once Step 3 provides enough information, proceed with implementation.

## Download Rules

- Use `git clone --depth 1 <url>` — GitHub URLs must be repo root only (no branch/subdirectory paths)
- On any download failure: report the error, provide the URL for manual download, never silently skip

## Links

- Console: https://console.shengwang.cn/
- Docs (CN): https://doc.shengwang.cn/
- GitHub: https://github.com/Shengwang-Community
