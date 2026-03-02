# ConvoAI Architecture

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        RTC Channel                          │
│                                                             │
│  User Device ──── audio ────► ConvoAI Agent                 │
│                                    │                        │
│                               ASR Engine                    │
│                                    │ transcript             │
│                               LLM Engine                    │
│                                    │ text response          │
│                               TTS Engine                    │
│                                    │ audio                  │
│  User Device ◄─── audio ──────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

1. User joins an RTC channel via Agora RTC SDK (Web, Android, iOS, etc.)
2. You call `POST /join` via REST API — ConvoAI agent joins the same channel
3. ASR transcribes user speech → LLM generates response → TTS converts to audio
4. Agent plays audio back into the RTC channel — user hears the AI response

## Key Design Constraints

- The ConvoAI agent is server-side only — there is no client SDK for the agent
- Agent and user must be in the **same RTC channel**
- `agent_rtc_uid` must not collide with any human participant's UID
- `remote_rtc_uids: ["*"]` means the agent listens to all participants; specify UIDs to restrict
- One agent per channel is the standard pattern; multiple agents require distinct UIDs

## Agent Lifecycle

```
POST /join
    │
    ▼
STARTING (1)
    │
    ▼
RUNNING (2) ◄──── RECOVERING (5)
    │                    ▲
    │                    │ (transient error)
    ▼                    │
STOPPING (3) ────────────┘
    │
    ▼
STOPPED (4)  or  FAILED (6)
```

- `RECOVERING`: agent hit a transient error and is self-healing — do not call `/leave` yet
- `FAILED`: unrecoverable — call `/leave` to clean up, then create a new agent
- `IDLE (0)`: agent created but not yet active (rare, usually transient)

Full state codes → see [references/convoai-restapi.yaml](../references/convoai-restapi.yaml) response schemas

## ASR → LLM → TTS Handoff

| Stage | What happens | Config location |
|-------|-------------|-----------------|
| ASR | Converts user speech to text | `properties.asr` in `/join` |
| LLM | Generates text response | `properties.llm` in `/join` |
| TTS | Converts LLM text to audio | `properties.tts` in `/join` |

- ASR is optional — defaults to `fengming` with `zh-CN` if omitted
- TTS is required when using a standard text LLM
- LLM `url` can point to any OpenAI-compatible endpoint (OpenAI, Azure, custom RAG server, etc.)

## VAD and Turn Detection

Turn detection controls when the agent decides the user has finished speaking:

- `turn_detection` field in `properties` (preferred, current API)
- Do NOT use deprecated `vadPayload` or `advancedFeatures.enableAIVad`
- Default behavior works for most cases; tune only if users report cut-off or delayed responses

## Idle Timeout

- `idle_timeout` (seconds): agent auto-stops after all `remote_rtc_uids` users leave the channel for this duration
- Default: 30s — set to `0` to keep agent alive until manually stopped
- Agent sends `farewell_config` message before stopping if configured at creation time
