# ConvoAI REST API Reference

Endpoint index with documentation URLs. For full request/response schemas, fetch the URL directly.

## Base URL

```
https://api.agora.io/cn/api/conversational-ai-agent/v2/projects/{AGORA_APP_ID}
```

## Authentication

HTTP Basic Auth — see [README.md](README.md#auth) and [general/credentials-and-auth.md](../general/credentials-and-auth.md).

## Endpoints

| Method | Path | Doc URL |
|--------|------|---------|
| POST | `/join` | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/convoai/restful/convoai/operations/start-agent` |
| POST | `/agents/{agentId}/leave` | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/convoai/restful/convoai/operations/stop-agent` |
| POST | `/agents/{agentId}/update` | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/convoai/restful/convoai/operations/agent-update` |
| GET | `/agents/{agentId}` | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/convoai/restful/convoai/operations/query-agent-status` |
| GET | `/agents` | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/convoai/restful/convoai/operations/get-agent-list` |
| POST | `/agents/{agentId}/speak` | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/convoai/restful/convoai/operations/agent-speak` |
| POST | `/agents/{agentId}/interrupt` | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/convoai/restful/convoai/operations/agent-interrupt` |
| GET | `/agents/{agentId}/history` | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/convoai/restful/convoai/operations/get-history` |

All endpoints index: `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/convoai/restful/convoai/operations`

## Error Response Format

All non-200 responses:
```json
{
  "detail": "error description",
  "reason": "ErrorCode"
}
```

Error diagnosis → [common-errors.md](common-errors.md)

## Docs Fallback

If fetch fails, use README.md Generation Rules + ask the user to verify against:
https://doc.shengwang.cn/doc/convoai/restful/get-started/quick-start
