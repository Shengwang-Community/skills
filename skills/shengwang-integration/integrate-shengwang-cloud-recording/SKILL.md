---
name: integrate-shengwang-cloud-recording
description: |
  Guides integration of Shengwang (Agora) Cloud Recording for server-side
  recording of RTC sessions. Covers acquire/start/stop/query lifecycle.
  Use when the user asks about recording video calls, archiving sessions,
  录制, 存档, or server-side recording.
license: MIT
metadata:
  author: shengwang
  version: "1.0.0"
---

# Shengwang Cloud Recording

Server-side recording of RTC channel audio/video. No client SDK needed — pure REST API.

## Quick Reference

| Item | Value |
|------|-------|
| What it does | Records RTC sessions to cloud storage (S3, OSS, Azure Blob, etc.) |
| Interface | REST API only (no SDK) |
| Auth | HTTP Basic Auth (`AGORA_CUSTOMER_KEY` + `AGORA_CUSTOMER_SECRET`) |
| Prerequisite | Cloud Recording service enabled in Agora Console |
| Depends on | Active RTC channel with participants |

## Quick Start URI (MCP)

| Topic | MCP URI |
|-------|---------|
| Quick Start | `docs://default/cloud-recording/restful/get-started/quick-start` |

## Workflow

### Step 1: Confirm Prerequisites

- [ ] `AGORA_APP_ID`, `AGORA_CUSTOMER_KEY`, `AGORA_CUSTOMER_SECRET` ready
- [ ] Cloud Recording service enabled in [Agora Console](https://console.agora.io/)
- [ ] Cloud storage configured (S3, Alibaba OSS, Azure Blob, etc.)

Missing credentials? → [general/references/credentials.md](../general/references/credentials.md)

### Step 2: Fetch Quick Start via MCP (MANDATORY)

```
get-doc-content {"uri": "docs://default/cloud-recording/restful/get-started/quick-start"}
```

Read the returned doc fully before writing any code.

### Step 3: Implement Recording Lifecycle

Cloud Recording follows a strict 3-step lifecycle:

```
acquire → start → stop
            ↑
          query (optional, check status)
```

#### 3a. Acquire Resource

```
POST /v1/apps/{appId}/cloud_recording/acquire
```
Returns a `resourceId` (valid for 5 minutes — must call start quickly).

#### 3b. Start Recording

```
POST /v1/apps/{appId}/cloud_recording/resourceid/{resourceId}/mode/{mode}/start
```
Modes: `individual` (per-user files), `mix` (single mixed file), `web` (web page recording).

#### 3c. Query Status (optional)

```
GET /v1/apps/{appId}/cloud_recording/resourceid/{resourceId}/sid/{sid}/mode/{mode}/query
```

#### 3d. Stop Recording

```
POST /v1/apps/{appId}/cloud_recording/resourceid/{resourceId}/sid/{sid}/mode/{mode}/stop
```

### Step 4: Validate

- [ ] Credentials from env vars, never hardcoded
- [ ] `acquire` called before `start` (resourceId has 5-min TTL)
- [ ] Storage config matches user's cloud provider
- [ ] RTC channel has active participants before starting recording
- [ ] `stop` called when recording is no longer needed (avoids billing)

## Recording Modes

| Mode | Output | Use case |
|------|--------|----------|
| `individual` | Separate audio/video file per user | Post-processing, transcription |
| `mix` | Single mixed audio/video file | Archival, playback |
| `web` | Records a web page as video | Web app recording, whiteboard |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 403 | Cloud Recording not enabled | Enable in Agora Console |
| 404 | Resource expired or invalid sid | Re-acquire resource, check sid |
| 432 | Recording already in progress | Query existing recording first |
| 435 | No users in channel | Ensure RTC channel has active participants |
| Storage error | Wrong storage config | Verify bucket name, access keys, region |

## Auth Pattern

Same as all Agora REST APIs — HTTP Basic Auth:
```
Authorization: Basic base64("{AGORA_CUSTOMER_KEY}:{AGORA_CUSTOMER_SECRET}")
```
See [general/references/authentication.md](../general/references/authentication.md)

## Docs Fallback

If MCP is unavailable: https://doc.shengwang.cn/doc/cloud-recording/restful/get-started/quick-start
