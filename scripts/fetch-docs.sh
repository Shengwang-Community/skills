#!/bin/bash
# Maintainer tool: refresh the official docs sitemap and rebuild bundled indexes
# Usage: bash scripts/fetch-docs.sh

set -euo pipefail

DOCS_URL="https://doc.shengwang.cn/llms.txt"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CACHE_DIR="${REPO_ROOT}/scripts/.cache"
mkdir -p "${CACHE_DIR}"
OUTPUT_FILE="${CACHE_DIR}/docs-sitemap.txt"
MAX_RETRIES=3

for i in $(seq 1 $MAX_RETRIES); do
  echo "Downloading doc index (attempt ${i}/${MAX_RETRIES}) ..."
  if curl -fSL --retry 2 --max-time 120 -o "${OUTPUT_FILE}" "${DOCS_URL}"; then
    echo "Saved to ${OUTPUT_FILE}"
    if command -v python3 >/dev/null 2>&1; then
      python3 "${REPO_ROOT}/scripts/build-doc-index.py" "${OUTPUT_FILE}" || echo "WARNING: docs sitemap downloaded but bundled indexes were not rebuilt."
    else
      echo "WARNING: python3 not found; skipped docs.index rebuild."
    fi
    exit 0
  fi
  echo "Attempt ${i} failed."
  sleep 2
done

echo "ERROR: Failed after ${MAX_RETRIES} attempts. Check your network and try again."
exit 1
