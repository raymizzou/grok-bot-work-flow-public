# #14 PR 评审闭环：独立纸面推演

原批次 WORKFLOW14-I1；C1 按 YOUR_OWNER t462u 及 Claude PR#15 @9e504c8c 的五项意见更新当前期望；仅文档核对，不运行 routine、Herdr 派单、GitHub 写入或信号。目标是复现方案里的失败输入，再人工判断授权下应有的下一手；不是检索几个关键词就宣称行为通过。

独立期望来源：PLAN §3 / A1–A6（历史示例，原记录不随公开包分发）、YOUR_OWNER 24h / 常驻同 issue tab 定案（历史示例，原记录不随公开包分发）、实现边界（历史示例，原记录不随公开包分发）。Main 提供的 `PLAN_S10.md` 与 `BRIEF_IMPL_MINI_t448u.md` 为本次原文输入，worker 已读；历史时间线是方案作者的快照，本批没有现场核 GitHub/云端/WAKE 原件，不新增真实性断言。

共同前提：issue OPEN、开发方案/验收和执行端已有明确批准；不含合并/部署批准。所有 PR 身份用当前完整 head/base，表里 H1/H2/H3 为符号，不是现网 SHA。Mac Main 已停、宽限已过、可读且无在途命令；若不同，按各用例的保护分支。所有结论都是 **PAPER PASS**（已人工对照文案），不能替代 live 验收。

## A1–A6 的 Given / When / Then

| ID | Given（从方案取的输入） | When（纸面事件） | Then（先确定的期望与人工对照） | 证据 / 运行状态 |
| --- | --- | --- | --- | --- |
| A1 | 已批任务新 PR head H1；该 head 未评；该 issue 的方案 review tab 已存在。 | Mac 发 PR milestone，H1 醒。 | 同回合核 GitHub 并由看板父代理派 H1 评审，复用该 issue 常驻云 Claude tab；不问 YOUR_OWNER，不新建逐 PR tab。出口先过原 gate，未派成功不写在审。 | lifecycle §5.2 第 1 项、§5.6；PR_REVIEW_BRIEF；PAPER PASS；**LIVE DEFERRED**：需真实 WAKE 与云 tab/ACK。 |
| A2 | Claude 已审 H1，提出已批范围可修意见；没有 YOUR_OWNER 决策。 | Claude 先发布/读回结论，再从独立云 review 路径发一次 milestone；Bot 醒。 | Bot 读所有开发 PR，先核原 Mac Main 无在途命令，再同回合续派修复、更新回应表/原 PR/信号；夜里同样派，不排 08:00。自然事件验收目标为发布后 10 分钟内实际开始，日 cap/发送失败时 fallback 只能如实延期，不宣称达标。 | lifecycle §5.2 第 2–3 项/§6、H1/H2 覆盖块；PAPER PASS；**LIVE DEFERRED**：需评论/云信号/WAKE/Mac ACK及实际开始时间。 |
| A3 | 同一结论 O1=P1 要 YOUR_OWNER 拍板，O2=P1 可独立修，4 个 P2 中已决定范围内修复；彼此依赖已明确。 | Bot 读到混合意见，夜间也一样。 | 先派 O2/可修 P2，再同回合 D blocked 问 O1（保留原选项/推荐）；只停依赖 O1 的部分，D/X19 不吞修复。夜里问句上板并在同次唤醒发聊天提醒，不延至早报。 | lifecycle §5.2 第 3 项、§3、X19；PAPER PASS；**LIVE DEFERRED**：需真实同回合派单和 blocked。 |
| A4 | 当前 head 评审已出、无未处理项、无其他待出评审。 | Bot 核门禁，分别输入缺声明、有冲突、R1–R4 齐三个互斥场景。 | 缺声明 notify 原 Main，不代造 ready；冲突派范围内解，复杂扩架构先问；全齐 E blocked 问 YOUR_OWNER 合并，无部署则明确无需部署。没有批准不合并。 | lifecycle §5.2 第 4 项、§5.1/§5.8、X19；PAPER PASS；**LIVE DEFERRED**：需三个自然门禁样本或获批试跑。 |
| A5 | 下列 #462/#463 方案历史快照，修复后的规则已交付但尚未安装。 | 按每个时间点逐步手推，核是否有人承接、结论是否过期。 | 已出结论不能仍在审；混合意见独立派修且问 YOUR_OWNER；后来冲突由非触发行全扫描发现并派解，不靠 YOUR_OWNER 点名。 | 下节时间线；**PAPER PASS，仅纸面**，不作真实运行验收。 |
| A6 | 当前 H1 评审派不出，云出口 gate 不合；第一次没有实际派出。 | 连续两次 wake 尝试当前任务同 head 均失败。 | 第一次如实记录精确失败，下一 wake 再试；第二次 D blocked 问「等恢复还是暂停」，不静默排队/假在审；实际成功派出才清零。夜间同次唤醒发送 blocked 聊天问句。 | lifecycle §5.2 第 5 项、H1/H2、出口补丁；PAPER PASS；**LIVE DEFERRED**：需两次 WAKE/失败原因/板问句。 |

