# ConvoAI Pipeline Integration

Use this file only after quickstart confirms all of these:
- the user already has a pipeline ID
- the user selected the sample platform to implement
- the normal provider path should be skipped

## Goal

Reuse the official sample repo as the structural baseline, but replace the default provider-based request path with the user's existing pipeline-based request path.

This flow is for implementation, not intake. Do not send the user back to provider selection.

## Core Rules

1. Reuse the sample repo that matches the selected platform via [sample-repos.md](sample-repos.md).
2. Do NOT keep the default three-stage provider request path (`ASR` / `LLM` / `TTS`) when the implementation switches to pipeline mode.
3. Read the pipeline ID from environment variables. Do not hardcode it.
4. Use the fixed pipeline request shape defined in this file as the source of truth for method, URL, headers, body shape, and response parsing.
5. Do not ask the user to paste the pipeline `curl` again during normal implementation. If the API contract changes, update this file instead.
6. Do not invent pipeline request fields that are not present in this file or explicitly confirmed by the user.
7. Reuse the sample's existing RTC token generation rules and code path whenever possible; only change which UID each token is generated for.

## Current Request Shape

Current fixed request shape for pipeline mode:

```text
POST https://api.agora.io/cn/api/conversational-ai-agent/v2/projects/{SHENGWANG_APP_ID}/join/
Authorization: agora token={RTC_HEADER_TOKEN}
Content-Type: application/json; charset=utf-8

{
  "name": "{channel}",
  "pipeline_id": "{SHENGWANG_PIPELINE_ID}",
  "properties": {
    "agent_rtc_uid": "{agent_rtc_uid}",
    "channel": "{channel}",
    "remote_rtc_uids": ["*"],
    "token": "{RTC_AGENT_TOKEN}"
  }
}
```

Field mapping rules:

| Request field | Source |
|--------------|--------|
| URL project segment | Existing `SHENGWANG_APP_ID` |
| `Authorization` header token | RTC token generated with the caller/user UID using the sample's existing token-generation path, never the literal `curl` value |
| `name` | Same value as `channel` |
| `pipeline_id` | `SHENGWANG_PIPELINE_ID` from env |
| `properties.agent_rtc_uid` | Runtime RTC UID string |
| `properties.channel` | Runtime channel value |
| `properties.remote_rtc_uids` | `["*"]` unless the user asks for specific UIDs |
| `properties.token` | Separate RTC token generated with the agent UID using the sample's existing token-generation path, never the literal `curl` value |

Do not reintroduce the old `llm`, `tts`, or `asr` request blocks in pipeline mode.
Do not reuse one RTC token for both the `Authorization` header and `properties.token`.

## Expected Success Response

Current success response shape confirmed by the user:

```json
{
  "agent_id": "A42AN36NC98HN49AT73FE64HV77JL73A",
  "create_ts": 1774514395,
  "status": "RUNNING"
}
```

Code generated for this flow should parse and preserve these response fields:
- `agent_id`
- `create_ts`
- `status`

## Required Inputs

Before code generation, confirm only the minimum missing implementation details:
- the selected platform
- whether code should be generated into an existing workspace or a cloned sample baseline

Do NOT ask the user to paste:
- the actual pipeline ID value
- the pipeline `curl`

Normal behavior for this path:
- generate code against the fixed request shape in this file
- add `SHENGWANG_PIPELINE_ID` as config/env placeholder
- let the user fill the actual pipeline ID value locally in config

## Env and Config Rules

- Prefer `SHENGWANG_PIPELINE_ID` as the default env var name for new pipeline-based integrations unless the user asks for a different naming scheme.
- Reuse `SHENGWANG_APP_ID` for the project segment in the request URL.
- Keep existing required Shengwang credentials that are still needed by the sample and the target request path.
- Remove provider-only config when it is no longer used by pipeline mode.
- Remove unused env vars or config entries for `ASR`, `LLM`, and `TTS` when those values were only required by the old three-stage flow.
- Add the new pipeline ID config in the platform-appropriate env/config file and wire code to read from env instead of literals.
- Treat `SHENGWANG_PIPELINE_ID` as a user-filled config value. Add the placeholder, but do not ask the user to paste the live value into the conversation during normal implementation.
- Stay close to the sample's config style on every platform. Do not invent extra config-loading layers unless the sample already uses them.
- Never hardcode the `Authorization` token or the RTC `properties.token` from the `curl`; they must come from runtime auth/token flow or env-backed configuration.
- The header token and the agent token are both RTC tokens, but they must be generated separately and cannot be reused.
- Reuse the sample's existing token builder/service rules for both tokens instead of inventing a parallel token-generation implementation.

