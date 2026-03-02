---
name: convoai-intake
description: |
  Collects ConvoAI-specific implementation details after the main intake has
  identified ConvoAI as the target product. Outputs a structured spec that
  drives code generation in integrate-shengwang-conversational-ai/SKILL.md.
---

# ConvoAI Detail Collection

Reached from [intake/SKILL.md](../SKILL.md) after ConvoAI is identified as the primary product.

## Language Detection

Detect the user's language from their most recent message:
- If the user writes in **Chinese** → use the **ZH** prompts below
- If the user writes in **English** (or any other language) → use the **EN** prompts below

Maintain the detected language consistently throughout the entire intake flow.

## Prerequisites

Before starting, the user should have:
- Confirmed ConvoAI is the right product (via main intake)
- A clear use case description

## Questions

**Fast-path rule:** If the user's initial description already contains 3+ of the following
(credentials status, LLM choice, TTS choice, dev language), skip individual questions.
Instead, generate the structured spec directly from what they said, fill defaults for anything
missing, and present it for confirmation.

Ask **one at a time** only when needed. Skip any question the user already answered during main intake.

### Q1 — Credentials & App Certificate

**ZH:**
> "你有 Agora 账号和项目凭证吗？"
>
> 需要以下信息：
> - `AppID` — 项目标识
> - `Customer Key` + `Customer Secret` — REST API 认证
> - `App Certificate` — 是否已开启？
>
> 选择：
> - A. 都准备好了，App Certificate 已开启
> - B. 都准备好了，App Certificate 未开启（或不确定）
> - C. 有账号但还没创建项目
> - D. 还没有账号

**EN:**
> "Do you have an Agora account and project credentials?"
>
> Required:
> - `AppID` — project identifier
> - `Customer Key` + `Customer Secret` — REST API auth
> - `App Certificate` — is it enabled?
>
> Options:
> - A. All ready, App Certificate is enabled
> - B. All ready, App Certificate is not enabled (or unsure)
> - C. Have an account but haven't created a project yet
> - D. Don't have an account yet

**If A** → Record `certificate = enabled`, token generation needed later.

| | Prompt |
|---|--------|
| ZH | "App Certificate 已开启，ConvoAI 创建 agent 时需要传入 RTC Token。我会在后续帮你生成 Token，需要用到 `AGORA_APP_CERTIFICATE` 环境变量。" |
| EN | "App Certificate is enabled. ConvoAI requires an RTC Token when creating an agent. I'll help you generate one later — you'll need the `AGORA_APP_CERTIFICATE` env var." |

**If B** → Record `certificate = not enabled`, token = empty string.

| | Prompt |
|---|--------|
| ZH | "如果后续在 Console 开启了 App Certificate，就需要改为传入 Token，否则 agent 会加入频道失败。" |
| EN | "If you enable App Certificate later in Console, you'll need to start passing a Token, otherwise the agent will fail to join the channel." |

**If C or D** → Direct to https://console.shengwang.cn/ and pause until ready.

### Q2 — LLM

**ZH:**
> "你打算用哪个 LLM？"
> - A. 阿里云（aliyun）
> - B. 字节跳动（bytedance）
> - C. 深度求索（deepseek）
> - D. 腾讯（tencent）
> - E. 用默认的就行

**EN:**
> "Which LLM would you like to use?"
> - A. Alibaba Cloud (aliyun)
> - B. ByteDance (bytedance)
> - C. DeepSeek (deepseek)
> - D. Tencent (tencent)
> - E. Use the default

**Default:** deepseek

### Q3 — TTS

**ZH:**
> "你打算用哪个 TTS（语音合成）？"
> - A. 字节跳动 / 火山引擎（bytedance）
> - B. 微软（microsoft）
> - C. MiniMax（minimax）
> - D. 阿里 CosyVoice（cosyvoice）
> - E. 腾讯（tencent）
> - F. 阶跃星辰（stepfun）
> - G. 用默认的就行

**EN:**
> "Which TTS (text-to-speech) provider would you like to use?"
> - A. ByteDance / Volcengine (bytedance)
> - B. Microsoft (microsoft)
> - C. MiniMax (minimax)
> - D. Alibaba CosyVoice (cosyvoice)
> - E. Tencent (tencent)
> - F. StepFun (stepfun)
> - G. Use the default

**Default:** bytedance (Volcengine TTS)

### Q4 — Development language

**ZH:**
> "你用什么语言开发服务端？"

**EN:**
> "What language are you using for the backend?"

Options (same for both):
> - A. Go
> - B. Java
> - C. Python / JavaScript / curl

### Q5 — MCP Status

Try calling MCP tool `search-docs {"query": "convoai"}` to detect if MCP is available.

**If MCP call succeeds** → Record `MCP = installed`, skip this question.

