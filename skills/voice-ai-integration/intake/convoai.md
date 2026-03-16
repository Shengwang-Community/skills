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

Use a friendly but explicit follow-up flow:
- Ask for all missing blocking fields in one consolidated message
- Keep the message short enough to scan, but complete enough to finish intake in one reply
- Skip anything the user already answered
- Show the available options and recommended default for each missing field
- If the user leaves a blocker unresolved, ask only a narrow repair follow-up for that field

Defaults policy:
- ASR vendor recommended default: `fengming`
- ASR language recommended default: `en-US` for clearly English scenarios, otherwise `zh-CN`
- LLM recommended default: `deepseek`
- TTS recommended default: `bytedance`

Blocking rule:
- Credentials status (Q1) must be explicitly answered or confirmed
- ASR vendor (Q4) must be explicitly answered or confirmed
- ASR language (Q5) must be explicitly answered or confirmed
- LLM provider (Q2) must be explicitly answered or confirmed
- TTS provider (Q3) must be explicitly answered or confirmed

"Use the default" counts as an explicit answer.
Silence, omission, or inference does NOT.

Ask the full missing-fields checklist first. Skip any question the user already answered during main intake
or in the user's initial request.
Doc index status is already determined by the main intake — do not re-check here.

## Consolidated Intake Message

When ConvoAI is the clear primary product, combine the missing kickoff fields and
the missing ConvoAI-specific questions into one message.

Message requirements:
- Use the user's language consistently
- Start with a one-line recap that ConvoAI requires RTC SDK on the client side
- Ask only for missing fields
- Under each missing field, show the supported options inline to reduce prompt height
- Number only the currently visible missing fields, starting from `1`
- Mark fields with defaults as optional
- Ask the user to reply once with numeric codes such as `1A 4B 6A`
- Do not mix this with a `key=value` quick-reply example in the same prompt
- Do not ask about account status, project creation, Customer Key/Secret, or App Certificate in this intake

If the user already provided enough detail for some fields, do not restate those
questions. Keep the option list only for the unresolved fields.

Numbering rules:
- Renumber based only on the fields shown in the current prompt
- Do not use stable global IDs across turns
- If a field is already known, omit it and do not reserve its number
- Platform and backend should also be numbered whenever they are missing
- If a visible field has a default, its number may be omitted from the reply

Parsing rules:
- Parse numeric answers against the current prompt's visible numbering
- Accept sparse one-line replies such as `1A 4B 6A`
- If a visible optional field is omitted, apply its default automatically
- If a visible mandatory field is omitted, ask only for that field
- If a selected option is `Other`, ask a narrow follow-up only for that field
- If a code is invalid or incomplete, ask only for the unresolved item
- Ignore certificate/account setup during intake unless the user explicitly makes it the topic

Suggested shape:

Include this question whenever credentials status or App Certificate state is still missing.

**ZH:**
```text
我还缺这几项信息，确认完我就可以继续：
1. [field 1]（可选，留空=默认）
   A. ...  B. ...  C. 用默认（...）
2. [field 2]
   A. ...  B. ...  C. 其他，直接写代码

补充说明：
- ConvoAI 服务端通过 REST 管理，客户端仍需要 RTC SDK 入会
- 可选题如果不写，就自动用默认值
- 你回一行就行，例如：2B 4A；没写出来的可选题会自动用默认
- 如果你的目标不是 Web，而是 iOS / Android / Electron，也一起按编号回复
```

**EN:**
```text
I still need these details before I continue:
1. [field 1] (optional, blank=default)
   A. ...  B. ...  C. Use default (...)
2. [field 2]
   A. ...  B. ...  C. Other, specify the code

Notes:
- ConvoAI is managed by REST on the server side, and the client still needs RTC SDK to join the channel
- If you omit an optional question, I will apply its default automatically
- Reply in one line, for example: `2B 4A`; omitted optional numbers will use defaults
- If your target is not Web, but iOS / Android / Electron, include that choice by number as well
```

### Q2 — LLM

Include this question only if the LLM provider has not already been confirmed.

