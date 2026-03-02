# Skill 评测用例

评测驱动迭代。每次修改 skill 后，用这些用例回归验证。

## 评测方法

对每个用例：
1. 将 "用户输入" 发送给模型（已加载 skills）
2. 检查模型行为是否符合 "期望行为"
3. 标记 PASS / FAIL
4. FAIL 的用例驱动 skill 修改

---

## 一、路由准确性（Root Router → Intake / Product Skill）

### R-01: 模糊请求必须走 intake

- 用户输入: "我想做一个 AI 客服"
- 期望行为: 进入 intake 流程，分析需求，推荐 ConvoAI + RTC SDK
- 判定标准: 模型未直接生成代码，而是先询问细节或输出需求分析
- 结果: ___

### R-02: 产品名不等于跳过 intake

- 用户输入: "帮我接入 ConvoAI"
- 期望行为: 进入 intake（或 ConvoAI intake），收集 LLM、语言等细节
- 判定标准: 模型未直接生成 /join 代码，而是先确认缺失信息
- 结果: ___

### R-03: 具体操作跳过 intake

- 用户输入: "帮我停掉 agent_abc12345"
- 期望行为: 直接路由到 ConvoAI skill，生成 /leave 调用
- 判定标准: 模型未走 intake 流程，直接执行操作
- 结果: ___

### R-04: 错误查询跳过 intake

- 用户输入: "ConvoAI 返回 403 是什么意思"
- 期望行为: 直接路由到 troubleshooting/common-errors.md
- 判定标准: 模型给出 403 的三种原因和修复方法
- 结果: ___

### R-05: 多产品请求走 intake

- 用户输入: "我想做视频通话加 AI 助手"
- 期望行为: 进入 intake，识别 RTC + ConvoAI 组合
- 判定标准: 模型输出包含多产品的需求分析
- 结果: ___

### R-06: Token 请求直接路由

- 用户输入: "用 Go 生成一个 RTC token"
- 期望行为: 直接路由到 implement-shengwang-token-on-server
- 判定标准: 模型生成 Go token 代码，未走 intake
- 结果: ___

### R-07: RTC 请求路由到 RTC skill

- 用户输入: "Web 端怎么实现视频通话"
- 期望行为: 路由到 integrate-shengwang-rtc，调用 MCP 获取 Web quick start
- 判定标准: 模型基于 RTC Web SDK 给出集成指导
- 结果: ___

### R-08: 下载请求直接路由

- 用户输入: "下载 ConvoAI Go SDK"
- 期望行为: 直接路由到 resource-downloader
- 判定标准: 模型执行 downloader 脚本或给出正确 URL
- 结果: ___

---

## 二、ConvoAI 代码生成质量

### C-01: agent_rtc_uid 类型正确

- 用户输入: (通过 intake 后) "用 Python 创建一个 ConvoAI agent"
- 期望行为: 生成的代码中 `agent_rtc_uid` 为 string `"0"`
- 判定标准: 不是 int `0`
- 结果: ___

### C-02: remote_rtc_uids 类型正确

- 用户输入: 同上
- 期望行为: 生成的代码中 `remote_rtc_uids` 为 `["*"]`
- 判定标准: 不是 string `"*"`
- 结果: ___

### C-03: agent name 唯一性

- 用户输入: 同上
- 期望行为: agent `name` 包含随机后缀 (如 `agent_{uuid[:8]}`)
- 判定标准: 不是固定字符串如 `"my_agent"`
- 结果: ___

### C-04: 凭证不硬编码

- 用户输入: 同上
- 期望行为: AppID、Customer Key/Secret 从环境变量读取
- 判定标准: 代码中无硬编码的凭证值
- 结果: ___

### C-05: 409 错误处理

- 用户输入: "创建 agent 时返回 409 怎么办"
- 期望行为: 建议提取已有 agent_id 或生成新 name 重试
- 判定标准: 给出两种解决方案
- 结果: ___

### C-06: MCP 文档获取

- 用户输入: "用 Go 接入 ConvoAI"
- 期望行为: 模型调用 `get-doc-content` 获取 Go quick start
- 判定标准: 使用 URI `docs://default/convoai/restful/get-started/quick-start-go`
- 结果: ___

---

## 三、Intake 需求分析质量

### I-01: 正确识别产品组合

- 用户输入: "我想做一个在线教育平台，老师和学生视频上课，课后可以回看录像"
- 期望行为: 识别 RTC SDK (视频) + Cloud Recording (回看)
- 判定标准: 输出的需求分析包含这两个产品
- 结果: ___

### I-02: ConvoAI 依赖 RTC 的提示

- 用户输入: "我想做一个 AI 语音助手"
- 期望行为: 识别 ConvoAI (主) + RTC SDK (客户端配套)
- 判定标准: 明确告知用户客户端需要 RTC SDK
- 结果: ___

### I-03: 快速路径生效

- 用户输入: "接入 ConvoAI，我有凭证，用 deepseek，Python 开发"
- 期望行为: 跳过逐个提问，直接生成结构化 spec 确认
- 判定标准: 未逐个问 Q1/Q2/Q3，而是直接输出 spec
- 结果: ___

---

## 四、失败路径覆盖

### F-01: resource-downloader 失败

- 用户输入: "下载 https://github.com/AgoraIO/nonexistent-repo"
- 期望行为: 报告下载失败，建议检查 URL 或从 Common Resources 表中选择
- 判定标准: 不是静默失败或编造内容
- 结果: ___

### F-02: MCP 不可用时的降级

- 场景: MCP server 无法连接
- 用户输入: "用 Python 接入 ConvoAI"
- 期望行为: 使用本地 OpenAPI spec + Generation Rules 生成代码，并提示用户验证
- 判定标准: 告知用户 MCP 不可用，给出 fallback URL
- 结果: ___

### F-03: 缺少凭证时的引导

- 用户输入: "创建一个 ConvoAI agent" (无 .env 文件)
- 期望行为: 检测到缺少凭证，引导到 credentials.md
- 判定标准: 不是用占位符直接生成代码
- 结果: ___

---

## 评测记录

| 日期 | 版本 | 通过 | 失败 | 失败用例 | 修复措施 |
|------|------|------|------|----------|----------|
| | | | | | |
