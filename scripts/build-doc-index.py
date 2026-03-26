#!/usr/bin/env python3
"""Maintainer tool: generate bundled doc indexes from the downloaded docs sitemap.

v3 — API reference separation:
- Main index (docs.index.json) excludes api-class records → ~2800 records, <1MB
- API class docs stored separately in api-reference.json as compact tree
- Per-product shards exclude api-class; API shards in shards/api-ref/
- MD shows API Reference as summary (product/platform → count + URI pattern)
- All v2 improvements retained: expanded kinds, rich tags, URIs in task view
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict, Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT = REPO_ROOT / "skills" / "voice-ai-integration"
DEFAULT_INPUT = REPO_ROOT / "scripts" / ".cache" / "docs-sitemap.txt"
OUT_DIR = ROOT / "references" / "doc-index"
OUT_JSON = OUT_DIR / "docs.index.json"
OUT_API_JSON = OUT_DIR / "api-reference.json"
OUT_MD = OUT_DIR / "docs.index.md"
SHARD_DIR = OUT_DIR / "shards"
API_SHARD_DIR = SHARD_DIR / "api-ref"

LINK_RE = re.compile(r"^- \[(.*?)\]\((https?://[^)]+)\)\s*$")

PRODUCT_MAP = {
    "convoai": "conversational-ai",
    "rtm2": "rtm",
}

TASK_ORDER = [
    "quickstart",
    "enable-service",
    "api-operations",
    "response-codes",
    "webhook",
    "billing",
    "release-notes",
    "resources",
]

# kind order for MD Product View (api-class excluded from main display)
KIND_ORDER = [
    "quickstart",
    "overview",
    "guide",
    "best-practice",
    "api-ref",
    "operation",
    "webhook",
    "resource",
    "integration",
    "example",
    "faq",
    "troubleshooting",
    "release-notes",
    "billing",
    "landing",
    "other",
]

# --- Slug-based kind overrides ---
SLUG_KIND_MAP: dict[str, str] = {
    "enable-service": "quickstart",
    "release-notes": "release-notes",
    "billing": "billing",
    "resources": "resource",
    "landing-page": "landing",
    "response-code": "api-ref",
    "glossary": "glossary",
}

SLUG_KIND_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^quick-start"), "quickstart"),
    (re.compile(r"^run-example|^sample-code|^demo|^run-demo"), "example"),
    (re.compile(r"^troubleshoot"), "troubleshooting"),
    (re.compile(r"^mcp-integrate|^skills-integrate|^integration-guide"), "integration"),
    (re.compile(r"^faq$|^common-errors$"), "faq"),
    (re.compile(r"^error-code"), "api-ref"),
    (re.compile(r"^billing"), "billing"),
    (re.compile(r"^architecture$|^product-overview$"), "overview"),
    (re.compile(r"^sunset-policy|^data-security|^firewall"), "guide"),
]

SECTION_KIND_MAP: dict[str, str] = {
    "operations": "operation",
    "api": "api-ref",
    "user-guides": "guide",
    "user-guide": "guide",
    "best-practice": "best-practice",
    "best-practices": "best-practice",
    "webhook": "webhook",
    "overview": "overview",
    "get-started": "quickstart",
    # Feature/guide sections
    "advanced-features": "guide",
    "basic-features": "guide",
    "create-extensions": "guide",
    "paas": "guide",
    "legacy": "guide",
    "security": "guide",
    "whiteboard-sdk": "guide",
    "fastboard-sdk": "guide",
    "custom-signaling": "guide",
    "metakit": "guide",
    "uikit": "guide",
    "sdk": "guide",
    "course-delivery": "guide",
    "course-resource": "guide",
    "school-resource": "guide",
    "product-overview": "overview",
    # Integration sections
    "integrate-extensions": "integration",
    # Billing sections
    "billing": "billing",
    # Error code sections
    "error-code": "api-ref",
    "error-codes": "api-ref",
    # Scenario/solution sections
    "ktv-scenario": "guide",
    "auikaraoke": "guide",
    "online-ktv-sdk": "guide",
}

FEATURE_KEYWORDS = {
    "token": "token", "auth": "auth", "ncs": "ncs",
    "tts": "tts", "asr": "asr", "llm": "llm", "stt": "stt",
    "interrupt": "interrupt", "speak": "speak",
    "subtitle": "subtitle", "recording": "recording",
    "transcod": "transcode", "webhook": "webhook",
}

CLIENT_PLATFORM_MAP = {
    "android": "client-android", "ios": "client-ios",
    "javascript": "client-web", "react": "client-web",
    "flutter": "client-flutter", "unity": "client-unity",
    "electron": "client-electron", "macos": "client-macos",
    "windows": "client-windows", "harmonyos": "client-harmonyos",
    "mini-program": "client-miniprogram", "rn": "client-rn",
}


def normalize_product(product_raw: str | None) -> str:
    if not product_raw:
        return "unknown"
    return PRODUCT_MAP.get(product_raw, product_raw)


def unique_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def classify(uri: str, title: str) -> dict:
    if not uri.startswith("docs://"):
        return {
            "product": "unknown", "platform": None,
            "section_group": None, "slug": title,
            "kind": "other", "tags": [], "path_tokens": [],
        }

    parts = uri.removeprefix("docs://").split("/")
    route = parts[0] if parts else "unknown"

    if route == "shared":
        rest_parts = parts[1:]
        slug = rest_parts[-1] if rest_parts else title
        return {
            "product": "shared", "platform": "shared",
            "section_group": "shared", "slug": slug,
            "kind": "other", "tags": ["shared"], "path_tokens": rest_parts,
        }

    if route in {"default", "api-reference"}:
        product_raw = parts[1] if len(parts) > 1 else None
        product = normalize_product(product_raw)
        platform = parts[2] if len(parts) > 2 else None
        rest_parts = parts[3:] if len(parts) > 3 else []
    elif route == "faq":
        product_raw = parts[1] if len(parts) > 1 else "faq"
        product = normalize_product(product_raw)
        platform = None
        rest_parts = parts[2:] if len(parts) > 2 else []
    elif route == "basics":
        product = "basics"
        platform = None
        rest_parts = parts[1:] if len(parts) > 1 else []
    else:
        product_raw = parts[1] if len(parts) > 1 else None
        product = normalize_product(product_raw)
        platform = parts[2] if len(parts) > 2 else None
        rest_parts = parts[3:] if len(parts) > 3 else []

    slug = rest_parts[-1] if rest_parts else title
    section_group = rest_parts[0] if rest_parts else None

    # Refine section_group from path tokens (check all known section groups)
    _sg_tokens = set(SECTION_KIND_MAP.keys())
    for token in rest_parts:
        if token in _sg_tokens:
            section_group = token
            break

    # --- Determine kind ---
    kind = "other"
    if slug in SLUG_KIND_MAP:
        kind = SLUG_KIND_MAP[slug]
    else:
        for pattern, k in SLUG_KIND_PATTERNS:
            if pattern.search(slug):
                kind = k
                break
        else:
            if section_group in SECTION_KIND_MAP:
                kind = SECTION_KIND_MAP[section_group]
            elif route == "api-reference":
                kind = "api-class"
            elif route == "faq":
                kind = "faq"

    # --- Build tags ---
    tags = [kind]
    if slug == "enable-service":
        tags.append("enable-service")
    if kind == "operation":
        tags.append("api-operations")
    if slug == "response-code":
        tags.append("response-codes")
    if kind == "webhook":
        tags.append("webhook")
    if slug == "billing":
        tags.append("billing")
    if slug == "release-notes":
        tags.append("release-notes")
    if kind == "resource":
        tags.append("resources")
    if slug.endswith("-go"):
        tags.append("backend-go")
    if slug.endswith("-java"):
        tags.append("backend-java")
    if slug.endswith("-nodejs"):
        tags.append("backend-nodejs")
    if slug.endswith("-python"):
        tags.append("backend-python")
    if platform and platform in CLIENT_PLATFORM_MAP:
        tags.append(CLIENT_PLATFORM_MAP[platform])
    slug_lower = slug.lower()
    for keyword, tag in FEATURE_KEYWORDS.items():
        if keyword in slug_lower:
            tags.append(f"feat-{tag}")

    return {
        "product": product, "platform": platform,
        "section_group": section_group, "slug": slug,
        "kind": kind, "tags": unique_keep_order(tags),
        "path_tokens": rest_parts,
    }


def parse_records() -> list[dict]:
    records = []
    docs_txt = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    for line in docs_txt.read_text(encoding="utf-8").splitlines():
        match = LINK_RE.match(line.strip())
        if not match:
            continue
        title, fetch_url = match.groups()
        parsed = urlparse(fetch_url)
        uri = parse_qs(parsed.query).get("uri", [None])[0]
        if not uri:
            continue
        meta = classify(uri, title)
        records.append({"title": title, "uri": uri, **meta})
    records.sort(key=lambda item: (
        item["product"], item["platform"] or "",
        item["section_group"] or "", item["slug"], item["uri"],
    ))
    return records


def split_records(records: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split into main (non-api-class) and api-class records."""
    main = [r for r in records if r["kind"] != "api-class"]
    api_class = [r for r in records if r["kind"] == "api-class"]
    return main, api_class