**ZH:**
> "LLM（可选，留空=默认 DeepSeek）"
> 选项（内联展示）：
> A. 阿里云（aliyun）  B. 字节跳动（bytedance）  C. 深度求索（deepseek）  D. 腾讯（tencent）  E. 用默认的就行（deepseek）

**EN:**
> "LLM (optional, blank=default DeepSeek)"
> Options (inline):
> A. Alibaba Cloud (aliyun)  B. ByteDance (bytedance)  C. DeepSeek (deepseek)  D. Tencent (tencent)  E. Use the default (deepseek)

**Default:** deepseek

### Q3 — TTS

Include this question only if the TTS provider has not already been confirmed.

**ZH:**
> "TTS（可选，留空=默认 bytedance）"
> 选项（内联展示）：
> A. 字节跳动 / 火山引擎（bytedance）  B. 微软（microsoft）  C. MiniMax（minimax）  D. 阿里 CosyVoice（cosyvoice）  E. 腾讯（tencent）  F. 阶跃星辰（stepfun）  G. 用默认的就行（bytedance）

**EN:**
> "TTS (optional, blank=default bytedance)"
> Options (inline):
> A. ByteDance / Volcengine (bytedance)  B. Microsoft (microsoft)  C. MiniMax (minimax)  D. Alibaba CosyVoice (cosyvoice)  E. Tencent (tencent)  F. StepFun (stepfun)  G. Use the default (bytedance)

**Default:** bytedance (Volcengine TTS)

### Q4 — ASR Vendor

Include this question only if the ASR provider has not already been confirmed.

**ZH:**
> "ASR（可选，留空=默认 fengming）"
> 选项（内联展示）：
> A. 声网凤鸣（fengming）  B. 腾讯（tencent）  C. 微软（microsoft）  D. 科大讯飞（xfyun）  E. 科大讯飞大模型（xfyun_bigmodel）  F. 科大讯飞方言（xfyun_dialect）  G. 用默认的就行（fengming）

**EN:**
> "ASR (optional, blank=default fengming)"
> Options (inline):
> A. Agora Fengming (fengming)  B. Tencent (tencent)  C. Microsoft (microsoft)  D. iFlytek (xfyun)  E. iFlytek BigModel (xfyun_bigmodel)  F. iFlytek Dialect (xfyun_dialect)  G. Use the default (fengming)

**Default:** fengming

### Q5 — ASR Language

Include this question only if the ASR language has not already been confirmed.

Choose the recommended default from the use case:
- English use case -> `en-US`
- Chinese or unspecified use case -> `zh-CN`

Even when the recommended value is obvious, the user must still confirm or override it.

**ZH:**
> "ASR 语言（可选，留空=默认 [zh-CN / en-US]）"
> 选项（内联展示）：
> A. 中文（zh-CN，支持中英混合）  B. 英文（en-US）  C. 其他，直接写代码  D. 用默认的就行

**EN:**
> "ASR language (optional, blank=default [zh-CN / en-US])"
> Options (inline):
> A. Chinese (zh-CN, supports Chinese-English mix)  B. English (en-US)  C. Other, specify the code  D. Use the default

**Default:** `en-US` for clearly English scenarios, otherwise `zh-CN`

Prompt rendering rule:
- In the actual user-facing prompt, render each visible question as two lines only:
  - line 1: question number + field name
  - line 2: all options inline, separated by two spaces
- Example:
  - `2. LLM（可选，留空=默认）`
  - `   A. aliyun  B. bytedance  C. deepseek  D. tencent  E. 用默认（deepseek）`
- Keep the detailed reference blocks below in vertical form; only the emitted prompt should be compact

### Platform Question

Include this question whenever platform is still missing.

**ZH:**
> "目标平台是什么？（必填）"
> 选项（内联展示）：
> A. Web  B. iOS  C. Android  D. Electron  E. 其他，直接写平台

**EN:**
> "What is the target platform? (required)"
> Options (inline):
> A. Web  B. iOS  C. Android  D. Electron  E. Other, specify the platform

### Backend Question

Include this question whenever backend language is still missing.

**ZH:**
> "服务端准备用什么语言？（必填）"
> 选项（内联展示）：
> A. Python  B. Go  C. Java  D. Node.js  E. 其他，直接写语言

