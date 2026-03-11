# Shengwang Doc Fetching Guide

## Overview

Shengwang docs are fetched directly via HTTP. The doc index is downloaded locally to `references/docs.txt`, which maps document names to fetchable URLs.

## Step 1: Ensure doc index exists

Before starting any work, check if `references/docs.txt` exists.

If not, download it:
```bash
bash skills/shengwang-integration/scripts/fetch-docs.sh
```

## Step 2: Find the document URL

Search `references/docs.txt` for keywords to find the target document URL.

Each entry in `docs.txt` follows this format:
```
- [doc-name](https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/...)
```

## Step 3: Fetch the document

Use web fetch to access the URL directly. It returns Markdown content.

Examples:
```
fetch https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/convoai/restful/get-started/quick-start
fetch https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/rtc/javascript/get-started/quick-start
```

## URL Pattern

All doc URLs follow a consistent format:
```
https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/{product}/{platform}/{path}
```

Common product prefixes:
| Product | URI prefix |
|---------|-----------|
| ConvoAI | `docs://default/convoai/restful/...` |
| RTC | `docs://default/rtc/{platform}/...` |
| RTM | `docs://default/rtm2/{platform}/...` |
| Cloud Recording | `docs://default/cloud-recording/restful/...` |
| Token Auth | `docs://default/rtc/{platform}/basic-features/token-authentication` |

## When to fetch

Fetch for:
- API field details, request/response schemas
- Vendor configurations (TTS, ASR)
- Error codes and meanings
- Any content that may change with doc updates

Do NOT fetch for:
- Generation rules (field types, naming conventions) — stable, in skill files
- Auth patterns — stable, in [general/credentials-and-auth.md](general/credentials-and-auth.md)
- Workflow steps — stable, in skill files

## Fallback

If HTTP fetch fails, use the Shengwang doc site URL:
```
https://doc.shengwang.cn/doc/{product}/{platform}/{path}
```
