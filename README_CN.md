# Shengwang (Agora) Skills

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md)

AI coding agent 的声网平台集成技能包。帮助 agent 更准确地完成声网产品的接入、配置和调试。

## 覆盖产品

| Skill | 产品 | 说明 |
|-------|------|------|
| [conversational-ai](skills/shengwang-integration/references/conversational-ai/README.md) | ConvoAI | AI 语音 agent 全流程：创建/停止/更新/查询，支持 Go/Java/Python |
| [rtc](skills/shengwang-integration/references/rtc/README.md) | RTC SDK | 实时音视频通话，支持 Web/Android/iOS/Flutter 等 |
| [rtm](skills/shengwang-integration/references/rtm/README.md) | RTM | 实时消息、信令、Presence |
| [cloud-recording](skills/shengwang-integration/references/cloud-recording/README.md) | Cloud Recording | 服务端录制 RTC 会话 |
| [token-server](skills/shengwang-integration/references/token-server/README.md) | Token Server | 服务端 Token 生成（AccessToken2） |
| [general](skills/shengwang-integration/references/general/credentials-and-auth.md) | 通用 | 凭证管理、REST 认证模式 |
| [intake](skills/shengwang-integration/intake/README.md) | 路由 | 需求分析 → 产品推荐 → 路由到具体模块 |

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

通过 `ClawHub install + sync` 的方式安装和更新。首次安装使用 `install`，后续更新使用 `sync`。

```bash
openclaw skill install <shengwang-placeholder>
openclaw skill sync <shengwang-placeholder>
```

### 2. 下载文档索引（推荐）

下载文档索引，用于开发过程中获取最新 API 文档：

```bash
bash skills/shengwang-integration/scripts/fetch-docs.sh
```

文档索引保存到 `skills/shengwang-integration/references/docs.txt`。Skills 通过它查找并直接 HTTP 获取文档内容，无需额外的服务进程。

> 没有文档索引也能用，skills 会降级到本地参考文档 + 外部文档链接。

### 3. 开始使用

直接向 agent 描述你的需求，skills 会自动触发：

- "我想做一个 AI 语音客服" → intake 分析 → ConvoAI + RTC 集成
- "用 Go 生成一个 RTC token" → Token Server 模块
- "Web 端怎么实现视频通话" → RTC SDK 模块
- "下载 ConvoAI Go SDK" → Resource Downloader

## 工作原理

```
用户请求
   │
   ▼
skills/shengwang-integration/SKILL.md (入口)
   │
   ├─ 模糊请求 → intake (需求分析 → 产品推荐)
   │                 │
   │                 ▼
   │            产品模块 (代码生成)
   │
   └─ 明确请求 → 直接路由到产品模块
```

入口 (`skills/shengwang-integration/SKILL.md`) 判断请求是否足够明确：
- 明确的 → 直接路由到对应产品模块
- 模糊的 → 先走 intake 收集需求，再路由

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
│   └── validate-skills.sh     # 链接和 frontmatter 校验
├── tests/
│   └── eval-cases.md          # 评测用例
└── skills/
    └── shengwang-integration/     # Skill 本体（agentskills.io 标准）
        ├── SKILL.md               # 入口和路由（唯一的 SKILL.md）
        ├── intake/                # 需求分析与产品路由
        └── references/            # 所有产品模块和共享知识
            ├── doc-fetching.md        # 文档获取指南
            ├── docs.txt               # 本地文档索引
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
bash scripts/validate-skills.sh
```

检查 SKILL.md 的 frontmatter 格式和 markdown 链接有效性。

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
