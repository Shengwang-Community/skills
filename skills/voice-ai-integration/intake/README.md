# Shengwang Intake — Needs Analysis & Product Routing

First entry point for requests that still need lightweight product routing before
implementation begins.

> **Note:** Step 0 doc-index setup is defined in [SKILL.md](../SKILL.md).
> If you are here, Step 0 has already been handled and the root router now needs
> only enough information to decide which Shengwang product module should take over.

---

## Goal

Use this intake to do **needs analysis and product routing**, not product-specific
solution design.

The top-level intake should answer only these questions:
- What is the user trying to build?
- Which Shengwang product is primary?
- Which supporting products are likely needed?
- Is there one remaining blocker that is still required to choose the right module?

Do **not** use this layer to collect provider choices, auth strategy, SDK details,
project structure, vendor configuration, or other product-internal implementation
choices unless one of those details is the only remaining routing blocker.

If the primary product is already obvious from the user's request, do not ask extra
questions here — route directly to the product module.

## Interaction Style

The intake should stay concise and routing-focused.

- Prefer natural wording over an interview script
- Ask only for missing information that changes product routing
- Ask at most one routing blocker at a time when the product is still unclear
- Do not ask product-specific configuration questions at the top level
- Do not propose project structures, implementation plans, or framework choices here
- If a detail is obvious from the user's message, infer it instead of asking again
- As soon as the product mapping is clear, route onward

## Product Routing Aid

Use this only to map the user's use case to the likely product set.

| Product | What it does | Typical user says |
|---------|-------------|-------------------|
| RTC SDK | Real-time audio/video between humans | "视频通话", "直播", "video call", "live streaming" |
| RTM | Real-time messaging / signaling | "聊天", "消息", "chat", "signaling", "notification" |
| ConvoAI | AI voice agent (ASR→LLM→TTS over RTC) | "AI语音", "voice bot", "对话式AI", "AI agent" |
| Cloud Recording | Record RTC sessions server-side | "录制", "recording", "存档" |
| Token generation | Generate RTC / RTM tokens | "token", "鉴权", "token server" |
| Credentials / Auth | Console credentials, REST auth, service activation | "App ID", "Customer Key", "REST auth", "开通服务" |

### Common combinations

| Use case | Products needed |
|----------|----------------|
| 1v1 / group video call | RTC SDK |
| Video call + chat | RTC SDK + RTM |
| AI voice assistant (user talks to AI) | ConvoAI + RTC SDK (client) |
| AI voice assistant + chat history | ConvoAI + RTC SDK + RTM |
| Live streaming with recording | RTC SDK + Cloud Recording |
| Chat / messaging only | RTM |
| Record AI conversations | ConvoAI + RTC SDK + Cloud Recording |

## Intake Flow

### Step 1: Determine product routing

Start from the user's existing message. Do not repeat information they already gave.

Priority order:
- Use case / target solution
- Primary product, if still unclear
- Supporting product, if the use case clearly requires one
- One routing blocker only if it is still needed to choose the right module

ConvoAI handoff:
- If ConvoAI is clearly the primary product, route directly to [conversational-ai](../references/conversational-ai/README.md)
- Do not expand ConvoAI-specific quickstart, provider, auth, or sample questions here
- Let the ConvoAI module handle `request-modes.md` and its internal sub-flows

Short prompt examples:
- Use case:
  - ZH: "你想做什么场景？"
  - EN: "What are you trying to build?"
- Primary product:
  - ZH: "你主要想用 RTC、RTM、ConvoAI，还是录制？如果不确定我可以帮你判断。"
  - EN: "Are you mainly using RTC, RTM, ConvoAI, or recording? If you're not sure, I can infer it."
- Supporting product:
  - ZH: "除了主链路外，还需要聊天、录制，或者 token 服务吗？"
  - EN: "Besides the main flow, do you also need chat, recording, or a token service?"

### Step 2: Produce routing summary

Present a short progress recap in the user's language:

**ZH:**
```text
已了解的信息
─────────────────────────────
场景：          [use case]
主要产品：      [primary product]
配套产品：      [supporting products / 无]
下一步：        [route to the product module / ask one routing blocker]
─────────────────────────────
```

**EN:**
```text
What I have so far
─────────────────────────────
Use case:       [use case]
Primary:        [primary product]
Supporting:     [supporting products / none]
Next:           [route to the product module / ask one routing blocker]
─────────────────────────────
```

Do not stop for a separate confirmation step.

- If the product mapping is clear -> continue automatically to the product module
- If one routing blocker is still missing -> ask only for that blocker, then continue

### Step 3: Route onward

For each identified product, route to its product module:

| Product | Product module |
|---------|---------------|
| ConvoAI | [conversational-ai](../references/conversational-ai/README.md) |
| RTC SDK | [rtc](../references/rtc/README.md) |
| RTM | [rtm](../references/rtm/README.md) |
| Cloud Recording | [cloud-recording](../references/cloud-recording/README.md) |
| Credentials / Auth | [general](../references/general/credentials-and-auth.md) |
| Token generation | [token-server](../references/token-server/README.md) |

When multiple products are needed, route to the primary product first,
then address supporting products in order.
