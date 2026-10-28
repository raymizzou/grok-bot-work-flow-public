# Grok Bot 进度板 SOP（全局版，供 YOUR_COORDINATOR 下发）

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

版本日期：2026-10-26（新版交付稿；日期不表示已激活）
依据：YOUR_OWNER 2026-10-22 硬性要求；#438 IMPL_PLAN；workflow#3（历史示例，原记录不随公开包分发） 的 OQ1–OQ5=A 确认（历史示例，原记录不随公开包分发）。
以供给的 10-25 版为底，旧版本保留。仓内回滚参考：10-22 历史版（历史材料未分发，不是安装依赖）；10-25 原件由安装者保留。
生命周期操作细则与各阶段 bullet：[lifecycle.md](lifecycle.md)。部署者须将两文件同目录安装并核对；本版不声称 routine、三端指令或云端检测已经生效。

## #24 四角色总纲（已批，部署另批）

| 角色 | 看板 Page | GitHub | 恢复/交接 |
| --- | --- | --- | --- |
| 任务流 Bot | 唯一读写者 | 判断并分发 | 每小时兜底，问 YOUR_OWNER |
| 本机脚本 | 不读写，只推信号 | 仅云每五分钟发现动静 | 原任务缺交接续原会话一次 |
| Claude / Codex | 不读写 | 按 brief 交付 | 每次停手写当前批交接并驱动脚本；worker 交 Main |
| YOUR_OWNER | 读板 | 无须盯 | 回答板上决策问句 |

