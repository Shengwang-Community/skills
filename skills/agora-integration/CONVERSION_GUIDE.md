# Shengwang → Agora Conversion Guide

This document describes how to create `skills/agora-integration/` from `skills/shengwang-integration/`.
The Agora version is NOT a 1:1 copy — it has its own branding, URLs, MCP endpoint,
vendor lists (overseas providers), and language (English-only for intake flow and descriptions).

## 1. Directory Structure

### Source (shengwang)
```
skills/shengwang-integration/
├── SKILL.md
├── mcp-tools.md
├── intake/
│   ├── SKILL.md
│   └── convoai.md
├── general/
│   ├── SKILL.md
│   └── references/
│       ├── authentication.md
│       └── credentials.md
├── integrate-shengwang-conversational-ai/
│   ├── SKILL.md
│   ├── concepts/
│   │   ├── architecture.md
│   │   └── authentication.md
│   ├── references/
│   │   ├── convoai-restapi.yaml
│   │   └── system-prompt-templates.md
│   └── troubleshooting/
│       └── common-errors.md
├── integrate-shengwang-rtc/
│   └── SKILL.md
├── integrate-shengwang-rtm/
│   └── SKILL.md
├── integrate-shengwang-cloud-recording/
│   └── SKILL.md
├── implement-shengwang-token-on-server/
│   ├── SKILL.md
│   └── references/
│       ├── api-spec.md
│       └── sdk-urls.md
└── resource-downloader/
    ├── SKILL.md
    └── scripts/
        └── downloader.py
```

### Target (agora)
```
skills/agora-integration/
├── SKILL.md
├── mcp-tools.md
├── intake/
│   ├── SKILL.md
│   └── convoai.md
├── general/
│   ├── SKILL.md
│   └── references/
│       ├── authentication.md
│       └── credentials.md
├── integrate-agora-conversational-ai/
│   ├── SKILL.md
│   ├── concepts/
│   │   ├── architecture.md
│   │   └── authentication.md
│   ├── references/
│   │   ├── convoai-restapi.yaml
│   │   └── system-prompt-templates.md
│   └── troubleshooting/
│       └── common-errors.md
├── integrate-agora-rtc/
│   └── SKILL.md
├── integrate-agora-rtm/
│   └── SKILL.md
├── integrate-agora-cloud-recording/
│   └── SKILL.md
├── implement-agora-token-on-server/
│   ├── SKILL.md
│   └── references/
│       ├── api-spec.md
│       └── sdk-urls.md
└── resource-downloader/
    ├── SKILL.md
    └── scripts/
        └── downloader.py
```

## 2. Branding Replacements (all .md and .yaml files)

Apply in order (longest match first to avoid partial replacements):

| # | Find | Replace With | Notes |
|---|------|-------------|-------|
| 1 | `Shengwang (Agora)` | `Agora` | Remove dual branding |
| 2 | `Shengwang-Community` | `AgoraIO-Community` | GitHub org |
| 3 | `shengwang-integration` | `agora-integration` | Skill name + paths |
| 4 | `shengwang-intake` | `agora-intake` | Skill name |
| 5 | `shengwang-general` | `agora-general` | Skill name |
| 6 | `shengwang-resource-downloader` | `agora-resource-downloader` | Skill name |
| 7 | `integrate-shengwang-` | `integrate-agora-` | Sub-directory refs |
| 8 | `implement-shengwang-` | `implement-agora-` | Sub-directory refs |
| 9 | `shengwang-skills` | `agora-skills` | Downloader script path |
| 10 | `author: shengwang` | `author: agora` | YAML front-matter |
| 11 | `# Shengwang ` | `# Agora ` | Markdown headings |
| 12 | `Shengwang Console` | `Agora Console` | UI references |
| 13 | `Shengwang` | `Agora` | Catch-all for remaining |

## 3. Domain Replacements

| Find | Replace With | Notes |
|------|-------------|-------|
| `console.shengwang.cn` | `console.agora.io` | Agora Console URL |
| `doc.shengwang.cn` | `doc.agora.io` | Documentation site |
| `doc-mcp.shengwang.cn` | `doc-mcp.agora.io` | MCP endpoint |

## 4. Chinese Text Replacements

| Find | Replace With | Notes |
|------|-------------|-------|
| `声网` | `Agora` | Chinese brand name — replace everywhere |
| `Shengwang, Agora, 声网,` in trigger keyword lists | `Agora,` | Simplify trigger keywords for Agora version |

