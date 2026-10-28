# 工作流生命周期 A–G（操作版）

> 路径约定：`~/ray-docs` 仅为 helper 默认的参考布局；`YOUR_` 值须由部署者填写，涉及真实主机/出口/凭据的值只留本机私有配置。

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

版本：2026-10-26；交付文档，不代表已安装或已完成真实票试跑。
来源：workflow#3（历史示例，原记录不随公开包分发）、YOUR_OWNER 确认 OQ1–OQ5=A（历史示例，原记录不随公开包分发）。
全停纠偏来源：workflow#7 方案 v1 / OQ1–OQ5=A（历史示例，原记录不随公开包分发），纸面用例见 [idle-sensitivity](cases/idle-sensitivity.md)。
方案交付规则来源：workflow#10（历史示例，原记录不随公开包分发）、获批 `PLAN_S10.md` 与 OQ1=A（云电脑 Claude 交付后发一次信号）；本文仅交付规则，安装与真实方案验收另批。
PR 闭环来源：workflow#14 方案（历史示例，原记录不随公开包分发）、YOUR_OWNER 24h / 同 issue 常驻 tab 定案（历史示例，原记录不随公开包分发）、实现边界（历史示例，原记录不随公开包分发）。补充来源：YOUR_OWNER t462u（2026-10-26）明确选 P1-3=A「全天照常发聊天提醒（要拍板的问题、合并请求）」。这些决定覆盖原方案的夜间排队、聊天静默与逐 PR 临时 tab 写法；纸面推演见 [PR review loop](cases/pr-review-loop.md)。
原会话恢复来源：workflow#17（历史示例，原记录不随公开包分发）、YOUR_OWNER t461u/t477u 已批简化方案；t433u 取消夜间延后，PR#23 已合入 main `21301ba`；其发现/回执与归属证据规则按下述 #24 优先级集成，不代表已安装。历史父辅助结果与自然路径未证实的边界见 [Claude auto-resume](cases/claude-auto-resume.md)。
与 [新版 SOP](bot-progress-board-sop_2026-10-26.md) 同目录安装；本文件给出阶段与门禁，SOP 给出板列、G1–G4、扫描与提醒规则。

## #24 四角色总纲（已批，部署另批）

| 角色 | 看板 Page | GitHub | 恢复/交接 |
| --- | --- | --- | --- |
| 任务流 Bot | 唯一读写者 | 判断并分发 | 每小时兜底，问 YOUR_OWNER |
| 本机脚本 | 不读写，只推信号 | 仅云每五分钟发现动静 | 原任务缺交接续原会话一次 |
| Claude / Codex | 不读写 | 按 brief 交付 | 每次停手写当前批交接并驱动脚本；worker 交 Main |
| YOUR_OWNER | 读板 | 无须盯 | 回答板上决策问句 |

