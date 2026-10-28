# 执行端生命周期追加稿（未安装）

> 路径约定：`~/ray-docs` 仅为 helper 默认的参考布局；`YOUR_` 值须由部署者填写，涉及真实主机/出口/凭据的值只留本机私有配置。

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

Air 仅交付草案；mini/云电脑待 owner 分别同步与核验。父代理负责备份并人工合并现有 AGENTS/CLAUDE 指针，不覆盖个人配置，保留 Superpowers 插件/skill 禁用规则。此稿不授予新代理、GitHub 写入、合并、部署、routine 或生产动作；使用各自已有授权。worker 仍只向 Main handoff，不能越过 brief POST。

来源：workflow#3（历史示例，原记录不随公开包分发）、OQ 确认（历史示例，原记录不随公开包分发）。
仓内：[lifecycle](../sop/lifecycle.md)、[新版 SOP](../sop/bot-progress-board-sop_2026-10-26.md)、[信号协议](../sop/board-signal.md)。
部署前先安装核对 `~/ray-docs/YOUR_COORDINATOR/sop/lifecycle.md` 及上述同目录 SOP；以下 ①–⑤ 可合并到实际执行 Main 的指令，Claude 只应用设计/评审边界。

---

涉及生命周期、PR ready 或验收收尾时先读 `~/ray-docs/YOUR_COORDINATOR/sop/lifecycle.md`。task_id 含 issue 号，tab/agent 为 `<tid>-<role>`；Claude 设计/评审，Codex 实现，Bot 独写板。所有 GitHub bot 评论末尾带 `【LLM：<实际身份>】`，问题用普通聊天文字。CI 绿不是合并或部署授权。

① **所有合进默认分支的 PR，未获 YOUR_OWNER 明确合并批准不得合并。** 批准绑定当时 PR head；记录原话、时间、head，与当前或实际合并 head 核对，批准后任何新提交都使批准失效。E 等待期间停手，除 YOUR_OWNER 要求外不再推送。合并与部署可一次批，但 E 问句必须写部署目标和回滚方式，B 方案已有步骤；实盘、资金、凭据、生产 cutover 必须明确写出，否则另问 G4。未经批准已合并仅报告，不自动 revert。

② **发 ready 之前逐项验证 R1–R4，全部成立才发 ready 的 blocked 合并问句并停手；结构性缺项按下述 gap 路径，不伪称通过。**

