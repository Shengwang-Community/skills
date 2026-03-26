#!/usr/bin/env python3
"""Doc-index benchmark: test lookup accuracy against gold URIs.

Supports single-version benchmarking or A/B comparison when a baseline exists.
Covers: 8 products, 6 kinds, EN/CN natural language, cross-platform lookups.

Usage:
    python3 scripts/ab-test-doc-index.py

To A/B test: copy current docs.index.json to docs.index.baseline.json before rebuilding.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_INDEX_DIR = REPO_ROOT / "skills" / "voice-ai-integration" / "references" / "doc-index"

INDEX_VERSIONS: dict[str, Path] = {}
_current = DOC_INDEX_DIR / "docs.index.json"
if _current.exists():
    INDEX_VERSIONS["current"] = _current
_baseline = DOC_INDEX_DIR / "docs.index.baseline.json"
if _baseline.exists():
    INDEX_VERSIONS["baseline"] = _baseline


# ── Benchmark Cases ──────────────────────────────────────────────

@dataclass
class Case:
    id: str
    query: str
    product: str
    category: str  # maps to kind filter
    gold_uri: str
    section: str = ""  # for grouping in output


CASES: list[Case] = [
    # ═══════════════════════════════════════════════════════════
    # 1. ConvoAI — Quickstart & Entry
    # ═══════════════════════════════════════════════════════════
    Case("CQ-01", "conversational-ai quickstart", "conversational-ai", "quickstart",
         "docs://default/convoai/restful/get-started/quick-start", "convoai-quickstart"),
    Case("CQ-02", "go quickstart conversational-ai", "conversational-ai", "quickstart",
         "docs://default/convoai/restful/get-started/quick-start-go", "convoai-quickstart"),
    Case("CQ-03", "java quickstart conversational-ai", "conversational-ai", "quickstart",
         "docs://default/convoai/restful/get-started/quick-start-java", "convoai-quickstart"),
    Case("CQ-04", "enable service conversational-ai", "conversational-ai", "quickstart",
         "docs://default/convoai/restful/get-started/enable-service", "convoai-quickstart"),

    # 2. ConvoAI — API Operations
    Case("CO-01", "start agent", "conversational-ai", "operation",
         "docs://default/convoai/restful/convoai/operations/start-agent", "convoai-ops"),
    Case("CO-02", "stop agent", "conversational-ai", "operation",
         "docs://default/convoai/restful/convoai/operations/stop-agent", "convoai-ops"),
    Case("CO-03", "agent update", "conversational-ai", "operation",
         "docs://default/convoai/restful/convoai/operations/agent-update", "convoai-ops"),
    Case("CO-04", "get history", "conversational-ai", "operation",
         "docs://default/convoai/restful/convoai/operations/get-history", "convoai-ops"),
    Case("CO-05", "query agent status", "conversational-ai", "operation",
         "docs://default/convoai/restful/convoai/operations/query-agent-status", "convoai-ops"),
    Case("CO-06", "agent interrupt", "conversational-ai", "operation",
         "docs://default/convoai/restful/convoai/operations/agent-interrupt", "convoai-ops"),
    Case("CO-07", "agent speak", "conversational-ai", "operation",
         "docs://default/convoai/restful/convoai/operations/agent-speak", "convoai-ops"),
    Case("CO-08", "get agent list", "conversational-ai", "operation",
         "docs://default/convoai/restful/convoai/operations/get-agent-list", "convoai-ops"),

    # 3. ConvoAI — Supporting Refs
    Case("CR-01", "response code conversational-ai", "conversational-ai", "api-ref",
         "docs://default/convoai/restful/api/response-code", "convoai-ref"),
    Case("CR-02", "voice ids conversational-ai", "conversational-ai", "api-ref",
         "docs://default/convoai/restful/api/voice-ids", "convoai-ref"),
    Case("CR-03", "api limits conversational-ai", "conversational-ai", "api-ref",
         "docs://default/convoai/restful/api/api-limits", "convoai-ref"),

    # 4. ConvoAI — Guides / Best Practice / Webhook
    Case("CG-01", "mcp integrate conversational-ai", "conversational-ai", "integration",
         "docs://default/convoai/restful/mcp-integrate", "convoai-guide"),
    Case("CG-02", "realtime subtitle conversational-ai", "conversational-ai", "guide",
         "docs://default/convoai/restful/user-guides/realtime-sub", "convoai-guide"),
    Case("CG-03", "custom llm conversational-ai", "conversational-ai", "guide",
         "docs://default/convoai/restful/user-guides/custom-llm", "convoai-guide"),
    Case("CG-04", "enable ncs webhook conversational-ai", "conversational-ai", "webhook",
         "docs://default/convoai/restful/webhook/enable-ncs", "convoai-guide"),
    Case("CG-05", "ncs events conversational-ai", "conversational-ai", "webhook",
         "docs://default/convoai/restful/webhook/ncs-events", "convoai-guide"),
    Case("CG-06", "opt latency conversational-ai", "conversational-ai", "best-practice",
         "docs://default/convoai/restful/best-practice/opt-latency", "convoai-guide"),
    Case("CG-07", "audio settings conversational-ai", "conversational-ai", "best-practice",
         "docs://default/convoai/restful/best-practice/audio-settings", "convoai-guide"),

    # ═══════════════════════════════════════════════════════════
    # 5. RTC — Cross-platform
    # ═══════════════════════════════════════════════════════════
    Case("RQ-01", "rtc web quickstart", "rtc", "quickstart",
         "docs://default/rtc/javascript/get-started/quick-start", "rtc"),
    Case("RQ-02", "rtc android quickstart", "rtc", "quickstart",
         "docs://default/rtc/android/get-started/quick-start", "rtc"),
    Case("RQ-03", "rtc flutter quickstart", "rtc", "quickstart",
         "docs://default/rtc/flutter/get-started/quick-start", "rtc"),
    Case("RQ-04", "token auth rtc", "rtc", "guide",
         "docs://default/rtc/android/basic-features/token-authentication", "rtc"),
    Case("RQ-05", "rtc kicking rule", "rtc", "operation",
         "docs://default/rtc/restful/channel-management/operations/post-dev-v1-kicking-rule", "rtc"),
    Case("RQ-06", "rtc webhook events", "rtc", "webhook",
         "docs://default/rtc/android/webhook/events", "rtc"),

    # ═══════════════════════════════════════════════════════════
    # 6. RTM
    # ═══════════════════════════════════════════════════════════
    Case("MQ-01", "rtm web quickstart", "rtm", "quickstart",
         "docs://default/rtm2/javascript/get-started/quick-start", "rtm"),
    Case("MQ-02", "rtm ios quickstart", "rtm", "quickstart",
         "docs://default/rtm2/ios/get-started/quick-start", "rtm"),
    Case("MQ-03", "rtm android enable service", "rtm", "quickstart",
         "docs://default/rtm2/android/get-started/enable-service", "rtm"),

    # ═══════════════════════════════════════════════════════════
    # 7. Cloud Recording
    # ═══════════════════════════════════════════════════════════
    Case("KQ-01", "cloud recording quickstart", "cloud-recording", "quickstart",
         "docs://default/cloud-recording/restful/get-started/quick-start", "cloud-recording"),
    Case("KO-01", "cloud recording acquire", "cloud-recording", "operation",
         "docs://default/cloud-recording/restful/cloud-recording/operations/post-v1-apps-appid-cloud_recording-acquire", "cloud-recording"),
    Case("KO-02", "cloud recording start", "cloud-recording", "operation",
         "docs://default/cloud-recording/restful/cloud-recording/operations/post-v1-apps-appid-cloud_recording-resourceid-resourceid-mode-mode-start", "cloud-recording"),
    Case("KW-01", "cloud recording webhook events", "cloud-recording", "webhook",
         "docs://default/cloud-recording/restful/webhook/ncs-events", "cloud-recording"),
    Case("KB-01", "cloud recording best practice checklist", "cloud-recording", "best-practice",
         "docs://default/cloud-recording/restful/best-practices/checklist", "cloud-recording"),

    # ═══════════════════════════════════════════════════════════
    # 8. Speech-to-Text
    # ═══════════════════════════════════════════════════════════
    Case("SQ-01", "speech to text quickstart", "speech-to-text", "quickstart",
         "docs://default/speech-to-text/restful/get-started/quick-start", "stt"),
    Case("SO-01", "speech to text join", "speech-to-text", "operation",
         "docs://default/speech-to-text/restful/v7/operations/join", "stt"),

    # ═══════════════════════════════════════════════════════════
    # 9. Media Push
    # ═══════════════════════════════════════════════════════════
    Case("PQ-01", "media push quickstart", "media-push", "quickstart",
         "docs://default/media-push/restful/get-started/call-api", "media-push"),
    Case("PW-01", "media push webhook", "media-push", "webhook",
         "docs://default/media-push/restful/webhook/ncs-events", "media-push"),

    # ═══════════════════════════════════════════════════════════
    # 10. Fusion CDN (non-focus product, tests shard path)
    # ═══════════════════════════════════════════════════════════
    Case("FQ-01", "fusion cdn quickstart", "fusion-cdn", "quickstart",
         "docs://default/fusion-cdn/restful/get-started/quick-start", "non-focus"),
    Case("FO-01", "fusion cdn get entry point list", "fusion-cdn", "operation",
         "docs://default/fusion-cdn/restful/streaming/operations/get-entry-point-list", "non-focus"),

    # ═══════════════════════════════════════════════════════════
    # 11. Flexible Classroom (non-focus, many platforms)
    # ═══════════════════════════════════════════════════════════
    Case("XQ-01", "flexible classroom web quickstart", "flexible-classroom", "quickstart",
         "docs://default/flexible-classroom/javascript/get-started/quick-start", "non-focus"),

    # ═══════════════════════════════════════════════════════════
    # 12. Natural Language — English
    # ═══════════════════════════════════════════════════════════
    Case("NE-01", "how do I create a conversational-ai agent", "conversational-ai", "operation",
         "docs://default/convoai/restful/convoai/operations/start-agent", "nl-en"),
    Case("NE-02", "set up cloud recording for my app", "cloud-recording", "quickstart",
         "docs://default/cloud-recording/restful/get-started/quick-start", "nl-en"),
    Case("NE-03", "what error codes does convoai return", "conversational-ai", "api-ref",
         "docs://default/convoai/restful/api/response-code", "nl-en"),
    Case("NE-04", "how to receive webhook notifications for recording", "cloud-recording", "webhook",
         "docs://default/cloud-recording/restful/webhook/enable-ncs", "nl-en"),
    Case("NE-05", "reduce latency in voice agent", "conversational-ai", "best-practice",
         "docs://default/convoai/restful/best-practice/opt-latency", "nl-en"),

    # ═══════════════════════════════════════════════════════════
    # 13. Natural Language — Chinese
    # ═══════════════════════════════════════════════════════════
    Case("NC-01", "用 Go 接入 conversational-ai", "conversational-ai", "quickstart",
         "docs://default/convoai/restful/get-started/quick-start-go", "nl-cn"),
    Case("NC-02", "哪里看 conversational-ai 的 voice ids", "conversational-ai", "api-ref",
         "docs://default/convoai/restful/api/voice-ids", "nl-cn"),
    Case("NC-03", "conversational-ai 怎么接 webhook", "conversational-ai", "webhook",
         "docs://default/convoai/restful/webhook/enable-ncs", "nl-cn"),
    Case("NC-04", "如何中断正在说话的 agent", "conversational-ai", "operation",
         "docs://default/convoai/restful/convoai/operations/agent-interrupt", "nl-cn"),
    Case("NC-05", "conversational-ai 的 Java 服务端怎么起步", "conversational-ai", "quickstart",
         "docs://default/convoai/restful/get-started/quick-start-java", "nl-cn"),
    Case("NC-06", "云录制怎么开始", "cloud-recording", "quickstart",
         "docs://default/cloud-recording/restful/get-started/quick-start", "nl-cn"),
    Case("NC-07", "RTC Android 怎么快速开始", "rtc", "quickstart",
         "docs://default/rtc/android/get-started/quick-start", "nl-cn"),
    Case("NC-08", "RTM 消息怎么接入 web", "rtm", "quickstart",
         "docs://default/rtm2/javascript/get-started/quick-start", "nl-cn"),
]


# ── Lookup Engine ────────────────────────────────────────────────

def tokenize_query(query: str) -> list[str]:
    query = query.lower()
    tokens = re.findall(r"[a-z0-9\-_]+|[\u4e00-\u9fff]+", query)
    stop = {"a", "an", "the", "do", "i", "how", "to", "is", "of", "in",
            "my", "for", "it", "on", "what", "does", "set", "up"}
    return [t for t in tokens if t not in stop and len(t) > 1]


@dataclass
class LookupResult:
    found: bool = False
    rank: int = -1
    candidates: int = 0
    steps: int = 0


def lookup_in_index(records: list[dict], case: Case) -> LookupResult:
    tokens = tokenize_query(case.query)
    gold = case.gold_uri

    # Step 1: Filter by product
    step1 = [r for r in records if r.get("product") == case.product]
    steps = 1
    if gold not in [r["uri"] for r in step1]:
        return LookupResult(found=False, candidates=len(step1), steps=steps)

    # Step 2: Filter by kind
    kind_map = {
        "quickstart": ["quickstart"],
        "operation": ["operation"],
        "api-ref": ["api-ref"],
        "guide": ["guide", "integration"],
        "integration": ["integration", "guide"],
        "webhook": ["webhook"],
        "best-practice": ["best-practice"],
    }
    target_kinds = kind_map.get(case.category, [])
    if target_kinds:
        step2 = [r for r in step1 if r.get("kind") in target_kinds]
        steps = 2
    else:
        step2 = step1

    candidates = step2 if gold in [r["uri"] for r in step2] else step1

    # Step 3: Score by token match
    def score(rec: dict) -> int:
        s = 0
        slug = (rec.get("slug") or "").lower()
        tags = [t.lower() for t in rec.get("tags", [])]
        path_tokens = [t.lower() for t in rec.get("path_tokens", [])]
        platform = (rec.get("platform") or "").lower()
        for token in tokens:
            if token in slug: s += 10
            if any(token in t for t in tags): s += 5
            if any(token in pt for pt in path_tokens): s += 3
            if token in platform: s += 3
        return s

    scored = sorted(candidates, key=lambda r: score(r), reverse=True)
    steps = 3
    scored_uris = [r["uri"] for r in scored]
    if gold in scored_uris:
        return LookupResult(found=True, rank=scored_uris.index(gold),
                            candidates=len(scored), steps=steps)
    return LookupResult(found=False, candidates=len(scored), steps=steps)


# ── Reporting ────────────────────────────────────────────────────

def load_index(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["records"]


def classification_stats(records: list[dict]) -> tuple[int, int, float]:
    total = len(records)
    other = sum(1 for r in records if r.get("kind") == "other")
    return total, total - other, (total - other) * 100 / total if total else 0


def run():
    if not INDEX_VERSIONS:
        print("ERROR: No index found."); sys.exit(1)

    single = len(INDEX_VERSIONS) == 1
    vdata: dict[str, tuple[list[dict], int, int, float, int]] = {}
    for label, path in INDEX_VERSIONS.items():
        recs = load_index(path)
        total, classified, pct = classification_stats(recs)
        vdata[label] = (recs, total, classified, pct, path.stat().st_size // 1024)

    labels = list(vdata.keys())
    n = len(CASES)
    cw = 15  # column width

    # ── Header ──
    print("=" * 100)
    title = f"Doc-Index Benchmark: {labels[0]}" if single else f"Doc-Index A/B: {' vs '.join(labels)}"
    print(title)
    print(f"{n} test cases across {len(set(c.product for c in CASES))} products")
    print("=" * 100)
    print()

    # ── Overview ──
    print(f"{'Metric':<30}" + "".join(f"{l:>{cw}}" for l in labels))
    print("─" * 30 + "─" * cw * len(labels))
    for metric, fn in [
        ("Records", lambda d: str(d[1])),
        ("Classified", lambda d: f"{d[2]} ({d[3]:.0f}%)"),
        ("JSON size", lambda d: f"{d[4]} KB"),
    ]:
        print(f"{metric:<30}" + "".join(f"{fn(vdata[l]):>{cw}}" for l in labels))
    print()

    # ── Per-section results ──
    stats: dict[str, dict[str, int | float]] = {
        l: {"top1": 0, "top3": 0, "found": 0, "total_cand": 0} for l in labels
    }
    section_stats: dict[str, dict[str, dict[str, int]]] = defaultdict(
        lambda: {l: {"top1": 0, "top3": 0, "count": 0} for l in labels}
    )

    current_section = ""
    for case in CASES:
        if case.section != current_section:
            current_section = case.section
            print(f"\n── {current_section} ──")
            hdr = f"  {'ID':<7} {'Query':<42}"
            for l in labels:
                hdr += f"{'Rank':>6}{'Cand':>6}"
            if not single:
                hdr += f"{'Best':>8}"
            print(hdr)

        results: dict[str, LookupResult] = {}
        for l in labels:
            results[l] = lookup_in_index(vdata[l][0], case)

        for l in labels:
            r = results[l]
            section_stats[case.section][l]["count"] += 1
            if r.found:
                stats[l]["found"] += 1
                if r.rank == 0:
                    stats[l]["top1"] += 1
                    section_stats[case.section][l]["top1"] += 1
                if r.rank < 3:
                    stats[l]["top3"] += 1
                    section_stats[case.section][l]["top3"] += 1
            stats[l]["total_cand"] += r.candidates

        # Best determination
        best_str = ""
        if not single:
            found_labels = [l for l in labels if results[l].found]
            if found_labels:
                best_rank = min(results[l].rank for l in found_labels)
                best = [l for l in found_labels if results[l].rank == best_rank]
                if len(best) == len(labels):
                    min_c = min(results[l].candidates for l in labels)
                    best = [l for l in labels if results[l].candidates == min_c]
                    best_str = "tie" if len(best) == len(labels) else ",".join(best) + "✓"
                else:
                    best_str = ",".join(best) + "✓"
            else:
                best_str = "✗"

        q = case.query[:40] + ".." if len(case.query) > 42 else case.query
        row = f"  {case.id:<7} {q:<42}"
        for l in labels:
            r = results[l]
            rank_s = str(r.rank + 1) if r.found else "MISS"
            row += f"{rank_s:>6}{r.candidates:>6}"
        if not single:
            row += f"{best_str:>8}"
        print(row)

    # ── Section Summary ──
    print()
    print("=" * 100)
    print("Section Summary")
    print("=" * 100)
    print()
    sec_hdr = f"{'Section':<25}{'Cases':>6}"
    for l in labels:
        sec_hdr += f"{'Top1':>8}{'Top3':>8}"
    print(sec_hdr)
    print("─" * 25 + "─" * 6 + ("─" * 16) * len(labels))
    for section in dict.fromkeys(c.section for c in CASES):
        ss = section_stats[section]
        count = ss[labels[0]]["count"]
        row = f"{section:<25}{count:>6}"
        for l in labels:
            t1 = ss[l]["top1"]
            t3 = ss[l]["top3"]
            row += f"{t1}/{count}({t1*100//count}%):>8"[0:0]  # placeholder
            row += f"  {t1}/{count:>2}  {t3}/{count:>2}"
        print(row)

    # ── Overall Summary ──
    print()
    print("=" * 100)
    print("Overall")
    print("=" * 100)
    print()
    print(f"{'Metric':<35}" + "".join(f"{l:>{cw}}" for l in labels))
    print("─" * 35 + "─" * cw * len(labels))
    for l in labels:
        stats[l]["avg_cand"] = stats[l]["total_cand"] / n if n else 0
    for metric, fn in [
        ("Top-1 hit rate", lambda l: f"{stats[l]['top1']}/{n} ({stats[l]['top1']*100/n:.0f}%)"),
        ("Top-3 hit rate", lambda l: f"{stats[l]['top3']}/{n} ({stats[l]['top3']*100/n:.0f}%)"),
        ("Found rate", lambda l: f"{stats[l]['found']}/{n} ({stats[l]['found']*100/n:.0f}%)"),
        ("Avg candidates/query", lambda l: f"{stats[l]['avg_cand']:.1f}"),
        ("Classification %", lambda l: f"{vdata[l][3]:.1f}%"),
        ("Main JSON size", lambda l: f"{vdata[l][4]} KB"),
    ]:
        print(f"{metric:<35}" + "".join(f"{fn(l):>{cw}}" for l in labels))

    # ── Per-product breakdown ──
    print()
    prod_stats: dict[str, dict[str, dict[str, int]]] = defaultdict(
        lambda: {l: {"top1": 0, "top3": 0, "count": 0} for l in labels}
    )
    for case in CASES:
        for l in labels:
            r = lookup_in_index(vdata[l][0], case)
            prod_stats[case.product][l]["count"] += 1
            if r.found and r.rank == 0:
                prod_stats[case.product][l]["top1"] += 1
            if r.found and r.rank < 3:
                prod_stats[case.product][l]["top3"] += 1

    print(f"{'Product':<25}{'Cases':>6}" + "".join(f"{'Top1':>10}{'Top3':>10}" for l in labels))
    print("─" * 25 + "─" * 6 + "─" * 20 * len(labels))
    for product in sorted(prod_stats):
        ps = prod_stats[product]
        count = ps[labels[0]]["count"]
        row = f"{product:<25}{count:>6}"
        for l in labels:
            t1 = ps[l]["top1"]
            t3 = ps[l]["top3"]
            row += f"  {t1}/{count} ({t1*100//count:>2}%)  {t3}/{count} ({t3*100//count:>2}%)"
        print(row)

    # ── Verdict ──
    if len(labels) >= 2:
        prev, curr = labels[-2], labels[-1]
        print()
        wins = sum([
            stats[curr]["top1"] >= stats[prev]["top1"],
            stats[curr]["top3"] >= stats[prev]["top3"],
            stats[curr]["avg_cand"] <= stats[prev]["avg_cand"],
            vdata[curr][3] >= vdata[prev][3],
            vdata[curr][4] <= vdata[prev][4],
        ])
        print(f"Verdict ({curr} vs {prev}): {curr} wins {wins}/5 metrics", end="")
        print(f" → {'better ✓' if wins >= 3 else 'investigate' if wins <= 2 else 'tie'}")


if __name__ == "__main__":
    run()