## #462 / PR#468 与 #463 / PR#467 时间线（A5）

时间均 PT，2026-10-25→26；输入来自方案 §1，不是本批重新观测。规则推演假设对应 wake 按修订后的全 PR 扫描执行；不声称改变了历史。

| 时间 / Given | When | Then（修订规则下） |
| --- | --- | --- |
| #463 22:30 修完 Dots 两条，待 Claude 复核。 | 22:34 wake，云出口不对，首次复评派不出。 | 保留原 gate，记录第一次失败及原因；不把「排了」写成「在审」。 |
| #463 22:34 首次失败。 | 23:04 下一连续 wake 仍派不出；同时看到 #462 PR#468。 | #463 第二次失败 D 问等出口恢复/暂停；#462 单独记录自己的第一次失败，不混计任务失败次数。不后台绕行。 |
| #462 22:55 开 PR；23:04 首次派评审失败。 | 假设下一 wake 仍失败，或出口恢复实际派出。 | 失败则第二次 D；成功实际派出才重置并核 ACK。不能从旧 cap/dispatch log 认在审。 |
| #463 23:42 YOUR_OWNER 手动推动后成功派评审，23:44 Claude 已贴无待修结论。 | 23:48 wake 由 #461 信号触发。 | 同样读 #463/PR467，看到 23:44 结论，结束等评审；核完成声明/冲突/所有 R 项，分别派补/派解/E 或真实 gap；绝不再写「Claude 在审」。 |
| #462 23:48 Claude 贴 O1/P1 要决策、O2/P1 可修、4 个 P2。 | 该结论云 signal 叫醒，或任意另一行 wake/H2。 | 当回合先回派 Air 修独立 O2/可修 P2；再 D 问 O1 原选项/推荐。23:48 夜间也派，并在同回合发 O1 聊天问句。不必等 YOUR_OWNER t440s 才派可修项。 |
| #463 评审已结论后，main 前进造成 PR467 冲突。 | 后续任意 wake 全读开发 PR，而非只读触发行。 | 发现 mergeability CONFLICTING，核原 Mini Main 无在途命令，派范围内解冲突；UNKNOWN 先核实，不能当可合/冲突。无需等 00:40 t446u 点名。若 E 等批准中停推，先报告并请 YOUR_OWNER 要求修再推。 |

若该回合没有自然 wake，仍是现有 08/13/19 PT fallback，不许凭纸面保证必然 10 分钟；A2 live 仍须取实际时差。真实出口恢复、实际 ACK、冲突复杂度均未在本批验证。

## 独立边界与失败推演

