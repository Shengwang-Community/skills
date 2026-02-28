# Environment Variables

Use these keys consistently across all Shengwang skills and examples.

## Required Credentials

- `AGORA_APP_ID`: Project App ID from console.
- `AGORA_CUSTOMER_KEY`: REST API customer key.
- `AGORA_CUSTOMER_SECRET`: REST API customer secret.
- `AGORA_APP_CERTIFICATE`: App certificate used for token generation.

## Runtime and Safety

- Store credentials in `.env` (local) and secret managers (production).
- Never hardcode credentials in source files.
- Never commit `.env` with real values.

## Optional Settings

- `AGORA_REGION`: Optional deployment region override.
- `LOG_LEVEL`: `debug|info|warn|error`.