## 5. MCP Endpoint Difference

The shengwang version uses `https://doc-mcp.shengwang.cn/mcp`.
The Agora version uses `https://doc-mcp.agora.io/mcp`.

This affects:
- `mcp-tools.md` — MCP endpoint declaration
- `intake/convoai.md` — Q5 MCP auto-install config block

The MCP config block in `intake/convoai.md` Q5 should read:
```json
{
  "mcpServers": {
    "agora-docs": {
      "type": "sse",
      "url": "https://doc-mcp.agora.io/mcp"
    }
  }
}
```

## 6. convoai-restapi.yaml

This file contains Chinese API documentation text with `doc.shengwang.cn` URLs and `声网` references.
Apply the same domain and branding replacements (Section 3 + 4) for consistency.

## 7. No Changes Needed

These are already Agora-branded and remain unchanged:
- `api.agora.io` — API base URL (already correct)
- `github.com/AgoraIO-Community` — GitHub org (already correct)
- `github.com/AgoraIO/Tools` — Token builder repo (already correct)
- `AGORA_APP_ID`, `AGORA_CUSTOMER_KEY`, etc. — Env var names (already correct)
- MCP doc URIs (`docs://default/...`) — Internal doc paths (already correct)
- `downloader.py` — No shengwang references in code

## 8. TTS / LLM / ASR Vendor Replacement (Overseas Providers)

The shengwang version targets Chinese domestic vendors. The Agora version must use overseas/international vendors.

### LLM Vendors

| Shengwang (domestic) | Agora (overseas) |
|---------------------|-----------------|
| `aliyun` (阿里云) | `openai` (OpenAI) |
| `bytedance` (字节跳动) | `openai` (OpenAI) — or user's choice |
| `deepseek` (深度求索) | `openai` (OpenAI) |
| `tencent` (腾讯) | `anthropic` (Anthropic) — or user's choice |

Agora `intake/convoai.md` Q2 should read:
```
"Which LLM would you like to use?"
- A. OpenAI (openai)
- B. Anthropic (anthropic)
- C. Google Gemini (gemini)
- D. DeepSeek (deepseek)
- E. Use the default

Default: openai
```

### TTS Vendors

| Shengwang (domestic) | Agora (overseas) |
|---------------------|-----------------|
| `bytedance` / 火山引擎 | `microsoft` (Azure TTS) |
| `minimax` | `elevenlabs` (ElevenLabs) |
| `tencent` | `microsoft` (Azure TTS) |
| `cosyvoice` (阿里) | `elevenlabs` (ElevenLabs) |
| `stepfun` (阶跃星辰) | — (remove) |

Agora `intake/convoai.md` Q3 should read:
```
"Which TTS (text-to-speech) provider would you like to use?"
- A. Microsoft Azure TTS (microsoft)
- B. ElevenLabs (elevenlabs)
- C. Use the default

Default: microsoft (Azure TTS)
```

### ASR Defaults

