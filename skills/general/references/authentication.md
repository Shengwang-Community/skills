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

## RTC Channel Token

The RTC token is separate from REST auth. It authorizes a user or agent to join an RTC channel.

| App Certificate status | Token value |
|-----------------------|-------------|
| Not enabled | `""` (empty string) — no token needed |
| Enabled | Generate server-side via Agora Token Builder |

### When to generate a token

- Any operation that joins an RTC channel (ConvoAI `/join`, RTC SDK join, etc.)
- Always generate server-side — never in client code
- Set expiry longer than the expected session duration

### Token Builder libraries

| Language | Package |
|----------|---------|
| Go | `github.com/AgoraIO/Tools/DynamicKey/AgoraDynamicKey/go` |
| Java | `github.com/AgoraIO/Tools/DynamicKey/AgoraDynamicKey/java` |
| Python | `github.com/AgoraIO/Tools/DynamicKey/AgoraDynamicKey/python` |
| Node.js | `github.com/AgoraIO/Tools/DynamicKey/AgoraDynamicKey/nodejs` |
| C++ | `github.com/AgoraIO/Tools/DynamicKey/AgoraDynamicKey/cpp` |

### Minimal Go example

```go
import rtctokenbuilder "github.com/AgoraIO/Tools/DynamicKey/AgoraDynamicKey/go/src/rtctokenbuilder2"

token, err := rtctokenbuilder.BuildTokenWithUid(
    os.Getenv("AGORA_APP_ID"),
    os.Getenv("AGORA_APP_CERTIFICATE"),
    channelName,
    uid,                                    // 0 for auto-assign
    rtctokenbuilder.RolePublisher,
    tokenExpireSeconds,                     // e.g. 3600
    privilegeExpireSeconds,                 // e.g. 3600
)
```

### Rules

- `uid` must match the UID used when joining the channel
- If token expires mid-session, update it via the product's update API
  - ConvoAI: `POST /agents/{agentId}/update` with new token
- Use `RolePublisher` for agents that send audio; `RoleSubscriber` for listen-only
