# Agora Credentials & Authentication

Cross-product knowledge shared by all Agora products.

## Credentials

| Credential | Where to find | Used for |
|------------|--------------|---------|
| `AGORA_APP_ID` | Console → Project Overview | All API calls and SDK init |
| `AGORA_CUSTOMER_KEY` | Console → Settings → RESTful API | REST API Basic Auth username |
| `AGORA_CUSTOMER_SECRET` | Console → Settings → RESTful API | REST API Basic Auth password |
| `AGORA_APP_CERTIFICATE` | Console → Project Overview | Token generation (only if enabled) |

Console: https://console.shengwang.cn/

### Environment Variables

```bash
AGORA_APP_ID=your_app_id
AGORA_CUSTOMER_KEY=your_customer_key
AGORA_CUSTOMER_SECRET=your_customer_secret
AGORA_APP_CERTIFICATE=your_app_certificate   # only if App Certificate enabled
```

- ALWAYS read from env vars — never hardcode
- NEVER put secrets in client-side code
- NEVER commit `.env` with real values

### Service Activation

Some products require extra activation in Console beyond having credentials:

| Product | Extra requirement |
|---------|------------------|
| ConvoAI | Enable ConvoAI service (403 if not done) |
| Cloud Recording | Enable Cloud Recording service |
| RTC / RTM | No extra activation needed |

## REST API Authentication

All Agora REST APIs (ConvoAI, Cloud Recording, etc.) use HTTP Basic Auth:

```
Authorization: Basic base64("{AGORA_CUSTOMER_KEY}:{AGORA_CUSTOMER_SECRET}")
```

**curl example:**
```bash
AUTH=$(echo -n "$AGORA_CUSTOMER_KEY:$AGORA_CUSTOMER_SECRET" | base64)
curl -H "Authorization: Basic $AUTH" \
     -H "Content-Type: application/json" \
     https://api.agora.io/...
```

For language-specific auth patterns (Go, Java, Python, Node.js), fetch the quick start docs for each product (see URLs in product module READMEs).

## RTC / RTM Token

Token generation is separate from REST auth. See [token-server](../token-server/README.md).

## Docs

| Topic | URL |
|-------|-----|
| Token authentication overview | `https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/rtc/android/basic-features/token-authentication` |

## Docs Fallback

If fetch fails: https://doc.shengwang.cn/doc/rtc/android/basic-features/token-authentication
