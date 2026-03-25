# ConvoAI Quickstart Flow

Use this file as the ConvoAI-internal quickstart intake after ConvoAI has already been selected as the primary product.
This is the first user-visible onboarding step for ConvoAI quickstarts and unproven integrations.
This file keeps the question-driven intake flow inside the ConvoAI module to avoid cross-directory back-and-forth.

## Scope

Use this file only for:
- `quickstart`
- `integration` when the user does **not** yet have a proven working ConvoAI baseline

Do **not** use this file as the default intake for every ConvoAI request.

Before using this file, classify the request mode with
[request-modes.md](request-modes.md).

If the request is `advanced-feature`, `debugging`, or `ops-hardening`, route to
[advanced-feature-routing.md](advanced-feature-routing.md)
instead of running the full quickstart-style intake.

For `quickstart`, or `integration` without a proven working baseline, use the project-readiness and provider-guardrail sections in this file before any provider choices are confirmed.

## Language Detection

Detect the user's language from their most recent message:
- If the user writes in **Chinese** → use the **ZH** prompts below
- If the user writes in **English** (or any other language) → use the **EN** prompts below

Maintain the detected language consistently throughout the entire intake flow.

## User-Visible Sequence

For ConvoAI quickstarts and unproven integrations, follow this exact user-visible order:
1. Product intro in plain language
2. Technical-path confirmation
3. Project-readiness checkpoint (`App ID`, `App Certificate`, ConvoAI activation, RTC Token path)
4. Provider confirmation
5. Detailed provider checklist only if customization is still needed

Do not skip ahead. Do not surface a later stage before the earlier stage is resolved.

## Project Readiness Rules

For the ConvoAI quickstart path used by this skill:
- `App ID`, `App Certificate`, and ConvoAI activation are fixed prerequisites
- RTC Token is the fixed auth path
- If any of those items are unclear, resolve them with the compact credential prompt before provider confirmation

## Questions

Use a friendly but explicit follow-up flow:
- Ask for a single decision group per turn. Do not combine technical-path, credential, and provider decisions in the same visible message.
- Use a consolidated provider checklist only when detailed provider selection is actually needed, and only after the technical path and credential status are already clear.
- Keep the message short enough to scan, but complete enough to finish the current decision in one reply
- Skip anything the user already answered
- Default to `sample-aligned` when the request clearly matches the official sample path
- Treat the default technical path and the default provider baseline as two separate decisions
- Do not propose a bespoke frontend/backend project structure before preflight and intake are complete
- Do not ask React / Vue / HTML or other custom stack questions when the user only asked for a generic Web quickstart and has not opted out of the official sample path
- If the user explicitly names a native platform such as Android / iOS / Flutter / Windows / macOS, infer that platform immediately instead of re-asking it
- For native-platform quickstart requests, skip backend, token-server, and server-stack questions unless the user explicitly says they want a custom architecture or an existing-project integration
- Do not ask about development experience or whether a ConvoAI Agent has already been created during quickstart intake; those are not routing blockers
- Do not announce concrete framework names such as Next.js / FastAPI until the user has accepted the default technical path or explicitly asked for sample details
- Before asking about providers, give a one- or two-sentence plain-language intro to what ConvoAI does in the chosen app path
- Do not lead with terms like `三段式`, `ASR`, `LLM`, `TTS`, or `provider` before that intro has been given
- Explain `App ID` and `App Certificate` in plain language before asking whether the user has them
- If the user explicitly names a provider, validate it against the supported provider list in this file immediately
- If the named provider is unsupported, resolve that blocker before asking any further credential or provider questions
- Show the available options and recommended default only for the fields that are still truly unresolved
- If the user leaves a blocker unresolved, ask only a narrow repair follow-up for that field

Defaults policy:
- Platform recommended default: `Web`
- Backend recommended default: `Python` (skip this field entirely for native platforms: iOS, Android, Flutter, Windows, macOS)
- ASR vendor recommended default: `fengming`
- ASR language recommended default: `en-US` for clearly English scenarios, otherwise `zh-CN`
- LLM recommended default: `aliyun`
- TTS recommended default: `bytedance`

