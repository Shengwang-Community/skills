---
name: shengwang-intake
description: |
  First skill to run for any Shengwang (Agora)-related request. Understands
  the full product landscape, identifies user needs, recommends the optimal
  product combination, and routes to product-specific intake or skill.
  Use when the user mentions Shengwang, Agora, 声网, or describes any real-time
  communication / AI use case.
triggers:
  - "shengwang"
  - "agora"
  - "声网"
  - "i want to build"
  - "help me build"
  - "how do i integrate"
  - "我想做一个"
  - "帮我做一个"
  - "怎么接入"
  - "conversational ai"
  - "convoai"
  - "ai voice agent"
  - "voice bot"
  - "ai agent"
  - "voice pipeline"
  - "real-time voice"
  - "voice agent"
  - "声网对话式AI"
  - "对话式AI"
  - "语音AI"
  - "AI语音助手"
  - "video call"
  - "视频通话"
  - "直播"
  - "live streaming"
  - "chat"
  - "聊天"
  - "recording"
  - "录制"
metadata:
  author: shengwang
  version: "2.1.0"
---

# Shengwang Intake — Product Routing & Needs Analysis

First entry point for all Agora-related requests. This skill understands the full
product landscape, identifies what the user needs, and routes to the right place.

## When to Skip Intake

Route directly to a product skill if the user:
- Has a specific, actionable request with technical details already provided
- Asks a direct question (e.g. "what does error 403 mean")
- Names a specific operation (e.g. "generate a token", "stop my agent")
- Already went through intake and has a structured spec

---

## Product Landscape

### Core Products

| Product | What it does | Typical user says |
|---------|-------------|-------------------|
| RTC SDK | Real-time audio/video between humans | "视频通话", "直播", "video call", "live streaming" |
| RTM | Real-time messaging / signaling | "聊天", "消息", "chat", "signaling", "notification" |
| ConvoAI | AI voice agent (ASR→LLM→TTS over RTC) | "AI语音", "voice bot", "对话式AI", "AI agent" |
| Cloud Recording | Record RTC sessions server-side | "录制", "recording", "存档" |
| Media Pull | Inject external media into RTC channel | "拉流", "media inject", "播放视频到频道" |
| Media Push | Push RTC stream to CDN | "推流到CDN", "RTMP push", "转推" |

### Product Relationships

```
                    ┌─────────────┐
                    │   RTC SDK   │  ← foundation layer
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────┴─────┐   ┌─────┴─────┐   ┌─────┴──────┐
    │  ConvoAI  │   │  Cloud    │   │  Media     │
    │ (AI Agent)│   │ Recording │   │ Push/Pull  │
    └───────────┘   └───────────┘   └────────────┘
          │
    ┌─────┴─────┐
    │    RTM    │  ← often paired for signaling
    └───────────┘
```

Key relationships:
- **ConvoAI depends on RTC** — the AI agent joins an RTC channel; the client needs RTC SDK
- **Cloud Recording depends on RTC** — records what happens in an RTC channel
- **RTM is independent** but often paired with RTC for signaling (call invitation, presence, etc.)
- **Media Push/Pull depends on RTC** — extends RTC channels to/from external sources

### Common Product Combinations

| Use case | Products needed |
|----------|----------------|
| 1v1 / group video call | RTC SDK |
| Video call + chat | RTC SDK + RTM |
| AI voice assistant (user talks to AI) | ConvoAI + RTC SDK (client) |
| AI voice assistant + chat history | ConvoAI + RTC SDK + RTM |
| Live streaming with recording | RTC SDK + Cloud Recording |
| Live streaming to CDN | RTC SDK + Media Push |
| Play video into a call | RTC SDK + Media Pull |
| Chat / messaging only | RTM |
| Record AI conversations | ConvoAI + RTC SDK + Cloud Recording |

---

## Intake Flow

### Step 1: Understand the Use Case

If the user's intent is not immediately clear, ask:

> "你想实现什么功能？请描述一下场景。"

Listen for keywords and map to products using the Product Landscape table above.

### Step 2: Identify Products

Based on the user's description, determine:

1. **Primary product** — the main capability they need
2. **Supporting products** — additional products required by the primary, or that enhance the use case
3. **Optional products** — nice-to-haves the user may not have thought of

Use the Product Relationships and Common Combinations to make this determination.

**Example analysis:**

> User: "我想做一个AI客服，用户打电话进来，AI自动接听回答问题"
>
> - Primary: ConvoAI (AI voice agent)
> - Supporting: RTC SDK (client-side for user to join channel)
> - Optional: Cloud Recording (record conversations for QA), RTM (send chat transcript)

### Step 3: Confirm with User

Present your analysis:

```
需求分析：
─────────────────────────────
场景：          [用户描述的场景]
主要产品：      [primary product]
配套产品：      [supporting products]
可选增强：      [optional products]
─────────────────────────────

这个方案合适吗？有需要调整的吗？
```

Wait for user confirmation before proceeding.

### Step 4: Route to Product-Specific Intake

For each identified product, route to its detail collection:

| Product | Detail intake | Product skill |
|---------|--------------|---------------|
| ConvoAI | [intake/convoai.md](convoai.md) | [integrate-shengwang-conversational-ai/SKILL.md](../integrate-shengwang-conversational-ai/SKILL.md) |
| RTC SDK | (external docs for now) | https://doc.shengwang.cn/doc/rtc/javascript/get-started/quick-start |
| RTM | (external docs for now) | https://doc.shengwang.cn/doc/rtm2/javascript/get-started/quick-start |
| Cloud Recording | (external docs for now) | https://doc.shengwang.cn/doc/cloud-recording/restful/get-started/quick-start |
| Credentials / Auth | — | [general/SKILL.md](../general/SKILL.md) |
| Token generation | — | [implement-shengwang-token-on-server/SKILL.md](../implement-shengwang-token-on-server/SKILL.md) |
| Download SDK | — | [resource-downloader/SKILL.md](../resource-downloader/SKILL.md) |

When multiple products are needed, run the primary product's intake first,
then address supporting products in order.

---

## Decision Shortcuts

For common patterns, skip the full intake flow:

| User says | Shortcut |
|-----------|----------|
| "接入ConvoAI" / "build voice bot" / "AI语音助手" | → [intake/convoai.md](convoai.md) directly |
| "视频通话" / "video call" / "直播" | → RTC SDK docs directly |
| "聊天" / "消息" / "chat" | → RTM docs directly |
| "录制" / "recording" | → Cloud Recording docs directly |
| "生成token" / "token server" | → [implement-shengwang-token-on-server/SKILL.md](../implement-shengwang-token-on-server/SKILL.md) directly |
| "下载SDK" / "download" | → [resource-downloader/SKILL.md](../resource-downloader/SKILL.md) directly |

---

## Adding New Products

When a new Agora product is added:

1. Add it to the Product Landscape table
2. Update the Product Relationships diagram
3. Add relevant combinations to Common Product Combinations
4. Create `intake/<product>.md` for detail collection
5. Add routing entry to Step 4 table
