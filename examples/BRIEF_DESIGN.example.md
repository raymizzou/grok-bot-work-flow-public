# BRIEF — #123 登录超时：出方案 v1（Claude 设计）

> 脱敏样例：根据参考实现的真实派单改写，业务内容已替换。文件放在 `<TASK_ROOT>/FEATURE-123-login-timeout/BRIEF_CLAUDE_S10.md`。

【LLM：<Bot 名>｜<模型>】

## 身份
- issue：https://github.com/YOUR_GH_OWNER/YOUR_BUSINESS_REPO/issues/123
- 进度板行名（逐字）：`登录偶发超时`
- task_id：`fe123-login`
- 主机：`YOUR_CLOUD_HOST` 的 Herdr default 会话；tab 标题 `123-login-timeout`；agent `fe123-login-review`
- 档位：Opus 5.5 / effort=high / fast=否
- cwd：`~/projects/YOUR_BUSINESS_REPO`（只读）

## 授权
负责人 <时间，带时区>：「123 跟进」。issue 已记【跟进】：<评论链接>。
负责人原话（问题描述）：「登录有时候要等 30 秒才报错，查一下为什么，给个修法。」

## 任务
写**方案 v1**。正文只准六块：
1. 问题　2. 原因（不确定就写清还不确定什么）　3. 修复方案　4. 当前架构图　5. 修复后架构图　6. Open Question（需要负责人澄清才加，最多 5 条，放末尾）

另附：G1 架构门初判（是否引入新服务/持久状态/跨端契约）、验收草案（编号 TA-1、TA-2…，每条可核验）。
大白话；不自造术语；不另加章节。读代码要读本机仓，不凭记忆。

## 交付
1. 全文落盘 `<TASK_ROOT>/FEATURE-123-login-timeout/PLAN_S10.md`。
2. 在 issue #123 贴评论：
   - 第一行：`【方案 v1】#123 登录偶发超时`
   - 正文：六块（可为摘要 + PLAN 路径）
   - 结尾：`Open Question：k 条` 或 `无 Open Question`
   - 最后一行：`【LLM：Claude@<主机>｜Opus 5.5｜effort=high｜fast=否】`
3. 读回评论确认已贴出，然后在本机发**一次**信号：
   `board-signal-post --task fe123-login`，`status=blocked`、`event=blocked`、`host=<Claude 主机枚举值>`，
   `pr` 填 issue 链接，`question` 用草稿：
   - 有 OQ：`<负责人> 需决策：#123 方案 v1 请拍板：① …；② …；（确认后由谁实现？建议 <较空闲的 Mac> Codex）`
   - 无 OQ：`<负责人> 需决策：#123 方案 v1 可以实现了，派谁做？（mini Codex / air Codex；建议 <较空闲的 Mac>）`
   `evidence` 写评论链接与 PLAN 路径。退出码按 board-signal 协议处理。

## 不做
- 不写实现代码、不开 PR、不改配置、不部署、不关 issue
- 不直接和负责人讨论；疑问写成 OQ
- 不写进度板

## 验收
- TA-1 issue 上有格式合格的【方案 v1】，时间晚于【跟进】
- TA-2 方案只有六块，大白话
- TA-3 验收草案每条可核验
- TA-4 信号已发（或按退出码如实报告待投递）
