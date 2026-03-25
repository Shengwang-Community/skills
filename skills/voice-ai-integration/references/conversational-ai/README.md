# Shengwang Conversational AI Engine (ConvoAI)

Real-time AI voice agent. User speaks into an RTC channel, agent responds via ASR → LLM → TTS pipeline.

## How It Works

```
User Device ── audio ──► RTC Channel ──► ConvoAI Agent (ASR → LLM → TTS)
User Device ◄── audio ── RTC Channel ◄── ConvoAI Agent
```

- Agent is server-side only — managed via REST API, no client SDK
- Client should prefer `agora-agent-client-toolkit` when it fits the target stack; otherwise use the RTC SDK directly to join the channel
- `POST /join` makes the agent join the same RTC channel

## Start Here

Always start ConvoAI work by classifying the request mode with
[request-modes.md](request-modes.md).

- `quickstart` and `integration` without a proven working baseline → start with
  [quickstart-intake.md](quickstart-intake.md), which now contains the full quickstart flow:
  product intro → technical path → credential checkpoint → provider choices
- `advanced-feature`, `debugging`, and `ops-hardening` → use
  [advanced-feature-routing.md](advanced-feature-routing.md)

## Flow Map

```text
request-modes.md
  ├─ quickstart / integration → quickstart-intake.md
  │    ├─ product intro
  │    ├─ technical path
  │    ├─ project readiness
  │    ├─ provider confirmation
  │    └─ sample-repos.md → code generation
  └─ advanced / debugging / ops → advanced-feature-routing.md
       ├─ common-errors.md
       └─ convoai-restapi/index.mdx or endpoint docs
```

## Architecture Defaults

Use this order unless the user explicitly asks for something else:

1. If a matching official ConvoAI sample repo exists, offer the sample-aligned path first and inspect that repo after the user accepts the default technical path or explicitly asks for sample-aligned implementation
2. Preserve the sample repo structure and keep `sample-aligned` as the default path unless the user explicitly asks for `minimal-custom`
3. On the server side, prefer `agent-server-sdk`
4. On the client side, prefer `agora-agent-client-toolkit` when the target stack supports it; otherwise fall back to the RTC SDK directly
5. Use fetched Shengwang docs to fill in missing product details after the sample path has been inspected
6. Use raw REST directly only for unsupported operations, debugging, or explicit REST-first requests

Do not treat the REST quick start or endpoint index as the default architecture for a new ConvoAI integration when a matching sample or official SDK path already exists.

## Auth Snapshot

- ConvoAI quickstart assumes a Shengwang project with `App ID`, `App Certificate`, and ConvoAI service activation already in place
- Quickstart uses RTC Token as the fixed auth path
- The `token` field in `/join` is for the RTC channel, not for REST auth
- Detailed credential rules → [../general/credentials-and-auth.md](../general/credentials-and-auth.md)
- Token generation → [../token-server/README.md](../token-server/README.md)

## Entry Navigation

- Request mode routing → [request-modes.md](request-modes.md)
- ConvoAI question-driven quickstart flow → [quickstart-intake.md](quickstart-intake.md)
- Existing-project features / debugging / ops → [advanced-feature-routing.md](advanced-feature-routing.md)
- Sample repos and sample workflow → [sample-repos.md](sample-repos.md)
- Stable generation constraints → [generation-rules.md](generation-rules.md)
- REST endpoint index → [convoai-restapi/index.mdx](convoai-restapi/index.mdx)
- Common diagnosis → [common-errors.md](common-errors.md)
- Doc fetching guide → [../doc-fetching.md](../doc-fetching.md)

## Docs Fallback

If fetch fails: https://doc.shengwang.cn/doc/convoai/restful/get-started/quick-start
