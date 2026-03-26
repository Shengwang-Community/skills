# Shengwang Skills

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md)

AI coding agent 的声网平台集成技能包。帮助 agent 更准确地完成声网产品的接入、配置和调试。

## 覆盖产品

| Skill | 产品 | 说明 |
|-------|------|------|
| [conversational-ai](skills/voice-ai-integration/references/conversational-ai/README.md) | ConvoAI | AI 语音 agent 全流程：创建/停止/更新/查询，支持 Go/Java/Python |
| [rtc](skills/voice-ai-integration/references/rtc/README.md) | RTC SDK | 实时音视频通话，支持 Web/Android/iOS/Flutter 等 |
| [rtm](skills/voice-ai-integration/references/rtm/README.md) | RTM | 实时消息、信令、Presence |
| [cloud-recording](skills/voice-ai-integration/references/cloud-recording/README.md) | Cloud Recording | 服务端录制 RTC 会话 |
| [token-server](skills/voice-ai-integration/references/token-server/README.md) | Token Server | 服务端 Token 生成（AccessToken2） |
| [general](skills/voice-ai-integration/references/general/credentials-and-auth.md) | 通用 | 凭证管理、REST 认证模式 |

## 快速开始

### 安装方式

#### Skills CLI

使用 CLI 安装：

```bash
npx skills add Shengwang-Community/skills
```

这是最直接的安装方式。安装完成后，再按对应 Coding Agent 的说明重启会话或刷新技能列表。

#### Claude Code Plugin Marketplace

在 Claude Code 中执行下面的命令安装：

```bash
plugin marketplace add Shengwang-Community/skills
```

#### OpenClaw

通过 `ClawHub` 安装。首次安装使用 `install`，后续更新使用 `update`。

```bash
clawhub install voice-ai-integration
clawhub update voice-ai-integration
```

### 2. 使用内置索引

skill 会随附预构建好的静态索引：

- `skills/voice-ai-integration/references/doc-index/docs.index.md` — 按产品组织的文档目录，重点产品直接附 URI
- `skills/voice-ai-integration/references/doc-index/shards/{product}.json` — 按产品分片的详细记录
- `skills/voice-ai-integration/references/doc-index/shards/api-ref/{product}-{platform}.json` — SDK 类文档

这些文件是 fallback lookup 工具。Agent 应先走被路由到的产品模块，只有当模块仍然需要外部文档定位时，才使用这些索引。

刷新索引（仅维护者）：
```bash
bash scripts/fetch-docs.sh
```

### 3. 开始使用

直接向 agent 描述你的需求，skills 会自动触发：

- "我想做一个 AI 语音客服" → ConvoAI + RTC 集成
- "用 Go 生成一个 RTC token" → Token Server 模块
- "Web 端怎么实现视频通话" → RTC SDK 模块
- "下载 ConvoAI Go SDK" → Resource Downloader

## 工作原理

```
用户请求
   │
   ▼
skills/voice-ai-integration/SKILL.md (入口)
   │
   ├─ 明确请求 → 直接路由到产品模块
   │
   └─ 模糊请求 → 问一个澄清问题，然后路由
```

入口 (`skills/voice-ai-integration/SKILL.md`) 将请求匹配到产品模块：
- 明确的 → 直接路由到对应产品模块
- 模糊的 → 问一个澄清问题，然后路由

每个产品模块遵循统一工作流：确认凭证 → 获取最新文档 → 生成代码 → 验证。

## 仓库结构

```
shengwang-skills/
├── README.md                  # 英文版
├── README_CN.md               # 本文件
├── AGENTS.md                  # Agent 入口指令
├── CLAUDE.md                  # → AGENTS.md
├── CONTRIBUTING.md            # 贡献规范
├── scripts/
│   ├── fetch-docs.sh          # 下载 sitemap + 重建 doc-index
│   ├── build-doc-index.py     # 从 sitemap 生成所有索引文件
│   ├── ab-test-doc-index.py   # Token 匹配基准测试（56 cases）
│   ├── llm-eval-doc-index.py  # LLM 端到端评测（72 cases）
│   └── validate-skills.sh     # 链接和 frontmatter 校验
├── tests/
│   ├── eval-cases.md          # 评测用例
│   └── doc-index-benchmark.md # Doc-index 基准测试结果
└── skills/
    └── voice-ai-integration/     # Skill 本体（agentskills.io 标准）
        ├── SKILL.md               # 入口和路由（唯一的 SKILL.md）
        └── references/            # 所有产品模块和共享知识
            ├── doc-fetching.md        # 文档获取指南
            ├── doc-index/             # 预构建文档索引
            │   ├── docs.index.md      # Agent 可读的产品目录
            │   ├── docs.index.json    # 完整机器可读索引
            │   ├── api-reference.json # SDK 类文档（独立）
            │   └── shards/            # 按产品分片
            ├── general/               # 凭证、REST 认证
            ├── conversational-ai/     # ConvoAI
            ├── rtc/                   # RTC SDK
            ├── rtm/                   # RTM
            ├── cloud-recording/       # Cloud Recording
            └── token-server/          # Token 生成
```

## 设计原则

- 行为指导优先于 API 知识：skills 教 agent "怎么做"，文档获取提供"具体 API"
- 单一职责：每个模块只做一件事
- 渐进式披露：SKILL.md 做导航，详细内容在 references/ 和各模块 README.md 中
- 失败路径显式定义：每个模块都有错误处理表
- 评测驱动迭代：修改后用 `tests/eval-cases.md` 回归验证

## 本地验证

```bash
# 验证 skill 结构和链接
bash scripts/validate-skills.sh

# 跑 doc-index token 基准测试（不需要 API key）
python3 scripts/ab-test-doc-index.py

# 跑 doc-index LLM 端到端评测（需要 OPENAI_API_KEY）
export OPENAI_API_KEY=sk-...
python3 scripts/llm-eval-doc-index.py

# 重建 doc-index（仅维护者）
bash scripts/fetch-docs.sh
```

## 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)。核心要求：

- 根 skill 目录有 `SKILL.md`，包含 YAML frontmatter（name, description, metadata.author, metadata.version）
- 子模块使用 `README.md`（无需 frontmatter）
- 目录名用 kebab-case
- 详细文档放 `references/`，SKILL.md 和 README.md 保持精简
- 提交前跑 `bash scripts/validate-skills.sh`

## 链接

- [Shengwang Console](https://console.shengwang.cn/)
- [声网文档](https://doc.shengwang.cn/)
- [GitHub](https://github.com/Shengwang-Community)