操作定义、记录 owner、送达确认、共享 100/day 预算与旧补丁废止范围见 [#24 总纲](cases/local-automation-design.md)。三种唤醒入口：本机脚本推送、云 GitHub 新动静、每小时 H2；08:00 保留早报。只有 Bot 写 Page；缺交接=卡住，由脚本一次恢复，失败交 Bot。未部署不得声称线上已生效。


## 1. 不变量与依赖

- Page 是进度唯一 SoT，只有 owner Bot 写；输入冲突按 YOUR_OWNER 明示 > GitHub 读回 issue 状态 > 最新执行信号 > Herdr 推断。聊天决定须同回合写回 issue，阶段不靠记忆。
- 不加板状态、helper 字段或阶段状态文件；#24 已批本机五分钟脚本和运行去重状态，待推送保留板行内容中，不另扩 Page 列。四个板状态仍是 todo/wip/blocked/finished；helper 仅收 wip/blocked/finished，15 字段见 [信号协议](board-signal.md)。
- `<tid>` 含 issue 号；tab/agent 命名 `<tid>-<role>`。Claude 设计/评审，Codex 实现，Bot 管板并关单。执行端不得代称别人正在做事，除非有对方 ACK。
- 所有 bot GitHub 评论以 `【LLM：…】` 结尾；YOUR_GH_OWNER 无尾标评论作为 YOUR_OWNER 本人意见。授权取明确原话，不从 CI 绿或模糊「行」猜测。
- H1 接本机脚本/GitHub 提示，H2 每小时，08:00 早报；共享 Bot admission 每日 100 次，超限事件保留并在早报/H2 报告。旧 30/day、三次 H2 与禁止定时脚本条文由 #24 废止；部署另批。授权内通知与 YOUR_OWNER/合并问句全天同次唤醒发送。
- CI_WATCH W1–W4/Y1–Y4 是待整合子规则，其 OQ（含断链自动新开 main2 等）尚待另批；本文件不批准这些自动化。只使用已有授权且实际核验的等待证据，未核实就标待核。云 Claude 的 E4 候选（launch.out start 无 end + 存活进程）可用性未验证，不能据此声称 working。

## 2. 阶段表与板面 bullet

wip/todo 仅一条短 bullet；blocked 可另加一条可直接回答的 `❓ YOUR_OWNER 需决策：…？`。表中时间是核验时间，技术身份放 evidence。

| 阶段 / 板状态 | 守卫与动作 | 谁接 / 退出 | bullet 模板 |
| --- | --- | --- | --- |
| A / todo | YOUR_OWNER 提问题或 G 开 follow-up；允许暂缺 issue。只入板，不派人；08:00 早报列待跟进 | YOUR_OWNER 说跟进 → B1；YOUR_OWNER 取消 → 人工取消完成 | `待 YOUR_OWNER 说跟进（入板日期）` |
| B1 / wip | YOUR_OWNER 明确说跟进；Bot 同回合开/补 issue、写【跟进】、派 Claude、刷 wip。brief 带精确板行名、task_id、issue 链接、YOUR_OWNER 原话、上一版方案与修改意见，要求按下述格式交付并发一次信号 | 云 Claude 常驻 `<tid>-review`（方案/代码共用），Opus 5.5/high，只设计；方案含 G1 初判、验收草案、≤5 OQ；有效交付 → B2 | `云电脑 Claude「<tid>-review」：出方案 v1` |
| B2 / blocked | 按下述 issue 证明核实最新方案已交付，等 YOUR_OWNER 拍板及点名实现端；先判交付，再看 working/等待。Bot 全天同次唤醒转述 ≤200 字+链接，按行+版本去重 | YOUR_OWNER 要改 → 同回合记【跟进修改】并回派 B1；最新方案与 G2 验收确认且 YOUR_OWNER 明确指定机器/agent → C；只答 OQ 未派人仍 B2 | `方案 vN 已出（issue 链接）`（无 OQ 加「无待定问题」）+ 下述对应 ❓ |
| C / wip | 最新方案有【方案确认】与已签验收，且 YOUR_OWNER 已明确点名实现端；无有效合并批准，R1–R4 未齐。按 YOUR_OWNER 指定派单，#421 容量仅供建议；brief 含方案、验收、batch、tab、handoff、禁止未批合并和 evidence 格式；所有开发 PR 每次唤醒按 §5.2 闭环 | mini/air Codex `<tid>-impl-main`；每扫描查 PR CI 与评审，变更通知执行端；R1–R4 齐 → E；需决策 → D | `mini Herdr「<tid>-impl-main」：实现中（PR#N）` 或 `执行端已停；等 PR CI；Bot 最迟 <下一个 H2 时刻> 核` 或 `处理评审意见 3/5（时间核验）` |
| D / blocked | G1–G4 或卡目标且必须等 YOUR_OWNER，覆盖 B1/C/F 的结果。G1 架构、G2 验收、G3 中途架构变化、G4 专属授权/合并/main CI 红等，完整定义见 SOP §3 | YOUR_OWNER 答后同回合记录、续派、改板，回原阶段 | `卡点一句话` + `❓ YOUR_OWNER 需决策：具体可回答的问题？` |
| E / blocked | R1–R4 同时成立，当次扫描必须进入；适用于所有合默认分支的 PR。执行端停手，Bot 全天发 ≤200 字说明 | YOUR_OWNER 明确批准 → F；YOUR_OWNER 要改或出现新提交 → C 重判 | `开发完成：CI 绿、评审意见已处理（时间核验）` + `❓ YOUR_OWNER 需决策：是否批准合并 PR#N 并部署到 <目标>？（回滚：<一句>）` |
| F / wip | 有效 head-bound【合并批准】；Bot 派执行端合并→等 main CI→在已授权范围部署→逐条验收 | 优先原 Codex；原 tab 不在可按现有授权用 `<tid>-impl-main2`、新 batch，不借待批 CI_WATCH 自动恢复。全 PASS 且 C1–C6 齐 → Bot 关单；下一扫描 CLOSED → finished | `mini Herdr「<tid>-impl-main」：已合并，部署中` 或 `验收 2/3（时间核验）` |
| finished / finished | issue CLOSED 且验收全 ☑ 或 YOUR_OWNER 已记录接受偏差；PR 合并本身不够。YOUR_OWNER 明确取消为人工例外 | 移完成折叠区；reopen 后重推导 | 完成依据留 evidence |
| G / 新行 todo | 范围外问题、上线后问题、合法转出的评审意见或实现中范围外发现；Bot 开 follow-up 并互链 | 新行从 A 等 YOUR_OWNER 跟进；父票按 OQ5 与 C1–C6 判断 | `follow-up：来自 #M（原因）；待 YOUR_OWNER 说跟进` |

### B1/B2 的方案交付、问句与提醒

下述新格式只约束安装后交付的新版方案；安装前已贴出的旧格式方案先按 [§5.7 存量迁移](#57-存量票迁移一次性仅在-f-执行) 核验，不因首行/结尾格式不同否定已交付的 B2。

有效交付同时要求：issue 上有 Claude 评论，**第一行**为 `【方案 vN】#M <标题>`，正文含方案（G1 初判、验收草案、≤5 OQ），结尾写 `Open Question：k 条` 或 `无 Open Question`，**最后一行**为 `【LLM：Claude@云电脑…】`；评论时间**严格晚于** issue 最近一次 `【跟进】` / `【跟进修改】` 记录。可只贴摘要并给出 `PLAN_S10*.md` 路径，全文作为补充证据；只有本地 PLAN 文件、信号或早于/等于最近跟进或修改的旧评论不算交付。H1/H2 都重新读 issue 核实，不以信号草稿直接改板。

- 有 OQ：`❓ YOUR_OWNER 需决策：#M 方案 vN 请拍板：① …；② …；（确认方案与验收后由谁实现？建议 <空闲的机器> Codex）`。逐条保留 OQ 要点，不把问题缩成仅问「确认吗」。
- 无 OQ：`❓ YOUR_OWNER 需决策：#M 方案 vN 可以实现了，派谁做？（mini Codex / air Codex；建议 <空闲的机器>）`。无 OQ 不是自动确认，派单仍须最新方案和 G2 验收确认。
- #421 容量建议仅供 YOUR_OWNER 选择；未明确点名机器/agent 不派。YOUR_OWNER 只答 OQ 时记录回答并保持 B2，只剩「派谁做」这一问；若尚未明确确认方案/验收，该门禁仍保留，不从「行」「可以」猜确认或人选。
- YOUR_OWNER 提修改时同回合在 issue 记 `【跟进修改】`、附原话/时间/链接并回派 Claude；该记录使此前的方案交付及针对旧版的确认不能用于本轮派单。新版评论必须晚于此记录，核实后重新 B2，不等 tab 停下。
- 全天同次唤醒发一条 ≤200 字提醒，含方案链接和问句；同一行同一版方案只提醒一次，H1/H2 共用现有 WAKE_/FALLBACK_ 记录去重，夜间已提醒的版本不在后续 wake 或早报重复。新版本才重新提醒。未收到信号、发送失败或日上限耗尽，由下一次现有 H2 按同样 issue 证明和去重规则兜底。

## 3. 每次 H1/H2 的阶段推导

**受理入口先发现，再做行级短路**：每个按原 `diff_id` 去重后新受理的 H1、每次 H2，先按 §5.6 对实际云主机当前默认 Herdr session 做一次恢复候选扫描，再续期 wait、行级短路或结束 wake。初始 `pending_dispatch=[]`、触发行无关、无开放开发 PR、跟进主机 Mini/Air、Mac Main 仍 working 或整行未 STOPPED，均不能跳过同任务云 Claude；F 的 PR 已 MERGED 也照核。重复 H1 不增扫描/唤醒。扫描只发现，不授新恢复资格；每小时 H2/共享 100/day 以 #24 为准，旧 #17 三次 H2/30 次条文废止。零动作也须有覆盖/缺口及父回执审计，UNKNOWN 不能当零候选。

先读所有开发阶段行的 issue/PR 当前事实、相关评论及记录、最新信号和 Herdr；包括非触发行，逐 PR 核当前 head/base、全部评论/评审、inline resolution、CI 和 mergeability，完整分页。信号只唤醒，GitHub 是 PR 事实来源；阶段每次重算，不另存。先执行 §5.2 中不依赖决策的授权内修复派单，再落 D 问句，不能因步骤 7 覆盖而漏派。

1. YOUR_OWNER 明确取消 → 记录取消后 finished；否则 CLOSED 且验收齐/偏差已接受 → finished。CLOSED 但验收不齐先执行 X18，不能落入完成。
2. 没有 issue → A todo；YOUR_OWNER 已说跟进则同回合先开/补 issue、写记录，再往下推导。
3. 没有【跟进】 → A todo。不得从 todo 自动启动设计或实现。
4. 有【跟进】、本轮尚未满足最新方案确认+G2 验收确认+明确实现端：先按 §2 核 issue 有效交付，满足即 B2 blocked，即使 Claude tab 仍 working 或旧 wait 称等方案/评审。YOUR_OWNER 只答 OQ 未指定实现端仍 B2，只问剩余派谁问题，不回 B1。若 YOUR_OWNER 最新修改之后尚无有效交付，已回派且确实执行 → B1 wip；未回派 → X14 本回合记【跟进修改】并回派。其他无交付情形再核真实执行/等待，不能用旧方案冒充本轮已交付。
5. 最新方案有【方案确认】、G2 验收确认且 YOUR_OWNER 明确点名实现端，无有效【合并批准】：R1–R4 齐 → E blocked（X15）；否则 C；C/B1/F 若 STOPPED 且无合法等待 → X19（§5.5、§7），S 为空的无人负责 → X14；S 非空、无 working 但非 STOPPED 时执行 §5.5 一次观察兜底。E 缺条件按 X16a/b 分流；合并门禁与合法等待并存时先按 §7 的等待约束判定。
6. 若最新 F 回报有原验收范围内未解决 FAIL，按 OQ5 回 C、原票 OPEN、新 batch（修复/重验或 YOUR_OWNER 明确接受偏差前不按旧批准直接回 F）。否则有有效【合并批准】且 issue OPEN → F wip，核验实际恢复方；STOPPED 且无合法等待 → X19，S 为空的无人负责 → X14；非 STOPPED 的无 working 行执行 §5.5 一次观察兜底。若已 MERGED 却无有效批准，按事实记录 F 并执行 X17，不能据此获得部署授权。
7. 任一阶段有未答 G1–G4 或卡目标且等 YOUR_OWNER 的问题 → D blocked，覆盖步骤 4–6；仅合并门禁缺口与其他 R 项合法等待并存的延后问法按 §7。B2/E 的自身决策问句保留对应阶段。
8. 结果与板不一致就纠偏，每次写 `row, from→to, 码, 依据`；不能以无 working 的旧 bullet 假装活跃。读不到主机时保持原状并标无法核验，早报报告，不强行 SSH。

有效合并批准必须引用对 E 问句或 §5.8 D 合批例外问句的明确回复，并记录批准时 head；须等于 PR 当前 head，合并后须等于实际合并的 PR head。批准后任何新提交使批准失效，回 C 重新核验并再问。记录可写 sha8，核验须唯一对应完整 head，不混淆 merge commit。D 例外同时记 `【合并批准】head=<sha8>` 与 `【门禁例外：R2，理由：…，原话链接】`（按实际豁免项填写）；只对该 PR 的该 head 生效，不形成仓级规则。

## 4. 每阶段完成检查

- A：只入板与早报；B1：同回合四步完成，≤10 分钟 ACK 窗口后必须看到实际开始。十分钟未确认按 §5.6 / #24 读 pane 一次并保留 unconfirmed，下一 wake 投递重推一次，再失败才 D；故障恢复另按一次预算，不盲重启。
- B2：先核 §2 的评论格式与严格时间先后，再转述方案/OQ及派谁问题；YOUR_OWNER 确认最新方案及验收、明确指定实现端后才发实现 brief。修改先记【跟进修改】再回派；只答 OQ 未指派继续 blocked。不凭 Claude working、旧 wait 或无 P0/P1 绕过 B2，不重复提醒同一行同一版。
- C：逐扫描核验 PR 当前 head 的 CI、完整评审输入和回应表；新未处理意见按 §5.2 同回合分流，核实原执行端已停且无在途命令后回派，不轮询。CI 红由执行端在范围内修，不自动 D；OUT_OF_SCOPE 且命中 G1 → D/G3。
- D：问句能一句话回答，查 YOUR_OWNER 是否已答；同回合记录决定并执行获批的下一步，不留旧 blocked。
- E：R1–R4 逐项核验；缺项按 X16a/b 承接，结构性缺口可报 gap，执行端不得抢发 ready。等待期间除 YOUR_OWNER 要求修改外停推送；修改后旧批准失效。
- F：核批准与部署边界，依次合并、main CI、部署、验收；main CI 红 → D/G4，不能自动重试到绿或部署失败 SHA。部署失败按方案中已获授权的回滚步骤回滚并回报，再问 YOUR_OWNER 修复重来还是 follow-up；没有回滚授权不得自行扩大动作。
- G：同仓开 follow-up（工作流/协调问题归本工作流仓），父票评论说明是否关闭及原因；全天简短告知，不把等待跟进的新行改成 blocked。

## 5. 门禁、评审、验收与恢复

### 5.1 E 的 R1–R4 必须全成立

| # | 条件与核验 |
| --- | --- |
| R1 | 执行端最新信号声明完成：status=blocked、event=blocked、合并问句，evidence 含 `ready: pr=#N head=<sha8>` |
| R2 | `gh pr view N --json headRefOid` 与 ready 一致；`gh pr checks N` 当前 head 必需检查全部 success。必需集按分支保护核实；无保护按全部检查，无 run/缺检查/未知不算 PASS，不新增 workflow 或代批 CI_WATCH |
| R3 | §5.2 评审回应表满足全部条件 |
| R4 | `gh pr view N --json mergeable` 为 MERGEABLE，且方案标「合并前」验收已 ☑；未标项均视作合并后验。UNKNOWN 要核验，不能当可合并 |

全部齐当次进 E；缺项按 X16a/b 与 X19 分流，不一律留/回 C。结构性缺口仅按 §5.8 单 PR/head 向 YOUR_OWNER 问例外，不把缺项算 PASS。ready/gap 是执行端声明，不由 Bot 代写。未经批准的合并按 X17，只记录、不自动 revert。

### 5.2 评审回应表（R3）

收集所有分页输入：PR inline threads（含 isResolved）、#426 Claude 在 PR/issue 的带尾标 P0/P1/P2 结论、YOUR_OWNER 在 PR/issue 无尾标评论，以及实际启用的其他评审机器人（是否启用待核）。空评论不等于已完成评审。

执行端维护一条可更新的 PR 评论并带尾标；每条意见对应原链接、严重性、结论与提交/依据：

```text
评审回应表（head <sha8>）
- [P1-1] <原意见链接，一句意见> → 已修 <sha8>；Claude 复核 <链接>
- [P2-3] <链接，一句意见> → 不改：<理由>
- [YOUR_OWNER-1] <链接，一句意见> → 已修 <sha8>
- [P2-4] <链接，一句意见> → 转 follow-up <issue 链接>（超出原验收：<一句>）
【LLM：<实际模型/工具身份>】
```

R3 同时要求：

- 每条意见有结论；inline 已 resolve 或回应表有对应行。resolve 本身不能替代实际修复验证。
- P0/P1 必须已修，修复提交后 Claude 复核一次；新 P0/P1 留 C。若拟不改/转出 P0/P1 或 YOUR_OWNER 意见，先 D 问 YOUR_OWNER，只有明确处置批准并留记录才可作为例外结案。
- 转 follow-up 只用于原验收范围外；范围内转出是改验收 G2，须 YOUR_OWNER 同意。P2 不改可由执行端给理由，不要求 P2 全清零。
- 最后评审后的每个新提交有对应回应行；修 P0/P1 或有评审未看过的改动必须复评。只有已记录在回应表的纯 P2 修复不强制全量复评；不能用一条回应掩盖其他未审改动。

### PR 发布、评审与回派闭环（§5.2 补充）

1. **同回合派当前 head**：开 PR/推新提交的信号到达后，Bot 重读 GitHub，按 R3 判本 head 是否需要初评/复评，生成 `review`，父代理本回合实际执行。方案评审和代码评审都由看板发起；每 issue 只保留一个云电脑 Herdr Claude `<tid>-review` tab（Opus 5.5/high），从方案到所有 PR/新 head 持续复用上下文，直到读回 issue CLOSED 才可关闭。存量的同 issue 设计 tab 或旧逐 PR review tab，先核验 issue/会话身份，再认作常驻 tab，记录旧名→常驻身份映射；不另开逐 PR 临时 tab，不能把另一个任务的 tab 拿来用。确认该 issue 没有常驻或可沿用 tab 时，按 §5.6 用 `launch` 新开 `<tid>-review`，在现有 WAKE_ 记录旧映射（无则记无）与新 tab/会话。主机不可达或状态 unknown 不是确认缺失，不能据此重复启动。未收到信号由每小时 H2 兜底，本机五分钟脚本发现动静，不增其他 watcher。
2. **先发布再叫醒**：reviewer 以精确 head/base 审阅，发布前再核身份，变化则刷新证据；先贴并读回 GitHub 结论 URL/作者/正文/审阅身份，再在云电脑本机发一次 §6 的 PR milestone。结论出现就结束该次「在审」，即使有未处理意见也应转修复/决策，不等回应表清零才承认评审已出。
3. **同回合先派能修的，再问需决策的**：完整收集所有来源及意见链接，批量分出已批契约内修复（含可修 P0/P1、决定要修的 P2、范围内 PR CI 红、与 main 冲突）和依赖 YOUR_OWNER 的架构/验收/授权问题。先按 §5.6 回派原 Mac 已停 Main/原 worktree，核无在途命令；brief 带意见链接、范围/负断言、回应表更新、原 PR 推修与进度信号要求。然后同回合 D blocked，保留评审的选项和推荐项并问 YOUR_OWNER。决策只阻止依赖它的工作；如 O1 待定，独立 O2/P2 照派。E 等合并期间仍停推，除 YOUR_OWNER 要求修改外不据本条推新提交。
4. **没有修复/决策项时查门禁**：缺执行端完成声明 → `notify` 原 Main 如实补 ready/review/gap，Bot 不代判；有冲突 → 派范围内解冲突（复杂/扩架构先问）；R1–R4 全真 → E blocked 问合并，无部署需求就说明无需部署。main-only CI 无 PR run 是 R2 结构性 gap，只有满足 §5.8 前提才问该 PR/head 例外，绝不算 CI PASS、不改触发/手动跑 CI。没有有效 head-bound 批准不合并/部署。
5. **有界失败，不假 wip**：本条处理一般新派评审失败；缺交接原会话故障恢复的失败/出口拒绝另按 §5.6 / #24，不借此自动重试。派不出只计实际出口、容量或主机失败；没有 tab 本身不计失败，按第 1 项核实后 launch。当前评审派不出第一次记录精确原因、时间、head、出口/容量/主机事实，bullet 写「评审派不出：<原因>；下次唤醒再试」。下一连续唤醒仍失败 → D，`YOUR_OWNER 需决策：PR#N 评审连续两次派不出（<原因>），等恢复还是暂停？`；成功实际派出才清零计数，仅排 pending 或创建 tab 不算成功。夜间也同回合发聊天问句。禁止后台 Claude、Mac Claude 或历史 dispatcher 绕行。
6. **有界复评**：同 PR 修复→复评到第三轮仍出现 P0/P1，停该循环问 `YOUR_OWNER 需决策：PR#N 第 3 轮仍有 P0/P1，是继续修、改方案，还是暂停？`，不自动第四轮。保留原意见与每轮 head/回应表/复核链接；不以新 head 清掉轮数，也不把所有失败当不同缺陷。

### 5.3 验收与关单（C1–C6）

Codex 在 issue 逐条回报 `验收 <编号>：PASS/FAIL，证据 <可读链接或路径>`，并发 accept 行。Bot 打开证据后按回报勾 ☑，不自行推断。存量「—」不是 PASS；缺口需 G2 确认。

| # | Bot 关单前必须核实 |
| --- | --- |
| C1 | PR 读回 MERGED；实际合并的 PR head 与有效批准一致 |
| C2 | 合并后默认分支准确 SHA 的 CI 全绿；PR CI 不能替代 |
| C3 | 方案要求部署时，执行端回报部署完成且证据可读；授权范围见下文 |
| C4 | 每条验收有执行端 PASS 并 ☑，或有 YOUR_OWNER 接受偏差的明确 G2 记录 |
| C5 | 无未答 ❓；最近 YOUR_OWNER 评论之后无未处理的 YOUR_OWNER 意见 |
| C6 | 如有 follow-up，已开票并与父票互链 |

全满足 → **Bot** 发带尾标关单评论（验收 n/n、合并提交、部署证据、follow-up），再关 issue；下一扫描读回 CLOSED 才 finished。Bot GitHub 关闭权限仍需核验，权限不足报告待处理，不冒称已关。执行端不关闭 issue。
F 验收全 PASS 发 `event=done,status=wip`，OPEN 不发 finished；C 阶段完成、PR 合并、单机结束只发 milestone。

OQ4=A：E 问句明确写部署目标与回滚方式、B 方案已有部署步骤时，一次批准可同时涵盖合并与该部署。实盘、资金、凭据、生产 cutover 必须在问句明确写出才算授权，否则另走 G4；CI 绿本身从不授予动作权限。

### 5.4 OQ5 失败恢复与 follow-up

原验收范围内失败：原票不关，回 C，同票新 batch 修复，保留 FAIL 证据；新提交重新绑定批准。要将范围内失败拆出须 D/G2 问 YOUR_OWNER，不能自己放宽验收。
范围外才开 follow-up；父票仅在自身 C1–C6 成立时关闭，不能因新票存在就关。

follow-up 最少含：标题 `follow-up(#父票)：一句问题`；父票/PR 与发现阶段；脱敏证据；现象、生产/资金影响、复现（不明写待核）；是否在父验收内及父票关否理由；不受影响验收；待 B 阶段 YOUR_OWNER 确认的验收草案；不含解决方案；末尾 LLM 尾标。新行 A todo 等 YOUR_OWNER 说跟进。

### 5.5 STOPPED、合法等待与无人跟进

先执行 §3/§5.6 的每 wake 独立云候选发现，再判下面行级 S/STOPPED 和等待；S/STOPPED、Main 状态或 pending 是否为空均不是发现入口的前置条件。

对板为 wip 的 B1/C/F 行，当次唤醒取跟进主机上名称前缀匹配 `<tid>-` 的全部 Herdr agent 为 S，含 Main、worker、investigator，B1 含常驻 review（兼设计）。**STOPPED** ⇔ S 非空、每个成员都是 idle/done 或下述现场确认已停，且不在 ≤10 分钟派单/launch 宽限内（含本回合或上回合 pending_dispatch 等 ACK）。Claude 退出后名字可能从 agent list 消失，须按本机 CLI help 补读 tab/pane inventory；只有可绑定当前 wip 行、原授权任务/会话的已停 pane 才补入 S，不以名字消失当作可新开会话。完成此核验后 S 仍为空才沿用 X14；主机读不到则保持原状、标无法核验并早报，不判 STOPPED，也不强行 SSH/启动重复工作。A 允许没人。

**Claude 现场确认已停**：原任务 pane 前台为 bash，且可见属于该原会话的 Claude 退出/`Resume this session with: claude --resume ...` 提示，并确认无在途命令，算已停；不能永远归为 unknown。bash 单独出现或 unknown 徽标单独出现均不够；Claude 仍在、命令活跃或是否在途无法核实时保留现场，不重启。普通退出也可能有 resume 提示，#24 不再要求猜 guard 原因：无本批交接即可按下节脚本恢复一次；已停身份与无在途命令仍须独立核清。无法绑定/读取时保留 UNKNOWN，不猜名字、ID 或停止时间。

先将指向 idle/done 或现场确认已停 tab 的 resume 按 `resume=bot` 处理，再核 V1–V3；合法等待须三项全成立：

| 条件 | 核验 |
| --- | --- |
| V1 未兑现 | 对象在当前 head（设计阶段为本轮方案）仍未发生。plan：先按 §2 核有效交付，已交付即等待已兑现，直接 B2；Claude tab working 或旧 plan/review wait 都不能把该行留 wip。未交付才能核真实等待。review：尚未完成的 requested reviewer，或看板已在常驻云 review tab 实际派该 head 且尚无 Claude 带尾标结论，或评审人明示稍后评；该 head 已有评审结论即该次评审等待已兑现（其他已核验的待出评审仍单独算在途）；评审已贴但有待办则转评审修复，不再等同一已贴评审。ci：该 head 有 queued/in_progress run；run 结束为已兑现；无 run 且触发规则不会产生则无对象。market/runtime：事件未发生且观测来源可读。 |
| V2 核验时限 | working 且实际盯对象的恢复方：next_check 须晚于本次唤醒。`resume=bot`：本次重新读回同一当前 head 对象、V1 仍真，就将 next_check 续到下一个现有 H2；旧 next_check 已过不使该被动等待失效。V1 为假或 UNKNOWN 不得续期。 |
| V3 有真实恢复方 | working 且实际盯该对象的 agent，或 `resume=bot`，由 Bot 下次唤醒核。idle/done tab 不作为自行恢复主体。 |

`resume=bot` 且 V1 读回为真时可留 wip，bullet 写 `执行端已停；等 <对象>；Bot 最迟 <下一个 H2 时刻> 核`，本次读回与续期记入现有 WAKE_/FALLBACK_，不写「Main 继续监控」。纯等外部评审不 blocked 只在 V1 为真时成立；已兑现、无对象或 working 恢复方时限已过的等待无效，STOPPED 时进入 X19。对象读不到或身份未核明则标无法核验、进早报，不盲续期，也不据此重复启动。未批 CI_WATCH/未验 E4 不算恢复证据；不增加 wake，被动等待最坏到下一个每小时 H2（例如 19:00→20:00；旧隔夜间隔废止），CI/市场等不因跨若干 H2 或累计时长自动升级；云 PR review 的兜底另按下面有界规则，不得无限续等。

**云 PR review 的兜底**：先核 §5.6 / #24 的当前批缺交接恢复及已持久化在途记录；旧 guard-only 条件废止。脚本为主，Bot 只对确认漏报且满足原身份/原生活动/无在途守卫的任务兜底一次，不另开恢复预算。其余情况，只有当前 head 已实际派、GitHub 尚无本次结论才能写「等 Claude 评审 PR#N（已派 <时间>，Bot 最迟 <下个 H2> 核）」，派单日志单独不够。到派出后的下一次定时 H2 仍无结果，只读该常驻 tab 一次。确认已停且无在途命令时，允许同 head 在同 tab **重派一次**（一般 review 同 head 去重的有界例外；不重置 #24 当前 batch/session 的一次恢复预算）；这次仍无结论就问 YOUR_OWNER，不再循环。unknown 本身既非 working 也非 stopped；在途命令/不可判定状态保留，不重派，按无法核验记录并由现有 H2 核。不是新增轮询或 CI_WATCH 自动恢复授权。

**无 working 的观察兜底**：S 非空、派单宽限已过且非 STOPPED（如等输入、权限弹窗或 unknown），只读相关 pane 一次并记录可见事实。确认已停/等输入/权限卡点且无在途命令时，仍先核 V1–V3；无合法等待按 §7 X19 顺序给出结果，确需 YOUR_OWNER 的权限走序 2，授权内下一手走序 3。若有真实在途命令或 pane 不可读/无法判定，保持原状、明确写「无法核验」并进早报；保留在途命令，不将 unknown 徽标单独当已停或正在 working；旧仅 guard-stop 恢复条件废止；当前批缺交接恢复只按 §5.6 / #24 的身份、原生完成证据与一次预算核验，未知不自动续派/重启。

B1/C/F 有 working、合法等待或有效派单宽限才算在跟；B1 仍须先核 §2 交付，已交付优先 B2。S 为空且无人跟进按 X14 当回合实际派下一手；STOPPED 无合法等待按 §7 X19。不自动 wip→todo。已授权 PR 评审修复、解冲突、补完成声明及云评审全天同样回派；其他未预授权工作不得据此启动。不伪称 working；真正 YOUR_OWNER 决策照常改 blocked，同回合发聊天问句，夜间同样适用。B2/D/E 每扫描查 YOUR_OWNER 是否已答，已答同回合记录，门禁齐备才续派；B2 只答 OQ 未明确指派仍 blocked，其他待派按已有授权留痕。

### 5.6 派续由父代理执行（pending_dispatch）

非云端 Main、H1/H2、Bot 与父代理收到东京/生产只读排查请求，按 [全局规则：东京与生产只读排查（YOUR_OWNER t529u）](bot-global-rules.md#东京与生产只读排查) 交给任务流 owner。H1/H2 只写 `pending_dispatch` 的既有 `kind=notify`（目标：任务流 owner/云电脑本机通道），父代理送达；owner 核实执行授权后，经既有 t475u 本机原生机器通道在云电脑本机 Shell 执行 SSH 并回传证据。请求范围、授权依据、结果位置及通道不可用处理均按全局规则；`notify` 只转交请求，不授予执行权限、不启动 Claude，不新增 kind，也不用 `review`/`launch` 承载 SSH 排查。SSH 不以 Claude/Herdr 或 Claude 专用 YOUR_PROXY 出口检查为前置；不得借派续重放已停止的 #21 FIX-01/R2 wrapper 修复。Claude 方案/评审仍遵守下述云 Herdr、出口与授权规则；本段不改 R2 CI、合并或部署门禁。

- H1/H2 子代理在本次 WAKE_/FALLBACK_ 留证，同时由 owner Bot 在板行持久保留 `pending_dispatch` 待推送列表（旧只存 wake 文件规定废止），每项含 `row, tid, kind, 目标 tab/主机, brief 路径, 授权引用, 依据码`；父代理执行派续。
- kind 仅六种：`resume` 给现有 `<tid>-*` tab 续派（X14/X19、YOUR_OWNER 已答）；`launch` 按已有 brief 新开 `<tid>-<role>`（B1 跟进、B2 回派、C 初派、F 已批，以及 §5.2 核实缺失的 issue 常驻 review tab）；`notify` 告知执行端 X16a 缺项或 X19 补声明，或向任务流 owner/云电脑本机通道转交上述只读 SSH 排查请求（不授予执行权限）；`review` 派 Claude PR 评审/P0P1 修后复核；`ask` 在 B2/D/E 问 YOUR_OWNER；`close` 在 C1–C6 齐后评论并关 issue。
- 涉及 Claude 的本次派单先按 [Claude 出口纪律 §1–§3](claude-discipline.md) 核验将实际运行 Claude 的云主机 YOUR_PROXY 代理：只认规定代理命令退出 0 且去首尾空白后的单个 IP 恰为 `YOUR_EGRESS_IP`；直连 IP（含正常的 `YOUR_DIRECT_IP`）不得作闸门，错误或无法核验为本次出口门禁 blocked_now；首次失败不自动转板面 blocked，PR 评审连续第二次 wake 派不出须按 §5.2 问 YOUR_OWNER。egress_ok 只清除此项检查，不替代其他授权/门禁；除本节 #24 已批当前批缺交接且身份/无在途均核实的一次原会话恢复外（旧 guard-only 条件废止），不授权任意启动或恢复，不自动重放历史 pending_dispatch。H1/H2 使用 [出口补丁](../templates/H1_H2_PROMPT_PATCH.md)；kind、父代理执行、ACK 保留；PR 同 head 有界重派、24h 授权按本节与 §5.5。
- 父代理同回合执行并回写 `dispatch_applied_at` 与结果，板行 pending 保留编号/目标/时间/attempt。派单十分钟无 ACK/新 working 先只读 pane 一次记因并标未确认；下一 wake 由 Bot 重推一次，第二次仍未确认才问 YOUR_OWNER，旧首次无 ACK 即问的规定废止；成功提交不当 ACK。原会话故障恢复严格另按 #24 一次预算，start/prompt/ACK 失败直接交 Bot，不借投递重推重启会话。
- 去重键为 `(row, kind, 依据)`，10 分钟宽限内不重复派；同一 PR head 不重复 `review`，一般 review 仅 §5.5 确认停止、无在途命令的同 tab 一次重派例外；旧 session+停止 occurrence 无限恢复规则废止；下述 #24 原会话恢复固定为当前 batch/session 一次，不是一般 review 重派豁免。X19 另按 §7 的 `(row, X19, head, 结果)` 去重，不因宽限到期重复派同一动作。
- #14 已批准的 PR 评审/复评、范围内修评审、解冲突、补完成声明 24h 执行，不排到 08:00；授权内聊天提醒（含 YOUR_OWNER 问题、E 合并请求）同回合全天发送。其他工作按其已有授权；无授权不启动。
- 原 Mac Main 已停时复用其会话/worktree，先核任务身份、dirty 工作和无在途命令。原 tab 确认不在才按现有容量及已有授权选空闲 Mac、用 `<tid>-impl-main2` 与新 batch；容量/授权不足则问 YOUR_OWNER。不能把主机不可达当 tab 丢失，不借 CI_WATCH 待批 OQ 自动新开。
- owner 另获安装授权后须从 H1 完整 prompt 移除整段 `arch_review_dispatch.py scan` 调用（issue 和 PR 扫描全部移除），统一由看板在常驻 tab 派；不保留独立旧扫描绕过看板/tab 规则。本批不改仓内脚本或已安装脚本，不声称 live 已停。备份/全文读回/回滚见 [H1/H2 追加稿](../templates/H1_H2_LIFECYCLE_APPEND.md)。
- pending_dispatch 不产生新授权：仅续做已记录范围；合并仍须 head-bound【合并批准】，部署按 OQ4，实盘/资金/凭据仍走 G4。

#### #24 本机原会话恢复为主，#17 Bot 兜底

PR#23（历史示例，原记录不随公开包分发） 已合入 main `21301ba4d9db5a3cd77748ea90ed8eb0625beb37`。#24 后批定案优先：本机脚本为主、无当前批交接触发、原 batch/session 一次恢复、H2 每小时、Bot 共用 100/day；旧 #17 的 Bot-only、guard-only、30/day、08/13/19 和每新 occurrence 重置次数规定废止。保留其发现先于等待短路、真实 inventory/UNKNOWN、父执行回执与具体 guard 归属安全证据。可选 runner 的 manifest/native 完成证明设计见 [#24 总纲](cases/local-automation-design.md)；合入源码不等于 SOP/routine 已安装或 live 验收通过。

##### 发现、资格与父执行

0. **实际发现与零动作审计**：依当前 CLI help 核实际云主机、当前默认 Herdr session 与真实 agent/tab/pane inventory，不用旧 `herdr437`/猜测 ID/继承环境代替。跨行映射当前已授权 wip 的云 Claude，名字退出后用同任务可证实历史映射与现场交叉核对；不因 Mac Main working、空 pending、无 open PR 或 F 已合并跳过。每次在现有 WAKE_/FALLBACK_ 记扫描时间、主机/session、inventory 覆盖范围/缺口、逐候选处置及空 pending 原因；缺失/不可读为扫描不完整/UNKNOWN，不能写“零 eligible”。告警读取的 UNKNOWN 单列，不拿它代替 inventory 覆盖事实。只增加既有证据文本，不新建 registry/cursor、阶段状态文件或 helper 字段。
1. **当前任务资格和无在途**：仅 active、原授权任务/当前批未交接，原 task/tab/pane/name/session/model/effort/worktree 唯一且匹配，才进入 #24 恢复核验。blocked、已交付/DONE（含故意杀已交付试跑）、preserve/do-not-resume、暂停/撤单、身份歧义均不续；不把旧 DONE/hint/等待 bullet 当本轮证明。working/busy/unknown、活跃或未核明命令不 start/prompt，保留 dirty 工作。前台 shell 或 interactive_ready 单独不证明无在途；沿用 #24 原生 call/handle 完成证据、进程后代/PID 出生身份、cwd 与可归属完整返回守卫，stdout 不作完成证明。
2. **一个预算，不与脚本竞争**：先核同一当前 batch/session 的本机恢复意图/结果、ACK 宽限和已消耗预算。脚本已有 pending/started/failed 或未知提交，Bot 不另 queue/start/prompt；一次恢复后再停仍无交接或 start/prompt/ACK 失败交 Bot 问 YOUR_OWNER，不能用新 kill/新 head/普通派单重推重置预算。不回放历史 pending。Bot 只对确认脚本漏报且原资格/无在途与预算都可核的候选兜底，优先由父代理驱动本机 runner 使用同一锁/记录；无法核清或无法通过原本机意图守卫时只报 UNKNOWN/按既有规则承接，不另开人工恢复额度。
3. **出口、执行与一次 ACK**：对合格 Claude 核本次实际云命令 `curl -s -m 8 -x YOUR_PROXY YOUR_IP_ECHO_URL`；仅 exit=0、trim 后单个 `YOUR_EGRESS_IP` 放行，失败/UNKNOWN 留证等下轮，不转直连、不与 guard/wrapper 对打。资格齐才排本次既有 `kind=resume`，带原目标/brief/授权和本批预算依据；父代理动作前重核状态、交付、保留指令与无在途。shell 先原 pane/name 恢复原 session/model/effort，绝不往 shell 发自然语言；readback 已新 working 不再 prompt，busy/unknown 不 prompt，只有原身份 idle/done+ready 且命令证据完整才固定提醒：

   ```text
   Continue the original brief from where you stopped. First check files already written and issue/PR comments already posted; do not post duplicates. Deliver as the original brief says.
   ```

   沿用当前批编号 ACK/新 working 的 ≤10 分钟核验；CLI accepted/pending 不算开始。恢复失败/未确认只读 pane 一次记因并问 YOUR_OWNER，不盲重启。普通派单的十分钟 unconfirmed、下一 wake 重推一次、第二次失败才问是**投递**规则，不授权再启恢复。既有 wrapper 再验、其他安全/容量/合并部署门禁不变，03:40 PT 也不排到早报。
4. **父回执与分层上报**：父代理消费/核对本 wake 每项 resume，结束 wake/刷新板前逐项链接 `dispatch_applied_at`、实际 start/prompt/身份/ACK/继续工作，或精确未执行原因；无动作同样写候选处置与空队列原因。缺回执标未证实，不补造 applied 时间，不因队列/CLI accepted/旧 waiting 宣称成功。分别记事件观察（如有）、候选资格、本次出口、排队、父执行、原身份 ACK/续写各层来源/时间或 UNKNOWN，不用一个布尔值代替全链。仅在事实未观察时才写“等自然 guard”；已见告警但归属/资格/续跑未明写“告警已见，受影响会话/续跑待核”。无 wake 的等待与已有 wake 漏扫描/执行分开取证，缺日志不证明未执行。只有 Bot 写 Page，执行端仍按本机交接推信号。

##### 仅在声称 guard kill 归属时

#24 一般缺当前交接恢复不要求猜停止原因。若声称某会话由一次 guard kill 停止，须保留 #23 的独立严格证据：实际云 `YOUR_GUARD_SCRIPT` 写入的 `YOUR_GUARD_ALERT_LOG`，杀线精确含 `已立刻停掉所有 Claude 任务`，时间为北京时间 UTC+08:00。记录实际原行、来源主机/路径与带时区观察时间；文件缺失/不可读/只有别机或 Mini 镜像为 UNKNOWN，不说“无 kill”，全局告警单独不证明会话归属或未交付资格。

一个 session 归属到该次 kill 的三项必须 **AND** 成立：

- 在该实际云按精确 session 找到唯一既有主会话 `~/.claude/projects/*/<session>.jsonl`，不用 subagent 文件或杀后 `~/.claude/sessions/<pid>.json`。保留当前/latest mtime 与告警的源时区、实际 mtime，归一时间并记带符号秒差 `Δ = t_mtime - t_alert`；只认已批“数秒内 / a few seconds”秒级对齐，不扩为分钟或另造窗口。来源/时区/精度/唯一性不明、mtime 不匹配均 UNKNOWN。
- 匹配后无更晚写入，既有动作前重读同一文件元数据；mtime 或文件变化即使仍在数秒内也使旧匹配失效，不挑历史 mtime，不忽略后续写入复用 occurrence，不加轮询/daemon。
- 同一原 pane 为 bash 且仅有该精确 session 的 resume hint；新 invocation/多个不匹配 hint 不许挑方便的旧 session。普通退出、徽标、旧 hint、全局告警各自都不够。

缺任一项就不宣称该 guard 归属，不把 UNKNOWN 时间填进带 kill 时间的提醒，不用不实归属启动会话。若另有**独立完整**的 #24 当前批未交接/身份/原生无在途/本批预算证据，仍只按一般缺交接路径核验并用上面的通用提醒，不借告警产生新资格；独立资格不全则不恢复。归属全真也不代替授权 wip、DONE/保留指令、无在途、新鲜出口及一次预算/ACK，DONE 试跑不因此复活。

#17 历史原文及实际父辅助试跑证据（历史材料未分发，不是安装依赖） 原样保留：曾报告同 pane/name/session 恢复续写，但未走自然 H1/H2，且有一次 post-resume prompt 未 ready；不能抹成“全部 live 未跑”，也不能提升为自然全链或 #24 验收 PASS。当前验收分层见 [恢复用例](cases/claude-auto-resume.md)。本批只集成文档，不安装/操作现场。

### 5.7 存量票迁移（一次性，仅在 F 执行）

本次新增的旧方案格式迁移随获批安装执行，安装后的首次 H2 核对现有 B2 行，不要求这些行先进入 F；其余存量标记迁移仍按原 F 阶段限制。

- 安装前已贴出的 Claude 方案评论，即使首行或结尾不符合 §2 新格式，仍按旧判定核实本轮交付：须有真实、带 Claude 尾标的 issue 方案评论，时间严格晚于最近【跟进】/【跟进修改】，且方案之后 YOUR_OWNER 没有新回复。符合时由 Bot 发带尾标的【迁移记录】，附原评论链接、交付时间、版本号与 OQ 条数；不要求 Claude 重贴。新格式只管安装后的新版方案，不能借格式迁移复活早于或等于最近跟进/修改的旧方案，也不能绕过 YOUR_OWNER 后续修改。
- 安装前已在 B2 且满足上述旧判定的行保持 B2 blocked，问句按 §2 新模板改写；只因旧格式不同不得回 B1、走 X19 或重新派 Claude。迁移记录不代替方案/G2 确认与明确实现端；原评论、版本或 OQ 条数无法核实时保留 UNKNOWN，按本节澄清规则处理，不编造交付或把未知当无 OQ。
- 对未 finished、有 issue、缺标记的存量行，Bot 从聊天、`YOUR_OWNER_DECISION.md`、`DISPATCH_*.md`、YOUR_GH_OWNER 无尾标评论找 YOUR_OWNER 原话，在 issue 发带尾标【迁移记录】，逐条写【跟进】/【方案确认】/已有授权范围，附原话、时间、链接。
- 找不到或含糊时不猜，合为一条批量 ❓ 同回合聊天询问，夜间同样适用。
- 已合并历史 PR 只记事实；之后的新 PR 一律核 R1–R4，齐则 E，结构性缺项仅按 §5.8 D 合批例外。存量验收「—」保持不变，不回填口径。
- 迁移前，存量行缺标记不得据此按 §3 推为 A todo；保持原状态并标「待迁移」。

### 5.8 D 合批例外（逐 PR/head）

只有执行端在已有授权内结构性补不了的 R 项缺失，其余 R 项已成立，且执行端已有完成声明（ready 或 §6 gap）时，才可问合批例外；未声明完成先走 X19 序 3 请执行端补声明。Bot 不代判完成、不补写 ready/gap。最新执行端已明确 blocked 并指出结构性缺项，即使旧格式缺 ready/gap，也须 X16b 承接成 D，保留原问题、已知缺项及声明缺失，不冒称 ready；是否满足合批例外前提另按事实核验，不能又驳回成静默 wip。

问句须写 PR/head、缺项、批准后行为与替代出路，例如（#439 历史 main-only CI 场景，不代表本仓触发政策）：

> ❓ YOUR_OWNER 需决策：PR#452 head a3c70c85 评审已无未处理意见，但本仓 PR 不跑 CI（只在 main 跑），R2 无法满足。是否批准照此合入、以合并后 main CI 为准（红了停下问你）？部署另批。（不批的话请指示：给 PR 补 CI 触发 / 先跑一次手动 CI / 其它）

替代出路是待 YOUR_OWNER 决策的选项，不授予改 workflow 或手动触发权限，手动 run 是否计入当前 head 检查仍需核验。批准按 §3 绑定并记录，只豁免点名的门禁；F 的 C2 准确 main SHA CI 全绿仍是硬门禁，红 → D/G4，不自动重试、部署或改仓级政策。

## 6. 信号 evidence 约定

helper 15 字段及退出码完全不变，仅在 evidence 加文本行。summary 每行一个人能读的结论；完整 SHA、run/PID 等只放证据。

| 行 | 何时 / 格式 |
| --- | --- |
| wait | 已授权等待前：`wait: kind=ci repo=<r> ref=<sha8或pr#N> resume=<working且盯该对象的tab或bot> next_check=<带时区ISO>`；review/部署等填真实 kind，按 §5.5 核 V1–V3 |
| review | 更新表后：`review: pr=#N ledger=<评论链接> open=<未处理条数>` |
| ready | R1–R4 全满足：`ready: pr=#N head=<sha8>`；status=blocked,event=blocked，question 为具体合并/部署问句，随后停手 |
| gap | 开发已完成、其余 R 项已核、仅点名缺项在已有授权内补不了：`gap: pr=#N head=<sha8> missing=R2 reason=<一句原因>`；可与 ready 同发，但不代表缺项 PASS；status=blocked,event=blocked，question 按 §5.8 |
| accept | F 每项回报：`accept: <编号>=PASS\|FAIL <证据链接>` |

执行端要 done/idle 时，wait 的 resume 写 `bot`；若写自己则须保持 working 真正在盯。等待对象兑现后仍 working 的执行端，在停手前须发一次 milestone 或 blocked，不能静默 done。

start 用于派单启动；milestone 用于等待/评审/阶段进展；blocked 用于 B2/D/E；done 只用于 F 验收全 PASS，status=wip。

#24 部署后旧执行端直接 POST 完成信号步骤废止：先贴好并核实 §2 issue 评论，再写当前批 handoff（evidence 含评论 URL/PLAN）并立即驱动本机脚本；以下保留 helper 协议与部署前 Main 兜底约定，不重复发。OQ1=A 的本机信号限定：在**云电脑本机**用现有 `~/.local/bin/board-signal-post --task <task_id>` 发一次 `status=blocked,event=blocked,host=云电脑` 信号。brief 必须给出精确 board_row、task_id 与 issue；question 用 §2 对应问句草稿，evidence 含评论 URL 和 PLAN 路径（若有），pr 暂填 issue URL。任务内方案评论发布与这一次完成信号，是通用「不授权外部写入」的明确例外，不扩展为其他外部动作。信号仅叫醒 Bot，Bot 必须读 issue 核验；Claude 不写 Page。

脚本或部署前 Main 仍使用 [board-signal](board-signal.md) 的全部 15 字段、现有状态、云端本机 seq+1、带时区 as_of、本机凭据与全天授权内提醒规则，计入 Bot 共享每日 100 次 admission；本机五分钟脚本为 #24 已批例外，不加 helper 字段或跨端 relay。退出 4 保持全部输入（含 seq/as_of）相同最多重试一次，仍失败停手报告待投递；退出 3 保留信号、报告本机配置缺失/不合格，不盲重试或自行扩大凭据修改；退出 1/2 按原协议处理，不套用通用重试。没收到信号仍由 H2 核 issue 兜底。可合并的具体指令见 [Claude 模板](../templates/CLAUDE_SNIPPET.md)；本文不执行安装、信号或生产部署。

### PR 评审阶段的单次云端信号（§6 补充）

与 #10 **设计交付 blocked/blocked** 区分：同一个常驻 tab 在 PR 阶段发布并核实 GitHub 结论后，只在云电脑本机用现有 helper 发 **一次 `status=wip,event=milestone,host=云电脑`**，不是 ready/批准。使用 `--task <原任务目录>-review` 写独立 `~/ray-docs/任务流/<原任务目录>-review/BOARD_SIGNAL.md`；`task_id`、`board_row` 与 Mac 原任务完全相同，`--task` 目录名不等于身份字段。Mac 原目录和云 review 目录必须不同，不能共写一个信号文件/互借 seq。使用既有 15 字段及同路径 seq 规则（先核本机信号和本机同路径 applied 记录，确认不存在按 0，取最大值 +1；不可读不当不存在），不增字段。`pr` 为 PR URL，summary 短句「Claude 评审已贴：要修 N 条 / 要 YOUR_OWNER 定 M 条 / 无阻塞」，evidence 为 issue/PR、review URL、审阅 head/base 和恢复方。`-review` 路径信号只叫醒，不是执行端信号；不参与 R1、冲突优先级，也不改变跟进方/跟进主机。seq 只与同一路径的信号及 applied.json 记录比较，不能按相同 task_id/board_row 合并两路序列或跨路径比大小；例如 Mac ready seq=5 不被稍后云 review milestone seq=99 覆盖。Bot 每次重读所有开发 PR；不能把 summary 当 R3 通过。

发布权限仅限受派任务的结论与这一次信号，不授权写 Page/其他任务、merge/deploy。沿用本节原退出码、秘密、带时区 as_of、逐主机本地执行；共享 Bot 100/day、每小时 H2 兜底；退出 4 仅原样一次重试，不额外生成 seq 冒充重试。完整派单见 [PR review brief](../templates/PR_REVIEW_BRIEF.md)。本仓模板未应用，也未试发信号。

## 7. 纠偏码 X14–X19

沿用已有 X1–X13，不重新定义尚待批准的 CI_WATCH X13 自动化。

| 码 | 判定 | 动作 | 夜间 |
| --- | --- | --- | --- |
| X14 | B1/C/F 无 working、合法等待或有效派单宽限；STOPPED 优先走 X19，S 为空沿用 X14；非 STOPPED 的无 working 行先按 §5.5 一次观察，不盲派 | 当回合实际派续，不能派且需决策 → D；不降 todo | §5.6 已批 PR 下一手全天派，其他工作按已有授权；不伪称 working |
| X15 | R1–R4 齐但仍 wip | 当次进 E blocked，补合并问句 | 同回合改板并发聊天问句 |
| X16a | E 缺项在已有授权内补得了，且有 working 或本回合可派的真实恢复方 | 回 C，issue 写缺项，实际 notify 并核承接；不能仅计划派单 | §5.6 已批 PR 补缺全天派；其他按已有授权 |
| X16b | E 缺项结构性/需政策或授权而补不了，或执行端已对该缺项明确 blocked 提问（含旧格式无 ready/gap） | 不得只驳回留 wip；改 D 问句，issue 写缺项/出路，执行端停手；合批例外前提按 §5.8，不代判完成 | 同回合改板并发聊天问句 |
| X17 | 已 MERGED 但无有效 head-bound 批准 | 记录 F 事实、issue 与早报报违规；不自动 revert，不据此部署；需 YOUR_OWNER 决策则 D | 同回合记录并发授权内聊天提醒 |
| X18 | CLOSED 但验收有未勾且无 YOUR_OWNER 偏差接受 | 不标 finished，blocked：`❓ YOUR_OWNER 需决策：#M 已关但验收 k/n，是接受偏差还是 reopen？` | 同回合改板并发聊天问句 |
| X19 | B1/C/F 为 wip、STOPPED 且无合法等待，或 §5.5 一次观察已确认停在输入/权限等卡点、无在途命令且无合法等待 | 当次按下表顺序给出一个结果并更新真实 bullet/上次更新；不得无动作留 wip | 已批 PR 下一手全天派；D/E 同回合发聊天问句 |

每次纠偏写 `row, from→to, 码, 依据` 到现有 WAKE_/FALLBACK_ 证据；不加阶段存储或新 watcher。

### X19 判定顺序与承接

先按 §5.2 派不依赖决策的授权内修复，再自上而下落板；D 决策不短路独立修复。记录 `row, from→to, X19-<结果>, 依据`：

| 序 | 条件 | 结果与板面 |
| --- | --- | --- |
| 1 | R1–R4 全齐 | X15 → E blocked + 合并问句。 |
| 2 | 需要 YOUR_OWNER 决定：① 结构性 R 缺口（如 main-only CI 无 PR run、分支保护读不到、需改触发政策），合批例外先核 §5.8；② 最新信号/handoff 为 blocked/BLOCKED/OUT_OF_SCOPE 且带问题；③ 下一手命中 G1–G4；④ 无主机/容量/授权而派不出，或持久派单在下一 wake 一次重推后仍无 ACK/实际开始（首次十分钟无确认先标未确认；原会话恢复失败按 #24 单次预算直接交 Bot） | D blocked，写缺门禁、可选出路与可回答 ❓。仅缺完成声明且未有执行端 blocked 问题时，不抢问合批例外，走序 3。 |
| 3 | 已授权下一手可做：处理评审意见、修范围内 PR head CI 红、派 P0/P1 修后复核或新 head 必需再评审、如实补 ready/review/gap 完成声明、F 剩余已授权验收步骤 | pending_dispatch 用既有 resume/notify/review（review 沿用 §5.6 同 head 去重），父代理同回合执行。wip：`执行端已停；Bot 已派 <谁> 做 <什么>（时间）`；已批 PR 下一手夜间也实际派，不写待 08:00 或旧等评审/CI。 |
| 4 | 无法判定下一手 | D blocked：`❓ YOUR_OWNER 需决策：#M 执行端已全停、下一步不明，是续派 <谁> 做 <X>，还是暂停？`。 |

- 合并门禁缺口与其他 R 项合法等待并存时（如 Claude 已派未贴），先保持 wip 等该项兑现，bullet 写 `执行端已停；等评审；Bot 最迟 <下一个 H2 时刻> 核；评审出来后需 YOUR_OWNER 定 R2 例外`；兑现后下次唤醒再分流。与合并门禁无关的 G1–G4 仍立即 D，不能用等待延误。
- 序 3 派出后按 §5.6 的持久送达规则：十分钟未确认先标 unconfirmed、下一 wake 重推一次，第二次失败才问 YOUR_OWNER；旧首次无 ACK 即 D 的规定废止。宽限内不判 STOPPED；恢复 start/prompt 与普通派单投递重推分开，#24 原会话恢复预算不能重置。
- 同一 `(row, X19, head, 结果)` 在同一 head 上只发一次 pending_dispatch/问句；结果已问未答保持 blocked。head 变后重判；§5.5 确认停止的一次同 tab review 重派，以及 §5.6 / #24 当前 batch/session 的一次原会话恢复须分别留证；旧每次 guard-stop 可再续规则废止，不因新 occurrence 重置预算，也不授权一般 review 反复重派；等待兑现或 ACK 失败等事实变化仍按顺序核验并记录新结果，不用去重保留过时 bullet。每次 X19 刷新上次更新与真实状态。
- 驳回执行端 blocked 必须同回合有承接：X16a 按 §5.6 全天实际派已批 PR 工作，或 X16b 进 D；「驳回、无 ❓、无派单且全停」是违规，下次唤醒按 X19 纠偏。