- R1：Main 确认开发完成，将由最新信号声明 status=blocked/event=blocked、明确合并问句及 `ready: pr=#N head=<sha8>`。
- R2：ready 的 head 等于 PR 当前 head；必需 CI 全 success，按分支保护核检查集，无保护看全部检查。缺 run、待定、失败、未知都不算 PASS，不自行改 workflow/触发政策。
- R3：按 [lifecycle §5.2 评审回应表与 PR 闭环](../sop/lifecycle.md#52-评审回应表r3) 核验；复评、回派、等待和信号分别沿其 §5.5/§5.6/§6 引用执行。
- R4：PR 当前 mergeable=MERGEABLE，方案标「合并前」验收项已勾；未标均视为合并后验。UNKNOWN 先核实，不抢发 ready。

授权内可补的缺项继续 C 的已批工作/核验并报 milestone、缺项与真实恢复方；分流按 [lifecycle §7 X16a/b、X19](../sop/lifecycle.md#7-纠偏码-x14x19)，不伪称 ready，也不替 Bot 标 E。开发已完成、其余 R 项已核、仅结构性缺项在已有授权内补不了时，用 evidence 文本 `gap: pr=#N head=<sha8> missing=R2 reason=<一句原因>`（可与 ready 同发，缺项仍不算 PASS），status=blocked/event=blocked；问句按 [lifecycle §5.8](../sop/lifecycle.md#58-d-合批例外逐-prhead) 写 head、缺门禁、批准后行为与其他出路。D 合批例外批准只限该 PR/head，须留【门禁例外】原话记录；main CI 的 C2 不豁免，不自行改 CI 或触发政策。待所有项齐发：

```text
status=blocked
event=blocked
question=YOUR_OWNER 需决策：是否批准合并 PR#N 并部署到 <已定目标>？（回滚：<方案中的一句>）
evidence:
ready: pr=#N head=<sha8>
review: pr=#N ledger=<回应表评论链接> open=0
```

无部署要求则问句只问合并并说明无需部署，不虚构目标。上述是信号取值示意，实际通过现有 helper 提交完整 15 字段：board、board_row、task_id、title、goal、status、question、host、pr、event、as_of、seq、summary、evidence、writer；gap/ready/review/accept 均为 evidence 文本，不增加顶层字段。

③ **F 逐项验收；全 PASS 发 event=done/status=wip。** 在 issue 回报 `验收 <编号>：PASS/FAIL，证据 <可读链接或路径>`，信号 evidence 用 `accept: <编号>=PASS|FAIL <证据>`。Bot 只按回报勾选，不凭 CI/合并推断。F 前必须有有效批准；依序合并→准确 main SHA CI 全绿→已授权部署→验收。C 阶段完成、PR 合并、单机结束只发 milestone，不发 done/finished。原验收内 FAIL 保持原票 OPEN，回 C 新 batch 修复；要拆到 follow-up 或接受偏差先问 G2。范围外问题报告 Bot 开 follow-up，不自扩范围。

④ **执行端不关 issue。** Bot 核 C1–C6：合并与批准 head 一致、准确 main CI 绿、需部署时已完成且证据可读、每项 PASS/勾或 YOUR_OWNER 已接受偏差、无未答问句/未处理 YOUR_OWNER 意见、follow-up 已互链，才由 Bot 关；下一扫描 CLOSED 才 finished。OPEN 时 F 全 PASS 的 done/wip 是专用回报，不代表整票完成。main CI 红报 D/G4；部署失败仅按已授权方案回滚并报告，不自动扩大动作。

⑤ **维护一条评审回应表 PR 评论，随同一任务修复更新，并发 review 行。** 所有来源完整分页，每个意见保留原链接；不得用“读过/过期/已分派”冒充已修或 resolved。

```text
评审回应表（head <sha8>）
- [P1-1] <原意见链接> <一句意见> → 已修 <sha8>；Claude 修后复核 <链接>
- [P2-1] <原意见链接> <一句意见> → 不改：<理由>
- [YOUR_OWNER-1] <原意见链接> <一句意见> → 已修 <sha8>
- [P2-2] <原意见链接> <一句意见> → 转 follow-up <issue链接>（原验收范围外：<一句>）
- [例外处置] <P0/P1或YOUR_OWNER意见> → <YOUR_OWNER明确批准链接及理由>（无批准不得结案）
【LLM：<实际身份>】
```

对应 evidence：

```text
review: pr=#N ledger=<评论链接> open=<未处理条数>
wait: kind=ci repo=<repo> ref=<sha8或pr#N> resume=<working且盯该对象的tab或bot> next_check=<带时区ISO>
gap: pr=#N head=<sha8> missing=R2 reason=<结构性缺项原因；仅符合条件时填写>
accept: <编号>=PASS|FAIL <可读证据>
```

等待按 [lifecycle §5.5 STOPPED / V1–V3](../sop/lifecycle.md#55-stopped合法等待与无人跟进) 核当前 head 对象仍未兑现和真实恢复方：working 真盯时 next_check 须未过；resume=bot（含旧 idle/done 恢复方）由 Bot 本次读回 V1 仍真才续到下一个现有 H2，旧 next_check 过期不自动失效，V1 假或 UNKNOWN 不续期。非 STOPPED 无 working 时按同节一次观察兜底，保留在途命令、不明状态标无法核验，不盲续派。要 done/idle 时，必须写 `resume=bot`；若写自己就保持 working 真正在盯。等待/idle 前发一次 milestone，说清等什么、Bot 最迟下个 H2 核或谁实际恢复，只陈述已 ACK 的接手者。对象兑现（评审贴出/CI 结束）后仍 working，停手前须发 milestone 或 blocked，不能静默 done。CI_WATCH OQ、云 E4 尚未批准/验证，不能据此自动开 main2 或声称 working。每台主机本地写本地 POST；helper 字段/退出码保持原协议；summary 是短句，技术身份只进 evidence，禁止秘密。

## #24 停手前交接（未安装）

执行端每次停手前按 [#24 总纲](../sop/cases/local-automation-design.md) 原子写当前 task/batch 的 DONE/BLOCKED/OUT_OF_SCOPE JSON handoff，默认由 Main 核实交接后按原 helper 协议发本机信号；只有另行提供、核验并授权安装 runner 后，才驱动同一 manifest 的可选本机观察。贴出需要 YOUR_OWNER 回答的问题就写 BLOCKED，保留问句；不能以 working/旧等待掩盖。worker 只原子交给 Main，由 Main 驱动脚本，不越 brief POST；部署前仍由 Main 用原 helper。只有 Bot 读写 Page，合并/部署/生产仍需明确授权，保留 Superpowers 禁用规则。
