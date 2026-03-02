---
name: shengwang-integration
description: |
  Integrate Shengwang (Agora) products: ConvoAI voice agents, RTC audio/video,
  RTM messaging, Cloud Recording, and token generation. Use when the user
  mentions Shengwang, Agora, 声网, ConvoAI, RTC, RTM, voice agent, AI agent,
  video call, live streaming, recording, token, or any Agora product task.
license: MIT
metadata:
  author: shengwang
  version: "4.0.0"
---

# Shengwang Integration

## Routing Rules

### Step 1: Check if intake can be skipped

Skip [intake/SKILL.md](intake/SKILL.md) and route directly ONLY when ALL of these are true:
- User names a specific operation (e.g. "stop agent xxx", "generate a token", "download SDK")
- User provides enough technical details to act immediately (channel name, agent ID, language, etc.)
- The request maps unambiguously to exactly one skill in the table below

Examples that SKIP intake:
- "帮我停掉 agent_abc123" → [integrate-shengwang-conversational-ai/SKILL.md](integrate-shengwang-conversational-ai/SKILL.md)
- "生成一个 RTC token，Go 语言" → [implement-shengwang-token-on-server/SKILL.md](implement-shengwang-token-on-server/SKILL.md)
- "error 403 是什么意思" → [integrate-shengwang-conversational-ai/troubleshooting](integrate-shengwang-conversational-ai/troubleshooting/common-errors.md)
- "下载 ConvoAI Go SDK" → [resource-downloader/SKILL.md](resource-downloader/SKILL.md)

Examples that MUST go through intake:
- "我想做一个 AI 客服" → needs analysis, go to intake
- "帮我接入 ConvoAI" → product identified but details missing, go to intake
- "我想做视频通话 + AI 助手" → multi-product, go to intake
- "voice bot" / "AI agent" → vague, go to intake

### Step 2: Route

| User intent | Route to |
|-------------|----------|
| New request, vague, or missing details | [intake/SKILL.md](intake/SKILL.md) |
| Credentials, AppID, REST auth | [general/SKILL.md](general/SKILL.md) |
| Download SDK, sample project, Token Builder, GitHub repo | [resource-downloader/SKILL.md](resource-downloader/SKILL.md) |
| Generate Token, token server, AccessToken2, RTC/RTM auth | [implement-shengwang-token-on-server/SKILL.md](implement-shengwang-token-on-server/SKILL.md) |
| ConvoAI operation (with details already known) | [integrate-shengwang-conversational-ai/SKILL.md](integrate-shengwang-conversational-ai/SKILL.md) |
| RTC SDK integration | [integrate-shengwang-rtc/SKILL.md](integrate-shengwang-rtc/SKILL.md) |
| RTM messaging / signaling | [integrate-shengwang-rtm/SKILL.md](integrate-shengwang-rtm/SKILL.md) |
| Cloud Recording | [integrate-shengwang-cloud-recording/SKILL.md](integrate-shengwang-cloud-recording/SKILL.md) |

## Links

- Console: https://console.agora.io/
- Docs (CN): https://doc.shengwang.cn/
- Docs (Global): https://docs.agora.io/
- GitHub: https://github.com/AgoraIO-Community
