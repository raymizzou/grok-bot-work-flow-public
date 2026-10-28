# H1/H2 生命周期追加稿（未安装）

> 路径约定：`~/ray-docs` 仅为 helper 默认的参考布局；`YOUR_` 值须由部署者填写，涉及真实主机/出口/凭据的值只留本机私有配置。

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

用于**现有**「任务流看板唤醒」H1 与「任务流看板兜底」H2 的共同扫描步骤；不是新 routine，不提供平台载荷。
父代理/owner 负责实际编辑，先把平台读回的**完整原始 prompt**（不是摘要）保存为
`~/ray-docs/任务流/<task_id>/backups/H1-prompt-before-<带时区时间>.txt`、`H2-prompt-before-<带时区时间>.txt`，记录读回时间、来源及回滚办法；原 prompt 如含敏感配置，仅本机保管，不入仓或同步。
本批 #14 仅仓内文档；owner 另获安装授权后，从 H1 完整 prompt 移除整段 `arch_review_dispatch.py scan` 调用（issue 和 PR 扫描全部移除），不保留独立旧扫描绕过看板和常驻 tab；不修改仓内/安装脚本，不声称 live 已停。应用时核对下文覆盖的旧夜间排队/聊天静默、逐 PR 临时 tab 和 X19 短路文案，逐条移除或标废；保留备份及逐份回滚办法。
本文不表示备份或 routine 修改已经发生。追加后读回全文与备份比较，单独验证 H1/H2，不自动启动新调度。

来源：workflow#3（历史示例，原记录不随公开包分发）、OQ1–OQ5=A（历史示例，原记录不随公开包分发）。
仓内权威：[新版 SOP](../sop/bot-progress-board-sop_2026-10-26.md)、[lifecycle](../sop/lifecycle.md)。
预期安装路径：`~/ray-docs/YOUR_COORDINATOR/sop/bot-progress-board-sop_2026-10-26.md`、同目录 `lifecycle.md`、`claude-discipline.md`、`board-state-machine.md`、`board-signal.md`。父代理先复制核对，路径存在不等于规则已激活。

分段应用：下方 `#24 / #17 兜底入口` 的完整 marker-to-marker 段（含两端及标记内紧随开头的手工模式说明；不要只取其后的自动化正文）须在原 diff_id 去重受理之后、任何 wait 续期/行级短路/“pending 为空就结束”之前；不是等已有 Claude pending 才扫描。普通阶段正文仍在原阶段推导位置，普通 Claude 出口检查另在实际派单前。H1/H2 各只保留一份入口段；与 [出口补丁](H1_H2_PROMPT_PATCH.md) 来源重复时替换同一段，不追加第二份。父代理回执/零动作审计须可达，完整保留两端标记及内部正文与占位符，text 围栏仅作展示；本批仅交付安装说明。

---

每次醒来先读已安装的新版 SOP 与 lifecycle；只按可读事实推导 A–G，板状态仍只有 todo/wip/blocked/finished，不存阶段文件、不加 helper 字段；#24 本机定时脚本与运行去重记录为已批例外。owner Bot 独写自己的 Page，执行端只发信号。原事件去重/seq 与共享 Bot 每日 100 次 admission；H2 每小时，08:00 早报，旧三次 H2/暂停自检条文废止。

本段覆盖基底「不要派 Codex/Claude」的限制：H1/H2 子代理只产出 `pending_dispatch`，由父代理按 lifecycle §5.6 在同回合执行。存量行迁移前缺标记时，按 §5.7 保持原状态并标「待迁移」，不得据此推为 A todo。

