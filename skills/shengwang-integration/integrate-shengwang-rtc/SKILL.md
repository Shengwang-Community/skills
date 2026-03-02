---
name: integrate-shengwang-rtc
description: |
  Guides integration of Shengwang (Agora) RTC SDK for real-time audio/video
  communication. Covers Web, Android, iOS, and other platforms.
  Use when the user asks about video calls, live streaming, voice calls,
  视频通话, 语音通话, 直播, or any real-time audio/video feature.
license: MIT
metadata:
  author: shengwang
  version: "1.0.0"
---

# Shengwang RTC SDK

Real-time audio/video communication SDK. Foundation layer for most Agora products.

## Quick Reference

| Item | Value |
|------|-------|
| What it does | 1v1 / group audio & video calls, live streaming |
| Client SDKs | Web, Android, iOS, macOS, Windows, Flutter, React Native, Electron, Unity |
| Auth | RTC Token (AccessToken2) — see [implement-shengwang-token-on-server](../implement-shengwang-token-on-server/SKILL.md) |
| Credentials | `AGORA_APP_ID` + optional `AGORA_APP_CERTIFICATE` |

## Supported Platforms & Quick Start URIs (MCP)

| Platform | MCP URI |
|----------|---------|
| Web (JS) | `docs://default/rtc/javascript/get-started/quick-start` |
| Android | `docs://default/rtc/android/get-started/quick-start` |
| iOS | `docs://default/rtc/ios/get-started/quick-start` |
| Flutter | `docs://default/rtc/flutter/get-started/quick-start` |
| React Native | `docs://default/rtc/react-native/get-started/quick-start` |
| Electron | `docs://default/rtc/electron/get-started/quick-start` |

## Workflow

### Step 1: Confirm Credentials

Need `AGORA_APP_ID`. If App Certificate is enabled, also need token server.
Missing? → [general/references/credentials.md](../general/references/credentials.md)

### Step 2: Identify Platform

Ask the user which platform they're targeting if not already clear.

### Step 3: Fetch Quick Start via MCP (MANDATORY)

Call `get-doc-content` with the URI matching the user's platform (table above).
Read the returned doc fully before writing any code.

### Step 4: Generate Code

Follow the quick start doc. Core flow for all platforms:
1. Initialize Agora engine with `AGORA_APP_ID`
2. Join channel with token (or empty string if no App Certificate)
3. Publish local audio/video tracks
4. Subscribe to remote tracks
5. Leave channel on exit

### Step 5: Validate

- [ ] AppID from env var, never hardcoded
- [ ] Token handling: empty string if no certificate, otherwise from token server
- [ ] Proper cleanup: leave channel and destroy engine on exit
- [ ] Camera/microphone permissions requested (mobile platforms)

## Common Patterns

| Pattern | Description |
|---------|-------------|
| 1v1 call | Two users join same channel, both publish |
| Group call | Multiple users join same channel |
| Live streaming | Host publishes, audience subscribes (set role) |
| Audio only | Disable video track, publish audio only |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `ERR_INVALID_APP_ID` | Wrong or missing AppID | Check `AGORA_APP_ID` |
| `ERR_INVALID_TOKEN` | Token expired or mismatched | Regenerate token, check channel name and UID match |
| `ERR_REFUSED` | Banned by server or token issue | Check Console for bans, verify token |
| Permission denied | No camera/mic permission | Request permissions before joining |

## Docs Fallback

If MCP is unavailable: https://doc.shengwang.cn/doc/rtc/javascript/get-started/quick-start