操作定义、记录 owner、送达确认、共享 100/day 预算与旧补丁废止范围见 [#24 总纲](cases/local-automation-design.md)。三种唤醒入口：本机脚本推送、云 GitHub 新动静、每小时 H2；08:00 保留早报。只有 Bot 写 Page；缺交接=卡住，由脚本一次恢复，失败交 Bot。未部署不得声称线上已生效。


## 1. 一 Bot 一 Page
- 每个 Bot 在 Grok Bot Library 里有且只有一个自己的进度板 Page（canvas），不做跨 Bot 的大总板。
- 命名：`<Bot 名>进度板`，例如「任务流进度板」「YOUR_COORDINATOR 进度板」「自媒体进度板」「健身教练进度板」。
- 位置：该 Bot 自己的 Library 下；创建后把 Page URL 记入自己的记忆/常驻笔记，并告知 YOUR_COORDINATOR 登记。
- 聊天不是进度的事实来源，Page 才是。

## 2. 谁来更新、何时更新
- **只有 owner Bot 可以写自己的 Page**（WriteCanvas / EditCanvas）。其他 Bot 只读，不得写入、不得代改。
- 需要别的 Bot 的进度变化时，用聊天通知 owner，由 owner 自己改。
- 更新时机：
  1. 任一任务状态变化（wip / blocked / finished 切换）。
  2. 任务流看板唤醒（webhook，每次）＋ 任务流看板兜底（每小时，08:00 PT 早报）。两者都按 §9 判定顺序扫描；兜底另外做全量健康扫描、检查 YOUR_OWNER 是否已答、早报列出待 YOUR_OWNER 跟进的 todo（§9.4）。旧三次 H2/暂停 30 分钟自检条文废止；按 #24 每小时核上次更新超一小时的 wip，并查有 wip 但一小时无推送的主机脚本/睡眠/可达性。
  2a. 全天适用同一套判定（不分日间/夜间）。按 YOUR_OWNER t462u 的 P1-3=A 定案，授权内通知和聊天提醒 24h 同回合发送，含 blocked 问句、合并请求、无法核验与待续派原因，不因夜间等 08:00。[workflow#14 已批 PR 修评审/解冲突/补声明与云评审](lifecycle.md) 24h 同回合派，不排到 08:00；其他工作按已有授权；不得冒称有人 working。
  3. 派活后收到执行结果（成功、失败、PR 打开/合并）。
  4. 新任务进入或旧任务关闭。
- 每次更新同步改 Page 的「截止时间」（AS_OF），写明时区。

## 3. 列定义（八列；YOUR_OWNER 2026-10-24 05:38 PT 增「上次更新」；03:33：当前状态第二列；目标仅 YOUR_OWNER 可改）
| 列 | 规则 |
|---|---|
| 任务 | 任务名（含编号便于检索）。 |
| 当前状态 | **固定第二列**。第一行只能是 `todo` / `wip` / `blocked` / `finished`；其下用 **短 bullet**。**精简（YOUR_OWNER 2026-10-24 05:55 PT）**：wip/todo **只留 1 条 bullet**，只回答「谁在跟进什么」——有 Herdr working 写 `主机 Herdr main「终端标题」：一句话总结`；Claude 评审仅在本轮已派且 GitHub 尚无结论时写等待 + issue/PR 链接（见 lifecycle §5.5），结论已出转修复/决策；等待写清核验时间与恢复方；无人跟进按 lifecycle §5.5 实际续派或问 YOUR_OWNER。禁止多条过程流水、CI/SHA/PID/采样数字（细节只进 evidence）。blocked 可再加 1 条 `❓` 问句，必须可直接回答。任务流刷板时技术原文必须改写成上述格式再上板。 |
| 上次更新 | **第三列**（YOUR_OWNER 2026-10-24 05:38 PT）。板面显示相对时间（N 分钟前 / N 小时前）。数据源为 `lastUpdateAt`（ISO8601，带时区）。**每次**唤醒/兜底/BOARD_SIGNAL 刷板都必须刷新该字段为本次刷板时刻；无时间戳则显示 `—`。这是验证状态机是否在刷的最直接证据。 |
| 目标 | 验收意图一句话，**独立成列**。**仅 YOUR_OWNER 可改**；刷板信号里的 goal 一律忽略，不得把过程流水写进目标。 |
| 验收 | **新开票必填**：列出验收口径条目；达成一条勾一条（板面用 ☑/☐）。**存量票**填 `—`，不补口径。全部勾完且 issue closed 才可 finished。 |
| 跟进方 | 只能是 `air` / `mini` / `云电脑` |
| Issue | 有 GitHub issue 时填完整 URL；无则 `—` |
| PR | 有 PR 时填完整 URL；无则 `—` |

- 状态枚举（#438 / YOUR_OWNER 2026-10-24）：
  - `todo`：已入板，**当前没人在干，也不卡 YOUR_OWNER**（不计三端「进行中项」）。todo→wip 只由 YOUR_OWNER 明确说「跟进」触发（OQ1=A）；08:00 早报列出待跟进项，由 YOUR_OWNER 挑，不自治派活。todo 可以暂时没有 issue，YOUR_OWNER 说跟进后同一回合先开/补 issue、记录、派 Claude、刷板。
  - `wip`：**Herdr 里有对应的 tab，且其中的 agent 处于 working**（YOUR_OWNER 2026-10-24）。「对应」= tab 名含该行 task_id，或含该行 issue 号。BOARD_SIGNAL、issue/PR 活动只刷新证据，不单独证明持续执行。YOUR_OWNER 说跟进或 Bot 续派后，派单宽限 ≤10 分钟可先标 wip；到期须核验 working 或已核验的等待声明，否则按 lifecycle §5.5 分 S 为空的 X14、STOPPED 的 X19 或非 STOPPED 无 working 的一次观察兜底。云端 Claude 的 E4（launch.out 有 start 无 end + 进程存活）仅为候选证据，检测可用性仍待核，未核验前不得据此声称 B1 working。进 wip 前必须有 GitHub issue。某端 Herdr 读不到时，该端的行维持原状，早报标「无法核验」，不降级。
  - **wip→todo 门禁（YOUR_OWNER 2026-10-24 06:40 PT）**：须 **YOUR_OWNER 明确同意**（聊天或 issue，无 `【LLM：…】` 尾标）。**未经同意，不得因 Herdr idle/done 自动把 wip 降为 todo**（#445 反例：执行端停工、远端 SSH 未核验、仓未建 → 更像 blocked，不是 todo）。执行端已停时：卡目标+等 YOUR_OWNER 决策 → `blocked`+❓；不卡 YOUR_OWNER 且等待符合 [lifecycle §5.5 V1–V3](lifecycle.md#55-stopped合法等待与无人跟进) → wip 如实写被动等待与 Bot 最迟下个 H2 核；STOPPED 且无 §5.5 合法等待 → X19 当次推进，S 为空按 X14；非 STOPPED 无 working 按同节一次观察兜底，保留在途命令/无法核验事实，不盲派；确需 YOUR_OWNER 决定才 D。X14/X19 按已有授权续派并如实标待派/无法核验，不伪造 working；不得自动降 todo。
  - `blocked`：**通则（YOUR_OWNER 2026-10-24 06:34 PT）**：凡**阻碍当前目标达成**、且**必须等 YOUR_OWNER 决策**才能继续 → `blocked`，执行端已停在卡点；格式带可直接回答的 `❓` 问句。G1–G4 是常见门禁清单（仍适用），**不是**穷尽枚举——合 main 后 CI 红等你定是否修、验收偏差要你认、部署/实盘要你批等，只要卡目标+等你，就算 blocked。
    - G1 方案架构：新组件/服务/routine/常驻进程/持久状态或 schema；跨端/跨 Bot 契约（信号字段、AGENTS、SOP）；实盘、资金、凭据、生产部署拓扑；与 YOUR_OWNER 既有决定冲突；Claude 评审留有未消解的 P0/P1 架构问题。卡点：派 Codex 实现之前；B2 方案交出等 YOUR_OWNER 确认即 blocked。
    - G2 验收口径：新票首次定口径；改、删、放宽验收；接受偏差。卡点：派实现前（偏差在关单前）；B2 方案与验收口径待确认即 blocked。
    - G3 中途架构调整：实现中出现 OUT_OF_SCOPE，且变更命中 G1 判据。卡点：偏离方案的实现开始之前。
    - G4 只有 YOUR_OWNER 能给的授权：实盘、资金、凭据、生产 cutover、提权、外部账号；所有合进默认分支的 PR，在 lifecycle §5.1 的 R1–R4 全成立后进 E blocked 等 YOUR_OWNER 批准合并（OQ2=A），结构性缺口按 §5.8 提 D 单 PR/head 合批例外，不能当门禁 PASS；合并进 main 后正式 CI 红、执行端已停、等 YOUR_OWNER 决定是否修 CI / 怎么修。
    - **不算 blocked**：不需要 YOUR_OWNER 决策的等待——执行端仍在自主修/跟；纯等 CI 变绿（已有授权继续）；等外部 review 出结论（当前 head 该项评审仍未贴出，无问句给 YOUR_OWNER）；等市场事件或运行时证据；等已派但尚未贴出的 Claude 评审；实现中途在已有授权内换 worker/机器。初次实现派谁由 YOUR_OWNER 明确指定，未指定仍 B2 blocked，不能自行按空闲容量挑人。有 Herdr working、有效派单宽限或 §5.5 V1–V3 合法等待 → wip，但须先核 B2 交付；STOPPED 且无合法等待走 X19，S 为空走 X14；其他无 working 情形按 §5.5 一次观察兜底。idle/done 不当自行恢复方，按 resume=bot 如实写被动等待；本次 V1 读回仍真才续到下一 H2，不因旧 next_check 过期误判 D。合并门禁结构性缺口与其他 R 项合法等待并存时先等该项，注明评审出来后需 YOUR_OWNER 定例外；不相关 G1–G4 立即 D。B2 待方案/验收确认或待 YOUR_OWNER 点名实现端属于 blocked，已有效交付时不能以 working 或旧「等方案/评审」绕过。
  - `finished`：已达成目标，**且**该板项对应的 GitHub issue 已满足验收并 **closed**（YOUR_OWNER 2026-10-23）。issue 仍 open 时禁止 finished；执行端只能报 `wip`/`blocked` + 当前进展。PR 合并/关闭不能单独作为 finished 依据。执行端逐条验收并回报；C1–C6 全满足后由 Bot 关单，下一次扫描读回 CLOSED 才标 finished。F 验收全 PASS 发 `event=done,status=wip`（issue 尚 OPEN 的唯一 done 用途），执行端不关单；其他阶段只发 milestone。E 或 D 合批例外已有有效批准且 C1–C6 齐时不再额外等关单批准；接受偏差或改口径仍走 G2。收到 finished 信号但 issue 仍 OPEN → 不采纳，记 override，按 §9 重判。YOUR_OWNER 明说取消的行可直接 finished。**没有**对应 issue 时：执行端不得自称 finished，是否可关由 YOUR_OWNER 人工判断后由 owner Bot 标 finished。保留到下一次自检后移到「已完成」折叠区或删除。
- **反例（YOUR_OWNER 2026-10-23）**：「无 issue 不能 finished」**不等于**「所以标 wip」。单端已落地、等 YOUR_OWNER 决定是否推其他端 / 开 issue / 关验收 → 必须 `blocked`+question，不能因为不能 finished 就改成 wip。
- **Issue 绑定**：每个板项必须有对应 GitHub issue；信号里要能定位到该 issue（无 PR 时 `pr` 列可先填 issue URL）。
- 跟进方：air = MacBook Air（Codex/Herdr）；mini = Mac mini（Codex/Herdr）；云电脑 = Grok Bot 云主机（Claude Code、Tailscale、routines）。填实际执行/托管方；不确定时保持已核实值并标无法核验，不猜、不改目标；只有必须等 YOUR_OWNER 决策才能继续时转 blocked。
- PR link：只填真实核对过的 URL，不得推测拼接。

## 4. 聊天 vs Page
- 聊天：仅报异常，≤200 字；附 Page 链接即可。
- Page：完整追踪表。长证据放文件路径，不贴进 Page。

## 5. 新 Bot 首次建板
1. 向 YOUR_COORDINATOR 确认本 Bot 的负责范围、跟进方取值及负责人对本 Bot 建板/写板的授权。
2. 仅由 owner Bot 使用所用平台现有的表格/画布入口创建自己的空白 Page，填写标题与任务数据，按此顺序建立八列（任务、当前状态、上次更新、目标、验收、跟进方、Issue、PR；存量行验收填 —），不依赖额外模板文件。
3. 读回列顺序和写权限，确认只有本 Bot 能写自己的 Page，取得并核对 URL。
4. 把 URL 记入自己的记忆，并回报 YOUR_COORDINATOR 登记。
5. 之后按第 2 节更新。

## 6. 禁止事项
- 不得编辑其他 Bot 的 Page。
- 不得新增状态值（除已批准的 `todo` / `wip` / `blocked` / `finished`）；「待验收」「等批」「开放」等一律归入 blocked + 问题，或 wip / todo。
- 不得擅自新增或改名列（「验收」列已由 YOUR_OWNER 2026-10-23 批准；2026-10-24 起「目标」独立且仅 YOUR_OWNER 可改；03:33 起「当前状态」固定第二列；05:38 起「上次更新」为第三列），不得合并成总板。
- Page 上不得放密钥、token、口令、私有 IP、其他凭据、完整内部路径中的敏感内容。
- 不得编造 PR URL、状态或跟进方。
- Page 不联网（无 fetch）。

## 7. Claude 设计与架构评审
- Claude 只在云电脑 Herdr 运行。所有 Claude 派单先按 [Claude 出口纪律 §1–§3](claude-discipline.md) 在将实际运行 Claude 的云主机核验 YOUR_PROXY 代理：仅 curl 退出 0 且去首尾空白后的单个 IP 恰为 `YOUR_EGRESS_IP` 才是 egress_ok。直连 `YOUR_DIRECT_IP` 正常，任何直连 IP 都不得作闸门；错误、超时或无法核验云端结果只阻止本次出口门禁，不自动改板 blocked。egress_ok 不替代其他门禁、不授权派单、不重放历史 pending。
- **触发 A**：新 item 先入 A todo；只有 YOUR_OWNER 说「跟进」才由 Bot 同一回合开/补 issue、写 `【跟进】`、派 Claude（Opus 5.5 / effort=high）、刷 wip。不因新 item 自动派设计。
- Claude 只设计/评审，Codex 实现；brief 带精确 board_row、task_id、issue 链接、YOUR_OWNER 原话、旧方案与修改意见。方案含 G1 初判、验收草案、≤5 OQ；安装前已交付的旧格式先按 [lifecycle §5.7](lifecycle.md#57-存量票迁移一次性仅在-f-执行) 迁移，保持有效 B2，不因格式回 B1/X19/重派；以下新格式仅约束安装后新版。issue 评论第一行 `【方案 vN】#M <标题>`，结尾 `Open Question：k 条` / `无 Open Question`，最后一行 Claude@云电脑 LLM 尾标。允许摘要附 `PLAN_S10*.md` 路径，文件单独存在不算交付。评论须严格晚于最近 `【跟进】` / `【跟进修改】`；YOUR_OWNER 提修改先同回合记【跟进修改】再原话回派，旧版交付/确认不能用于本轮。Claude 不直接和 YOUR_OWNER 讨论。
- workflow#10（历史示例，原记录不随公开包分发） OQ1=A：每版先发布上述任务内 issue 评论，再由云电脑 Claude 在云电脑本机调用现成 board-signal-post 发一次 blocked/blocked/host=云电脑 信号；question 为下述草稿，evidence 含评论 URL 与 PLAN 路径（若有）。此任务内评论和单次完成信号是通用外部写入限制的明确例外；15 字段、seq/as_of、共享 Bot 日上限改为 100，本机重试协议和 15 字段不变；#24 本机定时脚本为已批例外，不授予其他外部动作。细节见 [lifecycle §6](lifecycle.md#6-信号-evidence-约定) 和 [Claude 模板](../templates/CLAUDE_SNIPPET.md)。只有 Bot 写 Page，信号只唤醒，H1/H2 必须读 issue 核实。
- 核实有效交付后**先进入 B2 blocked**，即使 Claude tab 仍 working；不能以旧 plan/review wait 留 wip。有 OQ 问 `YOUR_OWNER 需决策：#M 方案 vN 请拍板：① …；② …；（确认方案与验收后由谁实现？建议 <空闲的机器> Codex）`；无 OQ 问 `YOUR_OWNER 需决策：#M 方案 vN 可以实现了，派谁做？（mini Codex / air Codex；建议 <空闲的机器>）`。板面一条方案 bullet+一条 ❓，保留各 OQ 要点。
- 最新方案 `【方案确认】`、G2 验收签认和 YOUR_OWNER 明确点名机器/agent 三者齐才可派实现；#421 容量只作建议。只答 OQ 未指定实现端仍 blocked，只问剩余「派谁做」；未明确确认的方案/验收门禁仍保留，不从「行」「可以」猜人选或授权，无 P0/P1 也不自动放行。
- 全天同次唤醒发一条 ≤200 字的方案链接+问句提醒；按同一行+方案版本在现有 WAKE_/FALLBACK_ 记录一次提醒，H1/H2 共用去重，夜间已提醒的版本不在后续 wake 或早报重复，新版才再提醒。Claude 未发/失败/当天 wake 达上限时，下一次现有 H2 用同一 issue 判定兜底，不重复已提醒的版本。本仓交付不代表已安装或真实试跑。
- **触发 B**：PR 发布、评审、复评与修复回派前必须读 [lifecycle §5.2 PR 闭环](lifecycle.md#52-评审回应表r3)，并按其中引用的 §5.5/§5.6/§6 执行。

## 8. 验收列
- 新票先列验收草案，B 阶段由 YOUR_OWNER 确认；改/删/放宽或接受偏差走 G2。存量票不回填猜测口径，显示「—」；缺口由 YOUR_OWNER 确认，不能把「—」当全部 PASS。
- Bot 只按执行端逐条 PASS/FAIL 回报及可打开的证据勾选，不从 CI 绿、PR 合并或信号摘要推断达成。信号 evidence 用 `accept: <编号>=PASS|FAIL <证据>`。
- 任务流信号/BOARD_ROWS 镜像可选 `acceptance`（`[{text, done}, …]`）沿用原约定；**helper 仍恰好 15 个字段**，不加 acceptance 字段。
- C1–C6、Bot 关单与 OQ5 失败恢复见 [lifecycle §5.3–§5.4](lifecycle.md)。

## 9. 状态判定与纠偏（任务流板专用；其他 Bot 只采用 §3 的 wip/blocked 定义，YOUR_OWNER 2026-10-24 OQ5=A）

### 9.1 每行判定顺序（唤醒和兜底都用）
1. YOUR_OWNER 明说取消 → 记录后 finished（人工取消例外，不伪称验收通过）。
2. issue CLOSED 且验收全勾（或有 YOUR_OWNER 偏差接受）→ finished；CLOSED 但验收不齐 → X18 blocked，问接受偏差还是 reopen。
3. 无 issue → A todo；只有 YOUR_OWNER 说跟进才先开/补 issue，随后继续阶段推导。
4. 完整执行 [lifecycle §3 阶段推导](lifecycle.md)：跟进、方案确认、有效 head-bound 合并批准、R1–R4，推导 A/B1/B2/C/E/F；任何未答 G1–G4 或卡目标且等 YOUR_OWNER 的问句覆盖板阶段为 D，但先派不依赖该决策的授权内修复；仅合并门禁缺口与其他 R 项合法等待并存的问法，按 lifecycle §7 先等该项，不相关 G1–G4 立即 D。
5. B1/C/F 必须核验实际跟进或等待声明；idle/done 不是完成，不自动降 todo，也不允许无人负责的 wip。按 lifecycle §5.5 核 STOPPED/V1–V3：全停且无合法等待按 X19 顺序当回合推进，S 为空按 X14 派续或 D；S 非空、无 working 但非 STOPPED 时按同节只读相关 pane 一次，确认已停/输入/权限卡点且无在途命令、无合法等待才 X19；在途命令或不明状态显式标无法核验、进早报，保留命令且不盲派；已批 PR 下一手全天回派，其他按已有授权并如实写明待派原因。Herdr 读不到则保留原状、标无法核验并早报，不绕过安全校验。
   派续由子代理产出 pending_dispatch、父代理同回合执行，见 [lifecycle §5.6](lifecycle.md#56-派续由父代理执行pending_dispatch)。H1/H2 涉及 Claude 时均先用 [Claude 出口纪律](claude-discipline.md) 核验实际云主机 YOUR_PROXY 代理；直连 IP 不参与闸门，未核验不得放行，出口恢复不自动回放历史 pending。可粘贴交付见 [H1/H2 出口补丁](../templates/H1_H2_PROMPT_PATCH.md)。
6. R1–R4 齐 → 当次 X15 进 E；E 缺条件 → X16a（授权内可补且有真实恢复方：回 C 实际通知）/X16b（补不了或执行端已 blocked 提问：改 D 写缺项与出路），不得只驳回留无承接 wip；无批准已合并 → X17 记录事实和违规、不自动 revert。各码与证据要求见 [lifecycle §7](lifecycle.md)。

### 9.2 YOUR_OWNER 是否已答
聊天里 YOUR_OWNER 的明确回答；或 issue/PR 上作者为 YOUR_GH_OWNER、**不带 `【LLM：…】` 尾标**、时间晚于问句的评论。含糊回复不猜授权。
已答 → **同一回合**把原话、聊天时间和链接写入 issue，按决定写 `【跟进】/【跟进修改】/【方案确认】/【合并批准】/【偏差接受】`；明确实现端也留痕，门禁齐备才实际续派并改板，不留过期 blocked。B2 只答 OQ 未指派仍 blocked，只问剩余派谁；YOUR_OWNER 修改先记【跟进修改】再回派，新版交付须晚于该记录，不沿用旧版确认。合并批准记录 head；新提交使旧批准失效。
受授权/启动失败等限制时如实记录待派或决策，不冒称 working；只在 YOUR_OWNER 同意时降 todo。

### 9.3 冲突优先级
YOUR_OWNER 明示决定 > issue 状态（gh 读回）> 执行端最新信号（仅同一路径比较 seq）> Herdr 推断。每条路径只和自己的 applied.json 记录比较，seq 不大于该路径已应用值才忽略。`-review` 目录信号只叫醒，不算执行端信号；不参与 R1、冲突优先级，不改跟进方/跟进主机。同 task_id/board_row 不合并两路序列：Mac ready seq=5 仍有效，稍后云 review milestone seq=99 不覆盖它。

### 9.4 todo 早报与跟进
08:00 早报逐行列出「待 YOUR_OWNER 说跟进」的 todo，由 YOUR_OWNER 挑；取消自治派活，不沿用「每次最多派 2 行」。
YOUR_OWNER 说跟进后同一回合执行 B1 的四步，派云电脑 Claude 设计；实现端按 §7 由 YOUR_OWNER 明确点名，#421 容量只作建议；暂停/低优不是自动启动授权。新 tab 按 §9.6 命名。
已获跟进授权的 B1/C/F 无人接手按 lifecycle §5.5 分 X14/X19 续派或问 YOUR_OWNER，不将其退成新 todo。

### 9.5 防抖与早报
同一行 24 小时内 wip↔todo 来回 ≥3 次 → 停止自动改这一行，早报标「横跳」。
Herdr 一直 working、但 24 小时内没有任何信号或 issue 活动 → 早报标「疑似卡住」，交给该端 Main，不自动改状态。
每次改状态都写证据：`row, from→to, 码, 依据`（WAKE_/FALLBACK_ 文件）。纠偏本身不发聊天；新增 blocked 问句与其他授权内提醒同回合全天发送。

### 9.6 Herdr 命名
执行端新开的 tab 名 = `<task_id>-<role>`，task_id 必须含 issue 号（例 `task123-impl-main`、`task123-review`（同 issue 方案/代码常驻））；agent 同名规则。原执行端不在时用 `-main2`、新 batch，须遵守现有授权和待批 CI_WATCH 边界，不能把本版当成新增恢复自动化授权。

## 10. 交付与激活边界
- [生命周期操作规则](lifecycle.md) 包含 §2–§7 全阶段表、R1–R4、C1–C6、证据格式和 X14–X19；每次 H1/H2 必须读取。
- [H1/H2 追加稿](../templates/H1_H2_LIFECYCLE_APPEND.md)、[执行端追加稿](../templates/LIFECYCLE_AGENTS_APPEND.md) 是未安装草案，实际修改、备份和三端同步由 owner 单独执行并取证。
- CI_WATCH OQ 尚待另批，云 E4 检测尚未验证；不能用它们跳过核验或新开恢复自动化。无 CI run 不等于 R2 PASS。

#14 的 PR reviewer 派单与信号执行前读 [lifecycle §6 PR 评审单次信号](lifecycle.md#pr-评审阶段的单次云端信号6-补充)。脚本、已安装 SOP/routine 本批未改，不能宣称 live 停 dispatcher 或完成三端验收。
