---
name: shengwang-resource-downloader
description: |
  Downloads Shengwang (Agora) SDKs, sample projects, Token Builder libraries,
  and GitHub repositories. Use when the user asks to download an SDK, clone a
  sample project, get the Token Builder, or fetch any related resource from
  GitHub or a direct URL.
triggers:
  - "shengwang download"
  - "download sdk"
  - "download sample"
  - "clone repo"
  - "get token builder"
  - "download agora"
  - "sample project"
  - "demo project"
  - "下载SDK"
  - "下载示例"
  - "下载demo"
  - "下载Token Builder"
  - "获取示例代码"
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
