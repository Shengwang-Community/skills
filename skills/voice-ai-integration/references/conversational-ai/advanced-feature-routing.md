# ConvoAI Advanced Feature Routing

Use this file for ConvoAI requests that already have a working baseline or that are clearly about
debugging or production work rather than first-run onboarding.

This file exists so users with working code do **not** get forced back through the full
quickstart-style intake.

## Use This File For

- `advanced-feature`
- `debugging`
- `ops-hardening`

Use [request-modes.md](request-modes.md) first if the mode is still unclear.

## Goal

Keep the questions tightly scoped to the requested capability or problem.

Do not re-run the full quickstart flow unless the user turns out to be blocked on a foundational
prerequisite that was never actually satisfied.

## Step 1: Confirm Baseline

Confirm the smallest useful baseline in one sentence:
- What is already working?
- Which platform or repo is this in?
- What exactly needs to change?

Examples:
- "Current status: Web ConvoAI sample is already running; next task is adding MCP tools."
- "Current status: Existing project can create and join agents; next task is debugging TTS vendor auth."

## Step 2: Route by Request Type

### A. Advanced feature implementation

### Feature Map

| Feature | Primary local doc | Fetch if needed |
|---------|-------------------|-----------------|
| MCP / tools | `convoai-restapi/start-agent.md` (`mcp_servers`) | ConvoAI MCP user guide |
| history | `convoai-restapi/get-history.md` | - |
| interrupt | `convoai-restapi/agent-interrupt.md` | - |
| speak | `convoai-restapi/agent-speak.md` | - |
| update LLM | `convoai-restapi/agent-update.md` | - |
| template variables | `convoai-restapi/start-agent.md` (`template_variables`) | - |
| status query | `convoai-restapi/query-agent-status.md` | - |
| stop agent | `convoai-restapi/stop-agent.md` | - |

Examples:
- MCP / tools
- history / interrupt / update / status APIs
- template variables / prompt work
- recording linkage
- multi-agent or orchestration behavior

Routing:
- Start from [README.md](README.md) for current architecture rules
- Use [sample-repos.md](sample-repos.md) if the feature must stay aligned with the official sample structure
- Use the relevant REST endpoint docs only for the exact unsupported or low-level operation

### B. Debugging

Examples:
- `403`
- vendor auth or param failures
- Agent `FAILED`
- token or channel mismatch
- join / update / leave behavior issues

Routing:
- Start from [common-errors.md](common-errors.md)
- Fetch endpoint-specific docs only for the failing operation when needed
- If the issue is provider-specific, run a **partial** provider check using the supported-provider and baseline rules in [quickstart-intake.md](quickstart-intake.md)

### C. Ops / hardening

Examples:
- auth strategy
- token generation path
- retries / backoff
- quota and concurrency handling
- monitoring and operational policy

Routing:
- Shared credentials / auth → [../general/credentials-and-auth.md](../general/credentials-and-auth.md)
- Token generation → [../token-server/README.md](../token-server/README.md)
- ConvoAI architecture constraints → [README.md](README.md)

## Step 3: Ask Only Targeted Questions

Ask only the minimum questions that unblock the specific request.

Examples:
- For MCP / tools: current server stack, current sample repo, desired tools, and whether the baseline is already running
- For provider switch: which stage is changing, current working provider, target provider, and whether required secrets already exist
- For 403: which auth path is being used, whether ConvoAI is enabled, and whether App ID matches the credentials project

Do not ask the user to reconfirm unrelated ASR / LLM / TTS stages when only one stage is changing.

## Partial Preflight Rule

Run only the narrowest possible validation for the touched scope:
- auth issue → auth only
- TTS issue → TTS only
- LLM change → LLM only
- sample alignment question → sample repo only

Escalate to the full quickstart preflight only if the conversation reveals there is no real working
baseline after all.

## Exit Rule

After the targeted questions, produce a short recap:

```text
ConvoAI mode: [advanced-feature / debugging / ops-hardening]
Working baseline: [one sentence]
Focus area: [feature or issue]
Next reference: [which local file or doc path will be used]
```
