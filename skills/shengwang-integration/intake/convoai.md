---
name: convoai-intake
description: |
  Collects ConvoAI-specific implementation details after the main intake has
  identified ConvoAI as the target product. Outputs a structured spec that
  drives code generation in integrate-shengwang-conversational-ai/SKILL.md.
---

# ConvoAI Detail Collection

Reached from [intake/SKILL.md](../SKILL.md) after ConvoAI is identified as the primary product.

## Prerequisites

Before starting, the user should have:
- Confirmed ConvoAI is the right product (via main intake)
- A clear use case description

## Questions

**Fast-path rule:** If the user's initial description already contains 2+ of the following
(credentials status, LLM choice, dev language), skip individual questions.
Instead, generate the structured spec directly from what they said, fill defaults for anything
missing, and present it for confirmation.

Ask **one at a time** only when needed. Skip any question the user already answered during main intake.

### Q1 — Credentials

> "你有 Agora 账号和项目凭证吗？（AppID、Customer Key、Customer Secret）"
> - A. 有，都准备好了
> - B. 有账号但还没创建项目
> - C. 还没有账号

**If B or C** → direct to https://console.agora.io/ and pause until ready.

### Q2 — LLM

> "你打算用哪个 LLM？"
> - A. 阿里云（aliyun）
> - B. 字节跳动（bytedance）
> - C. 深度求索（deepseek）
> - D. 腾讯（tencent）
> - E. 还没决定，用推荐的就行

**Default:** deepseek

### Q3 — Development language

> "你用什么语言开发服务端？"
> - A. Go
> - B. Java
> - C. Python / JavaScript / curl

---

## Output: Structured Spec

```
ConvoAI 需求规格
─────────────────────────────
凭证状态：        [已就绪 / 需先创建]
ASR：             [fengming (default) / tencent / microsoft / xfyun / xfyun_bigmodel / xfyun_dialect]
LLM：             [aliyun / bytedance / deepseek / tencent]
TTS：             [minimax / tencent / bytedance / microsoft / cosyvoice / bytedance_duplex / stepfun]
开发语言：        [Go / Java / Python/curl]
─────────────────────────────
```

## Defaults

| Field | Default | Notes |
|-------|---------|-------|
| ASR vendor | `fengming` | 声网凤鸣 ASR，默认 zh-CN |
| ASR language | `zh-CN` | 中文（支持中英混合） |
| LLM vendor | `deepseek` | 需用户提供 LLM url (OpenAI 兼容) |
| TTS vendor | `bytedance` | 火山引擎 TTS |
| LLM = 没决定 | `deepseek` | |

> ASR/TTS/LLM 可选值均来自 [convoai-restapi.yaml](../integrate-shengwang-conversational-ai/references/convoai-restapi.yaml)，不可自行编造。

## Route After Collection

Pass the structured spec to [integrate-shengwang-conversational-ai/SKILL.md](../integrate-shengwang-conversational-ai/SKILL.md),
skipping questions already answered.

| Detail | Routing hint |
|--------|-------------|
| Dev = Go | ConvoAI SKILL.md → MCP `get-doc-content {"uri": "docs://default/convoai/restful/get-started/quick-start-go"}` |
| Dev = Java | ConvoAI SKILL.md → MCP `get-doc-content {"uri": "docs://default/convoai/restful/get-started/quick-start-java"}` |
| Dev = Python/curl | ConvoAI SKILL.md → MCP `get-doc-content {"uri": "docs://default/convoai/restful/get-started/quick-start"}` |
| Needs Go/Java SDK | [resource-downloader/SKILL.md](../resource-downloader/SKILL.md) to download REST client SDK |
| Needs Token Builder | [resource-downloader/SKILL.md](../resource-downloader/SKILL.md) to download AgoraDynamicKey |