## Supported Provider Guardrails

- LLM: `aliyun`, `bytedance`, `deepseek`, `tencent`
- TTS: `bytedance`, `microsoft`, `minimax`, `cosyvoice`, `tencent`, `stepfun`
- ASR: `fengming`, `tencent`, `microsoft`, `xfyun`, `xfyun_bigmodel`, `xfyun_dialect`
- Current first-success baseline: `aliyun` + `bytedance` + `fengming`
- If a named provider is outside the supported list for its stage (for example `openai` or `azure openai` for LLM), treat it as unsupported and resolve that blocker before any further setup questions

Blocking rule:
- Any selected `Other` value must be clarified in a narrow follow-up
- Platform and Backend are optional when shown with defaults
- **LLM, TTS, ASR vendor, and ASR language still require explicit confirmation**, but that confirmation can come from either:
  - a single compact confirmation of the default provider baseline, or
  - a detailed provider-by-provider selection

Confirmation gate:
- If any mandatory provider fields (LLM, TTS, ASR vendor, ASR language) are unresolved, do NOT proceed silently.
- If the technical path is still unresolved and the official sample path is a good fit, ask only the compact technical-path confirmation prompt first.
- After the user answers that, if they have already named an unsupported provider, ask only the compact unsupported-provider prompt next.
- After the user answers that, if project readiness (`App ID`, `App Certificate`, ConvoAI activation) is still unclear, ask only the compact credential prompt next.
- After the user answers that, if provider fields are still unresolved, ask only the compact default-provider confirmation prompt, and only when the default baseline keys are available or explicitly confirmed by the user.
- If the user explicitly confirms the default provider baseline, treat that as explicit confirmation for all mandatory provider fields.
- Only expand into the full provider checklist if the user asks to customize, rejects the default provider baseline, has missing default-provider keys, or has already supplied partial non-default provider choices.
- For defaultable fields that are NOT mandatory confirmation fields (Platform, Backend), omission counts as explicit confirmation to use the default.
- For the compact default-provider prompt, the user must explicitly choose the default provider baseline or ask to customize; silence does not count.

If the technical path is unresolved and the official sample path fits, ask the compact technical-path prompt first and stop there.
If the user has already named an unsupported provider after that, ask the compact unsupported-provider prompt next and stop there.
If project readiness (`App ID`, `App Certificate`, ConvoAI activation) is unresolved after that, ask the compact credential prompt next and stop there.
If provider fields are unresolved after that, ask the compact default-provider prompt next and stop there.
Ask the full unresolved-fields checklist only after the user asks to customize, or when some provider fields are already non-default and still unresolved.
Do not show two separate option blocks such as `A/B` and `C/D` in the same turn.
Skip any question the user already answered during main intake or in the user's initial request.
Doc index status is already determined by the main intake — do not re-check here.

## Compact Technical-Path Prompt

When the request clearly matches the official quickstart path and the user has not asked for a custom stack,
prefer a compact technical-path confirmation prompt first.

Prompt rules:
- Keep it to one short intro line, one choice line, and at most three short notes
- Confirm only the technical path here; do not mix credential or provider choices into the same message
- If the user accepts the default technical path, only then move on to sample inspection and provider confirmation
- If the user asks to customize the stack, expand only the still-unresolved architecture questions
- For native-platform quickstart requests, use the native sample wording and do not mention backend or token-server by default

Suggested shape:

**ZH:**
```text
我建议先按官方 Web quickstart 路径继续，这样最快：
A. 用默认技术路径（官方 Web sample）
B. 我想自定义技术栈

说明：
- 如果你选 A，我会先检查官方 sample 路径，再确认 provider 配置
- 如果你选 B，我再问前后端栈
```

**EN:**
```text
I suggest starting with the official Web quickstart path to keep setup short:
A. Use the default technical path (official Web sample)
B. I want a custom stack

Notes:
- If you choose A, I will inspect the official sample path and then confirm the provider setup
- If you choose B, I will ask the frontend/backend stack questions
```

