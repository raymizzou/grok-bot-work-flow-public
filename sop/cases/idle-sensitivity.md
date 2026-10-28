# 执行端全停：判定用例与 #439 纸面重放

任务：workflow#7（历史示例，原记录不随公开包分发）。来源为 Claude 设计 v1 §2–§3、§5–§6，原件 `YOUR_TASK_ROOT/YOUR_TASK/DESIGN.md`；YOUR_OWNER 确认 OQ1–OQ5=A（历史示例，原记录不随公开包分发）。基线 `4958547ffc66a9b842bea8f50edadd758aa1f12f`。

这是文档规则的纸面核验，PASS 表示以下输入沿最终规则得到独立期望，不是已安装 H1/H2 的运行结果。权威规则：[lifecycle §3](../lifecycle.md#3-每次-h1h2-的阶段推导)、[§5.5 STOPPED/V1–V3](../lifecycle.md#55-stopped合法等待与无人跟进)、[§5.8 D 例外](../lifecycle.md#58-d-合批例外逐-prhead)、[§6 evidence](../lifecycle.md#6-信号-evidence-约定)、[§7 X16a/b 与 X19](../lifecycle.md#7-纠偏码-x14x19)。预期来自获批设计的具体快照和先后条件，不从新增文案反推期望。

## T1–T15：Given / When / Then

**历史范围提示（#14）**：下面 #7 / #439 的 PASS 是当时规则的纸面结论，不是当前 live 通过。下列 #7 / #439 历史表中的夜间聊天静默/08:00 延迟均已被 YOUR_OWNER t462u 的全天授权内提醒定案覆盖，不是当前操作期望；当前夜间案例见本文件 #10 AC-6/N5 与 PR review loop。旧 T4 的夜间补声明排 08:00、T18b/T18d 的 Claude 评审跨多个 H2 无界续等，以及 arch_review 字样均保留作 provenance，已被 [PR review loop](pr-review-loop.md) 的 24h 回派、常驻看板 review tab 和下一定时 H2 有界停止重派覆盖；其他 CI/市场等待不新增超时升级。#10 设计完成 blocked/blocked 信号仍有效。

共同输入：issue OPEN、对应阶段已有必要授权；除特别说明外，跟进主机可读、S 非空且含全部匹配 `<tid>-` 的 agent、派单宽限已过。D=非夜间；N=23:30–07:30 PT。每条核验结果均为纸面 PASS。

| ID | Given（输入） | When（本次核验） | Then（独立期望及理由） | 最终规则 / 结果 |
| --- | --- | --- | --- | --- |
| T1 | C，Main working，review 未出。 | D 唤醒。 | wip，非 X19：S 并非全部 idle/done；真实执行者在跟。 | §5.5 STOPPED；PASS |
| T2 | C，全 done；当前 head 有一名请求仍有效的 requested reviewer 尚未完成评审，无已兑现结论；next_check 未过；resume=bot。 | D，下一 H2 为 13:00。 | wip、非 X19；bullet `执行端已停；等评审；Bot 最迟 13:00 核`。对象未发生且有被动恢复方，不能写 Main 监控。 | §5.5 V1–V3；PASS |
| T3 | C，全 done；当前 head 已有评审、ledger open=0，无其他在途 reviewer；执行端未声明完成。 | D 唤醒。 | X19 序 3，notify Main 补 ready/gap 完成声明，wip `执行端已停；Bot 已派 Main 补完成声明`。评审等待已兑现，Bot 不能代判完成，也不能先问 D 合批例外。 | §5.5 V1、§5.8、§7 序 3；PASS |
| T4 | 同 T3。 | N 唤醒，无夜间续派预授权。 | X19 序 3，wip `执行端已停；待 08:00 续派 Main 补完成声明`；排队不执行、不聊天，不写等评审。 | §5.6、§7 序 3 夜间；PASS |
| T5 | C，全 done，无等待；执行端完成声明带 gap missing=R2；该 PR checks=0 且 workflow 只 push:main；其余 R 项已核，R3/R4 成立。 | N 唤醒。 | X16b / X19 序 2 → D blocked + 单 PR/head 合批例外 ❓；改板不聊天、进早报。无 PR run 是结构性缺口，不能算 R2 PASS，也不能让执行端自行改政策。 | §5.8、§7 X16b/序 2；PASS |
| T6 | C，全 done，无等待；R1–R4 全齐。 | 任意时段唤醒。 | X19 序 1 → X15/E blocked 合并问句；夜间仅改板。完整门禁优先于续派，不自动合并。 | §3、§7 序 1；PASS |
| T7 | C，全 done；当前 head CI run in_progress；next_check 未过；resume=bot。 | D 唤醒。 | wip、非 X19，被动等待 bullet 写执行端已停、等 CI、Bot 最迟下一 H2 核；仍有真实未完成对象。 | §5.5 V1–V3；PASS |
| T8 | C，全 done；所等当前 head CI run 已结束且红，问题在已批范围内。 | D 唤醒。 | X19 序 3，resume Main 修 CI；wip 写已派。run 结束意味着等待兑现，范围内修复无需 YOUR_OWNER 决策，不以 CI 红一律 D。 | §5.5 V1、§7 序 3；PASS |
| T9 | C，全 done；review 已贴出，新增未处理 P1，修复在已批范围。 | D 唤醒。 | X19 序 3，resume 修 P1，之后按 R3 修后复核；wip，不 D。评审已出意味着该等待对象结束，未处理意见成为可执行工作。 | §5.2、§7 序 3；PASS |
| T10 | C，全 done，无等待；最新 handoff BLOCKED 且问题为需新凭据。 | 任意时段唤醒。 | X19 序 2 → D/G4，问 YOUR_OWNER 凭据授权；夜间改板不聊天。凭据不在原授权内，不能自动补或续派绕过。 | §7 序 2②③；PASS |
| T11 | F，全 done，无等待；有效 head-bound 批准、已合并、准确 main SHA CI 绿；部署步骤已授权但未执行。 | D 唤醒。 | X19 序 3，resume 执行已授权部署；不重问同一授权，也不报验收完成。 | §5.3、§7 序 3；PASS |
| T12 | C，跟进主机不可读。 | 任意时段唤醒。 | 保持原状、标无法核验、进早报，非 X19；无法构造 S，不能把未知当全停，也不重复启动。 | §3 步骤 8、§5.5；PASS |
| T13 | C，全 done；Claude arch_review 已派而当前 head 未贴结论；next_check 未过，resume=bot；R2 结构性缺失。 | D 唤醒，随后评审贴出且无未处理意见、完成声明及其余 R 项齐。 | 首次 wip，bullet `执行端已停；等评审；Bot 最迟 <下一个 H2 时刻> 核；评审出来后需 YOUR_OWNER 定 R2 例外`；评审兑现后的下次唤醒才 X19 序 2 → D。合并门禁缺口不能让 YOUR_OWNER 在评审前批合；若另有无关 G1–G4 则立即 D。 | §7 合法等待并存约束、§5.8；PASS |
| T14 | T3 已实际派 notify；只等一次 10 分钟后仍全 done，无 ACK/实际开始。 | D 到期核验，不重复派。 | 读 pane 一次记可见原因/unknown → X19 序 2④ D 问是否重派。未启动不能假装 Main 已接，不能以 launch 宽限永久维持 wip。 | §5.6、§7 ACK 约束；PASS |
| T15 | 同 head 已有 X19 问句未答，执行端仍全 done，问题事实未变。 | 下一次唤醒。 | 保持 blocked、核是否已答，不重复问/派；去重键 (row,X19,head,结果)。head 变后重判；已问不是又回 C 的理由。 | §7 去重、§3；PASS |

附带边界核对：S 为空走 X14；≤10 分钟派单宽限不判 STOPPED，也不触发无 working 观察兜底；resume 指 idle/done 时先按 bot，再由本次 V1 读回决定是否续到下一 H2，不以旧 next_check 过期否定真实被动等待。market/runtime 要有可读观测源；未核实 CI/保护规则不能冒称 PASS。以上均由 §5.5/§7 明文覆盖，不制造运行样本。

## T16–T21：P1 follow-up 的独立边界

沿用上述共同输入。期望来自 OQ1 的全 idle/done 定义、OQ3=A 被动等到既有 H2、Claude 三条 P1 的反例和 Main C1 PLAN 的已批准核验契约（基线 `65ba7e41`）；不采用另加跨两 H2/24 小时升级政策。每个子场景单独核验，PASS 仍仅为纸面结果。

| ID | Given（输入） | When（本次核验） | Then（独立期望及理由） | 最终规则 / 结果 |
| --- | --- | --- | --- | --- |
| T16a | C，S 含等输入状态、无 working，宽限已过，无合法等待；pane 明确停在可按已有 brief 继续的输入处，无在途命令。 | 只读相关 pane 一次。 | STOPPED=false，但观察兜底 → X19 序 3，resume 已授权下一手，核 ACK；不能静默留旧活跃 bullet。输入本身不新增 YOUR_OWNER 决策。 | §5.5 观察兜底、§7 序 3；PASS |
| T16b | 同 T16a，但 pane 是需要 YOUR_OWNER 新增权限的弹窗，无在途命令。 | 一次观察确认所缺权限超出已有授权。 | X19 序 2 → D/G4，写明确授权问句；不代答弹窗或直接重启。是否卡 YOUR_OWNER 取决于授权事实。 | §5.5、§7 序 2；PASS |
| T16c | C，S 含 unknown、无 working，宽限已过；pane 可读且有真实在途命令。 | 一次观察。 | 保持原状，记无法核验及在途命令、进早报；STOPPED 不记 true，不声称 working，不续派/重启。无 working 标签不能证明命令已停。 | §5.5 观察兜底；PASS |
| T16d | 同 T16c，但 pane 不可读，无法确认命令是否还在途。 | 只尝试读取一次。 | 保持原状、记无法核验并早报，无重复工作；unknown 不等于确认停工。 | §5.5 观察兜底；PASS |
| T17a | C，全 done；P1 已在新 head 修复，按 R3 需要 Claude 修后复核，该 head 尚未派 review，无其他合法等待。 | D 唤醒。 | X19 序 3 派既有 review，按既有夜间/ACK/去重规则承接；复核是已授权下一手，不能因 V1 无对象走序 4 假 D。 | §5.2、§5.6、§7 序 3；PASS |
| T17b | C，全 done；同一新 head 的复核已派且尚无结论，V1 本次可读为真；或该 review 正在有效派单宽限内。 | 下一次唤醒。 | 前者合法被动等待，后者沿用宽限；均不再派同 head review。等待对象和派单记录独立防止重复。 | §5.5、§5.6 去重；PASS |
| T18a | C，全 done；resume=bot，旧 next_check=12:08，当前 head 同一 CI run 仍 in_progress。 | 13:00 H2 重新读回；下一 H2=19:00。 | V1 真，next_check 续到 19:00、wip 写 Bot 最迟该时刻核，非 X19/D；短 next_check 不能使真实被动 CI 等待失效。 | §5.5 V2；PASS |
| T18b | 同 T18a，但对象是已派且当前 head 仍未贴结论的 Claude 评审。 | 13:00 读回 V1 真。 | 续到 19:00，保持真实被动等待；评审与 CI 的被动恢复原则相同。 | §5.5 V1–V3；PASS |
| T18c | 同 T18a，但旧 resume 指 idle Main。 | 先归一为 bot，再读回同一 CI run。 | 与 T18a 相同，不先用旧 next_check 判无效；idle Main 不被冒称在监控。 | §5.5 归一顺序、V2；PASS |
| T18d | 同 T18b，但旧 resume 指 done Main，已连续多个 H2 仍可核验为同一当前 head 待出评审。 | 19:00 再读回；下一 H2=次日 08:00。 | 先按 bot，再续到次日 08:00；不加 wake，不因累计时间自动 D。OQ3=A 仅保留既有 H2 被动恢复。 | §5.5 V2 与等待上限；PASS |
| T19a | C，全 done；旧 bot 等待已过时，当前 head CI run 已结束且红，修复在已批范围。 | H2 读回已结束。 | V1 假、不续期，X19 序 3 修 CI；不能把失败 run 当 pending。 | §5.5 V1、§7 序 3；PASS |
| T19b | C，全 done；旧 bot 等待评审，当前 head 已贴结论、ledger open=0，无其他在途 reviewer，缺完成声明。 | H2 读回。 | V1 假、不续期，X19 序 3 notify 补声明，与 T3 相同。已完成评审不能用旧 wait 续命。 | §5.5 V1、§7 序 3；PASS |
| T19c | C，全 done；旧 bot 等 CI，但当前 head 无 run 且触发规则不会产生，执行端已声明结构性 R2 缺口、其余条件如 T5。 | H2 读回无对象。 | 不续期，X19 序 2/X16b → D；无 run 不是 queued 或 R2 PASS。 | §5.5 V1、§5.8；PASS |
| T19d | C，全 done；旧 wait 的 run/review 仅属于旧 head，当前 head 没有匹配对象，Main 可在原授权内核验当前 head 并补声明。 | H2 核对对象身份。 | 不将旧 head 等待续给新 head；X19 序 3 通知 Main 做已授权核验，不能接受旧 CI/评审为当前 head 证据。 | §5.5 V1、§7 序 3；PASS |
| T19e | C，全 done；旧 bot 等待对象的读回失败，或无法核实其 head 身份。 | H2 尝试核验。 | V1=UNKNOWN，不续期、不记合法等待；保持原状、显式无法核验并早报，不以 UNKNOWN 造停工/完成或重复启动。 | §5.5 无法核验边界；PASS |
| T20a | C，全 done；本回合 pending_dispatch 等 ACK，距实际派出 ≤10 分钟。 | 当前唤醒。 | STOPPED=false；不进 X19、不重复派。尚在启动宽限不能当失联。 | §5.5、§5.6；PASS |
| T20b | 同 T20a，但派单在上一回合，距实际派出恰 10 分钟，尚在获准的 ≤10 分钟窗口内。 | 当前唤醒。 | 沿用同一宽限，不重派；窗口结束核前次结果，失败走 T14，不永久延长宽限。 | §5.5、§7 ACK 约束；PASS |
| T20c | 同 T20a，但 S 有非 idle/done 状态、仍无 working，宽限有效。 | 当前唤醒。 | 不触发一次观察兜底或重派；该兜底也必须等启动宽限结束。 | §5.5 观察前提；PASS |
| T21a | C，跟进主机可读、S 为空，无合法等待/有效宽限，已有授权下一手可派。 | D 唤醒。 | STOPPED=false，沿用 X14 实际派续；非 X19，不自动降 todo。空集合不改原有路径。 | §5.5、§7 X14；PASS |
| T21b | C，跟进主机不可达，S 无法读取。 | 任意时段唤醒。 | 维持原状、无法核验并早报；S=unknown，不能写为空或全停，不强行 SSH/重复派。与 T12 相同。 | §3 步骤 8、§5.5；PASS |

## #439 / PR#452：历史纸面重放

来源：设计 v1 §1、§3 引用的 `WAKE_2026-10-24_2303.md`、`WAKE_2026-10-24_2325.md`、`WAKE_2026-10-25_0027.md`、`WAKE_2026-10-25_0030.md`，及 `YOUR_TASK_ID/BOARD_SIGNAL` seq=26、审阅时间线；均为设计提供的历史事实。本工作树主机未取得这些原件，不声称已现场读回其内容或 GitHub 状态；以下以设计快照为输入，真实性/完整性仍受该来源限制。

时区均为 PT，23:25 仍在 23:30 夜间界限前（设计表中的“白天”指非夜间）。固定 head `a3c70c85`；23:09 Dots COMMENTED 无新可操作意见，ledger open=0，假定无其他尚待完成 reviewer。**只有本历史 #439 fixture 是 main-only CI；当前 workflow 仓有 PR CI，不能迁移此缺口假设。**

| 时刻 | Given（历史快照 / 假设） | 旧结果 | 新结果与理由（纸面） |
| --- | --- | --- | --- |
| 10-24 23:03 | Main/fix-worker done；PR 待审；next_check≈23:11；旧 resume 指 done Main。 | C wip 等评审。 | 同为 wip，V1/V2 真；恢复方改按 bot，bullet `执行端已停；等 PR#452 评审；Bot 最迟 <下一个 H2 时刻> 核`，不称 Main 监控。 |
| **10-24 23:25** | 四 tab 全 done/idle、宽限已过；23:09 当前 head 已审且 open=0；seq=25 仍称等评审、next_check≈23:32；无执行端完成声明。 | C wip，称 Main 继续监控，漏判等待已兑现。 | **X19 序 3**：V1 假，父代理同回合 notify Main 补完成声明（ready；R2 结构性缺失用 gap），wip 写已派。不是 D 合批请求，Bot 不能替 Main 声明完成。对应 T3，PASS。 |
| ~10-24 23:35（设计推演，非实测） | 假设 Main 已 ACK/实际开始、随后发 gap missing=R2，完成声明与其余 R 项已核。 | 无旧样本。 | X16b → D 合批例外 ❓，夜间改板不聊天、进 08:00 早报；未 ACK 则走 T14，不假称此信号已发生。 |
| **10-25 00:27（旧格式分支）** | 执行端 seq=26 已明确 blocked 并问合批，无 ready，且自承 R2 PR CI 缺失≠PASS；checks=0、workflow 仅 main；执行端全停。 | X16 驳回回 C wip，notify 排 08:00，板无 ❓，无人实际承接。 | **X16b → D blocked**，保留执行端问题、R2 结构性缺口与缺 ready 的事实，写可选出路；不能只驳回留 wip。按 §5.8 核原执行端完成声明/其余门禁后才形成完整合批例外问句；不由 Bot 补造 ready/gap 或宣称可合。夜间只改板、进早报。此处 D 的直接依据是“已有 blocked 问题 + 结构性缺项”，与 23:25 尚未完成声明时先续派不同。PASS。 |
| 10-25 00:32 / 00:35 | 假设 YOUR_OWNER 明确回复的是已满足 §5.8 前提的 D 合批例外问句，批准/实际合入 head 都为 a3c70c85。 | 靠 YOUR_OWNER 明示覆盖旧 X16。 | 可记录【合并批准】和【门禁例外：R2，理由，原话链接】，合法进入 F；新提交使批准失效，准确 main SHA CI 仍须绿，红即 D/G4，部署另批。不是对历史批准有效性的新审计。 |

## AC 映射与交付边界

| 验收 | 文档证据 / 核验范围 | 结果 |
| --- | --- | --- |
| AC-1 | [lifecycle](../lifecycle.md) §3 步骤 5/批准效力、§5.5 STOPPED/V1–V3、§6 gap/wait、§7 X16a/b/X19；[状态机](../board-state-machine.md) 可观察状态；[进度 SOP](../bot-progress-board-sop_2026-10-26.md) §3 门禁与非 blocked、§9.1 步骤 5–6，覆盖设计 §2.7 对应落点。保留现有状态/八列/routine、pending_dispatch 六种 kind 和 helper 15 字段。 | **PASS（纸面）** |
| AC-2 | [H1/H2 追加稿](../../templates/H1_H2_LIFECYCLE_APPEND.md) 第 6 条、纠偏与 stopped/wait_valid 事实行；[执行端追加稿](../../templates/LIFECYCLE_AGENTS_APPEND.md) ②、gap/wait evidence 与 done/idle resume=bot；两者指向 lifecycle，覆盖设计 §2.7 余下落点。 | **PASS（纸面）** |
| AC-3 | 本文 T1–T21（含全部子场景）独立输入/期望逐项映射最终规则；#439 23:25=X19 序 3，00:27=X16b→D；完整证据假设与未知如上。 | **PASS（纸面）** |
| AC-4 | 单独获批安装后，首个自然全停样本的 WAKE_ 须有 stopped/wait_valid 事实行及 X19；本文不安装、不造样本。 | **DEFERRED，未运行，非 PASS** |

本批只交付六个仓内 Markdown 文件；未改线上 SOP、H1/H2 prompt、个人指令、helper、CI 触发、YOUR_BUSINESS_REPO 或调度。未运行后端全套，不制造 RED/GREEN。PR、评审、合并、安装与 AC-4 由 Main 按各自授权继续。

## #10：方案交付后 B2 与提醒（WORKFLOW10-I1 纸面用例）

本节独立于上面的 #7 / #439 历史与 AC 映射，不改其结果或延期验收。来源：workflow#10（历史示例，原记录不随公开包分发）、获批 `YOUR_TASK_ROOT/YOUR_TASK/PLAN.md` §3(1)–(4)、§3(7)，及同目录 `ADDENDUM_t425u_oq.md` 的 OQ1=A。期望先取自该方案的六条验收与明确反例，再手工沿本批六份文档核对；AC-6/N5 的夜间提醒期望按 YOUR_OWNER t462u P1-3=A 更新，其余授权门禁不变；不从改后的文案生成期望，不伪造 RED/GREEN 或真实运行。

共同输入：issue OPEN、YOUR_OWNER 已说跟进；task_id 含 issue 号，board_row 与板标题一致。除特别说明外，Claude issue 评论首行 `【方案 vN】#M <标题>`，正文方案/摘要及 PLAN 路径齐，结尾 OQ 数量或无 OQ、最后 Claude@云电脑 LLM 尾标；评论时间严格晚于最近【跟进】/【跟进修改】。时间均为 PT。下列结果全部仅为 **PAPER PASS**。

| #10 ID | Given（独立输入） | When（纸面事件） | Then（PLAN_S10 的独立期望） | 对照文档 / 结果 |
| --- | --- | --- | --- | --- |
| AC-1 无 OQ | 10:00【跟进】，10:05 v1 评论「无 Open Question」；本行 v1 未提醒。 | Claude 在云电脑先交 issue，再发一次 blocked/blocked 信号；H1 同次醒来核 issue。 | Bot 同次把行改 B2 blocked，一条「方案 v1 已出，无待定问题」bullet+❓问派谁（mini/air Codex，容量仅建议），≤200 字提醒含链接/问句一次；不自动派人，也不把无 OQ 当方案/G2 已确认。 | lifecycle §2/§3/§6；SOP §7；状态机 B2；H1/H2 第 2–3 条；Claude 模板；PAPER PASS |
| AC-2 OQ+指派 | v1 评论列两个 OQ，尚无 YOUR_OWNER 决定或实现端。 | H1 核实交付；随后 YOUR_OWNER 逐项答 OQ 并明确确认方案/G2，但未点名；再明确指派 mini Codex。 | 首次 B2 的 ❓逐条保留两个 OQ 并问派谁；只答 OQ 后仍 B2，只剩派谁，不因有回复回 wip。最后方案/G2+明确指派齐，Bot 同回合记原话/指派并派指定实现端进 C。 | lifecycle §2/§3/§4；SOP §7/§9.2；H1/H2 第 2–3、5 条；PAPER PASS |
| AC-3 修改后重交 | 18:10 v1 已交且已提醒；19:38 YOUR_OWNER 提修改，Bot 记【跟进修改】并回派，19:47 v2 评论交付。 | 修改时、v2 交付后的 H1 分别核 issue。 | 修改后回 B1 wip 重写，v1 不再证明本轮已交付/已确认；19:47 新评论晚于 19:38，重新 B2 blocked、按有/无 OQ 问句提醒一次。v1 去重记录不压制 v2。 | lifecycle §2/§3/§4；SOP §7/§9.2；H1/H2 第 2 条；PAPER PASS |
| AC-4 缺信号与去重 | 12:10 v1 已交；Claude 未发、退出 4 重试后仍失败，或日上限 30 耗尽；本行版本未提醒。 | 13:00 H2 核 issue；之后同版迟到信号 H1、19:00 H2 再核。另取 H1 已首先提醒的同版场景。 | 首个可执行的 H2 同样升 B2+全天一次提醒；迟到 H1/后续 H2 不重复。H1 先提醒的同版，H2 也不重发；不加唤醒通路或超过日上限。只读信号不算核实交付。 | lifecycle §2/§6；SOP §7；H1/H2 提醒共用段；Claude 模板退出码；PAPER PASS |
| AC-5 working 优先级 | 19:49 v2 有效交付；Claude tab 仍 working，旧 wait 称「等方案/评审」。 | H1 或 H2 先核 issue。 | 按新评论直接 B2 blocked，方案等待已兑现，不检查 working 先留 B1，不续旧 wait；未兑现的实现 PR CI/review 仍按原 V1–V3，不扩大为一律 blocked。 | lifecycle §3 步骤 4/§5.5 V1；状态机 B2；H1/H2 第 2 条与共用段；PAPER PASS |
| AC-6 夜间同回合提醒 | 23:40 v1 有效交付且本版尚未提醒；本夜又收到同版信号。 | 夜间 H1 核 issue，次日 08:00 H2 早报，再到 13:00 H2。 | 夜间照常 B2 blocked+问句，同次唤醒发送 ≤200 字方案链接+问题提醒并登记行+版本；重复夜间信号、08:00/13:00 H2 均不重发同版提醒。新版交付可再提醒；全天均不自动派未经点名的初次实现端。 | lifecycle §1/§2；SOP §7；H1/H2 共用段；Claude 模板；PAPER PASS |

### #10 负例与授权边界

| #10 ID | Given / When | Then（独立反例期望） | 对照文档 / 结果 |
| --- | --- | --- | --- |
| N1 旧版早于修改 | 19:47 v2 评论后，19:50 新【跟进修改】；旧信号再来。另取评论与修改时间相等。 | 两者都不满足严格晚于最新修改；不算本轮交付，不发旧版完成提醒；记录/回派修订，不沿用旧确认。 | lifecycle §2/§3；SOP §7；H1/H2 第 2 条；PAPER PASS |
| N2 只有本地 PLAN | 本地 `PLAN_S10_v3.md` 存在，或只有信号称完成；issue 无方案评论。另取安装后交付的新版评论缺首行/结尾/Claude 尾标；不含 N8 的安装前有效旧方案。 | 都不能证明有效交付；Bot 先核 issue，不能凭文件、信号或安装后的不合格新格式升交付 B2，按实际执行/等待与现有纠偏承接，不伪造 working。 | lifecycle §2/§3/§5.7；Claude 模板；H1/H2 第 2 条；PAPER PASS |
| N3 只答 OQ | YOUR_OWNER 明确 OQ1=A，并确认方案/G2，但没说机器/agent；#421 显示 air 空闲。 | 仍 B2 blocked，仅问派谁；容量建议不等于指派，不自动派 air。 | lifecycle §2/§3；SOP §3/§7；H1/H2 第 3 条；PAPER PASS |
| N4 含糊同意 | YOUR_OWNER 只回「行」或「可以」，没有明确方案/G2 与指派信息。 | 不猜确认或实现端，不派；保留尚缺门禁的可回答问句。无 OQ 不免除确认。 | lifecycle §1/§2；SOP §7/§9.2；Claude 模板；PAPER PASS |
| N5 夜间重复 | AC-6 夜间同版 H1 多次醒来，08:00 后还有同版信号。 | 夜间首次同回合提醒一次，重复 wake/08:00 H2 及之后同版不重复；新版可再提醒，不按 signal seq 当新方案；H2 08/13/19 与 cap30 不变。 | lifecycle §2；SOP §7；H1/H2 共用段；PAPER PASS |
| N6 信号错误不通用重试 | helper 退出 4、3、2 分别作为独立输入。 | 4 仅允许一次完全相同输入重试（seq/as_of 不变），再失败停手报告；3 保留信号报告配置缺失/不合格，不盲重试；2 修正输入而非原样再发。不扩大到凭据或基础设施修改。 | lifecycle §6；Claude 模板；原 board-signal 协议未改；PAPER PASS |
| N7 独写板/部署边界 | Claude 有任务内方案评论与一次云端信号权限，方案尚未获 YOUR_OWNER 确认或安装另批。 | Claude 不写 Page、不调用 Canvas；Bot 核 issue 后独写板。无安装、生产 routine/个人配置修改、merge/deploy 或其他外部动作授权；15 字段、原状态/30 次上限不变。 | lifecycle §1/§6；SOP §7/§10；H1/H2、Claude 未安装声明；PAPER PASS |
| N8 安装前旧格式 B2 | 安装前已有真实 Claude 带尾标的 issue 方案评论，版本/OQ 可核，严格晚于最近【跟进】/【跟进修改】，之后 YOUR_OWNER 无新回复，行已 B2；只有首行/结尾不符合新格式。 | 安装后首次 H2 保持 B2 blocked，按新模板改问句；Bot 发带尾标【迁移记录】，写原评论链接、交付时间、版本号与 OQ 条数，不回 B1、不走 X19、不要求 Claude 重贴或重派。安装后同样格式的新方案不享此例外（N2）；真实后续修改仍使旧方案失效（N1），不豁免确认/指派（N3/N4）。 | lifecycle §2/§5.7；SOP §7；状态机 B2；H1/H2 第 2 条；PAPER PASS |

N8 的独立期望来自 Claude PR#11 P1（历史示例，原记录不随公开包分发） 与 YOUR_OWNER t429u 已批准的 `ADDENDUM_t429u_fix_p1.md`；本次 WORKFLOW10-P1-I2 仅补存量交付迁移，不改变安装后的格式、时间、确认或指派门禁。

**#10 交付结果：AC-1–AC-6 与 N1–N8 均 PAPER PASS；LIVE DEFERRED（未安装、未发 live/dry-run 信号、未跑真实方案）。** 单独获批安装后，仍须用下一份真实方案取 AC-1 或 AC-2 的 issue 评论、信号、同次唤醒板面和提醒证据；纸面结果不替代该验收，也不改上面 #7 AC-4 的 DEFERRED。发布、CI、评审与后续生命周期由 Main 在各自授权内负责。
