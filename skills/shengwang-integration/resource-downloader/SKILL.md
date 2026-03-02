---
name: shengwang-resource-downloader
description: |
  Downloads Shengwang (Agora) SDKs, sample projects, Token Builder libraries,
  and GitHub repositories. Use when the user asks to download an SDK, clone a
  sample project, get the Token Builder, 下载SDK, 下载示例, or fetch any
  related resource from GitHub or a direct URL.
license: MIT
metadata:
  author: shengwang
  version: "1.1.0"
---

# Shengwang Resource Downloader

Downloads Shengwang (Agora) SDKs, sample projects, and GitHub repositories to the local workspace.

## Usage

```bash
python3 shengwang-skills/skills/resource-downloader/scripts/downloader.py <url> <workspace_root_path>
```

Supports:
- GitHub repositories (uses `git clone --depth 1`)
- Direct file URLs (ZIP, TAR, etc. — auto-extracted)
- Any public HTTP/HTTPS resource

Output: path to the downloaded folder under `<workspace_root>/.tmp/`

## Common Agora Resources

### Token Builder

| Language | URL |
|----------|-----|
| Go | `https://github.com/AgoraIO/Tools` |
| All languages | `https://github.com/AgoraIO/Tools` |

### ConvoAI SDK Samples

| Resource | URL |
|----------|-----|
| Go REST client | `https://github.com/AgoraIO-Community/agora-rest-client-go` |
| Java REST client | `https://github.com/AgoraIO-Community/agora-rest-client-java` |
| ConvoAI server sample | `https://github.com/Shengwang-Community/Conversational-AI-Server-Sample` |

### RTC SDK Samples

| Resource | URL |
|----------|-----|
| Web sample | `https://github.com/AgoraIO/API-Examples-Web` |
| Android sample | `https://github.com/AgoraIO/API-Examples` |

## Workflow

1. Identify the resource the user needs
2. Find the correct URL from the table above or ask the user
3. Run the downloader script
4. Tell the user where the files were downloaded

## Rules

- GitHub repo URLs must NOT include branch or subdirectory paths
  - ✅ `https://github.com/AgoraIO-Community/agora-rest-client-go`
  - ❌ `https://github.com/AgoraIO-Community/agora-rest-client-go/tree/main/services`
- Script requires `requests` library: `pip install requests`
- Script requires `git` to be installed for GitHub repos

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| `git clone` fails with 128 | Repo URL invalid or private | Verify URL exists and is public. Suggest correct URL from Common Resources table. |
| Network timeout | No internet or DNS failure | Retry once. If still fails, tell user to check network and try manually. |
| `requests` not installed | Missing Python dependency | Run `pip install requests` and retry. |
| `git` not found | Git not installed | Tell user to install git: `brew install git` (macOS) or `apt install git` (Linux). |
| Disk full / permission denied | Filesystem issue | Report the error message. Suggest checking disk space or permissions on target directory. |
| ZIP extraction fails | Corrupted download | Delete partial file, retry download. If still fails, provide direct URL for manual download. |

On any unrecoverable failure: report the exact error, suggest the user download manually from the URL, and do NOT silently skip or fabricate content.