Native-platform variant:

**ZH:**
```text
我建议直接按官方 Android / Native sample 路径继续，这样最快：
A. 用默认原生路径（官方 native sample）
B. 我有现有工程 / 我想自定义集成

说明：
- 如果你选 A，我会先检查官方 sample 路径，再确认 provider 配置
- 如果你选 B，我再问和现有工程相关的问题
```

**EN:**
```text
I suggest going straight with the official Android / native sample path to keep setup short:
A. Use the default native path (official native sample)
B. I have an existing project / I want a custom integration

Notes:
- If you choose A, I will inspect the official sample path and then confirm the provider setup
- If you choose B, I will ask the existing-project questions
```

## Compact Unsupported-Provider Prompt

Use this prompt when the user has already named a provider that is outside the supported local enum list for the requested stage.

Prompt rules:
- Keep it to one short intro line, one choice line, and at most three short notes
- Name the unsupported provider explicitly
- Tell the user that this quickstart path does not support it
- Do not pile on credential, sample, or other setup questions in the same turn

Suggested shape:

**ZH:**
```text
你刚才提到的 provider 当前不在这个 quickstart 的支持列表里：
- 当前不支持：OpenAI
- 我可以改成支持的 LLM，或者先把支持列表给你

A. 直接改用支持的默认 LLM
B. 先给我看支持的 LLM 列表
```

**EN:**
```text
The provider you named is not in the supported list for this quickstart path:
- Currently unsupported here: OpenAI
- I can switch to a supported default LLM, or show you the supported LLM list first

A. Switch to the supported default LLM
B. Show me the supported LLM list first
```

## Compact Credential Prompt

Use this prompt when the user has not yet been told what `App ID`, `App Certificate`, and ConvoAI activation mean, or when that project-readiness status is still unclear.

Prompt rules:
- Keep it to one short intro line, one choice line, and at most three short notes
- Explain `App ID` in plain language before asking about it
- Do not combine this credential prompt with a technical-path prompt or a provider prompt in the same turn
- Explain that this quickstart requires `App ID`, `App Certificate`, and ConvoAI service activation
- Mention that the quickstart auth path is fixed to RTC Token
- Do not ask provider questions until this project-readiness status is clear enough for preflight

Suggested shape:

**ZH:**
```text
继续前先确认三个前置条件：
- App ID：你的声网项目标识，接入一定会用到
- App Certificate：这个 quickstart 会用 RTC Token，因此这里也需要
- ConvoAI 开通：项目需要先开通 ConvoAI 服务

A. 这三个我都已经准备好了
B. 我还没有 / 不清楚，先告诉我去哪看
```

**EN:**
```text
Before we continue, I need to confirm three prerequisites:
- App ID: your Shengwang project identifier; the app will need this
- App Certificate: this quickstart uses RTC Token, so it is also required here
- ConvoAI activation: the project must have ConvoAI enabled

A. I already have all three ready
B. I do not have them / I am not sure — tell me where to find them first
```

## Compact Default-Provider Prompt

When the user has not requested custom providers and the default provider baseline is still acceptable,
prefer a compact provider confirmation prompt before expanding into the full checklist.

Prompt rules:
- Keep it to one short intro line, one choice line, and at most three short notes
- Do not restate an implementation plan, project tree, or framework recommendation here
- Do not combine this provider prompt with a technical-path prompt or a credential prompt in the same turn
- Only use this prompt when the required default-provider keys are already available or the user explicitly confirms they have them
- If the required default-provider keys are missing or unknown, skip this prompt and expand the provider options / readiness check instead
- If the user confirms the default provider baseline, continue without expanding the full provider checklist
- Only if the user asks to customize should the agent render the detailed provider options

Suggested shape:

**ZH:**
```text
如果你已经有默认 provider 所需的 key，我可以先按默认三段式继续：
A. 我有默认 provider key，按默认三段式继续
B. 我没有 / 不确定，我要自定义 provider

说明：
- 如果你选 A，我就按默认三段式继续
- 如果你选 B，我再展开 LLM / TTS / ASR 选项
```