## Implementation Workflow

1. Pick the sample repo from [sample-repos.md](sample-repos.md) that matches the selected platform.
2. Inspect the repo's actual entrypoints and env template files.
3. Identify where the sample currently constructs or forwards the provider-based request.
4. Delete or replace only the sections that are specific to the old provider-based path.
5. Generate the new request code from the fixed pipeline request shape in this file, preserving:
   - `POST /cn/api/conversational-ai-agent/v2/projects/{appId}/join/`
   - `Authorization: agora token=...`
   - JSON body with `name`, `pipeline_id`, and `properties`
6. Map dynamic fields to code/runtime sources:
   - `name` → same value as `channel`
   - `pipeline_id` → `SHENGWANG_PIPELINE_ID`
   - URL project segment → `SHENGWANG_APP_ID`
   - `Authorization` header token → RTC token generated with the caller/user UID via the sample's existing token flow
   - `properties.token` → separate RTC token generated with the agent UID via the sample's existing token flow
   - `channel` / `agent_rtc_uid` → runtime values
7. Update config/env templates:
   - remove stale `ASR` / `LLM` / `TTS` settings when no longer used
   - add `SHENGWANG_PIPELINE_ID` placeholder (or the user-confirmed equivalent naming)
8. Keep the repo structure and surrounding RTC/UI flow as close to the sample as possible.
9. Do not leave dead provider helper functions, stale config structs, or unused env reads behind after the replacement.
10. Parse the pipeline join response and keep `agent_id`, `create_ts`, and `status` available to the app flow that needs them.

## Platform Notes

### Native

- Reuse the chosen native sample subdirectory as the baseline.
- Replace the old three-stage request builder with the pipeline-based request builder generated from the `curl`.
- Keep the native app structure, RTC/channel flow, and existing project conventions unless the user asks otherwise.

#### Native Inspection Order

Before editing any native platform, inspect files in this order:
1. The cloned repo's root `AGENTS.md` to locate the target platform directory.
2. The platform's env/config files or config models.
3. The request service/model that currently builds the provider-based join request.
4. The existing token-generation or token-consumption path.
5. The response parsing/state layer that receives the join result.
6. The UI/controller/view-model layer that triggers the request.

Do not start by editing UI files before the request/config/token path is understood.

#### iOS

1. Clone the native sample repo from [sample-repos.md](sample-repos.md) and use its `AGENTS.md` to locate the current iOS app directory.
2. Follow the Native Inspection Order above inside the iOS directory, starting from config files and the request service/model that currently builds the provider-based join request.
3. Replace only that request-building path with the pipeline request shape from this file.
4. Keep the existing iOS token-generation path, but generate:
   - the header RTC token with the caller/user UID
   - the body `properties.token` with the agent UID
5. Keep the sample's current config style while removing stale provider config and adding `SHENGWANG_PIPELINE_ID` as a user-filled placeholder.
6. Keep the rest of the RTC flow and UI structure close to the sample.
7. Parse and preserve `agent_id`, `create_ts`, and `status` from the join response.

#### Android

1. Clone the native sample repo from [sample-repos.md](sample-repos.md) and use its `AGENTS.md` to locate the current Android app directory.
2. Follow the Native Inspection Order above inside the Android directory, starting from config files and the request service/model that currently builds the provider-based join request.
3. Replace only that request-building path with the pipeline request shape from this file.
4. Keep the existing Android token-generation path, but generate the header token and agent token separately.
5. Keep the sample's current config style while removing stale provider config and adding `SHENGWANG_PIPELINE_ID`.
6. Keep the rest of the RTC flow and UI structure close to the sample.
7. Parse and preserve `agent_id`, `create_ts`, and `status` from the join response.

#### Flutter

