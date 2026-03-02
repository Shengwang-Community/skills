# Shengwang (Agora) Skills

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md)

AI coding agent 的声网平台集成技能包。帮助 agent 更准确地完成声网产品的接入、配置和调试。

## 覆盖产品

| Skill | 产品 | 说明 |
|-------|------|------|
| [integrate-shengwang-conversational-ai](skills/shengwang-integration/integrate-shengwang-conversational-ai/SKILL.md) | ConvoAI | AI 语音 agent 全流程：创建/停止/更新/查询，支持 Go/Java/Python |
| [integrate-shengwang-rtc](skills/shengwang-integration/integrate-shengwang-rtc/SKILL.md) | RTC SDK | 实时音视频通话，支持 Web/Android/iOS/Flutter 等 |
| [integrate-shengwang-rtm](skills/shengwang-integration/integrate-shengwang-rtm/SKILL.md) | RTM | 实时消息、信令、Presence |
| [integrate-shengwang-cloud-recording](skills/shengwang-integration/integrate-shengwang-cloud-recording/SKILL.md) | Cloud Recording | 服务端录制 RTC 会话 |
| [implement-shengwang-token-on-server](skills/shengwang-integration/implement-shengwang-token-on-server/SKILL.md) | Token Server | 服务端 Token 生成（AccessToken2） |
| [general](skills/shengwang-integration/general/SKILL.md) | 通用 | 凭证管理、REST 认证模式 |
| [resource-downloader](skills/shengwang-integration/resource-downloader/SKILL.md) | 工具 | 下载 SDK、示例项目、Token Builder |
| [intake](skills/shengwang-integration/intake/SKILL.md) | 路由 | 需求分析 → 产品推荐 → 路由到具体模块 |

## 快速开始

## 安装

### 方式 A：Skills CLI（agentskills.io 标准）

```bash
npx skills add HugoChaan/agent-skills
```

### 方式 B：Git clone

将本仓库克隆到你的 AI coding agent 的 skills 目录：

```bash
# Claude Code
git clone https://github.com/HugoChaan/agent-skills.git .claude/skills/shengwang-skills

# Kiro
git clone https://github.com/HugoChaan/agent-skills.git .kiro/skills/shengwang-skills
```

### 2. 配置 MCP（推荐）

Skills 设计为配合 [Agora Doc MCP Server](https://doc-mcp.shengwang.cn) 使用。MCP 提供实时文档内容，skills 提供行为指导和工作流。

在你的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "agora-docs": {
      "type": "sse",
      "url": "https://doc-mcp.shengwang.cn/mcp"
    }
  }
}
```

> 没有 MCP 也能用，skills 会降级到本地 OpenAPI spec + 外部文档链接。

### 3. 开始使用

直接向 agent 描述你的需求，skills 会自动触发：

- "我想做一个 AI 语音客服" → intake 分析 → ConvoAI + RTC 集成
- "用 Go 生成一个 RTC token" → Token Server skill
- "Web 端怎么实现视频通话" → RTC SDK skill
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
- 明确的 → 直接路由到对应产品 skill
- 模糊的 → 先走 intake 收集需求，再路由

每个产品 skill 遵循统一工作流：确认凭证 → 通过 MCP 获取最新文档 → 生成代码 → 验证。

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
        ├── SKILL.md               # 入口和路由
        ├── mcp-tools.md           # MCP 工具使用指南
        ├── intake/                # 需求分析与产品路由
        ├── general/               # 凭证、REST 认证
        ├── integrate-shengwang-conversational-ai/  # ConvoAI
        ├── integrate-shengwang-rtc/               # RTC SDK
        ├── integrate-shengwang-rtm/               # RTM
        ├── integrate-shengwang-cloud-recording/   # Cloud Recording
        ├── implement-shengwang-token-on-server/   # Token 生成
        └── resource-downloader/                   # SDK/示例下载
```

## 设计原则

- 行为指导优先于 API 知识：skills 教 agent "怎么做"，MCP 提供"具体 API"
- 单一职责：每个 skill 只做一件事
- 渐进式披露：SKILL.md 做导航，详细内容在 references/
- 失败路径显式定义：每个 skill 都有错误处理表
- 评测驱动迭代：修改 skill 后用 `tests/eval-cases.md` 回归验证

## 本地验证

```bash
bash scripts/validate-skills.sh
```

检查所有 SKILL.md 的 frontmatter 格式和 markdown 链接有效性。

## 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)。核心要求：

- 每个 skill 目录必须有 `SKILL.md`，包含 YAML frontmatter（name, description, metadata.author, metadata.version）
- 目录名用 kebab-case
- 详细文档放 `references/`，SKILL.md 保持精简
- 提交前跑 `bash scripts/validate-skills.sh`

## 链接

- [Shengwang Console](https://console.shengwang.cn/)
- [声网文档](https://doc.shengwang.cn/)
- [GitHub](https://github.com/AgoraIO-Community)
