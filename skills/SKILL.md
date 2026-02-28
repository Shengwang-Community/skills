---
name: shengwang-platform
description: |
  Routes Shengwang (Agora) platform integration requests to the correct product
  skill. Use when the user mentions Shengwang, Agora, 声网, ConvoAI, RTC, RTM, voice agent,
  AI agent, or any Agora product integration task.
triggers:
  - "shengwang"
  - "agora"
  - "声网"
  - "agora sdk"
  - "agora console"
metadata:
  author: shengwang
  version: "3.1.0"
---

# Shengwang Platform

## Routing Table

> **MANDATORY**: For any new user request, run [intake/SKILL.md](intake/SKILL.md) FIRST.
> The ONLY exceptions are: direct error questions, specific operations with all details provided
> (e.g. "stop agent xxx"), or the user explicitly says they already completed intake.
> Do NOT skip intake just because you recognize a product name like "ConvoAI" or "AI agent".

| User intent | Route to |
|-------------|----------|
| Any new request, vague or product-specific | [intake/SKILL.md](intake/SKILL.md) (MUST run first) |
| Credentials, AppID, token setup, MCP tools | [general/SKILL.md](general/SKILL.md) |
| Download SDK, sample project, Token Builder, GitHub repo | [resource-downloader/SKILL.md](resource-downloader/SKILL.md) |
| Generate Token, token server, AccessToken2, RTC/RTM auth | [implement-shengwang-token-on-server/SKILL.md](implement-shengwang-token-on-server/SKILL.md) |
| Specific ConvoAI operation (with details already known) | [integrate-shengwang-conversational-ai/SKILL.md](integrate-shengwang-conversational-ai/SKILL.md) |
| RTC SDK, RTM, Cloud Recording, other products | https://doc.shengwang.cn/ |

## Links

- Console: https://console.agora.io/
- Docs (CN): https://doc.shengwang.cn/
- Docs (Global): https://docs.agora.io/
- GitHub: https://github.com/AgoraIO-Community
