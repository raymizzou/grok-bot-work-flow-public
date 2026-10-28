# 可合并的 Claude 指令片段（模板）

> 路径约定：`~/ray-docs` 仅为 helper 默认的参考布局；`YOUR_` 值须由部署者填写，涉及真实主机/出口/凭据的值只留本机私有配置。

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

备份并人工合并至 ~/.claude/CLAUDE.md，保留已有 Superpowers 插件/skill 禁用规则；不覆盖原配置。

> 进度板/wake 工作先读 ~/ray-docs/YOUR_COORDINATOR/sop/bot-global-rules.md、board-state-machine.md、board-signal.md；设计/评审生命周期再读同目录 lifecycle.md。
> Claude 派单出口另读同目录 claude-discipline.md：只认实际云主机 YOUR_PROXY 代理结果，直连 IP 不得作闸门；出口通过不替代其他授权或自动重放历史 pending。
> Claude 负责评审/设计，Codex 实现，owner Bot 管板。受派设计任务内的 issue 方案评论/单次设计信号，以及受派 PR 评审的结论/单次 PR 信号是已批准的外部写入例外；本片段不授权新代理或其他外部动作，Claude 不写 Page。
> 评审结论保留已核对代码身份、已知问题与 UNKNOWN；问题用正常聊天文字。

这是供新部署者使用的指针模板；不声称读过或修改了本机个人配置。

> 新任务只在 YOUR_OWNER 说跟进后由 Bot 派设计；brief 必须给出精确 board_row（逐字等于板行标题）、task_id（含 issue 号并匹配 Herdr 前缀）、board 与 issue 链接、YOUR_OWNER 原话、旧方案/修改意见。只设计/评审，方案含 G1 初判、验收草案、≤5 OQ，由 Bot 转述与回传修改，不直接和 YOUR_OWNER 讨论。
> **先发 issue 方案评论，再发信号。** 安装前已交付旧格式按 [lifecycle §5.7](../sop/lifecycle.md#57-存量票迁移一次性仅在-f-执行) 由 Bot 迁移，不要求 Claude 重贴；以下新格式只管安装后新版。评论第一行 `【方案 vN】#M <标题>`，正文可为摘要并给出 `PLAN_S10*.md` 全文路径；结尾写 `Open Question：k 条` 或 `无 Open Question`，最后一行为 `【LLM：Claude@云电脑…】` 实际身份尾标。评论时间须严格晚于 issue 最近【跟进】/【跟进修改】；本地 PLAN 文件单独不证明交付。YOUR_OWNER 修改后旧交付/确认不能用于本轮，Bot 先记【跟进修改】再回派，新版按相同格式交付。
> #24 部署后，每版发布并核实评论链接后，在云电脑本机写本批 BLOCKED handoff 并立即驱动本机脚本（含评论 URL/PLAN 的 evidence）；旧 Claude 直接 POST 完成信号步骤废止，以下是脚本使用的 helper 协议及部署前 Main 兜底说明，不重复发送。原 helper 为 `~/.local/bin/board-signal-post --task <task_id>` 发一次完成信号（workflow#10 OQ1=A）。保持现有恰好 15 字段：`board, board_row, task_id, title, goal, status, question, host, pr, event, as_of, seq, summary, evidence, writer`；取 brief 的精确板身份，`status=blocked,event=blocked,host=云电脑`，`pr` 填 issue URL，summary 短句写方案已出，evidence 写已核实评论 URL 和 PLAN 路径（若有），writer 写实际身份。先核本机已有 BOARD_SIGNAL 和本机可读的 `~/ray-docs/任务流/board-wake/applied.json`，只取同一信号路径的已应用 seq，`seq=max(本机信号 seq, 本机同路径已应用 seq)+1`（确认不存在的记录按 0）。不得借用其他任务/路径的 seq；无法读取不等于不存在，不猜值、不跨端读或等同步，交付仍由 H2 读 issue 兜底。本机记录同步落后或两端同时发送仍可能撞 seq，此规则不保证消除竞态，被忽略的信号同样由 H2 兜底。as_of 带时区；保留原协议备份与秘密边界。不引入字段/状态/跨端 relay；#24 本机定时脚本按总纲执行，不等待文件同步，计入 Bot 共享每日 100 次 admission（含每小时 H2）。
> question 是草稿：有 OQ 用 `YOUR_OWNER 需决策：#M 方案 vN 请拍板：① …；② …；（确认方案与验收后由谁实现？建议 <空闲的机器> Codex）`，无 OQ 用 `YOUR_OWNER 需决策：#M 方案 vN 可以实现了，派谁做？（mini Codex / air Codex；建议 <空闲的机器>）`。容量仅建议，不猜人选。信号只叫醒 Bot；Bot 必须重读 issue 核验新交付，即使 Claude tab 仍 working 也进 B2 blocked。最新方案/G2 验收确认且 YOUR_OWNER 明确点名机器/agent 后才能派实现；只答 OQ 未点名仍 blocked，只问剩余派谁，未明确确认的门禁保留，不从「行」「可以」猜授权。无 P0/P1 不自动放行。
> 信号退出码严格按 [board-signal](../sop/board-signal.md)：0 为写入且 POST 2xx（dry-run 只写，不算投递）；4 才允许保持**全部输入相同（含 seq/as_of）**最多重试一次，仍失败停手报告待投递；3 保留信号并报告本机配置缺失/不合格，不盲重试或自行扩大凭据修改；1 修复写入访问后按原协议处理，2 修正无效输入、不原样重试。不得把所有错误统一重试。凭据只用本机受保护文件，绝不写信号/日志。没收到信号由现有 H2 读 issue 兜底；本片段不授权安装或真实试跑。
> 全天照常发该单次信号，Bot 同次唤醒发 ≤200 字授权内聊天提醒（含 YOUR_OWNER 问题和合并请求），夜间不延到早报。Bot 以同一行+方案版本在现有 WAKE_/FALLBACK_ 记录去重（夜间与早报共用），H1/H2 不重复提醒，只有新版重新提醒。

与 [生命周期追加稿](LIFECYCLE_AGENTS_APPEND.md) 一起由 owner 人工核对；不表示三端指令已同步。

[Claude 出口纪律](../sop/claude-discipline.md) 是 workflow#12 新增限定补充；已有安装副本如含其他纪律，须备份后只合并本补充，不能整份覆盖。

> #14：受派 PR 评审前必须读 [lifecycle §5.2 PR 闭环](../sop/lifecycle.md#52-评审回应表r3)，并按其中引用的 §5.5/§5.6/§6 及派单模板执行；具体身份、发布权限和信号字段由 brief 给全。

#24 四角色、manifest/交接/ACK、持久待推送与一次恢复的操作来源：[看板中心总纲](../sop/cases/local-automation-design.md)。本模板未安装；三机调度、routine 和七天观察另批。

## #24 停手前交接（未安装）

执行端每次停手前按 [#24 总纲](../sop/cases/local-automation-design.md) 原子写当前 task/batch 的 DONE/BLOCKED/OUT_OF_SCOPE JSON handoff，默认由 Main 核实交接后按原 helper 协议发本机信号；只有另行提供、核验并授权安装 runner 后，才驱动同一 manifest 的可选本机观察。贴出需要 YOUR_OWNER 回答的问题就写 BLOCKED，保留问句；不能以 working/旧等待掩盖。worker 只原子交给 Main，由 Main 驱动脚本，不越 brief POST；部署前仍由 Main 用原 helper。只有 Bot 读写 Page，合并/部署/生产仍需明确授权，保留 Superpowers 禁用规则。
