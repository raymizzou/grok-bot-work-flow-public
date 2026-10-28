# BRIEF — #123 登录超时：实现（Codex）

> 脱敏样例：根据参考实现的真实派单改写，业务内容已替换。文件放在 `<TASK_ROOT>/FEATURE-123-login-timeout/BRIEF_CODEX_IMPL_C1.md`。

## 身份
- 主机：**`YOUR_AIR`**（负责人点名；当时 Air working=0、Mini working=1，属新开实现，可按空闲建议）
- 模型/档位：`YOUR_CODEX_MODEL`，effort=high，service_tier=default（非 fast）
- Herdr：新开 tab `123-login-timeout`；agent `fe123-login-impl-main`
- 仓：`YOUR_GH_OWNER/YOUR_BUSINESS_REPO`；cwd 先 `~/projects/YOUR_BUSINESS_REPO`，实现用**隔离 worktree**
- 基线：开工前 `git fetch`，核对 `origin/main` 最新提交
- 批次：`fe123-C1`；交接文件（绝对路径）：`<TASK_ROOT>/FEATURE-123-login-timeout/handoffs/fe123-C1-fe123-login-impl-main.md`

## 授权（【方案确认】）
负责人在 #123 的回复：<评论链接>（无 `【LLM】` 尾标）

| OQ | 负责人定案 |
| --- | --- |
| OQ1 超时上限 | 改为 5 秒 |
| OQ2 超时后是否自动重试 | 重试 1 次，不再多 |
| OQ3 是否顺带改注册页 | 本票不改 |

方案：issue【方案 v1】<评论链接>；全文 `<TASK_ROOT>/FEATURE-123-login-timeout/PLAN_S10.md`

## 必做
1. 按方案「修复方案」块 + 上表定案实现。
2. 测试：改方案点名的旧测试；新增「超时 5 秒报错」「重试 1 次后报错」「正常登录不受影响」对照。
3. 本地定向测试绿后开 PR，正文链接 #123。
4. 维护一条「评审回应表」PR 评论；Claude 评审意见逐条回应。
5. R1–R4 全满足后发 `blocked` 信号，evidence 含 `ready: pr=#N head=<sha8>`，然后停手。
6. 写 `RESULT_IMPL_C1.md`：PR、head、CI、OQ 对照表；尾标 `【LLM：Codex@air｜<模型>｜effort=high｜fast=否】`。

## 不做
- 不合并、不部署、不关 #123、不切任何线上开关
- 不改注册页；不并其他票
- 不改派到别的机器（同机跑完）

## 交接
- 停手只在三种情况：DONE（全部完成且检查通过）/ BLOCKED（缺权限或需要负责人决定）/ OUT_OF_SCOPE（要扩大范围，先报再做）。
- 范围内新冒出的测试失败继续修，不算 BLOCKED。
- 先写临时同目录文件再 rename；然后发信号通知 Main。

## 首行 ACK
`ACK: #123 login-timeout impl @air. Model is <你的模型>. Batch fe123-C1.`

## 验收
- TA-1 超时 5 秒后报错（测试证据）
- TA-2 自动重试恰好 1 次（测试证据）
- TA-3 正常登录路径测试全绿
- TA-4 PR 上正式 CI 全绿、评审回应表无未处理项
