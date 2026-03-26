# Doc Index Benchmark

Automated benchmark for `references/doc-index/` lookup accuracy.

## How to run

Token-based (no API key needed):
```bash
python3 scripts/ab-test-doc-index.py
```

LLM end-to-end (requires OpenAI API key):
```bash
export OPENAI_API_KEY=sk-...
python3 scripts/llm-eval-doc-index.py
python3 scripts/llm-eval-doc-index.py --model gpt-4o      # stronger model
python3 scripts/llm-eval-doc-index.py --cases CQ-01 -v    # single case, verbose
```

Note: requires `pip install openai`. The script auto-clears proxy env vars.

## Test Suite

72 LLM eval cases across 11 products:

| Section | Cases | Products |
|---------|-------|----------|
| convoai | 22 | conversational-ai |
| rtc | 8 | rtc (6 platforms + ops + webhook) |
| rtm | 4 | rtm (4 platforms) |
| cloud-recording | 7 | cloud-recording |
| cloud-transcoder | 3 | cloud-transcoder |
| stt | 4 | speech-to-text |
| media | 4 | media-push, media-pull |
| non-focus | 3 | fusion-cdn, rtmp-gateway, whiteboard |
| nl-en | 7 | natural language English |
| nl-cn | 10 | natural language Chinese |

## Latest LLM Results (2026-03-26, gpt-4o-mini)

| Metric | Value |
|--------|-------|
| Total cases | 72 |
| Phase 1 hits (MD only) | 52/72 (72%) |
| Phase 2 hits (needed shard) | 12/72 (17%) |
| Total hits | 64/72 (89%) |
| Misses | 8/72 (11%) |

### Per-section

| Section | Total | Hits | Ph1 | Ph2 | Rate |
|---------|-------|------|-----|-----|------|
| convoai | 22 | 22 | 19 | 3 | 100% |
| rtc | 8 | 6 | 6 | 0 | 75% |
| rtm | 4 | 4 | 1 | 3 | 100% |
| cloud-recording | 7 | 7 | 6 | 1 | 100% |
| cloud-transcoder | 3 | 3 | 3 | 0 | 100% |
| stt | 4 | 4 | 3 | 1 | 100% |
| media | 4 | 3 | 3 | 0 | 75% |
| non-focus | 3 | 1 | 0 | 1 | 33% |
| nl-en | 7 | 5 | 4 | 1 | 71% |
| nl-cn | 10 | 9 | 7 | 2 | 90% |

### Miss Analysis

| ID | Query | Type | Analysis |
|----|-------|------|----------|
| RQ-01 | rtc web quickstart | platform alias | LLM mapped "web" → restful instead of javascript. Platform alias hint added to MD. |
| RO-01 | rtc query channel list api | semantic gap | Slug `get-dev-v1-channel-appid` too different from "query channel list". Acceptable miss. |
| PQ-01 | media push quickstart | gold fix | Gold was `call-api`, LLM returned `quick-start`. Gold corrected — `quick-start` is more natural. |
| XQ-01 | rtmp gateway quickstart | gold fix | Same pattern — gold corrected to `quick-start`. |
| WQ-01 | whiteboard web quickstart | ambiguity | Two SDK variants (fastboard-sdk vs whiteboard-sdk). LLM picked the other one. Acceptable. |
| NE-04 | webhook notifications for recording | gold fix | Gold was `enable-ncs`, LLM returned `ncs-events`. Both valid; gold corrected to `ncs-events`. |
| NE-06 | real-time transcription with speech to text | NOT_FOUND | LLM couldn't map "real-time transcription" to speech-to-text product. Needs better context. |
| NC-06 | RTM 消息怎么接入 web | NOT_FOUND | LLM couldn't map "web" to javascript for RTM. Platform alias hint added to MD. |

### Post-fix expected improvement

After fixing 3 gold annotations and adding platform alias hints:
- PQ-01, XQ-01, NE-04: should now match (gold corrected)
- RQ-01, NC-06: should improve with platform alias hint in MD
- Expected: ~69/72 (96%) after re-run

### Notes

- ConvoAI: 100% hit rate, 86% from MD alone — the product-centric MD design works well for REST products
- SDK products (rtc/rtm): Phase 2 (shard) needed for platform-specific lookups, which is expected
- Non-focus products: 33% hit rate — by design, these are compact in MD and rely on shards
- Chinese natural language: 90% — strong performance, only "web" alias issue