| Field | Shengwang | Agora |
|-------|-----------|-------|
| ASR vendor | `fengming` (Agora Fengming) | `fengming` (same — Agora's own ASR) |
| ASR language | `zh-CN` | `en-US` |

### Structured Spec Output (Agora version)

```
ConvoAI Spec
─────────────────────────────
Credentials:      [Ready / Need to create]
App Certificate:  [Enabled / Not enabled]
Token:            [Need to generate / Empty string]
ASR:              [fengming (default) / microsoft]
LLM:              [openai (default) / anthropic / gemini / deepseek]
TTS:              [microsoft (default) / elevenlabs]
Dev Language:     [Go / Java / Python/curl]
MCP Status:       [Installed / Not installed]
─────────────────────────────
```

### Defaults Table (Agora version)

| Field | Default | Notes |
|-------|---------|-------|
| App Certificate | Not enabled | If user is unsure, treat as not enabled; remind them to pass Token if enabled later |
| ASR vendor | `fengming` | Agora Fengming ASR, default en-US |
| ASR language | `en-US` | English |
| LLM vendor | `openai` | Requires user to provide OpenAI-compatible LLM URL |
| TTS vendor | `microsoft` | Microsoft Azure TTS |
| MCP | Not installed | Auto-install config; fall back to local OpenAPI spec if install fails |

## 9. Intake Flow & Descriptions — Full English Conversion

The shengwang version has Chinese prompts, examples, and descriptions.
The Agora version must be fully English. This is NOT a simple find-replace — each file needs its own English content.

### Files requiring full English rewrite

#### `SKILL.md` (root router)

- `description`: Remove `声网`, `Shengwang`, Chinese trigger words (`"我想做一个"`, `"帮我接入"`)
- Agora description:
  ```yaml
  description: |
    Integrate Agora products: ConvoAI voice agents, RTC audio/video,
    RTM messaging, Cloud Recording, and token generation. Use when the user
    mentions Agora, ConvoAI, RTC, RTM, voice agent, AI agent,
    video call, live streaming, recording, token, or any Agora product task.
  ```
- Skip/route examples: replace Chinese examples with English equivalents
  - `"帮我停掉 agent_abc123"` → `"stop agent agent_abc123"`
  - `"生成一个 RTC token，Go 语言"` → `"generate an RTC token in Go"`
  - `"error 403 是什么意思"` → `"what does error 403 mean"`
  - `"下载 ConvoAI Go SDK"` → `"download ConvoAI Go SDK"`
  - `"我想做一个 AI 客服"` → `"I want to build an AI customer service bot"`
  - `"帮我接入 ConvoAI"` → `"help me integrate ConvoAI"`
  - `"我想做视频通话 + AI 助手"` → `"I want video call + AI assistant"`
- Links section:
  ```
  - Console: https://console.agora.io/
  - Docs: https://doc.agora.io/
  - GitHub: https://github.com/AgoraIO-Community
  ```

#### `intake/SKILL.md`

- `name`: `agora-intake`
- `description`: Full English, remove `声网`, `Shengwang`, Chinese triggers
  ```yaml
  description: |
    First skill to run for any Agora-related request. Understands
    the full product landscape, identifies user needs, recommends the optimal
    product combination, and routes to product-specific intake or skill.
    Use when the user mentions Agora, or describes any real-time
    communication / AI use case such as voice agent, video call, live streaming,
    chat, recording, ConvoAI, RTC, RTM.
  ```
- Title: `# Agora Intake — Product Routing & Needs Analysis`
- Product Landscape "Typical user says" column: English only
  - `"视频通话", "直播"` → `"video call", "live streaming"`
  - `"聊天", "消息"` → `"chat", "messaging", "signaling"`
  - `"AI语音", "voice bot", "对话式AI"` → `"voice bot", "AI agent", "conversational AI"`
  - `"录制", "recording"` → `"recording", "archive"`
  - `"拉流"` → `"media inject"`
  - `"推流到CDN"` → `"RTMP push", "CDN push"`
- Step 1 prompt: `"What are you trying to build? Please describe your use case."`
- Step 2 example:
  ```
  User: "I want to build an AI customer service bot that auto-answers calls"
  - Primary: ConvoAI (AI voice agent)
  - Supporting: RTC SDK (client-side for user to join channel)
  - Optional: Cloud Recording (record conversations for QA), RTM (send chat transcript)
  ```
- Step 3 confirmation template:
  ```
  Needs Analysis:
  ─────────────────────────────
  Use case:         [user's description]
  Primary product:  [primary product]
  Supporting:       [supporting products]
  Optional:         [optional products]
  ─────────────────────────────

  Does this look right? Anything to adjust?
  ```
- Decision Shortcuts: English only
  - `"接入ConvoAI"` → `"integrate ConvoAI"` / `"build voice bot"`
  - `"视频通话"` → `"video call"` / `"live streaming"`
  - `"聊天"` → `"chat"` / `"messaging"`
  - `"录制"` → `"recording"`
  - `"生成token"` → `"generate token"` / `"token server"`
  - `"下载SDK"` → `"download SDK"`

#### `intake/convoai.md`

- All question prompts in English (see Section 8 for Q2/Q3 vendor lists)
- Q1:
  ```
  "Do you have an Agora account and project credentials?"
  Required:
  - AppID — project identifier
  - Customer Key + Customer Secret — REST API auth
  - App Certificate — is it enabled?

  Options:
  - A. All ready, App Certificate is enabled
  - B. All ready, App Certificate is not enabled (or unsure)
  - C. Have an account but haven't created a project yet
  - D. Don't have an account yet
  ```
- Q1 responses in English:
  - If A: "App Certificate is enabled. ConvoAI requires an RTC Token when creating an agent. I'll help you generate one later — you'll need the `AGORA_APP_CERTIFICATE` env var."
  - If B: "If you enable App Certificate later in Console, you'll need to start passing a Token, otherwise the agent will fail to join the channel."
  - If C/D: direct to `https://console.agora.io/`
- Q4: `"What language are you using for the backend?"`
- Q5 prompts in English:
  - "Detected that Agora Doc MCP Server is not installed. Let me configure it for you..."
  - "Agora Doc MCP Server config added. MCP will auto-reconnect shortly."
- Structured spec output: English (see Section 8)
- Defaults table: English (see Section 8)
- Route After Collection table: English labels
  - `App Certificate = 已开启` → `App Certificate = Enabled`
  - `MCP = 未安装` → `MCP = Not installed`

#### Sub-skill descriptions (YAML front-matter `description` field)

Each sub-skill's `description` must be English-only. Remove Chinese trigger words.

| File | Agora `description` |
|------|-------------------|
| `integrate-agora-conversational-ai/SKILL.md` | `Guides integration of Agora ConvoAI — real-time voice AI agents. Handles agent lifecycle operations (create/stop/update/query/list) and code generation for Go, Java, and REST API (curl/Python/JS). Use when the user asks to create, stop, update, or query a ConvoAI agent, or mentions convoai, voice bot, conversational AI.` |
| `integrate-agora-rtc/SKILL.md` | `Guides integration of Agora RTC SDK for real-time audio/video communication. Covers Web, Android, iOS, and other platforms. Use when the user asks about video calls, live streaming, voice calls, or any real-time audio/video feature.` |
| `integrate-agora-rtm/SKILL.md` | `Guides integration of Agora RTM (Real-Time Messaging) SDK for signaling, messaging, presence, and pub/sub features. Use when the user asks about chat, messaging, signaling, notifications, presence, or real-time data sync.` |
| `integrate-agora-cloud-recording/SKILL.md` | `Guides integration of Agora Cloud Recording for server-side recording of RTC sessions. Covers acquire/start/stop/query lifecycle. Use when the user asks about recording video calls, archiving sessions, or server-side recording.` |
| `implement-agora-token-on-server/SKILL.md` | `Implements Agora Token generation on backend servers using AgoraDynamicKey. Use when the user asks to generate a Token, implement a token API endpoint, set up server-side authentication for RTC, RTM, or ConvoAI, or mentions AccessToken2, AgoraDynamicKey, token auth.` |
| `resource-downloader/SKILL.md` | `Downloads Agora SDKs, sample projects, Token Builder libraries, and GitHub repositories. Use when the user asks to download an SDK, clone a sample project, get the Token Builder, or fetch any related resource from GitHub or a direct URL.` |
| `general/SKILL.md` | `Agora platform general knowledge: credentials setup and REST API authentication patterns. Use when the user asks about AppID, Customer Key/Secret, App Certificate, or REST Basic Auth.` |

#### ConvoAI SKILL.md body text

- Title: `# Agora Conversational AI Engine (ConvoAI)`
- MCP fallback URL: `https://doc.agora.io/doc/convoai/restful/get-started/quick-start`
- Console link: `[Agora Console](https://console.agora.io/)`
- Remove Chinese trigger words from description (`AI语音助手`, `对话式AI`)

#### Other sub-skill body text

- RTC fallback URL: `https://doc.agora.io/doc/rtc/javascript/get-started/quick-start`
- RTM fallback URL: `https://doc.agora.io/doc/rtm2/javascript/get-started/quick-start`
- Cloud Recording fallback URL: `https://doc.agora.io/doc/cloud-recording/restful/get-started/quick-start`
- Token server official docs: `https://doc.agora.io/doc/rtc/android/basic-features/token-authentication`
- All `[Shengwang Console](https://console.shengwang.cn/)` → `[Agora Console](https://console.agora.io/)`

## 10. Execution Order

1. Copy entire `skills/shengwang-integration/` → `skills/agora-integration/`
2. Rename sub-directories inside `agora-integration/` (Section 1)
3. Apply text replacements in all `.md` and `.yaml` files (Sections 2, 3, 4 — longest first)
4. Apply vendor replacements (Section 8) — rewrite Q2, Q3, defaults table in `intake/convoai.md`
5. Rewrite intake flow and descriptions to English (Section 9) — NOT automated, each file needs manual English content
6. Verify: `grep -ri shengwang skills/agora-integration/` should return 0 results
7. Verify: `grep -ri 声网 skills/agora-integration/` should return 0 results
8. Verify: no Chinese text remains in intake flow prompts or YAML descriptions
