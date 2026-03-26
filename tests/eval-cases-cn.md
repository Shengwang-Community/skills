# Skill 评测用例

评测驱动迭代。每次修改 skill 后，用这些用例回归验证。

## 评测方法

对每个用例：
1. 将 "用户输入" 发送给模型（已加载 skills）
2. 检查模型行为是否符合 "期望行为"
3. 标记 PASS / FAIL
4. FAIL 的用例驱动 skill 修改

---

## 一、路由准确性（SKILL.md → 产品模块）

### R-01: 模糊请求触发澄清后路由

- 用户输入: "我想做一个 AI 客服"
- 期望行为: 通过 SKILL.md 路由辅助表推断 ConvoAI + RTC SDK，或问一个澄清问题
- 判定标准: 模型未直接生成代码，而是先询问细节或输出路由摘要
- 结果: ___

### R-02: 产品名不等于跳过 ConvoAI 内部 intake

- 用户输入: "帮我接入 ConvoAI"
- 期望行为: 路由到 ConvoAI 模块，进入 ConvoAI quickstart，并在一条消息里收集所有缺失的阻塞信息
- 判定标准: 模型未直接生成 /join 代码，而是先给出缺失问题及对应选项/默认值
- 结果: ___

### R-03: 具体操作直接路由

- 用户输入: "帮我停掉 agent_abc12345"
- 期望行为: 直接路由到 ConvoAI 模块，生成 /leave 调用
- 判定标准: 模型直接路由，未问澄清问题
- 结果: ___

### R-04: 错误查询直接路由

- 用户输入: "ConvoAI 返回 403 是什么意思"
- 期望行为: 直接路由到 convoai/common-errors.md
- 判定标准: 模型给出 403 的三种原因和修复方法
- 结果: ___

### R-05: 多产品请求触发路由澄清

- 用户输入: "我想做视频通话加 AI 助手"
- 期望行为: 通过 SKILL.md 常见组合表识别 RTC + ConvoAI 组合
- 判定标准: 模型输出包含多产品的需求分析，并在 ConvoAI 为主时提醒客户端仍需要 RTC SDK
- 结果: ___

### R-06: Token 请求直接路由

- 用户输入: "用 Go 生成一个 RTC token"
- 期望行为: 直接路由到 token-server
- 判定标准: 模型生成 Go token 代码，未问澄清问题
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

- 用户输入: (通过 ConvoAI quickstart 后) "用 Python 创建一个 ConvoAI agent"
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

### C-07: 已有 pipeline ID 时走 env + 清理旧 provider 配置

- 用户输入: （走完 pipeline-id 分支后）"按我现有的 pipeline ID 实现当前示例"
- 期望行为: 复用匹配的平台 sample 结构，从环境变量读取 pipeline ID，并在 pipeline 路径替换旧请求后清理无用的 `ASR` / `LLM` / `TTS` 配置
- 判定标准: 生成的代码或配置从 env 读取 pipeline ID，且被替换的流程里不再保留无用的 provider-only 配置
- 结果: ___

### C-08: 根据提供的 curl 生成同形状的 pipeline 请求代码

- 用户输入: （走完 pipeline-id 分支后）"为我当前的平台生成请求代码"
- 期望行为: 生成的平台请求代码保留 curl 的 `POST /projects/{appId}/join/` 形状、`Authorization: agora token=...` 头格式，以及 `name`、`pipeline_id`、`properties.agent_rtc_uid`、`properties.channel`、`properties.remote_rtc_uids`、`properties.token` 这些 JSON 字段
- 判定标准: 生成的请求代码遵循 curl 的结构，从 env 读取 `pipeline_id`，令 `name = channel`，沿用 sample 现有 token 生成规则为 header 和 `properties.token` 分别生成 RTC token，且不会把 curl 中的字面 token 值硬编码进源码
- 结果: ___

### C-09: 保留 pipeline 响应解析和 Web 薄代理

- 用户输入: （走完 pipeline-id 分支后）"实现 Web 的 pipeline 路径"
- 期望行为: Web 侧保留一个薄服务端代理，在代理里执行 pipeline join 请求，并解析成功响应中的 `agent_id`、`create_ts`、`status`
- 判定标准: Web 路径不会把 pipeline join 请求中的 token 暴露到前端代码，会先从 sample 中定位当前服务端请求路径再修改，且生成的流程会保留这三个响应字段供后续使用
- 结果: ___

### C-10: Native 平台的 pipeline 改造应保持贴近 sample

- 用户输入: （走完 pipeline-id 分支并选择 Android 后）"实现 Android 的 pipeline 路径"
- 期望行为: 复用 native sample 对应子目录，只替换 provider 请求/配置路径，沿用现有 token 生成路径，并保留 sample 的其余结构
- 判定标准: 生成的 Android 流程保留 sample 应用结构，先检查 config/request/token 文件再碰 UI，新增 `SHENGWANG_PIPELINE_ID`，为 header 和 agent 分别生成 RTC token，清理旧 provider 配置，并解析 `agent_id`、`create_ts`、`status`
- 结果: ___

### C-11: 正常实现流程不应要求用户再贴 pipeline ID 或 curl

- 用户输入: （走完 pipeline-id 分支后）"实现 iOS 的 pipeline 路径"
- 期望行为: 直接使用 skill 里固定的 pipeline 请求形状，新增 `SHENGWANG_PIPELINE_ID` 配置占位，并继续实现，不要求用户再贴 live 的 pipeline ID 值或 curl
- 判定标准: 模型在正常生成代码过程中，不会再向用户索取实际 pipeline ID 值或 pipeline curl
- 结果: ___

### C-12: 各平台配置风格都应保持贴近 sample

- 用户输入: （走完 pipeline-id 分支后）"实现当前平台的 pipeline 路径"
- 期望行为: 保持所选 sample 的配置风格，清理旧 provider 配置，新增 `SHENGWANG_PIPELINE_ID` 占位，不额外发明新的配置体系
- 判定标准: 生成的平台配置保持贴近 sample 的风格，不会增加没有必要的配置读取层，也不会把配置 key 名称本身当成运行时值
- 结果: ___

---

## 三、ConvoAI Quickstart Intake 质量

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

### I-03: 部分已知信息时仍聚焦当前 quickstart intake

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
- 判定标准: 输出的结构化 spec 只包含 quickstart 范围内的字段，且省略的可选项按默认值记录
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

### I-08: 额外的后续配置说明不应打断 quickstart intake

- 用户输入: "1A 2E 3G 4C 5A 6A 7A，后面的配置我自己处理"
- 期望行为: quickstart intake 仍聚焦产品选项，忽略额外的非 intake 说明
- 判定标准: 不会额外引入新的非 quickstart 提问
- 判定标准: 不会额外引入新的非 intake 提问
- 结果: ___

### I-09: provider 问题前必须先经过 pipeline-id 检查点

- 用户输入: 在前置条件问题后，用户回复 "A"
- 期望行为: 在任何默认 provider 提问之前，先确认用户是否已有 pipeline ID
- 判定标准: 下一轮是 pipeline-id 提问，且同一条消息里不会夹带默认 provider 提问
- 结果: ___

### I-10: 用户已有 pipeline ID 时跳出默认 provider 路径

- 用户输入: 在 pipeline-id 提问后，用户回复 "B"
- 期望行为: 停止当前默认 provider 路径，并继续追问要实现的示例平台
- 判定标准: 用户说明自己已有 pipeline ID 后，下一轮应是示例平台选择，不会再继续给默认 provider 提示或完整 provider checklist
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
