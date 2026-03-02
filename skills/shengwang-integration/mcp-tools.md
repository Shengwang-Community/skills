# Agora Doc MCP Tools

Internal guide for the model. Describes how to use the Agora Doc MCP server
to fetch up-to-date documentation content during skill execution.

**MCP endpoint:** `https://doc-mcp.shengwang.cn/mcp`

## Tools

| Tool | Input | Returns | When to use |
|------|-------|---------|-------------|
| `get-doc-content` | `{"uri": "docs://..."}` | Full markdown content | Read a specific doc (preferred) |
| `search-docs` | `{"query": "keyword"}` | List of matching doc URIs | Find docs when URI is unknown |
| `list-docs` | `{"category": "...", "limit": 20}` | All docs in a category | Browse available docs |

## Preferred Approach: Direct URI

When the doc URI is known, call `get-doc-content` directly — no search needed:

```
get-doc-content {"uri": "docs://default/convoai/restful/get-started/quick-start"}
```

## Known Doc URIs

Each product skill defines its own MCP URIs. Consolidated here for reference:

| Product | Topic | URI |
|---------|-------|-----|
| ConvoAI | Quick Start (Python/curl) | `docs://default/convoai/restful/get-started/quick-start` |
| ConvoAI | Quick Start (Go) | `docs://default/convoai/restful/get-started/quick-start-go` |
| ConvoAI | Quick Start (Java) | `docs://default/convoai/restful/get-started/quick-start-java` |
| RTC | Quick Start (Web) | `docs://default/rtc/javascript/get-started/quick-start` |
| RTC | Quick Start (Android) | `docs://default/rtc/android/get-started/quick-start` |
| RTC | Quick Start (iOS) | `docs://default/rtc/ios/get-started/quick-start` |
| RTM | Quick Start (Web) | `docs://default/rtm2/javascript/get-started/quick-start` |
| RTM | Quick Start (Android) | `docs://default/rtm2/android/get-started/quick-start` |
| RTM | Quick Start (iOS) | `docs://default/rtm2/ios/get-started/quick-start` |
| Cloud Recording | Quick Start | `docs://default/cloud-recording/restful/get-started/quick-start` |

## Fallback: Search Then Read

When the URI is unknown, search first:

```
Step 1: search-docs {"query": "convoai <topic>"}
        → returns [{uri: "docs://...", text: "..."}, ...]

Step 2: get-doc-content {"uri": "docs://..."}
        → returns full doc content
```

## When to Call MCP

**Always call for:**
- API field details, request/response formats
- Vendor configurations (TTS, ASR)
- Error codes and their meanings
- Any content that may change with documentation updates

**Do NOT call for:**
- Generation rules (field types, naming conventions) — stable, in skill files
- Auth patterns — stable, in [general/references/authentication.md](general/references/authentication.md)
- Workflow steps — stable, in skill files
