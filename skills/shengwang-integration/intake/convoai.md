# ConvoAI Detail Collection

Reached from [intake](README.md) after ConvoAI is identified as the primary product.
This file is for ConvoAI-specific follow-up only.

## Language Detection

Detect the user's language from their most recent message:
- If the user writes in **Chinese** → use the **ZH** prompts below
- If the user writes in **English** (or any other language) → use the **EN** prompts below

Maintain the detected language consistently throughout the entire intake flow.

## Prerequisites

Before starting, the user should have:
- Completed the main kickoff intake
- A clear use case description
- Platform / client-stack context already collected if relevant
- Backend language already collected if relevant

## Questions

**Fast-path rule:** If the user's initial description already contains 3+ of the following
(credentials status, LLM choice, TTS choice, ASR preference), skip individual questions.
Instead, generate the structured spec directly from what they said, fill defaults for anything
missing, and present it for confirmation.

Ask **one at a time** only when needed. Skip any question the user already answered during main intake.
Doc index status is already determined by the main intake — do not re-check here.

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
> - E. OpenAI（openai）
> - F. 用默认的就行

**EN:**
> "Which LLM would you like to use?"
> - A. Alibaba Cloud (aliyun)
> - B. ByteDance (bytedance)
> - C. DeepSeek (deepseek)
> - D. Tencent (tencent)
> - E. OpenAI (openai)
> - F. Use the default

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

### Q4 — ASR Vendor

Most users should use the default (Agora Fengming). Only ask if the user mentions a specific ASR preference.

**ZH:**
> "你想用哪个 ASR（语音识别）？"
> - A. 声网凤鸣（fengming）— 默认
> - B. 腾讯（tencent）
> - C. 微软（microsoft）
> - D. 科大讯飞（xfyun）
> - E. 科大讯飞大模型（xfyun_bigmodel）
> - F. 科大讯飞方言（xfyun_dialect）
> - G. 用默认的就行

**EN:**
> "Which ASR (speech recognition) provider would you like to use?"
> - A. Agora Fengming (fengming) — default
> - B. Tencent (tencent)
> - C. Microsoft (microsoft)
> - D. iFlytek (xfyun)
> - E. iFlytek BigModel (xfyun_bigmodel)
> - F. iFlytek Dialect (xfyun_dialect)
> - G. Use the default

**Default:** fengming

> Unless the user explicitly asks for a different ASR vendor, skip this question and use the default.

### Q5 — ASR Language

If the user's use case clearly involves a specific language (e.g. "英文客服", "English support bot"), infer the ASR language automatically and skip this question.

Otherwise ask:

**ZH:**
> "用户主要说什么语言？"
> - A. 中文（zh-CN，支持中英混合）
> - B. 英文（en-US）
> - C. 其他（请说明）

**EN:**
> "What language will users primarily speak?"
> - A. Chinese (zh-CN, supports Chinese-English mix)
> - B. English (en-US)
> - C. Other (please specify)

**Default:** zh-CN

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
ASR 语言：        [zh-CN / en-US / ja-JP / ko-KR / ...]
LLM：             [aliyun / bytedance / deepseek / tencent / openai]
TTS：             [bytedance (default) / minimax / tencent / microsoft / cosyvoice / stepfun]
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
ASR Language:     [zh-CN / en-US / ja-JP / ko-KR / ...]
LLM:              [aliyun / bytedance / deepseek / tencent / openai]
TTS:              [bytedance (default) / minimax / tencent / microsoft / cosyvoice / stepfun]
─────────────────────────────
```

The backend language should come from the main kickoff summary rather than this file.

## Defaults

| Field | Default | Notes (ZH) | Notes (EN) |
|-------|---------|------------|------------|
| App Certificate | Not enabled | 如果用户不确定，按未开启处理，提醒后续开启需改传 Token | If user is unsure, treat as not enabled; remind them to pass Token if enabled later |
| ASR vendor | `fengming` | 声网凤鸣 ASR | Agora Fengming ASR |
| ASR language | `zh-CN` | 中文（支持中英混合）；根据用户场景推断，英文场景用 `en-US` | Chinese (supports Chinese-English mix); infer from use case, use `en-US` for English scenarios |
| LLM vendor | `deepseek` | 如用户选默认则使用此值 | Used when user picks default |
| TTS vendor | `bytedance` | 火山引擎 TTS | Volcengine TTS |

> ASR/TTS/LLM valid values come from the /join API docs — run `bash skills/shengwang-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/convoai/operations/start-agent"` for the /join schema and vendor params. Do not invent values.

## Route After Collection

Pass the structured spec to [conversational-ai](../references/conversational-ai/README.md).
The product module will use the spec to fetch the right docs and generate code.

Key routing hints:
- Dev = Go → run `bash skills/shengwang-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start-go"`
- Dev = Java → run `bash skills/shengwang-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start-java"`
- Dev = Python/curl → run `bash skills/shengwang-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start"`
- App Certificate = Enabled → also run [token-server](../references/token-server/README.md)
- If fetch fails → use Generation Rules + fallback URL
