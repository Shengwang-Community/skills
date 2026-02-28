---
name: implement-shengwang-token-on-server
description: |
  Implements Shengwang (Agora) Token generation on backend servers using
  AgoraDynamicKey. Use when the user asks to generate a Token, implement a
  token API endpoint, or set up server-side authentication for RTC, RTM, or
  ConvoAI.
  Use when the user mentions token生成, 实现token, 鉴权, AccessToken2,
  AgoraDynamicKey, or server-side authentication for any Shengwang product.
triggers:
  - "shengwang token"
  - "rtc token"
  - "rtm token"
  - "agora token"
  - "token generation"
  - "token server"
  - "accesstoken2"
  - "agoradynamickey"
  - "token authentication"
  - "generate token"
  - "token endpoint"
  - "token鉴权"
  - "生成token"
  - "token服务"
  - "RTC鉴权"
  - "RTM鉴权"
metadata:
  author: shengwang
  version: "1.1.0"
---

# Shengwang Token Server

Implements server-side Token generation using the AgoraDynamicKey library.

## Overview

Agora uses **AccessToken2** (HMAC-SHA256) for channel authentication. Token generation:
1. Requires `AGORA_APP_ID` + `AGORA_APP_CERTIFICATE` (server-side only)
2. Uses the open-source `AgoraDynamicKey` library
3. Must be implemented server-side — never expose `APP_CERTIFICATE` to clients

## Supported Languages

| Language | Core Method | SDK |
|----------|-------------|-----|
| Go | `BuildTokenWithUid` | `github.com/AgoraIO/Tools/.../rtctokenbuilder2` |
| Java | `buildTokenWithUid` | AgoraDynamicKey Java |
| Python | `build_token_with_uid` | AgoraDynamicKey Python |
| Node.js | `buildTokenWithUid` | AgoraDynamicKey Node.js |
| PHP | `buildTokenWithUid` | AgoraDynamicKey PHP |
| C++ | `buildTokenWithUid` | AgoraDynamicKey C++ |

---

## Workflow

### Step 1: Detect Server Language

Check the codebase for:
- **Go**: `go.mod`, `.go` files
- **Java**: `pom.xml`, `build.gradle`, `.java` files
- **Python**: `requirements.txt`, `pyproject.toml`, `.py` files
- **Node.js**: `package.json`, `.ts`/`.js` files
- **PHP**: `composer.json`, `.php` files
- **C++**: `CMakeLists.txt`, `.cpp` files

If unclear, ask the user.

### Step 2: Download AgoraDynamicKey

Use the resource downloader to fetch the library:

```bash
python3 <path-to-skills>/resource-downloader/scripts/downloader.py \
  https://github.com/AgoraIO/Tools \
  <workspace_root>
```

> `<path-to-skills>` is the directory containing this skill (the parent of `token-server/`).
> For example, if skills are installed at `.claude/skills/agora/skills/`, use that path.

The `DynamicKey/AgoraDynamicKey/` directory contains all language implementations.

See [references/sdk-urls.md](references/sdk-urls.md) for direct per-language URLs.

### Step 3: Implement Token Endpoint

Create a `GET /api/agora/token` endpoint.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `channelName` | string | Yes | — | RTC channel name |
| `uid` | int/string | No | `0` | User ID (0 = auto-assign) |
| `role` | string | No | `publisher` | `publisher` or `subscriber` |
| `expireSeconds` | int | No | `3600` | Token validity in seconds |

**Environment Variables:**
```bash
AGORA_APP_ID=your_app_id
AGORA_APP_CERTIFICATE=your_app_certificate
```

**Response:** Plain text token string

**HTTP Status Codes:**
- `200` — Token generated successfully
- `400` — Missing required parameters
- `500` — Token generation failed

### Step 4: Configure Environment Variables

- Local: add to `.env`
- Production: configure in deployment environment
- NEVER commit `AGORA_APP_CERTIFICATE` to version control

---

## Token Types

### By Product

| Product | Builder class | Key method |
|---------|--------------|------------|
| RTC (channel join) | `RtcTokenBuilder2` | `BuildTokenWithUid` |
| RTM (messaging) | `RtmTokenBuilder` | `BuildToken` |
| Chat | `ChatTokenBuilder2` | `BuildUserToken` |

This skill focuses on **RTC token** (most common). RTM and Chat follow the same pattern — same library, different builder class.

### RTC: Standard Token (BuildTokenWithUid)

One expiry for all privileges. Use for most cases.

```
BuildTokenWithUid(appId, appCertificate, channelName, uid, role, tokenExpire, privilegeExpire)
```

- `role`: `RolePublisher` (send+receive) or `RoleSubscriber` (receive only)
- `tokenExpire`: seconds until token expires
- `privilegeExpire`: seconds until channel join privilege expires (set same as tokenExpire)

### Wildcard Token

For users who frequently switch channels or join multiple channels:

- Set `uid = 0` → token works for any UID
- Set `channelName = ""` → token works for any channel
- Both wildcard → single token for any user in any channel (use with caution)

### Fine-grained Token (BuildTokenWithUidAndPrivilege)

Set separate expiry for each privilege:
- `joinChannelPrivilege` — join channel
- `pubAudioPrivilege` — publish audio
- `pubVideoPrivilege` — publish video
- `pubDataStreamPrivilege` — publish data stream

Use when you need to control publish permissions independently (e.g. co-host scenarios).

---

## Token Expiry Handling

Client SDK fires these callbacks before/on expiry:

| Callback | When | Action |
|----------|------|--------|
| `onTokenPrivilegeWillExpire` | 30s before expiry | Fetch new token, call `renewToken()` |
| `onRequestToken` | Token expired | Fetch new token, call `renewToken()` |

For multi-channel (joinChannelEx): use `updateChannelMediaOptionsEx` to update token.

---

## ConvoAI Integration

When using token with ConvoAI `/join`:

```json
{
  "properties": {
    "channel": "my_channel",
    "token": "<token_generated_here>",
    "agent_rtc_uid": "0"
  }
}
```

- Generate token for `channelName` = the RTC channel the agent joins
- `uid` = the agent's UID (match `agent_rtc_uid`, or use `0` for auto-assign)
- If token expires mid-session → call `POST /agents/{agentId}/update` with new token

---

## References

- [references/sdk-urls.md](references/sdk-urls.md) — AgoraDynamicKey download URLs per language
- [references/api-spec.md](references/api-spec.md) — Token endpoint API spec
- Official docs: https://doc.shengwang.cn/doc/rtc/android/basic-features/token-authentication
