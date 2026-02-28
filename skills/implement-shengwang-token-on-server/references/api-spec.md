# Token Endpoint API Spec

## GET /api/agora/token

Generates an Agora RTC AccessToken2 for a user joining a channel.

### Request

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `channelName` | string | Yes | — | RTC channel name. Use `""` for wildcard (any channel). |
| `uid` | integer | No | `0` | User ID. `0` = auto-assign by Agora. Use `0` for wildcard (any user). |
| `role` | string | No | `publisher` | `publisher` (send+receive) or `subscriber` (receive only) |
| `expireSeconds` | integer | No | `3600` | Seconds until token expires. Max: 86400 (24h). |

### Response

**200 OK** — Plain text token string:
```
007eJxTYBBbsO...
```

**400 Bad Request:**
```json
{"error": "channelName is required"}
```

**500 Internal Server Error:**
```json
{"error": "token generation failed: <reason>"}
```

### Example Request

```bash
curl "http://localhost:8080/api/agora/token?channelName=my_channel&uid=12345&role=publisher&expireSeconds=3600"
```

### Environment Variables

```bash
AGORA_APP_ID=your_app_id           # from Agora Console → Project Overview
AGORA_APP_CERTIFICATE=your_cert    # from Agora Console → Project Overview
PORT=8080                          # optional, default 8080
```

## Role Values

| Role | Value | Privileges |
|------|-------|-----------|
| Publisher | `publisher` / `1` | Join channel + publish audio/video/data |
| Subscriber | `subscriber` / `2` | Join channel only (receive) |

## Token Validity Notes

- Set `expireSeconds` longer than the expected session duration
- Client SDK fires `onTokenPrivilegeWillExpire` 30s before expiry
- Client SDK fires `onRequestToken` when token expires
- For ConvoAI: update via `POST /agents/{agentId}/update` when token expires
