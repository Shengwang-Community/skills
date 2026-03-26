#!/usr/bin/env python3
"""LLM end-to-end evaluation for doc-index lookup.

Sends real queries to an LLM with doc-index content as context,
checks if the LLM returns the correct URI.

Two-phase lookup (mirrors real agent behavior):
  Phase 1: LLM reads docs.index.md + query → extracts URI
  Phase 2: If Phase 1 fails, LLM reads product shard → extracts URI

Requires: OPENAI_API_KEY env var, `pip install openai`

Usage:
    export OPENAI_API_KEY=sk-...
    python3 scripts/llm-eval-doc-index.py
    python3 scripts/llm-eval-doc-index.py --model gpt-4o-mini  # cheaper model
    python3 scripts/llm-eval-doc-index.py --cases CQ-01,CO-01  # specific cases
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_INDEX_DIR = REPO_ROOT / "skills" / "voice-ai-integration" / "references" / "doc-index"
MD_PATH = DOC_INDEX_DIR / "docs.index.md"
SHARD_DIR = DOC_INDEX_DIR / "shards"

# Clear proxy env vars to avoid SOCKS interference
for _proxy_var in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"):
    os.environ.pop(_proxy_var, None)


# ── Test Cases ───────────────────────────────────────────────────

@dataclass
class Case:
    id: str
    query: str
    product: str
    gold_uri: str
    section: str = ""


CASES: list[Case] = [
    # ═══════════════════════════════════════════════════════════
    # ConvoAI — Quickstart (4)
    # ═══════════════════════════════════════════════════════════
    Case("CQ-01", "conversational-ai quickstart", "conversational-ai",
         "docs://default/convoai/restful/get-started/quick-start", "convoai"),
    Case("CQ-02", "go quickstart conversational-ai", "conversational-ai",
         "docs://default/convoai/restful/get-started/quick-start-go", "convoai"),
    Case("CQ-03", "java quickstart conversational-ai", "conversational-ai",
         "docs://default/convoai/restful/get-started/quick-start-java", "convoai"),
    Case("CQ-04", "enable service conversational-ai", "conversational-ai",
         "docs://default/convoai/restful/get-started/enable-service", "convoai"),

    # ConvoAI — Operations (8)
    Case("CO-01", "start agent", "conversational-ai",
         "docs://default/convoai/restful/convoai/operations/start-agent", "convoai"),
    Case("CO-02", "stop agent", "conversational-ai",
         "docs://default/convoai/restful/convoai/operations/stop-agent", "convoai"),
    Case("CO-03", "agent update", "conversational-ai",
         "docs://default/convoai/restful/convoai/operations/agent-update", "convoai"),
    Case("CO-04", "get history", "conversational-ai",
         "docs://default/convoai/restful/convoai/operations/get-history", "convoai"),
    Case("CO-05", "agent interrupt", "conversational-ai",
         "docs://default/convoai/restful/convoai/operations/agent-interrupt", "convoai"),
    Case("CO-06", "agent speak", "conversational-ai",
         "docs://default/convoai/restful/convoai/operations/agent-speak", "convoai"),
    Case("CO-07", "query agent status", "conversational-ai",
         "docs://default/convoai/restful/convoai/operations/query-agent-status", "convoai"),
    Case("CO-08", "get agent list", "conversational-ai",
         "docs://default/convoai/restful/convoai/operations/get-agent-list", "convoai"),

    # ConvoAI — Refs, Guides, Webhook, Best Practice (10)
    Case("CR-01", "response code conversational-ai", "conversational-ai",
         "docs://default/convoai/restful/api/response-code", "convoai"),
    Case("CR-02", "voice ids conversational-ai", "conversational-ai",
         "docs://default/convoai/restful/api/voice-ids", "convoai"),
    Case("CR-03", "api limits conversational-ai", "conversational-ai",
         "docs://default/convoai/restful/api/api-limits", "convoai"),
    Case("CG-01", "enable ncs webhook conversational-ai", "conversational-ai",
         "docs://default/convoai/restful/webhook/enable-ncs", "convoai"),
    Case("CG-02", "ncs events conversational-ai", "conversational-ai",
         "docs://default/convoai/restful/webhook/ncs-events", "convoai"),
    Case("CG-03", "opt latency conversational-ai", "conversational-ai",
         "docs://default/convoai/restful/best-practice/opt-latency", "convoai"),
    Case("CG-04", "audio settings conversational-ai", "conversational-ai",
         "docs://default/convoai/restful/best-practice/audio-settings", "convoai"),
    Case("CG-05", "custom llm conversational-ai", "conversational-ai",
         "docs://default/convoai/restful/user-guides/custom-llm", "convoai"),
    Case("CG-06", "realtime subtitle conversational-ai", "conversational-ai",
         "docs://default/convoai/restful/user-guides/realtime-sub", "convoai"),
    Case("CG-07", "mcp integrate conversational-ai", "conversational-ai",
         "docs://default/convoai/restful/mcp-integrate", "convoai"),

    # ═══════════════════════════════════════════════════════════
    # RTC — Cross-platform (8)
    # ═══════════════════════════════════════════════════════════
    Case("RQ-01", "rtc web quickstart", "rtc",
         "docs://default/rtc/javascript/get-started/quick-start", "rtc"),
    Case("RQ-02", "rtc android quickstart", "rtc",
         "docs://default/rtc/android/get-started/quick-start", "rtc"),
    Case("RQ-03", "rtc flutter quickstart", "rtc",
         "docs://default/rtc/flutter/get-started/quick-start", "rtc"),
    Case("RQ-04", "rtc ios quickstart", "rtc",
         "docs://default/rtc/ios/get-started/quick-start", "rtc"),
    Case("RQ-05", "rtc unity quickstart", "rtc",
         "docs://default/rtc/unity/get-started/quick-start", "rtc"),
    Case("RQ-06", "rtc harmonyos quickstart", "rtc",
         "docs://default/rtc/harmonyos/get-started/quick-start", "rtc"),
    Case("RO-01", "rtc query channel list api", "rtc",
         "docs://default/rtc/restful/channel-management/operations/get-dev-v1-channel-appid", "rtc"),
    Case("RW-01", "rtc webhook events", "rtc",
         "docs://default/rtc/android/webhook/events", "rtc"),

    # ═══════════════════════════════════════════════════════════
    # RTM (4)
    # ═══════════════════════════════════════════════════════════
    Case("MQ-01", "rtm web quickstart", "rtm",
         "docs://default/rtm2/javascript/get-started/quick-start", "rtm"),
    Case("MQ-02", "rtm ios quickstart", "rtm",
         "docs://default/rtm2/ios/get-started/quick-start", "rtm"),
    Case("MQ-03", "rtm android quickstart", "rtm",
         "docs://default/rtm2/android/get-started/quick-start", "rtm"),
    Case("MQ-04", "rtm flutter quickstart", "rtm",
         "docs://default/rtm2/flutter/get-started/quick-start", "rtm"),

    # ═══════════════════════════════════════════════════════════
    # Cloud Recording (7)
    # ═══════════════════════════════════════════════════════════
    Case("KQ-01", "cloud recording quickstart", "cloud-recording",
         "docs://default/cloud-recording/restful/get-started/quick-start", "cloud-recording"),
    Case("KQ-02", "cloud recording go quickstart", "cloud-recording",
         "docs://default/cloud-recording/restful/get-started/quick-start-go", "cloud-recording"),
    Case("KO-01", "cloud recording acquire resource", "cloud-recording",
         "docs://default/cloud-recording/restful/cloud-recording/operations/post-v1-apps-appid-cloud_recording-acquire", "cloud-recording"),
    Case("KO-02", "cloud recording start recording", "cloud-recording",
         "docs://default/cloud-recording/restful/cloud-recording/operations/post-v1-apps-appid-cloud_recording-resourceid-resourceid-mode-mode-start", "cloud-recording"),
    Case("KO-03", "cloud recording stop", "cloud-recording",
         "docs://default/cloud-recording/restful/cloud-recording/operations/post-v1-apps-appid-cloud_recording-resourceid-resourceid-sid-sid-mode-mode-stop", "cloud-recording"),
    Case("KW-01", "cloud recording webhook events", "cloud-recording",
         "docs://default/cloud-recording/restful/webhook/ncs-events", "cloud-recording"),
    Case("KB-01", "cloud recording best practice checklist", "cloud-recording",
         "docs://default/cloud-recording/restful/best-practices/checklist", "cloud-recording"),

    # ═══════════════════════════════════════════════════════════
    # Cloud Transcoder (3)
    # ═══════════════════════════════════════════════════════════
    Case("TQ-01", "cloud transcoder enable service", "cloud-transcoder",
         "docs://default/cloud-transcoder/restful/get-started/enable-service", "cloud-transcoder"),
    Case("TO-01", "cloud transcoder create task", "cloud-transcoder",
         "docs://default/cloud-transcoder/restful/cloud-transcoder/operations/post-v1-projects-appId-rtsc-cloud-transcoder-tasks", "cloud-transcoder"),
    Case("TW-01", "cloud transcoder webhook events", "cloud-transcoder",
         "docs://default/cloud-transcoder/restful/webhook/ncs-events", "cloud-transcoder"),

    # ═══════════════════════════════════════════════════════════
    # Speech-to-Text (4)
    # ═══════════════════════════════════════════════════════════
    Case("SQ-01", "speech to text quickstart", "speech-to-text",
         "docs://default/speech-to-text/restful/get-started/quick-start", "stt"),
    Case("SO-01", "speech to text join", "speech-to-text",
         "docs://default/speech-to-text/restful/v7/operations/join", "stt"),
    Case("SO-02", "speech to text leave", "speech-to-text",
         "docs://default/speech-to-text/restful/v7/operations/leave", "stt"),
    Case("SW-01", "speech to text webhook events", "speech-to-text",
         "docs://default/speech-to-text/restful/webhook/ncs-events", "stt"),

    # ═══════════════════════════════════════════════════════════
    # Media Push & Pull (4)
    # ═══════════════════════════════════════════════════════════
    Case("PQ-01", "media push quickstart", "media-push",
         "docs://default/media-push/restful/get-started/quick-start", "media"),
    Case("PW-01", "media push webhook events", "media-push",
         "docs://default/media-push/restful/webhook/ncs-events", "media"),
    Case("LQ-01", "media pull enable service", "media-pull",
         "docs://default/media-pull/restful/get-started/enable-service", "media"),
    Case("LW-01", "media pull webhook events", "media-pull",
         "docs://default/media-pull/restful/webhook/ncs-events", "media"),

    # ═══════════════════════════════════════════════════════════
    # Non-focus products (3) — tests shard fallback
    # ═══════════════════════════════════════════════════════════
    Case("FQ-01", "fusion cdn quickstart", "fusion-cdn",
         "docs://default/fusion-cdn/restful/get-started/quick-start", "non-focus"),
    Case("XQ-01", "rtmp gateway quickstart", "rtmp-gateway",
         "docs://default/rtmp-gateway/restful/get-started/quick-start", "non-focus"),
    Case("WQ-01", "whiteboard web quickstart", "whiteboard",
         "docs://default/whiteboard/javascript/fastboard-sdk/get-started/enable-service", "non-focus"),

    # ═══════════════════════════════════════════════════════════
    # Natural Language — English (7)
    # ═══════════════════════════════════════════════════════════
    Case("NE-01", "how do I create a conversational-ai agent", "conversational-ai",
         "docs://default/convoai/restful/convoai/operations/start-agent", "nl-en"),
    Case("NE-02", "what error codes does convoai return", "conversational-ai",
         "docs://default/convoai/restful/api/response-code", "nl-en"),
    Case("NE-03", "reduce latency in voice agent", "conversational-ai",
         "docs://default/convoai/restful/best-practice/opt-latency", "nl-en"),
    Case("NE-04", "how to receive webhook notifications for recording", "cloud-recording",
         "docs://default/cloud-recording/restful/webhook/ncs-events", "nl-en"),
    Case("NE-05", "integrate custom LLM provider with convoai", "conversational-ai",
         "docs://default/convoai/restful/user-guides/custom-llm", "nl-en"),
    Case("NE-06", "set up real-time transcription with speech to text", "speech-to-text",
         "docs://default/speech-to-text/restful/get-started/quick-start", "nl-en"),
    Case("NE-07", "check cloud recording status via best practices", "cloud-recording",
         "docs://default/cloud-recording/restful/best-practices/recording-status", "nl-en"),

    # ═══════════════════════════════════════════════════════════
    # Natural Language — Chinese (10)
    # ═══════════════════════════════════════════════════════════
    Case("NC-01", "用 Go 接入 conversational-ai", "conversational-ai",
         "docs://default/convoai/restful/get-started/quick-start-go", "nl-cn"),
    Case("NC-02", "如何中断正在说话的 agent", "conversational-ai",
         "docs://default/convoai/restful/convoai/operations/agent-interrupt", "nl-cn"),
    Case("NC-03", "conversational-ai 怎么接 webhook", "conversational-ai",
         "docs://default/convoai/restful/webhook/enable-ncs", "nl-cn"),
    Case("NC-04", "云录制怎么开始", "cloud-recording",
         "docs://default/cloud-recording/restful/get-started/quick-start", "nl-cn"),
    Case("NC-05", "RTC Android 怎么快速开始", "rtc",
         "docs://default/rtc/android/get-started/quick-start", "nl-cn"),
    Case("NC-06", "RTM 消息怎么接入 web", "rtm",
         "docs://default/rtm2/javascript/get-started/quick-start", "nl-cn"),
    Case("NC-07", "conversational-ai 的 Java 服务端怎么起步", "conversational-ai",
         "docs://default/convoai/restful/get-started/quick-start-java", "nl-cn"),
    Case("NC-08", "怎么查看 conversational-ai 的 voice ids", "conversational-ai",
         "docs://default/convoai/restful/api/voice-ids", "nl-cn"),
    Case("NC-09", "云录制怎么停止录制", "cloud-recording",
         "docs://default/cloud-recording/restful/cloud-recording/operations/post-v1-apps-appid-cloud_recording-resourceid-resourceid-sid-sid-mode-mode-stop", "nl-cn"),
    Case("NC-10", "语音转文字怎么接入", "speech-to-text",
         "docs://default/speech-to-text/restful/get-started/quick-start", "nl-cn"),
]


# ── LLM Client ───────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a documentation lookup assistant. You will be given a documentation index and a user query.

Your task: find the SINGLE most relevant document URI (starting with `docs://`) for the query.

Rules:
- Return ONLY the URI, nothing else. No explanation, no markdown, no quotes.
- If the URI is directly listed in the index, return it exactly as shown.
- If you need to infer the URI from patterns (e.g., replacing {platform} with the actual platform), do so.
- If you cannot find a matching URI, return exactly: NOT_FOUND
- The user already knows which product they need — focus on finding the right document within that product.
"""