**EN:**
```text
If you already have the keys needed for the default providers, I can continue with the default provider baseline:
A. I have the default provider keys — continue with the default provider baseline
B. I do not have them / I am not sure — I want to customize providers

Notes:
- If you choose A, I will continue with the default provider baseline
- If you choose B, I will expand the LLM / TTS / ASR options
```

## Detailed Provider Checklist

Use this only after the user has already chosen a technical path and the credential status is clear.
Do not use this as the first onboarding prompt.
When the user has asked to customize providers, combine only the still-unresolved provider-specific questions into one message.

Message requirements:
- Use the user's language consistently
- Start with at most one short recap line
- Ask only about unresolved provider fields that are still unresolved
- Under each unresolved field, show the supported options inline to reduce prompt height
- Number only the currently visible unresolved fields, starting from `1`
- Mark fields with defaults as optional
- Ask the user to reply once with numeric codes such as `1A 4B 6A`
- Do not mix this with a `key=value` quick-reply example in the same prompt

If the user already provided enough detail for some fields, do not restate those
questions. Keep the option list only for the unresolved fields.

Numbering rules:
- Renumber based only on the fields shown in the current prompt
- Do not use stable global IDs across turns
- If a field is already known, omit it and do not reserve its number
- Platform and backend should also be shown whenever they are unresolved, even though they are optional
- LLM, TTS, ASR, and ASR language should still be shown whenever they are unresolved, even though they are optional
- If a visible field has a default, its number may be omitted from the reply

Parsing rules:
- Parse numeric answers against the current prompt's visible numbering
- Accept sparse one-line replies such as `1A 4B 6A`
- If a visible optional field is omitted, apply its default automatically
- If a visible mandatory field is omitted, ask only for that field
- If a selected option is `Other`, ask a narrow follow-up only for that field
- If a code is invalid or incomplete, ask only for the unresolved item

Suggested shape:

**ZH:**
```text
我还缺这几项信息，确认完我就可以继续：
1. [field 1]（可选，留空=默认）
   A. ...  B. ...  C. 用默认（...）
2. [field 2]
   A. ...  B. ...  C. 其他，直接写代码

补充说明：
- ConvoAI 默认优先走官方 sample；服务端优先用 `agent-server-sdk`
- 客户端优先用 `agora-agent-client-toolkit`，如果目标栈不适配再直接用 RTC SDK 入会
- Native 平台（iOS / Android / Flutter / Windows / macOS）走多平台 sample repo，客户端直接调 ConvoAI REST API，不需要 `agent-server-sdk` 和 `agora-agent-client-toolkit`，也不需要配套服务端
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
- ConvoAI should usually follow the official sample path, use `agent-server-sdk` on the server side, and use `agora-agent-client-toolkit` on the client side when possible instead of building from the REST spec from scratch
- If the client toolkit is not a fit for the target stack, the client should still join with the RTC SDK directly
- Native platforms (iOS / Android / Flutter / Windows / macOS) use the multi-platform sample repo, call the ConvoAI REST API directly from the client, and do not need `agent-server-sdk`, `agora-agent-client-toolkit`, or a separate server
- If you omit an optional question, I will apply its default automatically
- Reply in one line, for example: `2B 4A`; omitted optional numbers will use defaults
- If your target is not Web, but iOS / Android / Electron, include that choice by number as well
```

### Q2 — LLM

Include this question only if the LLM provider has not already been confirmed.

**ZH:**
> "LLM（可选，留空=默认 DeepSeek）"
> 选项（内联展示）：
> A. 阿里云（aliyun）  B. 字节跳动（bytedance）  C. 深度求索（deepseek）  D. 腾讯（tencent）  E. 用默认的就行（aliyun）

**EN:**
> "LLM (optional, blank=default DeepSeek)"
> Options (inline):
> A. Alibaba Cloud (aliyun)  B. ByteDance (bytedance)  C. DeepSeek (deepseek)  D. Tencent (tencent)  E. Use the default (aliyun)

