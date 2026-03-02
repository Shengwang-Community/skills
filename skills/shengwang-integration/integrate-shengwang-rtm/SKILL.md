---
name: integrate-shengwang-rtm
description: |
  Guides integration of Shengwang (Agora) RTM (Real-Time Messaging) SDK
  for signaling, messaging, presence, and pub/sub features.
  Use when the user asks about chat, messaging, signaling, notifications,
  presence, 聊天, 消息, 信令, or real-time data sync.
license: MIT
metadata:
  author: shengwang
  version: "1.0.0"
---

# Shengwang RTM (Real-Time Messaging)

Real-time messaging and signaling SDK. Often paired with RTC for call invitation, presence, and chat.

## Quick Reference

| Item | Value |
|------|-------|
| What it does | Messaging, signaling, presence, pub/sub, storage |
| Current version | RTM v2 |
| Client SDKs | Web, Android, iOS, macOS, Windows, Flutter, React Native, Electron, Unity |
| Auth | RTM Token — see [implement-shengwang-token-on-server](../implement-shengwang-token-on-server/SKILL.md) |
| Credentials | `AGORA_APP_ID` + `AGORA_APP_CERTIFICATE` |

## Supported Platforms & Quick Start URIs (MCP)

| Platform | MCP URI |
|----------|---------|
| Web (JS) | `docs://default/rtm2/javascript/get-started/quick-start` |
| Android | `docs://default/rtm2/android/get-started/quick-start` |
| iOS | `docs://default/rtm2/ios/get-started/quick-start` |

## Workflow

### Step 1: Confirm Credentials

Need `AGORA_APP_ID` and `AGORA_APP_CERTIFICATE` (RTM always requires token).
Missing? → [general/references/credentials.md](../general/references/credentials.md)

### Step 2: Identify Platform

Ask the user which platform they're targeting if not already clear.

### Step 3: Fetch Quick Start via MCP (MANDATORY)

Call `get-doc-content` with the URI matching the user's platform (table above).
Read the returned doc fully before writing any code.

### Step 4: Generate Code

Follow the quick start doc. Core flow:
1. Create RTM client with `AGORA_APP_ID`
2. Login with RTM token and user ID
3. Subscribe to channels / topics
4. Publish messages
5. Handle incoming messages via event listeners
6. Logout on exit

### Step 5: Validate

- [ ] AppID from env var, never hardcoded
- [ ] RTM token generated server-side (not RTC token — different builder)
- [ ] Proper logout and cleanup on exit
- [ ] Message event listeners registered before subscribing

## Core Features

| Feature | Description |
|---------|-------------|
| Message Channel | Pub/sub messaging to channels |
| Stream Channel | Low-latency data streaming (like RTC data channel) |
| Presence | Track who is online in a channel |
| Storage | Key-value storage per channel or user |
| Lock | Distributed locking for concurrency control |

## RTM vs RTC Token

RTM uses a different token builder class than RTC:

| Product | Builder | Method |
|---------|---------|--------|
| RTC | `RtcTokenBuilder2` | `BuildTokenWithUid` |
| RTM | `RtmTokenBuilder2` | `BuildToken` |

Both are in the same AgoraDynamicKey library. See [implement-shengwang-token-on-server](../implement-shengwang-token-on-server/SKILL.md).

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Login failed | Invalid token or expired | Regenerate RTM token |
| Subscribe failed | Channel name invalid | Check channel naming rules (no special chars) |
| Permission denied | Token doesn't match user ID | Ensure token was generated for the correct userId |

## Docs Fallback

If MCP is unavailable: https://doc.shengwang.cn/doc/rtm2/javascript/get-started/quick-start
