# Shengwang RTC SDK

Real-time audio/video communication SDK. Foundation layer for most Agora products.

## What It Does

- 1v1 / group audio & video calls
- Live streaming (host publishes, audience subscribes)
- Audio-only or video+audio
- Cross-platform: Web, Android, iOS, macOS, Windows, Flutter, React Native, Electron, Unity

## Core Flow

1. Initialize Agora engine with `AGORA_APP_ID`
2. Join channel with token (or empty string if no App Certificate)
3. Publish local audio/video tracks
4. Subscribe to remote tracks
5. Leave channel and destroy engine on exit

## Auth

- `AGORA_APP_ID` required
- If App Certificate enabled → need RTC token from server, see [token-server](../token-server/README.md)
- Credentials setup → [general/credentials-and-auth.md](../general/credentials-and-auth.md)

## Quick Start Docs

| Platform | URL |
|----------|-----|
| Web (JS) | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/rtc/javascript/get-started/quick-start` |
| Android | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/rtc/android/get-started/quick-start` |
| iOS | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/rtc/ios/get-started/quick-start` |
| Flutter | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/rtc/flutter/get-started/quick-start` |
| React Native | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/rtc/react-native/get-started/quick-start` |
| Electron | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/rtc/electron/get-started/quick-start` |

Fetch the URL directly using web fetch to get Markdown content.

## Demo Projects

| Platform | Repo |
|----------|------|
| Web | https://github.com/AgoraIO/API-Examples-Web |
| Android / iOS | https://github.com/AgoraIO/API-Examples |

## Docs Fallback

If fetch fails: https://doc.shengwang.cn/doc/rtc/javascript/get-started/quick-start