**Default:** aliyun

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
> A. Shengwang Fengming (fengming)  B. Tencent (tencent)  C. Microsoft (microsoft)  D. iFlytek (xfyun)  E. iFlytek BigModel (xfyun_bigmodel)  F. iFlytek Dialect (xfyun_dialect)  G. Use the default (fengming)

**Default:** fengming

### Q5 — ASR Language

Include this question only if the ASR language has not already been confirmed.

Choose the recommended default from the use case:
- English use case -> `en-US`
- Chinese or unspecified use case -> `zh-CN`

If the question is shown and the user omits it, apply the recommended default automatically.

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
  - `   A. aliyun  B. bytedance  C. deepseek  D. tencent  E. 用默认（aliyun）`
- Keep the detailed reference blocks below in vertical form; only the emitted prompt should be compact

### Platform Question

Include this question whenever platform is still missing.

**ZH:**
> "目标平台是什么？（可选，留空=默认 Web）"
> 选项（内联展示）：
> A. Web  B. iOS  C. Android  D. Electron  E. 其他，直接写平台  F. 用默认的就行（Web）

**EN:**
> "What is the target platform? (optional, blank=default Web)"
> Options (inline):
> A. Web  B. iOS  C. Android  D. Electron  E. Other, specify the platform  F. Use the default (Web)

**Default:** Web

### Backend Question

Include this question whenever backend language is still missing.
Skip this question entirely if the user's confirmed platform is a native platform (iOS, Android, Flutter, Windows, macOS) — native ConvoAI apps are self-contained and call the REST API directly, no separate server needed. Record backend as "不涉及" / "not needed" in the spec.

**ZH:**
> "服务端准备用什么语言？（可选，留空=默认 Python）"
> 选项（内联展示）：
> A. Python  B. Go  C. Java  D. Node.js  E. 其他，直接写语言  F. 用默认的就行（Python）

**EN:**
> "What backend language are you using? (optional, blank=default Python)"
> Options (inline):
> A. Python  B. Go  C. Java  D. Node.js  E. Other, specify the language  F. Use the default (Python)

**Default:** Python

---

## Output: Structured Spec

After the user replies, normalize the answers immediately into a compact internal spec.
Do not ask for a separate confirmation turn if every blocking field is resolved.

```yaml
use_case: [text]
primary: ConvoAI
supporting: [RTC SDK | RTC SDK + RTM | RTC SDK + Cloud Recording | none]
platform: [Web | iOS | Android | Electron | other]
implementation: [sample-aligned | minimal-custom | unspecified]
backend: [Python | Go | Java | Node.js | other | not needed]
project_readiness:
  app_id: [ready | missing | unknown]
  app_certificate: [ready | missing | unknown]
  convoai_activation: [ready | missing | unknown]
  rtc_token_path: [ready | missing | unknown]
providers:
  asr: [fengming | tencent | microsoft | xfyun | xfyun_bigmodel | xfyun_dialect]
  asr_language: [zh-CN | en-US | other]
  llm: [aliyun | bytedance | deepseek | tencent]
  tts: [bytedance | minimax | tencent | microsoft | cosyvoice | stepfun]
```

Apply the defaults declared earlier in this file when the user has explicitly accepted them.
Do not invent provider values beyond the supported lists in this file.

## Route After Collection

After the structured spec is ready:
- Follow the architecture rules in [README.md](README.md)
- Use [sample-repos.md](sample-repos.md) for sample inspection and clone workflow
- Use [generation-rules.md](generation-rules.md) for stable generation constraints
- Use the backend-language mapping below when the demo does not cover the chosen server language
- Use `convoai-restapi/index.mdx` or endpoint docs only for missing low-level API details

### Backend Language → Official Quickstart

| Backend | Primary official doc |
|---------|----------------------|
| `Go` | `docs://default/convoai/restful/get-started/quick-start-go` |
| `Java` | `docs://default/convoai/restful/get-started/quick-start-java` |

When the chosen backend is not covered by the sample repo, treat the flow as:
- frontend / architecture reference from the sample repo when useful
- backend implementation details from the mapped official quickstart doc above