| ID | Given | When | Then（独立期望） | 人工对照 / 结果 |
| --- | --- | --- | --- | --- |
| N1 常驻上下文 | 同 issue 已有设计 tab，会话已核；B1→B2→C 新 PR H1→修后 H2，issue 仍 OPEN。 | 看板分别派设计/初评/复评，随后 PR 合并；最后另一次读回 issue CLOSED。 | 前四步只用原常驻 tab，不因新 PR/head/merge 关闭。只有 issue CLOSED 才可关；已有旧设计名核身份记录映射，不借其他任务 tab。设计先 issue+blocked/blocked，PR 先 GitHub+独立目录 milestone/wip。 | lifecycle §5.2/§6、review brief；PAPER PASS。 |
| N2 重复输入 | 同一评论/同 head review 已派，重复云信号或其他行 wake；云/Mac 两个路径各有自己的 seq。 | H1/H2 再次醒。 | 同 head 不重复评审，读当前 GitHub；相同结论不新发一次 milestone，只有 exit 4 原样一次重试。路径分离不等于 task_id/board_row 变化；不得互借 seq。 | §5.6/§6、信号协议、review brief；PAPER PASS。 |
| N3 复评触发 | H1 已审；H2 仅含回应表完整记录的纯 P2 修复；另输入 H3 含 P1 修复或未审改动。 | Mac push 后 wake。 | H2 不强制全量再审；H3 必需复评并同 head 去重。不能只填一行回应就遮掉未审代码；P0/P1 不改/转出仍须 YOUR_OWNER 明确处置。 | §5.2 R3/闭环、H1/H2；PAPER PASS。 |
| N4 失败重置 | wake1 派失败；wake2 成功实际派出并 ACK；之后新 head wake3 又失败。 | 按现有 WAKE 记录核失败序列。 | 成功后清零，wake3 是首次；仅 pending 清单无实际派出不清零。失败不得改出口判据或复用旧授权重放 pending。 | §5.2 第 5 项/§5.6；PAPER PASS。 |
| N5 unknown/在途 | 下一个 H2 仍无结论；Herdr=unknown，pane 可见命令还在跑；另输入不可读。 | 单次读该 tab。 | unknown 不能判 working/stopped；两输入都保留命令、不重派，记无法核验并由现有 H2 核，不制造 fake wip 或中断进程。 | §5.5、状态机；PAPER PASS。 |
| N6 一次停止重派 | 当前 head 评审实际派出后到下个定时 H2 没结论；单读确认 tab 已停且无在途命令。 | Bot 复用同 tab 重派一次；之后仍无结果。 | 这一次是同 head 去重的有界例外，留下证据，不开新 tab。再无结果问 YOUR_OWNER，不重复 H2→重派循环；确认未停不能走此例外。 | §5.5/§5.6、H1/H2；PAPER PASS。 |
| N7 第三轮 | 同 PR 连续第三轮修后复评仍有 P0/P1，head 每轮不同。 | Bot 读第三轮结论。 | 停自动第四轮，问继续/改方案/暂停；新 head 不重置轮数；保留已确认问题/证据，不弱化负断言。 | §5.2 第 6 项；PAPER PASS。 |
| N8 no PR CI | 项目只 main CI，当前 PR head checks 无 run；执行端完成声明和其余 R 项已核。 | Bot 查合并门。 | R2 缺失不 PASS，仅按 §5.8 问 PR/head 例外，缺声明先派补；不改 workflow/手动 dispatch。不因无评审待办就 E。main 精确 SHA CI 仍 C2，红停问 YOUR_OWNER。 | §5.1/§5.8、H1/H2；PAPER PASS。 |
| N9 E 与批准 | 当前 head H1 已进 E 等 YOUR_OWNER；没有批准；或 YOUR_OWNER 批 H1 后又有 H2。 | wake 发现新意见/新提交。 | E 停推，除 YOUR_OWNER 要求修改不推修；H2 使 H1 批准失效，重核/重问。CI 绿/评审无意见/24h 回派都不授权合并部署/关单；issue OPEN 不 finished。 | §3/§4/§5.1/§5.3、执行端模板；PAPER PASS。 |
| N10 原 Main 丢失 | 原 Main 可能不可达，或已确认 tab 不存在。 | Bot 找执行端。 | 不可达不等不存在，保留未知不重复启动；确认缺失才按既有容量和授权 main2/新 batch，不借待批 CI_WATCH。无容量/授权问 YOUR_OWNER，保留 dirty 工作。 | §5.6、H1/H2；PAPER PASS。 |
| N11 helper 错误 | 云端发布已验证；helper 返回 4/3/2，分别输入。 | reviewer 准备回报。 | 4 原样含 seq/as_of 仅重试一次，再失败报待投递；3 保留报配置未合格，不盲改凭据；2 修输入，不原样重试。无有效配置/可读 seq 不猜值。H2 仍核 GitHub，不用发新信号冒充重试。 | §6、review brief、原信号协议；PAPER PASS。 |
| N12 安装隔离 | 仓内 SOP/templates 已改；H1/H2 与脚本未改。 | owner 以后另获安装授权。 | 先备份 H1/H2 完整 prompt、保留回滚，移除 H1 整段 `arch_review_dispatch.py scan` 调用（issue 与 PR 扫描全部移除），不留独立旧扫描；分别全文读回检查。此刻不能宣称 live disabled/已部署/三端通过；本批脚本/tests/CI 无改。 | H1/H2 应用说明、README；PAPER PASS。 |

