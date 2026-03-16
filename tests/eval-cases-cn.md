# Skill 评测用例

评测驱动迭代。每次修改 skill 后，用这些用例回归验证。

## 评测方法

对每个用例：
1. 将 "用户输入" 发送给模型（已加载 skills）
2. 检查模型行为是否符合 "期望行为"
3. 标记 PASS / FAIL
4. FAIL 的用例驱动 skill 修改

---

## 一、路由准确性（Root Router → Intake / Product Module）

### R-01: 模糊请求必须走 intake

- 用户输入: "我想做一个 AI 客服"
- 期望行为: 进入 intake 流程，分析需求，推荐 ConvoAI + RTC SDK
- 判定标准: 模型未直接生成代码，而是先询问细节或输出需求分析
- 结果: ___

### R-02: 产品名不等于跳过 intake

- 用户输入: "帮我接入 ConvoAI"
- 期望行为: 进入 ConvoAI intake，并在一条消息里收集所有缺失的阻塞信息
- 判定标准: 模型未直接生成 /join 代码，而是先给出缺失问题及对应选项/默认值
- 结果: ___

### R-03: 具体操作跳过 intake

- 用户输入: "帮我停掉 agent_abc12345"
- 期望行为: 直接路由到 ConvoAI 模块，生成 /leave 调用
- 判定标准: 模型未走 intake 流程，直接执行操作
- 结果: ___

### R-04: 错误查询跳过 intake

- 用户输入: "ConvoAI 返回 403 是什么意思"
- 期望行为: 直接路由到 convoai/common-errors.md
- 判定标准: 模型给出 403 的三种原因和修复方法
- 结果: ___

### R-05: 多产品请求走 intake

- 用户输入: "我想做视频通话加 AI 助手"
- 期望行为: 进入 intake，识别 RTC + ConvoAI 组合
- 判定标准: 模型输出包含多产品的需求分析，并在 ConvoAI 为主时提醒客户端仍需要 RTC SDK
- 结果: ___

### R-06: Token 请求直接路由

- 用户输入: "用 Go 生成一个 RTC token"
- 期望行为: 直接路由到 token-server
- 判定标准: 模型生成 Go token 代码，未走 intake
- 结果: ___

### R-07: RTC 请求路由到 RTC 模块

- 用户输入: "Web 端怎么实现视频通话"
- 期望行为: 路由到 rtc，获取 Web quick start 文档
- 判定标准: 模型基于 RTC Web SDK 给出集成指导
- 结果: ___

### R-08: 下载请求直接路由

- 用户输入: "下载 ConvoAI Go SDK"
- 期望行为: 路由到相关产品模块，给出正确 URL
- 判定标准: 模型给出正确 URL 或执行 git clone
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

### C-06: 文档获取

- 用户输入: "用 Go 接入 ConvoAI"
- 期望行为: 模型 fetch Go quick start 文档 URL
- 判定标准: 通过运行 `bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start-go"` 获取内容
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

### I-03: 部分已知信息时仍聚焦当前 intake

- 用户输入: "接入 ConvoAI，用 deepseek，Python 开发"
- 期望行为: 只针对剩余缺失项发出一条集中式问题
- 判定标准: 未逐个问 Q1/Q2/Q3，而是在同一条消息里继续展示尚未确认但有默认值的问题，并把 platform、backend 和 provider 默认项都标成可选，并要求稀疏的一行数字回复
- 结果: ___

### I-04: 信息较少时给出完整清单

- 用户输入: "用 Python 接入 ConvoAI"
- 期望行为: 一次性给出 ConvoAI 的缺失字段清单，包含 kickoff 和 provider 相关问题
- 判定标准: 保持聚焦 platform、backend 和 provider 选择；仍列出尚未确认的 platform、backend、LLM、TTS、ASR、ASR 语言问题并标成可选，并附带类似 `5A 6A` 的稀疏示例
- 结果: ___

### I-05: 一次回复后产出结构化 spec

- 用户输入: "做一个 Web AI 语音助手，Python 服务端，其他用默认"
- 期望行为: 直接归一化成 ConvoAI 结构化 spec 并继续
- 判定标准: 输出的结构化 spec 只包含 intake 范围内的字段，且省略的可选项按默认值记录
- 结果: ___

### I-06: 数字回复可正确解析

- 用户输入: "5A 6A"
- 期望行为: 按当前提示里的编号正确解析，并归一化成 ConvoAI spec
- 判定标准: 接受稀疏数字代码，未填写的可选题自动按默认值处理，包含 platform 和 backend
- 结果: ___

### I-07: 选择 Other 时只追问该字段

- 用户输入: "4C 5A 6A"
- 期望行为: 只针对自定义语言做一次窄追问，其余字段直接保留
- 判定标准: 不会把已确认字段重新打开
- 结果: ___

### I-08: 额外的后续配置说明不应打断 intake

- 用户输入: "1A 2E 3G 4C 5A 6A 7A，后面的配置我自己处理"
- 期望行为: intake 仍聚焦产品选项，忽略额外的非 intake 说明
- 判定标准: 不会额外引入新的非 intake 提问
- 结果: ___

---

## 四、失败路径覆盖

### F-01: 下载失败

- 用户输入: "下载 https://github.com/AgoraIO/nonexistent-repo"
- 期望行为: 报告下载失败，建议检查 URL
- 判定标准: 不是静默失败或编造内容
- 结果: ___

### F-02: 文档获取失败时的降级

- 场景: HTTP fetch 文档失败
- 用户输入: "用 Python 接入 ConvoAI"
- 期望行为: 使用 Generation Rules + fallback URL 生成代码，并提示用户验证
- 判定标准: 告知用户文档获取失败，给出 fallback URL
- 结果: ___

### F-03: 缺少凭证时的引导

- 用户输入: "创建一个 ConvoAI agent" (无 .env 文件)
- 期望行为: 检测到缺少凭证，引导到 credentials-and-auth.md
- 判定标准: 不是用占位符直接生成代码
- 结果: ___

---

## 评测记录

| 日期 | 版本 | 通过 | 失败 | 失败用例 | 修复措施 |
|------|------|------|------|----------|----------|
| | | | | | |
