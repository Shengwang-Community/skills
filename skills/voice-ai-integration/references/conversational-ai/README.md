# Shengwang Conversational AI Engine (ConvoAI)

Real-time AI voice agent. User speaks into an RTC channel, agent responds via ASR → LLM → TTS pipeline.

## How It Works

```
User Device ── audio ──► RTC Channel ──► ConvoAI Agent (ASR → LLM → TTS)
User Device ◄── audio ── RTC Channel ◄── ConvoAI Agent
```

- Agent is server-side only — managed via REST API, no client SDK
- Client should prefer `agora-agent-client-toolkit` when it fits the target stack; otherwise use the RTC SDK directly to join the channel
- `POST /join` makes the agent join the same RTC channel

## Default Integration Path

Use this order unless the user explicitly asks for something else:

1. Follow the matching official ConvoAI sample repo and preserve its structure
2. On the server side, prefer `agent-server-sdk`
3. On the client side, prefer `agora-agent-client-toolkit` when the target stack supports it; otherwise fall back to the RTC SDK directly
4. Use fetched Shengwang docs to fill in missing product details
5. Use raw REST directly only for unsupported operations, debugging, or explicit REST-first requests

Do not treat the REST quick start or endpoint index as the default architecture for a new ConvoAI integration when a matching sample or official SDK path already exists.

## Auth

ConvoAI REST API 支持两种鉴权方式，推荐使用 RTC Token：