## C1：五项评审修复的当前纸面用例

独立期望取自 YOUR_OWNER t462u 的 P1-1/P1-2/P1-3=A 定案与 Claude PR#15 原评审 P2-1/P2-2；本批读取的是 Main 提供的原文，不声称重新核过线上状态。以下均为 **PAPER PASS，仅文案人工推演**，没有执行 launch、提醒、信号或安装。

| ID | Given / When | Then（独立期望） | 对照 / 结果 |
| --- | --- | --- | --- |
| C1-1 两路信号 | 同 task_id/board_row：Mac ready blocked seq=5，随后独立云 `-review` milestone wip seq=99；两路径各有 applied.json 记录。 | Mac ready 仍是执行端 R1 来源，跟进方/主机不变；云信号只 wake，不参与冲突优先级。每路仅与本路径 applied 值比 seq 并独立去重，绝不以 99 覆盖 5。 | lifecycle §6、SOP §9.3、H1/H2；PAPER PASS。 |
| C1-2 常驻 tab | 分别输入：① 可读且确认该 issue 无常驻/可沿用 tab；② 同 issue 已有设计 tab 或旧逐 PR review tab，身份已核；③ 云主机不可读或 unknown。 | ① 过既有授权/出口 gate 后 launch 一个 `<tid>-review`，WAKE 写旧映射（无则记无）与新身份，核一次 ACK；② 认作常驻沿用并记映射，不重复开；③ 不猜缺失、不启动副本。无 tab 不计派出失败，仅 pending/建 tab 不清零；实际出口/容量/主机派出失败才按原两次规则计数，成功实际派出才重置。 | lifecycle §5.2/§5.6、H1/H2；PAPER PASS。 |
| C1-3 夜间混合意见与 E | 23:48 读到独立可修 O2 和需 YOUR_OWNER 决策 O1；另一个 PR R1–R4 全齐、无需部署、尚无合并批准。 | 同回合先派已批 O2，再发 O1 聊天问句；另一行 E 合并请求同回合上板并发聊天，说明无需部署。不等待 08:00，也不产生 merge/deploy/手动 CI/main2 授权；E 仍停推。 | lifecycle §1/§2/§5.2/§5.6/§7、H1/H2；PAPER PASS。 |
| C1-4 夜间提醒去重 | 同行方案 v1 夜间首次有效交付；同夜重复 wake、08:00 H2；随后有效 v2。 | v1 首次同回合提醒一次，重复 wake/H2 不重发，v2 可提醒一次。H1/H2 共用行+版本记录，不按 signal seq 认新版；08/13/19 PT、cap30 和授权不变。 | lifecycle §2、SOP §7、H1/H2；idle-sensitivity 的 #10 AC-6/N5 同步；PAPER PASS。 |
| C1-5 旧扫描安装边界 | 当前只有仓内文档更新，H1/H2 与脚本未动；之后 owner 另获安装批准。 | 现在不宣称停用；届时先备份全文、移除 H1 整段 `arch_review_dispatch.py scan`（issue+PR），分别读回/可回滚；保留仓内/安装脚本，无本批运行或脚本改动。 | lifecycle §5.6、README、H1/H2；PAPER PASS。 |
| C1-6 规则入口 | 从状态机、全局规则、SOP §7、Claude/执行端片段进入 PR 发布/复评/修复。 | 每个所需入口链接可调用并指向 lifecycle 权威段；完整闭环保留在 lifecycle §5.2/§5.5/§5.6/§6 和可粘贴 H1/H2。其他已有职责/字段/示例保留，不用摘要替代完整授权、UNKNOWN 与 no-replay 保护。 | 上述五个摘要、lifecycle、H1/H2；本批本地链接/锚点检查；PAPER PASS。 |

## 交付与未验事项

A5、N1–N12、C1-1–C1-6 仅人工纸面核对；A1/A2/A3/A4/A6 **LIVE DEFERRED，非 PASS**。后续安装和自然样本需 owner 在已有授权内取证；本批不制造样本，不自动改线上 H1/H2、脚本、个人指令、凭据或 CI，不开新 watcher/routine，不发 live/dry-run signal。TDD 对文档豁免，不虚构 RED/GREEN；代码/测试节点无变化。Main 按批准范围负责仓库 CI、PR 发布、外部评审与后续验收，worker 仅交接文档与静态检查证据。