def build_api_reference(api_class_records: list[dict]) -> dict:
    """Build compact API reference tree: {product: {platform: [{slug, uri}]}}."""
    tree: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for r in api_class_records:
        tree[r["product"]][r["platform"] or "unknown"].append({
            "slug": r["slug"],
            "uri": r["uri"],
        })
    # Sort for deterministic output
    return {
        p: {pl: sorted(entries, key=lambda e: e["slug"])
            for pl, entries in sorted(platforms.items())}
        for p, platforms in sorted(tree.items())
    }


def build_api_summary(api_class_records: list[dict]) -> dict[str, dict[str, int]]:
    """Build summary counts: {product: {platform: count}}."""
    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in api_class_records:
        counts[r["product"]][r["platform"] or "unknown"] += 1
    return {p: dict(sorted(pls.items())) for p, pls in sorted(counts.items())}


def build_views(records: list[dict]) -> dict:
    """Build views from main (non-api-class) records only."""
    by_product: dict[str, dict[str, dict[str, list[dict]]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(list))
    )
    by_task: dict[str, list[dict]] = defaultdict(list)
    api_index: dict[str, dict[str, list[dict]]] = defaultdict(
        lambda: {"operations": [], "supporting_refs": []}
    )

    for rec in records:
        product = rec["product"]
        platform = rec["platform"] or "unknown"
        kind = rec["kind"]
        entry = {"slug": rec["slug"], "uri": rec["uri"], "tags": rec["tags"]}
        by_product[product][platform][kind].append(entry)

        for tag in rec["tags"]:
            if tag in TASK_ORDER:
                by_task[tag].append(entry | {"product": product, "platform": platform})

        if kind == "operation":
            api_index[product]["operations"].append(entry | {"platform": platform})
        elif kind == "api-ref":
            api_index[product]["supporting_refs"].append(entry | {"platform": platform})

    return {
        "by_product": {
            p: {pl: dict(kinds) for pl, kinds in platforms.items()}
            for p, platforms in by_product.items()
        },
        "by_task": dict(by_task),
        "api_index": dict(api_index),
    }