1. **RTC Token（推荐）**：使用声网对话式 AI 引擎项目的 RTC Token
   - 传参示例：`Authorization: agora token="007abcxxxxxxx123"`
   - 测试环境：从[声网控制台](https://console.shengwang.cn/)生成临时 Token（有效期 24 小时）
   - 生产环境：部署 [token-server](../token-server/README.md) 生成 Token
   - 优势：只需要 `APP_ID` + `APP_CERTIFICATE`，与客户端 token 共用同一套凭证，无需额外配置 Customer Key/Secret

2. **Basic Auth（备选）**：使用 `SHENGWANG_CUSTOMER_KEY` + `SHENGWANG_CUSTOMER_SECRET` 生成 Base64 编码
   - 传参示例：`Authorization: Basic NDI1OTQ3N2I4MzYy...YwZjA=`
   - 参考[实现 HTTP 安全认证](https://doc.shengwang.cn/doc/convoai/restful/user-guides/http-basic-auth)
   - 仅在无法使用 RTC Token 时使用（例如纯服务端场景、无 App Certificate 等）

鉴权方式选择规则：
- 默认使用 RTC Token 方式，减少环境变量数量，与客户端 token 生成逻辑统一
- 仅在用户明确要求 Basic Auth、或项目不具备 App Certificate 时才使用 Basic Auth
- 使用 `agent-server-sdk` 时，SDK 内部自动处理 token 鉴权，无需手动构造 Authorization header

其他注意事项：
- ConvoAI requires separate activation in [Shengwang Console](https://console.shengwang.cn/) — 403 without it
- The `token` field in `/join` body is for the RTC channel, NOT for REST auth:
  - App Certificate not enabled → `""`
  - App Certificate enabled → generate via [token-server](../token-server/README.md)
- Do not ask about App Certificate during ConvoAI intake by default; confirm token handling later only if implementation is blocked or the user explicitly asks
- Credentials → [general/credentials-and-auth.md](../general/credentials-and-auth.md)

## Sample Repos

For reference projects and starter layouts, use [sample-repos.md](sample-repos.md).

When a matching ConvoAI sample repo exists for the requested stack, it is the default implementation reference.

Required workflow:
- Pick the relevant entry from `sample-repos.md`
- Clone the repo on demand with `git clone --depth 1 <repo-url>`
- Inspect the current stack, folder map, key files, env template files, and API surface
- Inspect the sample repo's actual env template files before coding, such as `.env.example`, `.env.local.example`, and similar sample-provided files
- Prefer `agent-server-sdk` on the server side and `agora-agent-client-toolkit` on the client side when the sample repo or target stack supports them, instead of building a direct REST integration from scratch
- Keep the implementation aligned with the sample repo's architecture, env var names discovered from those template files, dependency choices, and API shape
- Use Shengwang doc fetching only for missing API or product details that the sample repo does not cover
- Keep raw REST calls narrowly scoped to capabilities that are not covered by the chosen SDK or sample architecture

Multi-platform repo handling:
- If the matched sample repo is a multi-platform monorepo (indicated by "Multi-platform" in Default Stack):
  1. Clone the repo to a temporary path (e.g. `/tmp/convoai-native-full`)
  2. Read the repo's `AGENTS.md` to discover the directory layout and per-platform entrypoints
  3. Based on the user's confirmed platform, locate the corresponding subdirectory
  4. Copy only that subdirectory to a clean temporary path (e.g. `/tmp/convoai-native-ios`), then delete the full clone
  5. Inspect the extracted subdirectory's complete demo code (architecture, env templates, API calls, dependencies) — same as the Web workflow
  6. Locate the empty project template folder inside the extracted subdirectory (path specified in the repo's `AGENTS.md`)
  7. If the user's workspace already contains a project with build/project files for the target platform, skip the template copy and write business code directly into the user's existing project. Otherwise, copy the empty project template to the user's project as the starting point
  8. Referencing the complete demo code, write business code on top of the empty template — keep project/build files untouched, only write/modify the business code files indicated by the repo's `AGENTS.md`
  9. Apply the user's confirmed provider choices with a minimal diff, same as the Web workflow
- The repo's `AGENTS.md` is the source of truth for which directory maps to which platform, where the empty template is, and which files are business code vs project files
- If the repo's `AGENTS.md` does not list the requested platform, fall back to Shengwang doc fetching and `minimal-custom` mode

Implementation modes:
- `sample-aligned` is the default mode whenever a matching sample repo exists
- `minimal-custom` may only be used if the user explicitly asks for a minimal demo or says not to follow the sample repo

Alignment rules:
- Preserve the sample repo's env var names from the inspected env template files unless the user explicitly asks to rename or normalize them
- Preserve the sample repo's folder structure and backend/frontend boundaries unless the user explicitly asks for a redesign
- Preserve the sample repo's dependency choices and API shape by default; only swap what is necessary for the user's confirmed provider choices
- Prefer `agent-server-sdk` for server integration and `agora-agent-client-toolkit` for client integration when they cover the required behavior
- Use direct REST only for unsupported capability gaps, debugging, or when the user explicitly asks for raw REST
- Do not invent env names from memory or from this skill's static docs when the sample repo provides template files

Diff budget rule:
- Make only the minimum necessary changes for the user's confirmed provider choices
- Optional modules may be removed if they are not needed
- Do not redesign env naming, folder structure, and API shape all at once unless the user explicitly asks for a custom implementation

Before editing code, state:
- which sample repo is being followed
- whether `agent-server-sdk` and `agora-agent-client-toolkit` are being followed, or why a different SDK path or direct REST is required
- which env template files were inspected
- what exact differences will be introduced

REST docs are still the low-level reference for request/response schemas and unsupported operations, but they are not the default starting point when the sample repo or official libraries already cover the needed flow.

When the user asks how to integrate ConvoAI in general, recommend the sample path plus `agent-server-sdk` on the server and `agora-agent-client-toolkit` on the client when possible. Only propose a from-scratch REST build when the user explicitly asks for it or when the required capability is not covered by the sample and official libraries.

Keep repo URLs in `sample-repos.md` only so future URL changes stay centralized.

## Quick Start Docs

Fetch docs using the doc fetching script (see [doc-fetching.md](../doc-fetching.md)) only after checking the sample repo and official SDK path first:

| Language | Command |
|----------|---------|
| Python / JS / curl | `bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start"` |
| Go | `bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start-go"` |
| Java | `bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start-java"` |

API endpoint index → [convoai-restapi.md](convoai-restapi.md)

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
