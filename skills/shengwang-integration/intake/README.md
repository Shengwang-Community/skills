# Shengwang Intake — Kickoff Information Collection

First entry point for requests that still need a small amount of information
before implementation can begin.

> **Note:** Step 0 doc-index setup is defined in [SKILL.md](../SKILL.md).
> If you are here, Step 0 has already been handled and the root router needs
> a lightweight kickoff summary before moving into implementation research.

---

## Goal

Collect only the minimum missing information needed to proceed.
Do not run a broad discovery interview. Do not ask the user to confirm a full
solution design before continuing.

Ask only for unanswered details that materially affect routing or implementation:
- Use case / target solution
- Main Shengwang / Agora product
- Platform or client stack
- Backend language if relevant
- Any key details already known that affect the next step

Once those details are gathered, produce a short kickoff summary and continue
to Step 2 automatically unless a required field is still missing.

## Product Routing Aid

Use this only to map the user's use case to the likely product set.

| Product | What it does | Typical user says |
|---------|-------------|-------------------|
| RTC SDK | Real-time audio/video between humans | "视频通话", "直播", "video call", "live streaming" |
| RTM | Real-time messaging / signaling | "聊天", "消息", "chat", "signaling", "notification" |
| ConvoAI | AI voice agent (ASR→LLM→TTS over RTC) | "AI语音", "voice bot", "对话式AI", "AI agent" |
| Cloud Recording | Record RTC sessions server-side | "录制", "recording", "存档" |

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

### Step 1: Ask only for missing kickoff details

Start from the user's existing message. Do not repeat information they already gave.

Use the shortest set of questions needed to fill the gaps.

Typical kickoff questions:

- Use case:
  - ZH: "你想实现什么功能？请描述一下场景。"
  - EN: "What are you trying to build? Describe the use case."
- Main product:
  - ZH: "你主要想用哪个声网产品？如果不确定，我可以帮你判断。"
  - EN: "Which Shengwang product do you mainly want to use? If you're not sure, I can infer it."
- Platform / client stack:
  - ZH: "你做的是哪个平台或客户端？例如 Web、iOS、Android、小程序。"
  - EN: "Which platform or client stack are you targeting, such as Web, iOS, Android, or mini program?"
- Backend language, when relevant:
  - ZH: "服务端准备用什么语言？例如 Go、Java、Python、Node.js。"
  - EN: "What backend language are you using, such as Go, Java, Python, or Node.js?"

Ask follow-up only when a missing detail affects routing or implementation.

### Step 2: Determine product mapping

From the user's answers, determine:
- Primary product
- Supporting products, if required
- Any remaining gaps that block implementation

Use the routing aid above to infer combinations.

### Step 3: Produce kickoff summary

Present a short summary in the user's language:

**ZH:**
```text
项目启动信息
─────────────────────────────
场景：          [use case]
主要产品：      [primary product]
配套产品：      [supporting products / 无]
平台：          [platform / client stack]
服务端语言：    [backend language / 不涉及]
剩余缺口：      [none / missing details]
─────────────────────────────
```

**EN:**
```text
Kickoff Summary
─────────────────────────────
Use case:       [use case]
Primary:        [primary product]
Supporting:     [supporting products / none]
Platform:       [platform / client stack]
Backend:        [backend language / not needed]
Gaps:           [none / missing details]
─────────────────────────────
```

Do not stop for a separate confirmation step.

- If no required detail is missing → continue automatically to Step 2 in the root workflow.
- If a required detail is still missing → ask only for that blocker, then continue.

### Step 4: Route onward

For each identified product, route to its detail collection:

| Product | Detail intake | Product module |
|---------|--------------|---------------|
| ConvoAI | [intake/convoai.md](convoai.md) | [conversational-ai](../references/conversational-ai/README.md) |
| RTC SDK | — | [rtc](../references/rtc/README.md) |
| RTM | — | [rtm](../references/rtm/README.md) |
| Cloud Recording | — | [cloud-recording](../references/cloud-recording/README.md) |
| Credentials / Auth | — | [general](../references/general/credentials-and-auth.md) |
| Token generation | — | [token-server](../references/token-server/README.md) |

> Products without a detail intake (marked "—") go directly to the product module.
> The module itself should only collect product-specific missing details.

When multiple products are needed, run the primary product's intake first,
then address supporting products in order.
