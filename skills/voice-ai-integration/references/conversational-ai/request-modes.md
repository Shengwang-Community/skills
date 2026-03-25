# ConvoAI Request Modes

Use this file before choosing a ConvoAI workflow.

ConvoAI is only one product inside the Shengwang skill set. Do **not** change the top-level
product routing for RTC, RTM, Cloud Recording, or token work. This file only decides which
ConvoAI sub-flow to use after ConvoAI has already been selected as the primary product.

## Goal

Separate requests that need a full quickstart-style onboarding flow from requests that already
have a working baseline and only need targeted implementation, debugging, or production work.

The key distinction is **working baseline**:
- A working baseline means the user already has ConvoAI code that can run, or explicitly says
  they already have a working project / demo / codebase.
- If the user only has RTC code, or only has a sample repo checked out but has **not** proven a
  working ConvoAI path yet, treat that as **not** having a working baseline.

## Modes

| Mode | Use when | Default next step |
|------|----------|-------------------|
| `quickstart` | The user is starting from scratch, wants a minimal demo, wants the official sample path, or has not yet run ConvoAI successfully | [quickstart-intake.md](quickstart-intake.md) |
| `integration` | The user already has an app or repo, but the ConvoAI path is not yet fully connected or verified | [quickstart-intake.md](quickstart-intake.md), then targeted implementation if a working baseline is still missing |
| `advanced-feature` | The user explicitly says the existing ConvoAI code is already running and only wants incremental capability work | [advanced-feature-routing.md](advanced-feature-routing.md) |
| `debugging` | The user provides errors, logs, broken behavior, or asks why an existing flow does not work | [advanced-feature-routing.md](advanced-feature-routing.md) |
| `ops-hardening` | The user asks about production auth, scaling, retries, quota, observability, or cost | [advanced-feature-routing.md](advanced-feature-routing.md) |

## Detection Rules

### Route to `quickstart`

Choose `quickstart` when the user says things like:
- "从零开始"
- "帮我跑一个最小 demo"
- "第一次接 ConvoAI"
- "按官方 sample 来"
- "想先跑通"

Also choose `quickstart` when the user has not yet confirmed any working ConvoAI baseline.

### Route to `integration`

Choose `integration` when the user already has an app, workspace, or product context, but the
ConvoAI path is still not proven end-to-end.

Examples:
- RTC app exists, now adding ConvoAI
- Existing web / mobile project wants ConvoAI business logic inserted
- The user wants sample-aligned integration into an existing codebase
- The user wants to swap one provider path but has not yet proven the overall ConvoAI flow works

### Route to `advanced-feature`

Choose `advanced-feature` only when the user has already confirmed a working ConvoAI baseline and
the ask is incremental.

Examples:
- Add MCP / tools
- Add history or interrupt APIs
- Add template variables or prompt customization
- Add recording, multi-agent behavior, or other capability extensions
- Switch a provider for a known working flow

### Route to `debugging`

Choose `debugging` when the user leads with a failure signal:
- Error codes like `400`, `403`, `409`, `422`, `503`
- Agent `FAILED`
- Vendor auth / parameter issues
- Token, channel, or join behavior problems
- "why is this not working" with existing code / logs

### Route to `ops-hardening`

Choose `ops-hardening` when the request is about production readiness rather than first-run
success.

Examples:
- Auth strategy
- Quota management
- Retry policy
- Monitoring / alerts
- Cost optimization

## Transition Rules

- `quickstart` and `integration` should start with the ConvoAI quickstart flow in `quickstart-intake.md`.
- `advanced-feature`, `debugging`, and `ops-hardening` should **skip** the full quickstart intake.
- `integration` should still use the full quickstart intake if the user has not yet proven that a
  ConvoAI baseline works in their environment.
- `advanced-feature` and `debugging` may still trigger a **partial** preflight for the exact part
  being changed, such as auth, token handling, or a single provider.

## Required Output

Before continuing, summarize the classification in one short recap:

```text
ConvoAI mode: [quickstart / integration / advanced-feature / debugging / ops-hardening]
Why: [one sentence]
Next step: [which reference file will be used]
```

## Safety Rule

Do not force users with an existing working ConvoAI project back through the full quickstart path.
Do not skip the quickstart path for users who are still blocked on foundational prerequisites.