每次唤醒对**所有开发阶段 PR**（包括非触发行）逐个收集 issue 状态、PR 当前 head/base/mergeable/CI、issue/PR 评论与评审线程（完整分页、含 resolution）、最新执行端信号及匹配 task_id 的 Herdr。task_id 含 issue 号，tab/agent 用 `<tid>-<role>`。证据冲突按 YOUR_OWNER 明示 > GitHub issue 状态读回 > 最新执行端信号 > Herdr 推断；不能把旧信号当当前 working。`-review` 目录信号只叫醒，不是执行端信号，不参与 R1、冲突优先级或跟进方/跟进主机；seq 仅与同一路径信号及 applied.json 记录比较。同 task_id/board_row 不合并序列，Mac ready seq=5 不受稍后云 review milestone seq=99 覆盖；每路独立去重。

1. YOUR_OWNER 明确取消：留取消记录后 finished。否则 issue CLOSED 且验收全勾/有明确偏差接受才 finished；CLOSED 验收不齐走 X18。无 issue 为 A todo，除非 YOUR_OWNER 已说跟进，才先开/补 issue、写记录并继续。todo 允许无人；仅 YOUR_OWNER 明确「跟进」可启动，08:00 早报列待跟进项，由 YOUR_OWNER 挑，取消自治派 todo。
2. 无【跟进】记录 → A todo。有跟进、本轮尚未同时满足最新方案确认+G2 验收签认+YOUR_OWNER 明确指定实现端：**先核 issue 交付**；安装前已交付的旧格式先按 [lifecycle §5.7](../sop/lifecycle.md#57-存量票迁移一次性仅在-f-执行) 迁移，保持有效 B2，不因格式回 B1/X19/重派；安装后新版才用下述格式。Claude 评论第一行 `【方案 vN】#M <标题>`，结尾 `Open Question：k 条` / `无 Open Question`，最后 Claude@云电脑 LLM 尾标，评论时间严格晚于最近【跟进】/【跟进修改】。摘要可附 `PLAN_S10*.md` 路径，PLAN 文件或信号单独不算交付。有效交付立即 B2 blocked，即使 常驻 review tab 仍 working/旧 wait 称等方案或评审。有 OQ 问 `YOUR_OWNER 需决策：#M 方案 vN 请拍板：① …；② …；（确认方案与验收后由谁实现？建议 <空闲的机器> Codex）`；无 OQ 问 `YOUR_OWNER 需决策：#M 方案 vN 可以实现了，派谁做？（mini Codex / air Codex；建议 <空闲的机器>）`。只答 OQ 未点名仍 blocked，只问剩余派谁；未明确确认的方案/验收门禁保留，不从「行」「可以」猜授权或人选。#421 容量仅给建议。YOUR_OWNER 提修改先同回合记【跟进修改】并原话回派 B1，旧版交付/确认失效，新评论须晚于该记录；无有效交付再核实际 working/等待，未回派走 X14。YOUR_OWNER 首次说跟进的同一回合，必须开/补 issue、写【跟进】、由看板派云电脑常驻 `<tid>-review` Claude Opus 5.5/high（同 issue 方案/代码共用，issue CLOSED 前不关）、刷板；brief 带精确 board_row/task_id/issue、原话与修改意见，方案只设计，含 G1 初判、验收草案、≤5 OQ，按 [Claude 模板](CLAUDE_SNIPPET.md) 在 issue 交付后云端本机发一次信号。Bot 转述与回传原话，Claude 不直接和 YOUR_OWNER 讨论。
3. 最新方案有【方案确认】且 G2 验收签认，**YOUR_OWNER 已明确点名实现机器/agent**，无有效【合并批准】：按 YOUR_OWNER 指定派实现，不自治选 idle Mac；逐项核 R1–R4。R1 执行端最新 status=blocked/event=blocked、合并问句与 `ready: pr=#N head=<sha8>`；R2 ready 与当前 head 一致且该 head 必需 CI 全 success（保护规则待核，无保护按全部检查，无 run/未知不算 PASS）；R3 全部评审有回应结论，P0/P1 已修并经 Claude 修后复核，拒改/转出 P0/P1 或 YOUR_OWNER 意见须其明确批准，范围内转出须 G2；R4 PR=MERGEABLE 且方案标「合并前」项已勾，未标项均合并后验。全齐 → E blocked；否则核实际跟进，按 lifecycle §7 X16a/b 与 X19 分流，不能一律回 C。结构性缺项由执行端 gap 声明，按 §5.8 提 D 合批例外，缺项不算 PASS。不能仅凭 CI 绿或“开发完”进 E。
4. 有效【合并批准】必须是 YOUR_OWNER 对具体 E 或 lifecycle §5.8 D 合批例外问句的明确回复，D 例外还记【门禁例外：点名门禁，理由，原话链接】，只限该 PR/head；记录批准时 head，等于当前 PR head 或实际合并的 PR head；任何新提交使旧批准失效，回 C 重判。最新 F 回报有原验收范围内未解决 FAIL 时优先按 OQ5 回 C、原票 OPEN、新 batch，修复/重验或 YOUR_OWNER 接受偏差前不按旧批准回 F；否则批准且 issue OPEN → F，派已授权执行端合并→等准确 main SHA CI→在授权范围部署→逐项验收。优先原 `<tid>-impl-main`；需新接手时先核现有授权，不能援引待批 CI_WATCH OQ 自动新开 main2。已 MERGED 却无批准走 X17，不自动 revert 或继续部署。
5. 任意未答 G1–G4/卡目标且必须等 YOUR_OWNER 的问句 → D blocked（B2/E 保留本阶段），覆盖板阶段；先按下述 PR 闭环派独立授权内修复，再问决策，不能因 D 短路漏派；仅合并门禁缺口与其他 R 项合法等待并存先按 lifecycle §7 等该项，不相关 G1–G4 立即 D。G1 架构，G2 验收，G3 中途架构，G4 专属授权/所有默认分支合并/main CI 红等，细则读 SOP §3。纯等尚未兑现的 CI/review/市场且合法等待不是 blocked。YOUR_OWNER 回复须同回合在 issue 记【跟进】/【跟进修改】/【方案确认】/【合并批准】/【偏差接受】，引用原话、聊天时间与链接，明确点名实现端也须留痕，再在门禁齐备时实际续派、改板；只答 OQ 不作实现指派。无尾标 YOUR_GH_OWNER 评论算 YOUR_OWNER，bot 评论必须尾标【LLM：…】。含糊授权再问，不猜。
6. B1/C/F 按 [lifecycle §5.5](../sop/lifecycle.md#55-stopped合法等待与无人跟进) 核 STOPPED（S 非空、匹配 tid 的全部成员 idle/done 或现场确认已停、派单宽限已过；退出名字缺失先查 tab/pane 映射，详见下方 #24 块）和 V1–V3。先将 idle/done 恢复方按 bot；working 真盯的 next_check 须未过，resume=bot 本次读回同一当前 head 对象、V1 仍真就续到下一现有 H2，旧 next_check 过期本身不作失效依据；V1 假或 UNKNOWN 不续期。被动等待 bullet 必须写执行端已停、等什么、Bot 最迟下一个 H2 核，不能写 Main 继续监控。只有 working、有效宽限或合法等待算在跟。CI_WATCH OQ 仍待另批，云 E4 working 检测未验证，不当作已核验 working；本机无交接恢复按下方 #24 块，#17 仅保留 Bot 兜底；不启用其他候选自动化。普通派单十分钟无 ACK/新 working 先读 pane 一次并记未确认，保留板行 pending，下次 wake 重推一次，第二次失败才问 YOUR_OWNER；旧首次无确认即问规定废止。故障恢复失败另按 #24 一次预算，不能借此再启。读不到主机保持原状标无法核验，不强行 SSH，不重复启动未核明工作。S 为空执行 X14；S 非空、无 working 但非 STOPPED 且宽限已过时，按同节只读相关 pane 一次，确认停在输入/权限等卡点且无在途命令、无合法等待才 X19；在途命令或不明/不可读状态保持原状、显式标无法核验并早报，保留命令、不盲续派/重启。STOPPED 且无合法等待当次 X19，必须有下一手/决策，不能被动保留旧等评审/CI bullet，也不能自动降 todo。
7. R3 收集所有 inline、Claude、YOUR_OWNER 和实际启用机器人意见；每条对应回应表行（链接、严重性、已修提交/不改理由/follow-up）。P2 可不改+理由，无须清零；最后评审后无对应行的新提交需再评审。Bot 不代写 ready、不代判开发完成。执行端 E 停手，无有效 head-bound 合并批准不得合并。
8. F 验收只按 Codex 在 issue 的逐项 PASS/FAIL 回报及可打开证据勾选，并核 `accept:` 行；全 PASS 信号 event=done/status=wip，执行端不关单。Bot 只有 C1 已 MERGED 且批准 head 一致、C2 合并后准确默认分支 SHA CI 全绿、C3 需部署时完成且证据可读、C4 每项 PASS/勾或 YOUR_OWNER 已接受偏差、C5 无未答问句/未处理 YOUR_OWNER 意见、C6 follow-up 已开并互链，六项齐才发关单评论并关 issue，权限需核验；下一扫描 CLOSED 才 finished。未授权部署不推断为完成。
9. OQ4：合并批准可含部署，仅限 E 问句明确目标/回滚且 B 方案含步骤；实盘/资金/凭据/生产 cutover 需问句明确写出，否则另走 G4。main CI 红 → D；部署失败只按已授权回滚方案执行并问 YOUR_OWNER。OQ5：原验收内 FAIL 保持原票 OPEN、回 C 新 batch 修，留 FAIL 证据；范围外才开同仓 follow-up 入 A todo。范围内拆出是 G2，先问 YOUR_OWNER；父票仍需自身 C1–C6，不能因 follow-up 自动关。

每扫描执行新增纠偏：

- X14：B1/C/F 无人在跟（STOPPED 优先走 X19；非 STOPPED 无 working 先按第 6 条观察，不盲派）→ 按 lifecycle §5.6 产出 pending_dispatch，由父代理本回合实际派续，bullet `Bot 已派 <谁> 续（时间）`；派不了且需 YOUR_OWNER 决定 → D。已批 PR 修评审/解冲突/补声明及云评审全天回派，授权内聊天提醒全天发送；其他工作按已有授权，不伪称 working。
- X15：R1–R4 齐却 wip → 当次 E blocked + 合并问句。
- X16a：缺项在授权内可补且 working/本回合可派真实恢复方 → C，issue 写缺项、按 #14 全天实际 notify 已批 PR 补缺。X16b：结构性补不了或执行端已对缺项 blocked 提问（含无 ready/gap 的旧信号）→ D，写缺项与出路；Bot 不代判完成，合批例外前提仍核 lifecycle §5.8。禁止驳回 blocked 后全停、无 ❓、无承接。
- X19：STOPPED 无合法等待或第 6 条一次观察确认卡点且无在途命令、无合法等待，先按 lifecycle §5.2 同回合派独立可修部分，再按 §7 落板（D 只挡依赖决策的部分）：① R1–R4 齐走 X15/E；② 需 YOUR_OWNER 决定走 D；③ 授权内下一手用既有 resume/notify/review（包括先补缺失的完成声明、派修后复核/新 head 必需再评审；review 沿用同 head 去重及 §5.5 确认停止的一次同 tab 重派例外；#24 原会话恢复按本批 session 的一次预算去重），父代理同回合执行；④ 不明下一手走 D。合并门禁缺口与其他 R 项合法等待并存先等，写明评审后需 YOUR_OWNER 定例外；其他 G1–G4 立即 D。派单十分钟未确认按 #24 先标未确认并保留 pending、下次 wake 重推一次，再失败才 D；故障恢复的一次预算独立；同一 (row,X19,head,结果) 只派/问一次，head 变重判；本批一次恢复后再停转问 YOUR_OWNER，不被新 guard-stop 重置预算，不作一般 review 重派豁免。已批 PR 下一手 24h 实际派；D/E 同回合改板并发聊天问句，夜间同样适用。每次刷新上次更新和真实 bullet。
- X17：MERGED 无有效批准 → 记录 F 事实并在 issue/早报报违规，不自动 revert、不由此授权部署；需 YOUR_OWNER 决策转 D。
- X18：CLOSED 验收不齐且无偏差接受 → 不标 finished，blocked 问 `YOUR_OWNER 需决策：#M 已关但验收 k/n，是接受偏差还是 reopen？`。

子代理每扫描在现有 WAKE_/FALLBACK_ 加文本事实行 `stopped: S=<成员及各 agent_status> launch_grace=<依据> result=<true/false/unknown>` 与 `wait_valid: V1=<判定及来源> V2=<判定> V3=<真实恢复方或bot> result=<合法/无效/unknown>`；缺等待写无对象，主机读不到写 unknown，不造观察。它们与 gap 都不是 helper 顶层字段。

方案交付的信号只叫醒，不作为交付证明：H1/H2 先读 issue 按第 2 条核实；未收到信号、发送失败或日上限耗尽时，下一次现有 H2 同样核实、升 B2。全天在同次唤醒发一条 ≤200 字提醒（方案链接+问句），按同一行+版本在现有 WAKE_/FALLBACK_ 共用去重记录，只提醒一次；H1 已提醒的 H2 不重发，新版才重新提醒。夜间已提醒的同版在重复 wake 和 H2/早报均不重发。有效交付意味着 plan 等待已兑现，不能续旧 plan/review wait 留 wip；其他未兑现 CI/review 等待按 V1–V3/X19 核验；云 PR review 另受 §5.5 下个定时 H2 一次读 tab/有界重派限制，不无限续等。

每次纠偏写 `row, from→to, 码, 依据`（X19 写 X19-<结果>）到现有 WAKE_/FALLBACK_。板面 wip/todo 仅一条短 bullet，blocked 可再一条 ❓，CI run/全 SHA/PID 只留 evidence。按 YOUR_OWNER t462u P1-3=A，授权内通知与聊天提醒全天同回合发送，含 YOUR_OWNER 问题、E 合并请求、无法核验与待派原因，不因夜间延至 08:00。不得添加新状态或跨主机 POST relay；#24 本机脚本为已批例外 或自动关闭权限假设。

## #14 PR 闭环共同覆盖块（仍未安装）

此块与上文一并应用，优先于旧「遇决策即停全部派单」「夜间 PR 工作排 08:00」「派出就一直在审」写法。每 wake 先完整分页读**全部开发 PR** 当前 head/base、评论/评审/inline resolution、CI/mergeability，包含非触发行；信号只是 wake，GitHub 是 PR 事实来源。

1. 当前 head 应初评/复评且未派 → 父代理同回合实际 `review`，先过原云出口闸门。一 issue 一常驻云 Claude `<tid>-review` tab，方案→PR→新 head 共用上下文，issue CLOSED 才可关；同 issue 旧设计 tab 或已有逐 PR review tab，核 issue/会话身份后认作常驻并记旧名→常驻身份映射，不另开逐 PR 临时 tab。确认无常驻或可沿用 tab 时用既有 `launch` 新开 `<tid>-review`，在 WAKE_ 记旧映射（无则记无）和新 tab/会话；launch 保留已有授权与云出口 gate；十分钟未确认按 #24 持久送达重推一次、第二次失败问 YOUR_OWNER，故障恢复仍只一次。主机不可达/unknown 不等于确认缺失，不重复启动。派单用 [PR_REVIEW_BRIEF](PR_REVIEW_BRIEF.md)。同 head 去重，P0/P1 修后或未审改动需复评；只有回应表已记录的纯 P2 修复不强制全量再审。
2. reviewer 先发布并读回 GitHub 结论，再从独立 `<原任务目录>-review/BOARD_SIGNAL.md` 在云本机发一次 milestone/wip/host=云电脑，15 字段、同 task_id/board_row、按该路径 seq。该路径只 wake，不参与 R1/冲突优先级/跟进主机，seq 和 applied.json 仅按同一路径比较，不覆盖 Mac ready。设计阶段仍依 #10 发 blocked/blocked；共用 tab 不等于共用两端信号路径或混用阶段信号。
3. 结论一出立即结束「在审」。混合意见先 `resume` 原已停 Mac Main/原 worktree 修独立可修项，再同回合 `ask` → D blocked 问架构/验收/授权项，保留意见选项/推荐；决策不挡独立修复。回派前核无在途命令；原 tab 确认缺失才按现有容量与授权用 main2/新 batch，CI_WATCH OQ 不提供兜底授权。原 PR、回应表和信号要求写进修复 brief。
4. 无修复/决策时：缺完成声明 `notify` 原执行端；冲突派范围内修；R1–R4 真才 E。main-only PR 无 CI 按 §5.8 单 PR/head gap，不记 PASS、不改 workflow/手动触发；E 等批准停推，批准绑定 head，不自动合并/部署。
5. 先核下方 #24 本机恢复/在途记录，Bot 只兜底；符合时在当前 wake 续原 brief，不等下个 H2，也不算一般 review 重派。其余派不出只计实际出口/容量/主机失败；没有 tab 本身不计失败，先按第 1 条核实并 launch。第一次派评审失败记精确原因/head/时间并如实待下次 wake；第二次连续 wake 失败 D 问「YOUR_OWNER 需决策：PR#N 评审连续两次派不出（原因），等恢复还是暂停？」；成功实际派出才清零，仅 pending 或建 tab 不清零。派后下一个定时 H2 无结论，只读同 tab 一次，确认 stopped 且无在途命令才同 head 重派一次；仍无结果问 YOUR_OWNER，不再循环。unknown 徽标本身不当 working/stopped；下方 #24 现场确认另判，保留在途/未知命令；不得后台/别机 Claude 绕过出口。第三轮修复/复评仍有 P0/P1，问继续/改方案/暂停，不自动第四轮。
6. 24h 执行上述已批 PR 修评审/解冲突/补声明、云评审，夜里不排到 08:00；授权内通知和聊天提醒（包括 YOUR_OWNER 问题与合并请求）同回合全天发送，提醒共用既有去重，不延到早报。共享预算为 100/day、H2 每小时；15 字段、既有 kind、权限和 no-replay 不变。

每项真实派单、失败计数/重置、当前 head/复评轮次、一次有界重派和核验结果写现有 WAKE_/FALLBACK_，派单待办存板行，脚本只建本机运行去重/投递记录，不建阶段状态文件。两端已停时只写三种诚实 bullet：`执行端已停；Bot 已派 <谁> 做 <什么>（时间）` / `执行端已停；等 Claude 评审 PR#N（已派 <时间>，Bot 最迟 <下个 H2> 核）` / blocked + 可回答问句；首次派单失败如实用第 5 条失败 bullet，不装在审。不自动退 todo。纸面验证见 [PR loop cases](../sop/cases/pr-review-loop.md)，线上 A1/A2/A3/A4/A6 未验。

## #24 / #17 共同入口段（H1/H2 分别应用，未安装）

与出口补丁的下段逐字一致；仅此入口段前置，普通出口段仍在实际 Claude 派单前。每份 H1/H2 恰好一份；安装后分别读回完整 prompt，核入口可达、零 pending/零动作与父回执，不把文件合入当已安装。

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

当前 [lifecycle §5.6](../sop/lifecycle.md#56-派续由父代理执行pending_dispatch) 是发现、资格、guard 归属与父回执的权威步骤；历史证据（历史材料未分发，不是安装依赖） 仅历史，不能覆盖 #24 的演员/触发/频率/预算。
