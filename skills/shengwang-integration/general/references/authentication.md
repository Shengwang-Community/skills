# Agora Authentication Patterns

## REST API — HTTP Basic Auth

All Agora REST APIs use HTTP Basic Auth with Customer Key and Secret.

```
Authorization: Basic base64("{AGORA_CUSTOMER_KEY}:{AGORA_CUSTOMER_SECRET}")
```

### Code Examples

**curl:**
```bash
AUTH=$(echo -n "$AGORA_CUSTOMER_KEY:$AGORA_CUSTOMER_SECRET" | base64)
curl -H "Authorization: Basic $AUTH" https://api.agora.io/...
```

**Python:**
```python
import base64, os

auth = base64.b64encode(
    f"{os.getenv('AGORA_CUSTOMER_KEY')}:{os.getenv('AGORA_CUSTOMER_SECRET')}".encode()
).decode()
headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}
```

**Node.js:**
```javascript
const auth = Buffer.from(
  `${process.env.AGORA_CUSTOMER_KEY}:${process.env.AGORA_CUSTOMER_SECRET}`
).toString('base64');
const headers = { 'Authorization': `Basic ${auth}` };
```

**Go:**
```go
import "github.com/AgoraIO-Community/agora-rest-client-go/agora/auth"

credential := auth.NewBasicAuthCredential(
    os.Getenv("AGORA_CUSTOMER_KEY"),
    os.Getenv("AGORA_CUSTOMER_SECRET"),
)
```

**Java:**
```java
import io.agora.rest.core.BasicAuthCredential;

BasicAuthCredential credential = new BasicAuthCredential(
    System.getenv("AGORA_CUSTOMER_KEY"),
    System.getenv("AGORA_CUSTOMER_SECRET")
);
```

---

## RTC / RTM Token

Token generation is a separate concern from REST auth. For full details on token types,
supported languages, code examples, and token expiry handling, see:

→ [implement-shengwang-token-on-server/SKILL.md](../../implement-shengwang-token-on-server/SKILL.md)