**If MCP call fails or unavailable** → Help the user install Agora Doc MCP Server:

1. Inform the user:

| | Prompt |
|---|--------|
| ZH | "检测到你还没有安装 Agora Doc MCP Server，我来帮你配置。这个 MCP 可以获取最新的 API 文档，对后续开发很有帮助。" |
| EN | "Detected that Agora Doc MCP Server is not installed. Let me configure it for you — it provides access to the latest API docs and will be helpful for development." |

2. Read the workspace MCP config file `.kiro/settings/mcp.json` (if it exists), append the following to `mcpServers` (do not overwrite existing servers):
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

3. After writing the config:

| | Prompt |
|---|--------|
| ZH | "已添加 Agora Doc MCP Server 配置。MCP 会自动重连，稍等片刻即可生效。" |
| EN | "Agora Doc MCP Server config added. MCP will auto-reconnect shortly." |

4. Wait briefly, then retry the MCP tool call to verify. If it still fails, prompt the user to check the config or restart the IDE, then continue with local reference docs.

Record MCP status — it affects the doc-fetching strategy during code generation.

---

## Output: Structured Spec

**ZH:**
```
ConvoAI 需求规格
─────────────────────────────
凭证状态：        [已就绪 / 需先创建]
App Certificate： [已开启 / 未开启]
Token：           [需要生成 / 空字符串]
ASR：             [fengming (default) / tencent / microsoft / xfyun / xfyun_bigmodel / xfyun_dialect]
LLM：             [aliyun / bytedance / deepseek / tencent]
TTS：             [bytedance (default) / minimax / tencent / microsoft / cosyvoice / stepfun]
开发语言：        [Go / Java / Python/curl]
MCP 状态：        [已安装 / 未安装]
─────────────────────────────
```

**EN:**
```
ConvoAI Spec
─────────────────────────────
Credentials:      [Ready / Need to create]
App Certificate:  [Enabled / Not enabled]
Token:            [Need to generate / Empty string]
ASR:              [fengming (default) / tencent / microsoft / xfyun / xfyun_bigmodel / xfyun_dialect]
LLM:              [aliyun / bytedance / deepseek / tencent]
TTS:              [bytedance (default) / minimax / tencent / microsoft / cosyvoice / stepfun]
Dev Language:     [Go / Java / Python/curl]
MCP Status:       [Installed / Not installed]
─────────────────────────────
```

## Defaults

| Field | Default | Notes (ZH) | Notes (EN) |
|-------|---------|------------|------------|
| App Certificate | Not enabled | 如果用户不确定，按未开启处理，提醒后续开启需改传 Token | If user is unsure, treat as not enabled; remind them to pass Token if enabled later |
| ASR vendor | `fengming` | 声网凤鸣 ASR，默认 zh-CN | Agora Fengming ASR, default zh-CN |
| ASR language | `zh-CN` | 中文（支持中英混合） | Chinese (supports Chinese-English mix) |
| LLM vendor | `deepseek` | 如用户选 E 则使用此默认值 | Used when user picks E (default) |
| TTS vendor | `bytedance` | 火山引擎 TTS | Volcengine TTS |
| MCP | Not installed | 自动帮用户安装配置，安装失败时降级到本地 OpenAPI spec + fallback URL | Auto-install config; fall back to local OpenAPI spec if install fails |

> ASR/TTS/LLM valid values come from [convoai-restapi.yaml](../integrate-shengwang-conversational-ai/references/convoai-restapi.yaml) — do not invent values.

## Route After Collection

Pass the structured spec to [integrate-shengwang-conversational-ai/SKILL.md](../integrate-shengwang-conversational-ai/SKILL.md),
skipping questions already answered.

| Detail | Routing hint |
|--------|-------------|
| Dev = Go | ConvoAI SKILL.md → MCP `get-doc-content {"uri": "docs://default/convoai/restful/get-started/quick-start-go"}` |
| Dev = Java | ConvoAI SKILL.md → MCP `get-doc-content {"uri": "docs://default/convoai/restful/get-started/quick-start-java"}` |
| Dev = Python/curl | ConvoAI SKILL.md → MCP `get-doc-content {"uri": "docs://default/convoai/restful/get-started/quick-start"}` |
| App Certificate = Enabled | [implement-shengwang-token-on-server/SKILL.md](../implement-shengwang-token-on-server/SKILL.md) to generate RTC Token |
| Needs Go/Java SDK | [resource-downloader/SKILL.md](../resource-downloader/SKILL.md) to download REST client SDK |
| Needs Token Builder | [resource-downloader/SKILL.md](../resource-downloader/SKILL.md) to download AgoraDynamicKey |
| MCP = Not installed | Use local OpenAPI spec + Generation Rules, add fallback URL in output |
