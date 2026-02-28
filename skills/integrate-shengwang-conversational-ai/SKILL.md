---
name: integrate-shengwang-conversational-ai
description: |
  Guides integration of Shengwang (Agora) ConvoAI — real-time voice AI agents.
  Handles agent lifecycle operations (create/stop/update/query/list)
  and code generation for Go, Java, and REST API (curl/Python/JS).
triggers:
  - "join agent"
  - "create agent"
  - "stop agent"
  - "update agent"
  - "query agent"
  - "list agents"
  - "agent speak"
  - "interrupt agent"
  - "convoai api"
  - "convoai restapi"
metadata:
  author: shengwang
  version: "5.2.0"
---

# Shengwang Conversational AI Engine (ConvoAI)

## Routing Guardrails

> **STOP — Check before proceeding:**
> No structured spec and no confirmed product selection?
> → Redirect to [intake/SKILL.md](../intake/SKILL.md) first.
> Do NOT start building just because the user said "AI agent" or "voice bot".

- From intake with structured spec → skip to Workflow step 2.
- Skip-intake fast path (specific operation/troubleshooting with enough details) → proceed directly.

---

## Resource Lookup

| Priority | Source | Use for |
|----------|--------|---------|
| 1 | [references/convoai-restapi.yaml](references/convoai-restapi.yaml) | API endpoints, field definitions, vendor params (AUTHORITATIVE) |
| 2 | Generation Rules (below) | Field type gotchas, naming, error handling — things the spec can't express |
| 3 | MCP Quick Start (see table below) | **MUST fetch before generating code** — runnable examples, integration flow |
| 4 | MCP `search-docs` → `get-doc-content` | Everything else (release notes, advanced guides, non-ConvoAI topics) |

**Decision:** Local files (1+2) first. Need working code → must call MCP (3). Topic outside ConvoAI → MCP search (4).

### Quick Start URIs (MCP)

| Language | URI |
|----------|-----|
| Python / JS / curl | `docs://default/convoai/restful/get-started/quick-start` |
| Go | `docs://default/convoai/restful/get-started/quick-start-go` |
| Java | `docs://default/convoai/restful/get-started/quick-start-java` |

**MCP fallback:** If unavailable, use OpenAPI spec + Generation Rules, and tell the user to verify against https://doc.shengwang.cn/doc/convoai/restful/get-started/quick-start

---

## Workflow

### Step 1: Confirm Credentials & Service Activation

Need `AGORA_APP_ID`, `AGORA_CUSTOMER_KEY`, `AGORA_CUSTOMER_SECRET`.
Missing? → [general/references/credentials.md](../general/references/credentials.md)

> **ConvoAI requires separate activation.** The user must enable ConvoAI for their project in [Agora Console](https://console.agora.io/), otherwise API calls return 403.
> Details → [concepts/authentication.md](concepts/authentication.md#enabling-convoai-service)

Need Go/Java SDK or AgoraDynamicKey? → [resource-downloader/SKILL.md](../resource-downloader/SKILL.md)

### Step 2: Fetch Quick Start via MCP (MANDATORY)

Call `get-doc-content` with the URI matching the user's dev language (table above).
Read the returned doc fully before writing any code.

### Step 3: Generate Code

1. Quick start doc as primary code reference
2. Consult OpenAPI spec for detailed field definitions
3. Apply Generation Rules (below)
4. Apply user's intake spec (language, LLM, TTS vendor, etc.)

### Step 4: Validate

- [ ] Credentials from env vars, never hardcoded
- [ ] `agent_rtc_uid` is string `"0"`, not int `0`
- [ ] `remote_rtc_uids` is `["*"]`, not `"*"`
- [ ] `name` has random suffix (`agent_{uuid[:8]}`) to avoid 409
- [ ] Error handling covers 409 and 503/504
- [ ] TTS/ASR params match vendor schema in OpenAPI spec

---

## Quick Reference

**Architecture:**
`User Voice → RTC Channel → ASR → LLM → TTS → RTC Channel → User hears AI`
Agent joins RTC channel via REST API (no client-side SDK for the agent).
Details → [concepts/architecture.md](concepts/architecture.md)

**Auth:** HTTP Basic Auth on all ConvoAI REST calls:
`Authorization: Basic base64("{CUSTOMER_KEY}:{CUSTOMER_SECRET}")`
Details → [concepts/authentication.md](concepts/authentication.md)

**Base URL:** `https://api.agora.io/cn/api/conversational-ai-agent/v2/projects/{AGORA_APP_ID}`

---

## Generation Rules

Stable constraints that do NOT change with API updates. Always apply.

### Field Types
- `agent_rtc_uid`: STRING `"0"`, not int `0`
- `remote_rtc_uids`: array `["*"]`, not `"*"`
- `name`: unique per project — use `agent_{uuid[:8]}`

### Create Agent
- `token`: `""` if no App Certificate; otherwise RTC token builder
- `agent_rtc_uid`: `"0"` for auto-assign
- `remote_rtc_uids`: `["*"]` unless user specifies UIDs

### Update Agent
- `llm.params` is FULLY REPLACED — always send complete object
- Only `token` and `llm` are updatable; everything else is immutable

### Terminology
- `agentId` in URL paths (`/agents/{agentId}/leave`) = `agent_id` in JSON bodies
- `/join` returns `agent_id` (snake_case); use it as path param

### Error Handling
- 409: extract existing `agent_id` or generate new name, retry
- 503/504: exponential backoff, max 3 retries
- Always parse `detail` + `reason` from error responses
- Diagnosis → [troubleshooting/common-errors.md](troubleshooting/common-errors.md)
