# Agora Credentials

All Agora products share the same credential system.

## Credential Reference

| Credential | Where to find | Used for |
|------------|--------------|---------|
| `AGORA_APP_ID` | Console → Project Overview | Identifies your project in all API calls and SDK init |
| `AGORA_CUSTOMER_KEY` | Console → Settings → RESTful API | REST API Basic Auth username |
| `AGORA_CUSTOMER_SECRET` | Console → Settings → RESTful API | REST API Basic Auth password |
| `AGORA_APP_CERTIFICATE` | Console → Project Overview | RTC token generation (only needed if App Certificate is enabled) |

Get all credentials at: https://console.agora.io/

## Generation Rules

- ALWAYS read credentials from environment variables — never hardcode
- NEVER put `AGORA_CUSTOMER_SECRET` or `AGORA_APP_CERTIFICATE` in client-side code
- If user doesn't have credentials → direct to https://console.agora.io/ to create a project

## Product-Specific Notes

Each product may require additional setup beyond having credentials:

| Product | Extra requirement |
|---------|------------------|
| ConvoAI | Enable ConvoAI service in Agora Console (causes 403 if not done) |
| Cloud Recording | Enable Cloud Recording service in Console |
| RTC | No extra service activation needed |

## Environment Variable Names

Standard names used across all skill examples:

```bash
AGORA_APP_ID=your_app_id
AGORA_CUSTOMER_KEY=your_customer_key
AGORA_CUSTOMER_SECRET=your_customer_secret
AGORA_APP_CERTIFICATE=your_app_certificate   # only if App Certificate enabled
```

All product skills use these same env var names. Never hardcode credentials in source files or commit `.env` with real values.
