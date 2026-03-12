# Shengwang Conversational AI Engine (ConvoAI)

Real-time AI voice agent. User speaks into an RTC channel, agent responds via ASR → LLM → TTS pipeline.

## How It Works

```
User Device ── audio ──► RTC Channel ──► ConvoAI Agent (ASR → LLM → TTS)
User Device ◄── audio ── RTC Channel ◄── ConvoAI Agent
```

- Agent is server-side only — managed via REST API, no client SDK
- Client uses RTC SDK (Web/Android/iOS) to join the channel
- `POST /join` makes the agent join the same RTC channel

## Auth

ConvoAI REST API 支持两种鉴权方式（任选其一）：

1. **RTC Token**：使用声网对话式 AI 引擎项目的 RTC Token
   - 传参示例：`Authorization: agora token="007abcxxxxxxx123"`
   - 测试环境：从[声网控制台](https://console.shengwang.cn/)生成临时 Token（有效期 24 小时）
   - 生产环境：部署 [token-server](../token-server/README.md) 生成 Token

2. **Basic Auth**：使用 `AGORA_CUSTOMER_KEY` + `AGORA_CUSTOMER_SECRET` 生成 Base64 编码
   - 传参示例：`Authorization: Basic NDI1OTQ3N2I4MzYy...YwZjA=`
   - 参考[实现 HTTP 安全认证](https://doc.shengwang.cn/doc/convoai/restful/user-guides/http-basic-auth)

其他注意事项：
- ConvoAI requires separate activation in [Shengwang Console](https://console.shengwang.cn/) — 403 without it
- The `token` field in `/join` body is for the RTC channel, NOT for REST auth:
  - App Certificate not enabled → `""`
  - App Certificate enabled → generate via [token-server](../token-server/README.md)
- Credentials → [general/credentials-and-auth.md](../general/credentials-and-auth.md)

## Quick Start Docs

Fetch docs using the doc fetching script (see [doc-fetching.md](../doc-fetching.md)):

| Language | Command |
|----------|---------|
| Python / JS / curl | `bash skills/shengwang-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start"` |
| Go | `bash skills/shengwang-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start-go"` |
| Java | `bash skills/shengwang-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start-java"` |

API endpoint index → [convoai-restapi.md](convoai-restapi.md)

## Sample Repos

For reference projects and starter layouts, use [sample-repos.md](sample-repos.md).

When a matching ConvoAI sample repo exists for the requested stack, it is the default implementation reference.

Required workflow:
- Pick the relevant entry from `sample-repos.md`
- Clone the repo on demand with `git clone --depth 1 <repo-url>`
- Inspect the current stack, folder map, key files, env template files, and API surface
- Inspect the sample repo's actual env template files before coding, such as `.env.example`, `.env.local.example`, and similar sample-provided files
- Keep the implementation aligned with the sample repo's architecture, env var names discovered from those template files, dependency choices, and API shape
- Use Shengwang doc fetching only for missing API or product details that the sample repo does not cover

Implementation modes:
- `sample-aligned` is the default mode whenever a matching sample repo exists
- `minimal-custom` may only be used if the user explicitly asks for a minimal demo or says not to follow the sample repo

Alignment rules:
- Preserve the sample repo's env var names from the inspected env template files unless the user explicitly asks to rename or normalize them
- Preserve the sample repo's folder structure and backend/frontend boundaries unless the user explicitly asks for a redesign
- Preserve the sample repo's dependency choices and API shape by default; only swap what is necessary for the user's confirmed provider choices
- Do not invent env names from memory or from this skill's static docs when the sample repo provides template files

Diff budget rule:
- Make only the minimum necessary changes for the user's confirmed provider choices
- Optional modules may be removed if they are not needed
- Do not redesign env naming, folder structure, and API shape all at once unless the user explicitly asks for a custom implementation

Before editing code, state:
- which sample repo is being followed
- which env template files were inspected
- what exact differences will be introduced

Keep repo URLs in `sample-repos.md` only so future URL changes stay centralized.

## Generation Rules

Stable constraints that do NOT change with API updates. Always apply when generating code.

### Field Types (common pitfalls)
- `agent_rtc_uid`: STRING `"0"`, not int `0`
- `remote_rtc_uids`: array `["*"]`, not `"*"`
- `name`: unique per project — use `agent_{uuid[:8]}`
- `agent_rtc_uid` must not collide with any human participant's UID

### Create Agent (`POST /join`)
- `token`: `""` if no App Certificate; otherwise RTC token
- `agent_rtc_uid`: `"0"` for auto-assign
- `remote_rtc_uids`: `["*"]` unless user specifies UIDs

### Update Agent (`POST /update`)
- `llm.params` is FULLY REPLACED — always send complete object
- Only `token` and `llm` are updatable; everything else is immutable

### Terminology
- `agentId` in URL paths = `agent_id` in JSON bodies
- `/join` returns `agent_id` (snake_case); use it as path param

### Error Handling
- 409: extract existing `agent_id` or generate new name, retry
- 503/504: exponential backoff, max 3 retries
- Always parse `detail` + `reason` from error responses
- Full diagnosis → [common-errors.md](common-errors.md)

## Demo Projects

See [sample-repos.md](sample-repos.md) for the maintained ConvoAI sample registry.

## Docs Fallback

If fetch fails: https://doc.shengwang.cn/doc/convoai/restful/get-started/quick-start