**EN:**
> "What backend language are you using? (required)"
> Options (inline):
> A. Python  B. Go  C. Java  D. Node.js  E. Other, specify the language

---

## Output: Structured Spec

After the user replies, normalize the answers immediately into this spec. Do not
ask for a separate confirmation turn if every blocking field is resolved.

**ZH:**
```
ConvoAI 需求规格
─────────────────────────────
场景：            [use case]
主要产品：        [ConvoAI]
配套产品：        [RTC SDK / RTC SDK + RTM / RTC SDK + Cloud Recording / 无]
平台：            [platform / client stack]
实现方式：        [sample-aligned / minimal-custom / 未指定]
服务端语言：      [backend language / 不涉及]
凭证状态：        [后续确认 / 用户已说明]
Token：           [后续确认]
ASR：             [fengming (default applied) / tencent / microsoft / xfyun / xfyun_bigmodel / xfyun_dialect]
ASR 语言：        [zh-CN (default applied) / en-US (default applied) / ja-JP / ko-KR / ...]
LLM：             [aliyun / bytedance / deepseek (default applied) / tencent]
TTS：             [bytedance (default applied) / minimax / tencent / microsoft / cosyvoice / stepfun]
─────────────────────────────
```

**EN:**
```
ConvoAI Spec
─────────────────────────────
Use case:         [use case]
Primary:          [ConvoAI]
Supporting:       [RTC SDK / RTC SDK + RTM / RTC SDK + Cloud Recording / none]
Platform:         [platform / client stack]
Implementation:   [sample-aligned / minimal-custom / unspecified]
Backend:          [backend language / not needed]
Credentials:      [confirm later / user specified]
Token:            [confirm later]
ASR:              [fengming (default applied) / tencent / microsoft / xfyun / xfyun_bigmodel / xfyun_dialect]
ASR Language:     [zh-CN (default applied) / en-US (default applied) / ja-JP / ko-KR / ...]
LLM:              [aliyun / bytedance / deepseek (default applied) / tencent]
TTS:              [bytedance (default applied) / minimax / tencent / microsoft / cosyvoice / stepfun]
─────────────────────────────
```

If credentials status is `Need to create`, pause and direct the user to
https://console.shengwang.cn/ before moving on.

## Defaults

| Field | Default | Notes (ZH) | Notes (EN) |
|-------|---------|------------|------------|
| Supporting product | `RTC SDK` | ConvoAI 默认需要 RTC SDK 作为客户端配套，除非用户已明确是纯服务端讨论 | ConvoAI normally needs RTC SDK as the client-side companion unless the user is discussing a server-only topic |
| ASR vendor | `fengming` | 推荐默认值，需由用户确认后才按 `default applied` 记录 | Recommended default; only record as `default applied` after user confirmation |
| ASR language | `zh-CN` / `en-US` | 推荐默认值，英文场景优先 `en-US`，其他场景优先 `zh-CN`；需用户确认 | Recommended default; prefer `en-US` for clearly English use cases, otherwise `zh-CN`; requires user confirmation |
| LLM vendor | `deepseek` | 推荐默认值，需由用户确认后才按 `default applied` 记录 | Recommended default; only record as `default applied` after user confirmation |
| TTS vendor | `bytedance` | 推荐默认值，需由用户确认后才按 `default applied` 记录 | Recommended default; only record as `default applied` after user confirmation |

> ASR/TTS/LLM valid values come from the /join API docs — see [convoai-restapi/start-agent.md](../references/conversational-ai/convoai-restapi/start-agent.md) for the /join schema and vendor params. Do not invent values.

## Route After Collection

Pass the structured spec to [conversational-ai](../references/conversational-ai/README.md).
The product module will use the spec to fetch the right docs and generate code.

Key routing hints:
- Dev = Go → run `bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start-go"`
- Dev = Java → run `bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start-java"`
- Dev = Python/curl → run `bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start"`
- Credentials and token setup → confirm later only if implementation is blocked or the user explicitly asks
- If fetch fails → use Generation Rules + fallback URL