1. Clone the native sample repo from [sample-repos.md](sample-repos.md) and use its `AGENTS.md` to locate the current Flutter app directory.
2. Follow the Native Inspection Order above inside the Flutter directory, starting from config files and the API service/model that currently builds the provider-based join request.
3. Replace only that request-building path with the pipeline request shape from this file.
4. Keep the existing Flutter token-generation path, but generate the header token and agent token separately.
5. Keep the sample's current config style while removing stale provider config and adding `SHENGWANG_PIPELINE_ID`.
6. Keep the rest of the RTC flow and UI structure close to the sample.
7. Parse and preserve `agent_id`, `create_ts`, and `status` from the join response.

#### Windows

1. Clone the native sample repo from [sample-repos.md](sample-repos.md) and use its `AGENTS.md` to locate the current Windows app directory.
2. Follow the Native Inspection Order above inside the Windows directory, starting from config files and the request service/model that currently builds the provider-based join request.
3. Replace only that request-building path with the pipeline request shape from this file.
4. Keep the existing Windows token-generation path, but generate the header token and agent token separately.
5. Keep the sample's current config style while removing stale provider config and adding `SHENGWANG_PIPELINE_ID`.
6. Keep the rest of the RTC flow and UI structure close to the sample.
7. Parse and preserve `agent_id`, `create_ts`, and `status` from the join response.

#### macOS

1. Clone the native sample repo from [sample-repos.md](sample-repos.md) and use its `AGENTS.md` to locate the current macOS app directory.
2. Follow the Native Inspection Order above inside the macOS directory, starting from config files and the request service/model that currently builds the provider-based join request.
3. Replace only that request-building path with the pipeline request shape from this file.
4. Keep the existing macOS token-generation path, but generate the header token and agent token separately.
5. Keep the sample's current config style while removing stale provider config and adding `SHENGWANG_PIPELINE_ID` as a user-filled placeholder.
6. Keep the rest of the RTC flow and UI structure close to the sample.
7. Parse and preserve `agent_id`, `create_ts`, and `status` from the join response.

### Web

- Reuse the official Web sample as the baseline structure.
- Keep a thin server proxy for Web.
- Generate the pipeline request in the server proxy rather than directly in the frontend.
- The `Authorization` token and the agent RTC token must not be exposed in browser code.
- Replace the old provider-based request/config path with the pipeline-based path generated from the `curl`.

#### Web Inspection Order

Before editing the Web sample, inspect files in this order:
1. The repo's `AGENTS.md` and current top-level directory layout.
2. Server-side env/config files.
3. The current server entry and server-side request path that starts the agent.
4. Server-side token helper/auth utility files used by the sample.
5. Server-side request/response helper or model files.
6. The current frontend entry and any directly related UI state files.

Do not start by deleting frontend provider controls before the server request path and token path are understood.

#### Web Implementation Steps

1. Clone the Web sample repo from [sample-repos.md](sample-repos.md).
2. Follow the Web Inspection Order above before changing any request/config code.
3. Keep the frontend-to-server interaction shape close to the sample; do not move the pipeline join request into the browser.
4. In the current server path that starts the agent, replace the provider-based request body with the pipeline request shape from this file.
5. Keep the sample's existing token-generation path, but generate:
   - the header RTC token with the caller/user UID
   - the body `properties.token` with the agent UID
6. Remove stale provider-only env/config and add `SHENGWANG_PIPELINE_ID` to the server-side config.
7. If the frontend currently exposes provider controls, remove or replace them with the minimum pipeline-relevant inputs.
8. Return or preserve `agent_id`, `create_ts`, and `status` from the server response so the frontend can keep the same control flow.

## Validation

Before finishing, verify all of these:
- the pipeline ID is read from env, not hardcoded
- the generated request still matches the fixed pipeline request shape in this file: URL path, auth header form, and body fields
- `name` is derived from `channel`
- the header token and `properties.token` are generated separately and are not reused
- both tokens still follow the sample's existing token-generation rules
- removed provider-only config is no longer referenced
- literal token values from the request example are not copied into source files
- the implementation path did not require the user to paste the live pipeline ID value or the `curl`
- the success response parsing keeps `agent_id`, `create_ts`, and `status`
- the selected sample platform still builds around the sample's original structure

## Blockers

Stop and report the blocker if:
- the selected sample repo cannot be inspected
- the Web path would expose secrets that must stay server-side
