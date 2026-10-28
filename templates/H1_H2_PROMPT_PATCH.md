# H1/H2 Claude 出口提示词补丁（未安装）

> 路径约定：`~/ray-docs` 仅为 helper 默认的参考布局；`YOUR_` 值须由部署者填写，涉及真实主机/出口/凭据的值只留本机私有配置。

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

依据 workflow#12（历史示例，原记录不随公开包分发）。本文件仅交付文案；本批不执行 UpdateRoutine、不修改线上 prompt、不启动 Claude、不冲历史 pending。
适用对象是现有 **H1「任务流看板唤醒」和 H2「看板兜底」两份 prompt**，不是新 routine。规则来源：[Claude 出口纪律](../sop/claude-discipline.md)、[lifecycle §5.6](../sop/lifecycle.md#56-派续由父代理执行pending_dispatch)。

## Owner 应用与读回

1. 先按 [bootstrap §2](../bootstrap/README.md#2-复制-helper-和-sop) 比较、备份并人工合并 SOP；不能假定三端已同步。
2. owner 在已有授权内分别读回 H1/H2 **完整现有 prompt**，本地带时区备份到 `~/ray-docs/任务流/<task_id>/backups/H1-prompt-before-<带时区时间>.txt` 和 `H2-prompt-before-<带时区时间>.txt`；记录来源、时间和用各自备份回滚的办法。含敏感内容仅本机保存，不入仓、不同步、不贴聊天。
3. 分段安装：仅下方 `【#24 本机恢复 / #17 Bot 兜底入口；…】` 至 `【#24 / #17 兜底入口结束】`（含两端及标记内紧随开头的手工模式说明；不要只取其后的自动化正文）置于 diff_id 去重受理之后、wait 续期/行级短路/任何已有 Claude pending 条件之前；普通 `【Claude 出口检查；…】` 段仍放实际 Claude 派单前，不随入口前移。每份 H1/H2 入口段只一份，若已用 LIFECYCLE_APPEND 则核对替换同一 marker-to-marker 段，不再追加；完整保留两端标记及内部正文/字面占位符，text 围栏仅作展示。清除旧空 pending/无 open PR/Mac Main working 即跳过云扫描、guard-only/无限恢复及冲突直连 gate 的 operative 文字。
4. 本批不改线上 routine；另批按 #24 部署每小时 H2/共享100/day，本机脚本主恢复、Bot 同一预算兜底。保持其他授权、安全门禁、wrapper/no replay/一次 ACK，聊天提醒全天。PR#23 源码已合入 main21301ba，不等于本模板已应用。
5. 修改后逐份读回 H1/H2 完整 prompt 与备份比较：入口段恰好一份且先于等待短路、普通出口段仍派单前；无 pending 也可达扫描、零动作留覆盖/缺口、父消费当前 wake 条目并逐项执行/未执行原因及身份/ACK 回执。核无新 gate 冲突后，走 [T1–T7](../sop/cases/claude-egress.md) 与 [恢复用例](../sop/cases/claude-auto-resume.md)。纸面 PASS/源码合入不证明真实 routine 或出口成功。

## 共同可粘贴内容（两段分放，H1/H2 各一份）

```text
【#24 本机恢复 / #17 Bot 兜底入口；旧演员、guard-only、每 occurrence 重启和三次/30 次条文废止】
公开模板默认使用手工交接和现有 board-signal-post：未另行提供、核验并授权安装本机 runner 时，不执行下面自动恢复/manifest 驱动步骤；Main 核实本批交接后按原 15 字段协议发本机信号，Bot 继续核验 GitHub/Herdr。脚本缺失不产生人工恢复、重派或绕过守卫的权限。
先读 ~/ray-docs/YOUR_COORDINATOR/sop/lifecycle.md §5.5/§5.6、同目录 claude-discipline.md 和 cases/local-automation-design.md；四角色为 Bot 独读写 Page，本机脚本只推信号/恢复，Claude/Codex 交付，YOUR_OWNER 答板上问句。
每个按原 diff_id 去重后受理的 H1、每次 H2，先做一次实际云候选发现，再续期 wait、行级短路或结束 wake；重复 H1 不增扫描/唤醒。初始 pending_dispatch=[]、触发行无关、无 open PR、跟进主机 Mini/Air、Mac Main working、整行非 STOPPED 或 F PR 已 MERGED，均不跳过同任务云 Claude；发现不产生新恢复资格。
依当前 CLI help 核实际云主机当前默认 Herdr session 与真实 agent/tab/pane inventory；名字消失用可证实原任务映射和现场交叉核，不借旧 herdr437/猜 ID。零动作也在现有 WAKE_/FALLBACK_ 记时间/主机/session、inventory 覆盖缺口、逐候选处置及空 pending 原因；不可读/缺证据为 UNKNOWN，不当零 eligible，不造 registry/cursor 或 helper 字段。
#24 资格是当前原授权 active 任务无本批交接，精确原 task/tab/pane/name/session/model/effort/worktree，完整原生命令/handle 与后代进程无在途证明；前台 shell/interactive_ready 单独不够，stdout 不作完成证明。blocked/DONE（含已交付故意杀试跑）、preserve/do-not-resume、暂停/撤单、live/未知命令或歧义不恢复。
具体声称 guard kill 时，依 lifecycle 核实际云 YOUR_GUARD_ALERT_LOG，精确杀线 已立刻停掉所有 Claude 任务，北京时间 UTC+08:00；实际原行/主机/来源/观察时间留证。归属须唯一既有主 transcript ~/.claude/projects/*/<session>.jsonl（不用 subagent/PID 文件）的当前 mtime 与告警源时区归一、带符号 Δ=t_mtime-t_alert 在已批“数秒内 / a few seconds”，匹配后无更晚写入且动作前重读未变，同原 pane bash 的精确 session hint 三项 AND；缺失/多值/精度不明/后写/不符均 UNKNOWN，不扩为分钟或猜时间。归属不替代任务资格；一般 #24 缺交接路径不需编造 kill 原因，只有独立资格全齐才按通用提醒核验，不把 UNKNOWN kill 时间填入提醒。
本机脚本为主，Bot 只对确认漏报兜底；先核本机同一 batch/session 恢复意图/结果/ACK 宽限和预算，已有 pending/started/failed、已耗预算或未知在途就不再 queue/start/prompt。新 kill/head 不重置一次预算，不能与脚本竞争或回放历史 pending；无法核清只报 UNKNOWN/按既有规则承接。父代理优先驱动同一 runner/锁/记录，不另开人工恢复额度。
资格齐才排本 wake 既有 kind=resume，带原目标/brief/授权与预算依据；父动作前重核交付/保留指令/身份/无在途。Claude 本次实际云 curl -s -m 8 -x YOUR_PROXY YOUR_IP_ECHO_URL 必须 exit0 且 trim 仅YOUR_EGRESS_IP，保留 wrapper 再验；错/UNKNOWN 出口等下轮，不直连、不与 guard 对打。shell 先原 pane/name/session/model/effort start，绝不往 shell 发话；readback 已新 working 不再 prompt，busy/unknown 不 prompt；仅原身份 idle/done+ready 且命令证明完整才 lifecycle 的固定通用提醒。
恢复只核一次十分钟内编号 ACK/新 working；失败读 pane 一次记因并问 YOUR_OWNER，不盲重启。普通派单十分钟 unconfirmed、下一 wake 重推一次、第二次失败才问是投递规则，不能借它再启恢复。父结束 wake/刷新板前逐项对账 dispatch_applied_at、实际 start/prompt/身份/ACK/续写或精确未执行原因；无动作亦审计，缺回执标未证实，不造 applied 时间，CLI accepted/pending/旧 waiting 不算成功。
分层记录事件已观察（如有）、候选资格、本次出口、排队、父执行、原身份 ACK/续写，各有来源/时间或 UNKNOWN。仅事件未观察才写等自然 guard；已见告警但归属/资格/续跑未明，写告警已见、受影响会话/续跑待核。没有 wake 的调度等待与已有 wake 漏扫描/执行分开，缺日志不证明未执行；本批不加告警触发/daemon/hooks。
三入口为本机脚本、云 GitHub 新动静、每小时 H2；08:00 保留早报，共享 Bot admission100/day 含 H2，超限保留待办并早报/H2报告。入口云候选发现独立于一般板行健康检查；后者只核 wip 上次更新超一小时的行，并核有 wip 却一小时无推送的主机脚本/睡眠/可达性。不是各机各100次，不增跨机 relay。
Bot 在板行持久保留待推送内容/编号/目标/时间/派前 seq/attempt；本机 Main 原子刷新 manifest，只有当前 task/batch/编号 ACK 或派前 seq 后新 working 才收据，旧 ACK/working 不算。每次停手写本批 handoff 并驱动脚本，worker 只交 Main；正常 DONE 发 milestone/wip，需 YOUR_OWNER 答实际问题才 BLOCKED。问题同次 wake 保留选项/推荐/停点，夜间也提醒，不能擅自关单。
PR#23 已合入 main21301ba；历史父辅助续写不等于自然 H1/H2 或#24 live PASS，原证据不得抹去。另批才安装三机脚本/定时与线上H1/H2，当前不改线上频率/个人配置/guard/wrapper。#2 已并入关闭，#24 AC-6七天未跑不算PASS。合并/部署/实盘权限仍独立。
【#24 / #17 兜底入口结束】
```

以下普通出口段保持在实际 Claude 派单前：

```text
公开模板默认使用手工交接和现有 board-signal-post：未另行提供、核验并授权安装本机 runner 时，不执行下面自动恢复/manifest 驱动步骤；Main 核实本批交接后按原 15 字段协议发本机信号，Bot 继续核验 GitHub/Herdr。脚本缺失不产生人工恢复、重派或绕过守卫的权限。
【Claude 出口检查；本段优先于本 prompt 中旧的出口判定文字】
本段保持出口门禁；#24 的频率/预算另按共同覆盖块部署，不改变其他授权和安全边界。
H1/H2 子代理发现不依赖已有 pending，合格才排本次条目并由父代理按 lifecycle §5.6 消费/核对；板行持久 pending 与执行回执要求不变。
涉及 Claude 时先读 ~/ray-docs/YOUR_COORDINATOR/sop/claude-discipline.md。
Claude 只在云电脑 Herdr 运行。在本次派单前核实将实际运行 Claude 的云主机，必须在该主机执行唯一出口检查命令：
curl -s -m 8 -x YOUR_PROXY YOUR_IP_ECHO_URL
仅 curl 退出码为 0，且输出去掉首尾空白后为单个 IP、整串恰等于 YOUR_EGRESS_IP，才记 egress_ok。
代理 IP 不同、输出为空/格式错误/多值、超时、连接失败或其他非零退出码，一律记本次出口门禁 blocked_now；不派该次 Claude。
无法核实实际云主机、只有 Mini/Air 本机结果、只有旧结果或没有可验证的本次云端观测，也记 blocked_now（出口未核验）；保留 UNKNOWN，不补造成功记录。
直连公网 IP YOUR_DIRECT_IP 正常，与 Claude 出口无关。任何直连 IP（即使为 YOUR_EGRESS_IP）都不得作闸门，也不得在代理失败时改用直连重试来放行。
在本次 WAKE_/FALLBACK_ 或派单证据中记录核实的主机、带时区时间、完整代理命令、curl 退出码、代理结果或脱敏短错误；直连诊断可选，必须标不参与门禁，不覆盖代理结果，不记录秘密。
egress_ok 只清除出口检查，本身不授权任意 launch/resume/replay；仅入口 #24 / #17 全部资格核验满足可续已批无交接原会话，不覆盖其他门禁失败；仍逐项核既有授权、容量与安全约束，不凭出口结果自动派单。
代理恢复不自动清空、冲刷或重放历史 pending_dispatch；只处理当前任务已有授权及本次核验，不凭出口恢复产生新授权。
blocked_now 是本次出口门禁结果，不是新增板状态；首次失败不自动改板 blocked；同 PR 连续第二次 wake 派不出评审时按 lifecycle §5.2 转 D 问 YOUR_OWNER，成功实际派出重置。仍按 lifecycle 与 SOP 判断，只有卡目标且必须等 YOUR_OWNER 决策才发 blocked 和普通聊天问句。
保持 pending_dispatch 六种 kind 与父代理执行；普通派单十分钟未确认先读 pane 一次并保留板行 pending/unconfirmed，下一 wake 重推一次，第二次失败才问 YOUR_OWNER；旧首次未 ACK 即问规定废止。故障恢复另按 #24 一次预算，失败不重启。去重键 (row, kind, 依据) 的 10 分钟宽限、同 PR head 去重（一般 review 仅 lifecycle §5.5 确认停且无在途命令时一次同 tab 重派例外）及 X19 专用去重保留；#24 原会话恢复按当前 batch/session 一次预算去重，决策不能漏派独立可修项。
按 #14 已批 PR 评审/复评、修评审、解冲突、补完成声明 24h 实际派；其他按已有授权。授权内通知和聊天提醒全天同回合发送，包括 YOUR_OWNER 问题与合并请求，不将提醒或已批 PR 下一手排到 08:00；H1/H2 共用原有提醒去重。
不得修改或削弱 ~/.local/bin/claude wrapper、YOUR_GUARD_SCRIPT；不启动历史派单或未授权 Claude，不改变其他安全门禁。

【Claude 出口检查结束】
```

本补丁的出口判据不变；#14 常驻 issue review tab、24h 回派、连续失败升级与 H1 移除整段旧 `arch_review_dispatch.py scan`（issue 与 PR 扫描）的完整应用/备份/回滚要求见 [共同追加稿](H1_H2_LIFECYCLE_APPEND.md)。不以旧 issue dispatcher 绕过看板/tab。

## 本批交付状态

只完成文案与纸面检查。H1/H2 是否已安装、分别读回、真实云端观测及 routine 实际运行均 **UNKNOWN / 本批未验证**；没有实际 routine ID，不得据本文声称线上生效。
