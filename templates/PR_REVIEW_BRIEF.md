# 云 Claude PR 评审派单说明（未应用模板）

> 路径约定：`~/ray-docs` 仅为 helper 默认的参考布局；`YOUR_` 值须由部署者填写，涉及真实主机/出口/凭据的值只留本机私有配置。

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

来源：workflow#14 YOUR_OWNER 定案（历史示例，原记录不随公开包分发）、[lifecycle](../sop/lifecycle.md)。由看板父代理在同回合填全并交付；本文件不派单、不发信号，不授予安装权限。

## 必填身份与范围

- task_id：`<含 issue 号的 tid>`；board：`<板名>`；board_row：`<板标题原文>`；title/goal：`<已有任务信息>`。
- issue：`<已核实 URL>`；PR：`<URL/编号>`；当前完整 head/base：`<SHA>` / `<SHA>`；基准分支：`<branch>`；当前轮次：`<初评/第 N 轮修后复评>`。
- 云主机/工作区/常驻 tab/agent/会话：`<实际身份>`，tab `<tid>-review`，Opus 5.5/high。tab 的存量核验沿用、确认缺失后 launch 和 WAKE 映射按 [lifecycle §5.2](../sop/lifecycle.md#52-评审回应表r3)；只使用已核实的同 issue 常驻身份。
- 精确只读 checkout/代码目标：`<路径及 head/base>`；方案/验收、批准契约、TDD 契约/已有验证证据：`<可读路径>`；历史结论/回应表：`<链接>`；原 Mac Main/worktree/主机与 handoff：`<身份和路径>`。
- 原任务目录名：`<original-task-directory>`；**独立云 PR 信号目录名**：`<original-task-directory>-review`。Mac 信号路径：`<原路径>`；云 PR 信号路径：`~/ray-docs/任务流/<original-task-directory>-review/BOARD_SIGNAL.md`，确认两者不同。
- 任务内 GitHub 结论发布 owner：`<受派 Claude>`；授权引用：`<现有授权>`。仅本任务结论评论和下面一次云本机信号例外；无 Git 写入、代码编辑、GitHub APPROVE、merge/deploy、Page、其他任务或凭据变更权限。若 brief 缺身份/范围/授权，停并报派单方，不猜。

## 执行步骤

1. 先 ACK task/batch、目标/步骤/排除项给派单方。按 [出口纪律](../sop/claude-discipline.md) 使用实际云主机本次 YOUR_PROXY 代理门禁，不能从 Mac/后台 Claude 绕行；出口过关不重放历史 pending。
2. 核对 PR 当前 head/base 与只读代码；完整分页取评论、reviews、inline threads/resolution、YOUR_OWNER 无尾标意见、实际机器人意见及回应表。以批准行为与独立验证证据审当前 diff；保留原编号/链接、严重性、可修部分和依赖 YOUR_OWNER 的部分，不把重复失败当多缺陷。
3. 结论发布前再读 PR head/base；变更则刷新评审目标和证据，不给未审 head 背书。检查已有本轮结果防重复，发布/更新本任务 GitHub 结论，最后一行 `【LLM：<实际身份>】`；写 reviewed head/base、问题/UNKNOWN、证据与限制。只修 P2 且回应表有完整记录不强制全量再审；P0/P1 修后和未审改动需要复评。
4. 读回评论 URL、作者、正文、精确 head/base，确认发布成功后，#24 部署后写本批 DONE handoff（evidence 含结论 URL/head/base），立即驱动云本机脚本，**只由脚本发一次 helper milestone**；旧 reviewer 直接 POST 步骤废止，部署前由 Main 按旧协议兜底，不重复发送。发布失败不伪造完成信号；回报精确原因和 GitHub 现状。信号不宣告门禁 PASS、ready、合并或任务完成。
5. 回报 GitHub URL、审阅身份、发现与信号实际结果给派单方，等待同 issue 下轮 brief；不关闭常驻 tab，不自行发新任务。第三轮修后仍有 P0/P1，由 Bot 问 YOUR_OWNER 继续/改方案/暂停。

## PR 阶段信号（恰好 15 字段）

调用既有 `~/.local/bin/board-signal-post --task <original-task-directory>-review`，通过 stdin 传完整 JSON：

```json
{
  "board": "<板名>",
  "board_row": "<板标题原文>",
  "task_id": "<与 Mac 相同 tid>",
  "title": "<原任务标题>",
  "goal": "<已有目标>",
  "status": "wip",
  "question": "",
  "host": "云电脑",
  "pr": "<PR URL>",
  "event": "milestone",
  "as_of": "<带时区 ISO>",
  "seq": 1,
  "summary": "Claude 评审已贴：要修 N 条 / 要 YOUR_OWNER 定 M 条 / 无阻塞（按实际填）",
  "evidence": "issue: <URL>\nreview: <已验证结论 URL> head=<完整 SHA> base=<完整 SHA>\nresume=bot；由 Bot 下次现有 wake/H2 核全部开发 PR",
  "writer": "<实际 Claude 身份>"
}
```

`seq:1` 仅占位：先核**云端本机此独立路径**的信号 seq 和本机同路径 applied.json 记录，确认不存在按 0，取最大 +1；不可读不当不存在，不借 Mac/别任务路径 seq，不等同步。task_id/board_row 与原任务相同，目录单独不是改任务身份。相同结论/同 head 不因重复 wake 再发新信号；仅退出 4 原样重试例外。同 head 评审去重的有界停止重派由 Bot 按 lifecycle §5.5 判，Claude 不自己重派。

helper [原协议](../sop/board-signal.md) 不变：0=写入+POST 2xx（dry-run 不算投递）；1=未写，修访问；2=无效未写，纠正输入而非原样重试；3=已写、配置不合格，保留并报待投递，不盲重试/自行改凭据；4=已写网络失败，仅保持全部输入含 seq/as_of 相同最多重试一次，再失败停并报待投递。凭据仅本机受保护文件，不写信号/日志/参数。15 字段和现有枚举不变；共享 Bot admission 100/day、每小时 H2（08:00 早报）；授权内聊天提醒全天同回合发送；仅 #24 已批本机五分钟脚本，不增其他 watcher/跨端 relay。Bot 必须重读 GitHub，不以信号为评审/交付/批准证明。

**与设计阶段区分**：同一常驻 tab 的方案交付仍按 [Claude 设计模板](CLAUDE_SNIPPET.md) 和 #10 先贴 issue，再发一次 blocked/blocked/host=云电脑 信号；PR 阶段用上面的独立 review 目录 milestone/wip。共用上下文不混用阶段信号。

#24 四角色、manifest/交接/ACK、持久待推送与一次恢复的操作来源：[看板中心总纲](../sop/cases/local-automation-design.md)。本模板未安装；三机调度、routine 和七天观察另批。
