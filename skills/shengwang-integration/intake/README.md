# Shengwang Intake — Product Routing & Needs Analysis

First entry point for all Agora-related requests. Understands the full
product landscape, identifies what the user needs, and routes to the right module.

> **Note:** Skip-intake logic is defined in [SKILL.md](../SKILL.md) (root router).
> If you are here, the root router has already determined that intake is needed.
> Do NOT second-guess the routing decision — proceed with the intake flow below.

---

## Product Landscape

### Core Products

| Product | What it does | Typical user says |
|---------|-------------|-------------------|
| RTC SDK | Real-time audio/video between humans | "视频通话", "直播", "video call", "live streaming" |
| RTM | Real-time messaging / signaling | "聊天", "消息", "chat", "signaling", "notification" |
| ConvoAI | AI voice agent (ASR→LLM→TTS over RTC) | "AI语音", "voice bot", "对话式AI", "AI agent" |
| Cloud Recording | Record RTC sessions server-side | "录制", "recording", "存档" |

### Product Relationships

```
                    ┌─────────────┐
                    │   RTC SDK   │  ← foundation layer
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────┴─────┐   ┌─────┴─────┐   ┌─────┴──────┐
    │  ConvoAI  │   │  Cloud    │   │    RTM     │
    │ (AI Agent)│   │ Recording │   │ (signaling)│
    └───────────┘   └───────────┘   └────────────┘
```

Key relationships:
- **ConvoAI depends on RTC** — the AI agent joins an RTC channel; the client needs RTC SDK
- **Cloud Recording depends on RTC** — records what happens in an RTC channel
- **RTM is independent** but often paired with RTC for signaling (call invitation, presence, etc.)

### Common Product Combinations

| Use case | Products needed |
|----------|----------------|
| 1v1 / group video call | RTC SDK |
| Video call + chat | RTC SDK + RTM |
| AI voice assistant (user talks to AI) | ConvoAI + RTC SDK (client) |
| AI voice assistant + chat history | ConvoAI + RTC SDK + RTM |
| Live streaming with recording | RTC SDK + Cloud Recording |
| Chat / messaging only | RTM |
| Record AI conversations | ConvoAI + RTC SDK + Cloud Recording |

---

## Doc Index Setup

Before routing to any product module, ensure the local documentation index is available.

Check if `skills/shengwang-integration/references/docs.txt` exists.

**If it exists** → Proceed. The doc index is ready for use.

**If it does not exist** → Download it:

| | Prompt |
|---|--------|
| ZH | "正在下载声网文档索引，用于后续获取最新 API 文档。" |
| EN | "Downloading Shengwang doc index for fetching latest API docs." |

Run:
```bash
bash skills/shengwang-integration/scripts/fetch-docs.sh
```

If the download fails (network issue), proceed with local reference docs and fallback URLs in each product module. Inform the user:

| | Prompt |
|---|--------|
| ZH | "文档索引下载失败，将使用本地参考文档。如需最新文档，请稍后手动运行 `bash skills/shengwang-integration/scripts/fetch-docs.sh`。" |
| EN | "Doc index download failed. Using local reference docs. Run `bash skills/shengwang-integration/scripts/fetch-docs.sh` manually later for latest docs." |

---

## Intake Flow

### Step 1: Understand the Use Case

If the user's intent is not immediately clear, ask:

> ZH: "你想实现什么功能？请描述一下场景。"
> EN: "What are you trying to build? Describe your use case."

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

Present your analysis (match the user's language):

**ZH:**
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

**EN:**
```
Needs Analysis:
─────────────────────────────
Use case:       [user's description]
Primary:        [primary product]
Supporting:     [supporting products]
Optional:       [optional products]
─────────────────────────────

Does this look right? Anything to adjust?
```

Wait for user confirmation before proceeding.

### Step 4: Route to Product Module

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
> The module itself will collect any missing info (credentials, platform, language) as needed.

When multiple products are needed, run the primary product's intake first,
then address supporting products in order.