# Products that get full URI treatment in Task View (skill focus products)
FOCUS_PRODUCTS = {
    "conversational-ai", "rtc", "rtm", "cloud-recording",
    "cloud-transcoder", "speech-to-text", "media-push", "media-pull",
}




def render_md(data: dict, api_summary: dict[str, dict[str, int]], total_all: int, api_class_count: int) -> str:
    """Render a compact, agent-optimized MD index.

    Design: agent already knows the product when it reaches this file.
    So we organize by product, inline URIs for focus products, and
    point to shards for everything else. No separate Task/API views.
    """
    records = data["records"]

    # Build per-product record groups
    by_product: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        by_product[r["product"]].append(r)

    # High-value kinds that get URI treatment
    HV_KINDS = {"quickstart", "operation", "webhook", "api-ref", "best-practice", "overview", "guide", "integration", "billing", "release-notes"}
    # Kinds shown with URIs for focus products
    URI_KINDS_REST = {"quickstart", "operation", "webhook", "api-ref", "best-practice"}
    # For SDK products (many platforms), deduplicate by slug
    URI_KINDS_SDK = {"quickstart", "operation", "webhook"}

    lines: list[str] = []

    # --- Header ---
    lines.append("# Documentation Index")
    lines.append("")
    lines.append("You already know the product — find it below, grab the URI, and fetch.")
    lines.append("")
    lines.append("How to use:")
    lines.append("1. Find your product in the catalog below")
    lines.append("2. If the URI is listed → fetch it directly with `fetch-doc-content.sh`")
    lines.append("3. If not listed → load `shards/{product}.json` and search by slug/kind")
    lines.append("4. For SDK class/interface docs → load `shards/api-ref/{product}-{platform}.json`")
    lines.append("")

    # --- Focus Products (full catalog with URIs) ---
    lines.append("---")
    lines.append("")

    for product in sorted(FOCUS_PRODUCTS):
        recs = by_product.get(product, [])
        if not recs:
            continue

        is_sdk = product in ("rtc", "rtm")
        uri_kinds = URI_KINDS_SDK if is_sdk else URI_KINDS_REST

        lines.append(f"## {product}")
        lines.append("")
        if is_sdk:
            lines.append("Platform aliases: web=javascript, 鸿蒙=harmonyos. Replace `{platform}` in URI pattern `docs://default/{product_uri}/{platform}/...`"
                         .replace("{product_uri}", "rtm2" if product == "rtm" else product))
            lines.append("")

        # Group by kind
        by_kind: dict[str, list[dict]] = defaultdict(list)
        for r in recs:
            by_kind[r["kind"]].append(r)

        for kind in KIND_ORDER:
            kind_recs = by_kind.get(kind, [])
            if not kind_recs:
                continue

            if kind in uri_kinds:
                if is_sdk:
                    # Deduplicate by slug, show one representative URI + platform list
                    seen_slugs: dict[str, dict] = {}
                    slug_platforms: dict[str, list[str]] = defaultdict(list)
                    for r in kind_recs:
                        if r["slug"] not in seen_slugs:
                            seen_slugs[r["slug"]] = r
                        slug_platforms[r["slug"]].append(r["platform"] or "unknown")

                    lines.append(f"**{kind}** ({len(kind_recs)} entries, {len(seen_slugs)} unique):")
                    for slug, r in sorted(seen_slugs.items()):
                        platforms = sorted(set(slug_platforms[slug]))
                        plat_note = f" [{', '.join(platforms)}]" if len(platforms) > 1 else ""
                        lines.append(f"- `{slug}`{plat_note} → `{r['uri']}`")
                else:
                    # REST product: show all URIs (manageable count)
                    lines.append(f"**{kind}** ({len(kind_recs)}):")
                    for r in kind_recs:
                        lines.append(f"- `{r['slug']}` → `{r['uri']}`")
            else:
                # Non-URI kind: just count
                platforms = Counter(r["platform"] or "unknown" for r in kind_recs)
                plat_str = ", ".join(f"{p}({c})" for p, c in sorted(platforms.items()))
                lines.append(f"**{kind}** ({len(kind_recs)}): {plat_str}")

        # API class summary
        if product in api_summary:
            api_parts = ", ".join(f"{p}({c})" for p, c in sorted(api_summary[product].items()))
            lines.append(f"**api-class** (separate): {api_parts} → `shards/api-ref/{product}-{{platform}}.json`")

        lines.append("")

    # --- Other Products (compact, one line each) ---
    lines.append("---")
    lines.append("")
    lines.append("## Other Products")
    lines.append("")
    lines.append("Load `shards/{product}.json` for full records.")
    lines.append("")

    other_products = sorted(set(by_product.keys()) - FOCUS_PRODUCTS)
    for product in other_products:
        recs = by_product[product]
        kinds = Counter(r["kind"] for r in recs)
        kind_str = ", ".join(f"{k}({v})" for k, v in sorted(kinds.items()) if k != "other")
        other_count = kinds.get("other", 0)
        if other_count:
            kind_str += f", other({other_count})" if kind_str else f"other({other_count})"
        api_note = ""
        if product in api_summary:
            total_api = sum(api_summary[product].values())
            api_note = f" + {total_api} api-class"
        lines.append(f"- `{product}`: {len(recs)} docs ({kind_str}){api_note}")

    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_shards(main_records: list[dict], api_class_records: list[dict]) -> tuple[dict[str, int], dict[str, int]]:
    """Write per-product shards (main) and per-product-platform API ref shards."""
    SHARD_DIR.mkdir(parents=True, exist_ok=True)
    API_SHARD_DIR.mkdir(parents=True, exist_ok=True)

    # Clean old shards
    for f in SHARD_DIR.glob("*.json"):
        f.unlink()
    for f in API_SHARD_DIR.glob("*.json"):
        f.unlink()

    # Main shards (non-api-class)
    by_product: dict[str, list[dict]] = defaultdict(list)
    for rec in main_records:
        by_product[rec["product"]].append(rec)
    main_counts = {}
    for product, recs in sorted(by_product.items()):
        path = SHARD_DIR / f"{product}.json"
        path.write_text(
            json.dumps(recs, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        main_counts[product] = len(recs)

    # API reference shards: per product-platform
    api_by_pp: dict[str, list[dict]] = defaultdict(list)
    for rec in api_class_records:
        key = f"{rec['product']}-{rec['platform'] or 'unknown'}"
        api_by_pp[key].append({"slug": rec["slug"], "uri": rec["uri"]})
    api_counts = {}
    for key, entries in sorted(api_by_pp.items()):
        entries.sort(key=lambda e: e["slug"])
        path = API_SHARD_DIR / f"{key}.json"
        path.write_text(
            json.dumps(entries, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        api_counts[key] = len(entries)

    return main_counts, api_counts


def main() -> None:
    all_records = parse_records()
    main_records, api_class_records = split_records(all_records)

    views = build_views(main_records)
    api_ref_tree = build_api_reference(api_class_records)
    api_summary = build_api_summary(api_class_records)

    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

    # --- Main JSON (non-api-class only) ---
    payload = {
        "version": 3,
        "source": "maintainer-refreshed official docs sitemap",
        "generated_at": now,
        "record_count": len(main_records),
        "api_class_count": len(api_class_records),
        "total_sitemap_count": len(all_records),
        "records": main_records,
        "views": views,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # --- API Reference JSON (compact tree) ---
    api_payload = {
        "version": 3,
        "source": "maintainer-refreshed official docs sitemap (api-reference route)",
        "generated_at": now,
        "record_count": len(api_class_records),
        "tree": api_ref_tree,
    }
    OUT_API_JSON.write_text(json.dumps(api_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # --- Shards ---
    main_shard_counts, api_shard_counts = write_shards(main_records, api_class_records)

    # --- MD ---
    OUT_MD.write_text(render_md(payload, api_summary, len(all_records), len(api_class_records)), encoding="utf-8")

    # --- Summary ---
    total = len(main_records)
    kind_counts: dict[str, int] = defaultdict(int)
    for r in main_records:
        kind_counts[r["kind"]] += 1
    classified = total - kind_counts.get("other", 0)
    pct = classified * 100 / total if total else 0

    print(f"=== v3 Build Summary ===")
    print(f"Main index: {OUT_JSON.relative_to(REPO_ROOT)} ({OUT_JSON.stat().st_size / 1024:.0f} KB, {total} records)")
    print(f"API reference: {OUT_API_JSON.relative_to(REPO_ROOT)} ({OUT_API_JSON.stat().st_size / 1024:.0f} KB, {len(api_class_records)} records)")
    print(f"MD: {OUT_MD.relative_to(REPO_ROOT)} ({OUT_MD.stat().st_size / 1024:.0f} KB)")
    print(f"Main shards: {len(main_shard_counts)} products in {SHARD_DIR.relative_to(REPO_ROOT)}/")
    print(f"API ref shards: {len(api_shard_counts)} product-platform files in {API_SHARD_DIR.relative_to(REPO_ROOT)}/")
    print(f"Classification (main): {classified}/{total} ({pct:.0f}%), {kind_counts.get('other', 0)} other")
    for kind in KIND_ORDER:
        if kind in kind_counts:
            print(f"  {kind}: {kind_counts[kind]}")
    print(f"Separated: {len(api_class_records)} api-class records → api-reference.json + shards/api-ref/")


if __name__ == "__main__":
    main()
