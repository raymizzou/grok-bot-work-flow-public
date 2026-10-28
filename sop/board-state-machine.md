# 当前进度板状态机（2026-10-26 版文档）

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

操作入口为 [新版 SOP](bot-progress-board-sop_2026-10-26.md) 与 [生命周期 A–G](lifecycle.md)，依据 workflow#3 的 OQ1–OQ5=A（历史示例，原记录不随公开包分发）。本仓交付不证明 routine/三端已激活。

## #24 操作入口（未部署）

四角色、三种唤醒、每小时 H2、共享 Bot 每日 100 次 admission、持久待推送/编号收据与本机一次恢复，统一见 [#24 总纲](cases/local-automation-design.md)。旧 30/day、三次 H2 和禁止本机定时恢复的冲突补丁废止。执行端停手前写当前批交接并立即驱动脚本；worker 只交 Main；只有 Bot 读写 Page。

## 身份与可观察状态

任务 ID 含 GitHub issue 号；tab/agent 为 `<task_id>-<role>`。信号 task_id 与命名前缀一致，board_row 与板任务标题逐字相同。
匹配任务且 agent_status=working 才证明当前活跃；≤10 分钟 launch 宽限或实际核验的等待声明可维持相应阶段，不能用旧信号、idle 或未验证的云 E4 冒称 working。
Main 与全部 worker（含 investigator/design）idle/done，无 §5.5 合法等待且已过派单宽限 → 当次按 [lifecycle §5.5 / §7](lifecycle.md#55-stopped合法等待与无人跟进) 的 STOPPED/X19 推进，不能只凭 wait 声明保留 wip。S 非空、无 working 但非 STOPPED 时，按同节一次观察兜底；已确认停在输入/权限等卡点且无在途命令、无合法等待才走 X19，无法核验则显式标记并早报，保留在途命令，不盲派。
idle/done 不代表任务完成；wip→todo 需 YOUR_OWNER 明确同意。B1/C/F 无人跟进要当回合实际派续（按已有授权），派不了且需 YOUR_OWNER 决定 → D，不能只保留无 owner 的 wip。

Page 仍为 todo/wip/blocked/finished；helper 仅收 wip/blocked/finished，15 字段不变。helper 不替调用方验证 issue/门禁；CI_WATCH OQ 尚待另批，不能推断已授权自动接手。

## 阶段与完成

- todo 只等 YOUR_OWNER 说跟进，早报列出，不自治派活；跟进同回合开/补 issue、记录、派 Claude 设计并刷板。
- B2 安装前已交付的旧格式先按 [lifecycle §5.7](lifecycle.md#57-存量票迁移一次性仅在-f-执行) 迁移，保持有效 B2，不因格式回 B1/X19/重派；安装后新版才按下述严格格式。先按 [lifecycle §2](lifecycle.md#2-阶段表与板面-bullet) 核 issue 评论：首行 `【方案 vN】#M <标题>`、结尾 OQ 数量/无 OQ、最后 Claude@云电脑 LLM 尾标，时间严格晚于最近【跟进】/【跟进修改】。PLAN 文件单独不算交付；有效交付即 blocked，优先于 working tab 或旧 plan/review wait。YOUR_OWNER 改方案先记录【跟进修改】回派，旧交付/确认不再用于本轮。有 OQ 逐项问拍板并问派谁，无 OQ 问派谁；最新方案/G2 验收确认和 YOUR_OWNER 明确指定机器/agent 齐才派实现。只答 OQ 未点名仍 blocked，只问剩余派谁，不从「行」「可以」猜；#421 容量仅建议。G1–G4 完整定义见新版 SOP §3，无 P0/P1 不绕过确认。
- Claude 每版 issue 交付后只在云电脑本机发一次 blocked 信号唤醒，Bot 重读 issue 再改板，只有 Bot 写板。H1/H2 共用同一行+版本去重，全天同次唤醒 ≤200 字提醒一次，夜间也发送；后续 wake/H2/早报不重复同版。缺信号或日上限耗尽由现有 H2 兜底，15 字段/状态不变，共享 Bot 日上限为 100；安装与真实验收另批。
- C 核 CI 与评审回应表；R1–R4（完成声明、当前 head CI、评审处理、可合并且合并前验收齐）全部成立，当次进 E blocked 等合并批准。所有合默认分支 PR 适用；结构性缺项按 lifecycle §5.8 / X16b 走 D 合批例外，不能算 E ready。E/D 例外批准均绑定该 PR/head，新提交使批准失效，F 的 main CI 门禁不变。
- 纯等尚未兑现的 CI/review/市场/Claude 且符合 V1–V3 不是 blocked；B2 已交付不能再等同一方案。问句必须是卡目标且要 YOUR_OWNER 决策，写 `YOUR_OWNER 需决策：…？`。全停等待按 lifecycle §5.5 核 V1–V3，idle/done 恢复方按 resume=bot 被动等待，本次读回 V1 仍真才续期到下个 H2，旧 next_check 过期本身不使被动等待失效；写清 Bot 最迟下个 H2 核，idle 前发 milestone。合并门禁缺口可按 §5.8 提 D 合批例外，其他 R 项合法等待未兑现先等；不相关 G1–G4 立即 D。
- F 逐条验收，全 PASS 发 event=done/status=wip。执行端不关 issue，Bot 按 C1–C6 关单，下一扫描 CLOSED 且验收齐/偏差已接受才 finished；其他阶段完成只发 milestone。
- 原验收内 FAIL 保留原票回 C 新 batch；范围外才 follow-up 入 A，父票自身 C1–C6 仍须成立。无批准已合并不自动 revert，CLOSED 验收不齐问 YOUR_OWNER，不伪称完成。

每次扫描按 lifecycle §3 重推导，按 §7 X14–X19 纠偏并写证据。板面短 bullet；AS_OF 带时区，技术细节进 evidence。

## #14 PR 评审闭环与诚实板面

PR 发布、评审与修复回派前必须读 [lifecycle §5.2 PR 闭环](lifecycle.md#52-评审回应表r3)，并按其中引用的 §5.5/§5.6/§6 执行；下列仅为板面示例。

- `执行端已停；Bot 已派 <谁> 做 <什么>（时间）`
- `执行端已停；等 Claude 评审 PR#N（已派 <时间>，Bot 最迟 <下个 H2> 核）`：须本 head 已实际派、GitHub 尚无该次结论；不是按日志猜 working。
- blocked + `❓ YOUR_OWNER 需决策：<可直接回答的问题>？`

首次派评审失败另写真话「评审派不出：<原因>；下次唤醒再试」，不冒称在审或 working。