def call_llm(model: str, system: str, user_msg: str, api_key: str) -> str:
    """Call OpenAI-compatible API. Returns the response text."""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: `openai` package not installed. Run: pip install openai")
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg},
        ],
        temperature=0,
        max_tokens=256,
    )
    return resp.choices[0].message.content.strip()


def extract_uri(response: str) -> str | None:
    """Extract a docs:// URI from LLM response."""
    # Try exact match first
    if response.startswith("docs://"):
        return response.split()[0].strip("`\"'")
    # Search for URI in response
    import re
    match = re.search(r"(docs://[^\s`\"']+)", response)
    return match.group(1) if match else None


# ── Evaluation Logic ─────────────────────────────────────────────

@dataclass
class EvalResult:
    case_id: str
    query: str
    gold_uri: str
    phase1_uri: str | None = None
    phase2_uri: str | None = None
    phase1_match: bool = False
    phase2_match: bool = False
    final_match: bool = False
    phase: int = 0  # which phase found it (1 or 2, 0 = not found)
    error: str = ""


def run_eval(model: str, api_key: str, case_filter: set[str] | None = None, verbose: bool = False):
    # Load index content
    md_content = MD_PATH.read_text(encoding="utf-8")

    cases = CASES
    if case_filter:
        cases = [c for c in CASES if c.id in case_filter]
    if not cases:
        print("No matching cases found.")
        return

    results: list[EvalResult] = []
    total = len(cases)

    print("=" * 90)
    print(f"LLM Doc-Index Evaluation — model: {model}, cases: {total}")
    print("=" * 90)
    print()
    print(f"{'ID':<7} {'Query':<40} {'Phase':>5} {'Match':>6} {'Notes'}")
    print("─" * 7 + " " + "─" * 40 + " " + "─" * 5 + " " + "─" * 6 + " " + "─" * 20)

    for i, case in enumerate(cases):
        result = EvalResult(case_id=case.id, query=case.query, gold_uri=case.gold_uri)

        # ── Phase 1: MD only ──
        phase1_prompt = f"""Here is the documentation index:

<doc-index>
{md_content}
</doc-index>

The user is working with the product: {case.product}

Query: {case.query}

Return the most relevant document URI."""

        try:
            phase1_resp = call_llm(model, SYSTEM_PROMPT, phase1_prompt, api_key)
            result.phase1_uri = extract_uri(phase1_resp)
            result.phase1_match = result.phase1_uri == case.gold_uri

            if result.phase1_match:
                result.final_match = True
                result.phase = 1
            else:
                # ── Phase 2: Add product shard ──
                shard_path = SHARD_DIR / f"{case.product}.json"
                if shard_path.exists():
                    shard_content = shard_path.read_text(encoding="utf-8")
                    phase2_prompt = f"""Here is the documentation index overview:

<doc-index>
{md_content}
</doc-index>

Here are the detailed records for the product "{case.product}":

<product-shard>
{shard_content}
</product-shard>

The user is working with the product: {case.product}

Query: {case.query}

Return the most relevant document URI."""

                    phase2_resp = call_llm(model, SYSTEM_PROMPT, phase2_prompt, api_key)
                    result.phase2_uri = extract_uri(phase2_resp)
                    result.phase2_match = result.phase2_uri == case.gold_uri

                    if result.phase2_match:
                        result.final_match = True
                        result.phase = 2
                else:
                    result.error = "no shard"

        except Exception as e:
            result.error = str(e)[:50]

        results.append(result)

        # Print row
        phase_str = str(result.phase) if result.phase > 0 else "✗"
        match_str = "✓" if result.final_match else "✗"
        notes = ""
        if result.error:
            notes = f"ERR: {result.error}"
        elif not result.final_match:
            got = result.phase2_uri or result.phase1_uri or "NOT_FOUND"
            notes = f"got: {got[-50:]}"
        q = case.query[:38] + ".." if len(case.query) > 40 else case.query
        print(f"{case.id:<7} {q:<40} {phase_str:>5} {match_str:>6} {notes}")

        if verbose and not result.final_match:
            print(f"        gold: {case.gold_uri}")
            if result.phase1_uri:
                print(f"        ph1:  {result.phase1_uri}")
            if result.phase2_uri:
                print(f"        ph2:  {result.phase2_uri}")

        # Rate limit
        time.sleep(0.3)

    # ── Summary ──
    print()
    print("=" * 90)
    print("Summary")
    print("=" * 90)
    print()

    phase1_hits = sum(1 for r in results if r.phase == 1)
    phase2_hits = sum(1 for r in results if r.phase == 2)
    total_hits = sum(1 for r in results if r.final_match)
    errors = sum(1 for r in results if r.error)

    print(f"Total cases:     {total}")
    print(f"Phase 1 hits:    {phase1_hits}/{total} ({phase1_hits*100//total}%) — found from MD alone")
    print(f"Phase 2 hits:    {phase2_hits}/{total} ({phase2_hits*100//total}%) — needed shard")
    print(f"Total hits:      {total_hits}/{total} ({total_hits*100//total}%)")
    print(f"Misses:          {total - total_hits - errors}/{total}")
    if errors:
        print(f"Errors:          {errors}/{total}")
    print()

    # Per-section breakdown
    sections: dict[str, dict[str, int]] = {}
    for r in results:
        case = next(c for c in CASES if c.id == r.case_id)
        sec = case.section
        if sec not in sections:
            sections[sec] = {"total": 0, "hits": 0, "p1": 0, "p2": 0}
        sections[sec]["total"] += 1
        if r.final_match:
            sections[sec]["hits"] += 1
        if r.phase == 1:
            sections[sec]["p1"] += 1
        if r.phase == 2:
            sections[sec]["p2"] += 1

    print(f"{'Section':<20} {'Total':>6} {'Hits':>6} {'Ph1':>6} {'Ph2':>6} {'Rate':>8}")
    print("─" * 20 + " " + "─" * 6 + " " + "─" * 6 + " " + "─" * 6 + " " + "─" * 6 + " " + "─" * 8)
    for sec in dict.fromkeys(c.section for c in cases):
        s = sections.get(sec, {"total": 0, "hits": 0, "p1": 0, "p2": 0})
        rate = f"{s['hits']*100//s['total']}%" if s["total"] else "—"
        print(f"{sec:<20} {s['total']:>6} {s['hits']:>6} {s['p1']:>6} {s['p2']:>6} {rate:>8}")

    # Misses detail
    misses = [r for r in results if not r.final_match and not r.error]
    if misses:
        print()
        print("Misses:")
        for r in misses:
            print(f"  {r.case_id}: query=\"{r.query}\"")
            print(f"    gold: {r.gold_uri}")
            print(f"    got:  {r.phase2_uri or r.phase1_uri or 'NOT_FOUND'}")


def main():
    parser = argparse.ArgumentParser(description="LLM end-to-end doc-index evaluation")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model (default: gpt-4o-mini)")
    parser.add_argument("--cases", default=None, help="Comma-separated case IDs to run (default: all)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show details for misses")
    parser.add_argument("--output", "-o", default=None, help="Save output to file (default: auto-generated in tests/)")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: Set OPENAI_API_KEY environment variable")
        print("  export OPENAI_API_KEY=sk-...")
        sys.exit(1)

    case_filter = set(args.cases.split(",")) if args.cases else None
    run_eval(args.model, api_key, case_filter, args.verbose)


if __name__ == "__main__":
    main()
