# 可合并的 Codex 指令片段（模板）

> 路径约定：`~/ray-docs` 仅为 helper 默认的参考布局；`YOUR_` 值须由部署者填写，涉及真实主机/出口/凭据的值只留本机私有配置。

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

先备份并人工合并，不覆盖整个 ~/.codex/AGENTS.md；保持已有 Superpowers 禁用规则。
不要把本标题或整份 SOP 无条件复制成常驻上下文，合并下面指针并确认路径已安装即可：

> 涉及进度板状态与 wake 时，先读 ~/ray-docs/YOUR_COORDINATOR/sop/bot-global-rules.md、board-state-machine.md、board-signal.md；生命周期/ready/验收工作再读同目录 lifecycle.md 与 bot-progress-board-sop_2026-10-26.md。
> Main 在当前主机按信号协议执行；worker 只交接给 Main，不能越过 brief 自行 POST 或写 Page。
> 信号 board_row 与板标题一致，task_id 含 issue 编号并匹配 Herdr 命名；每机自己写自己 POST。
> issue 仍 open 不发 finished；F 验收全 PASS 专用 event=done/status=wip，其他阶段完成报 milestone，执行端不关单。idle 不自动降 todo，wip→todo 需 YOUR_OWNER 明确同意。
> blocked 按新版 SOP 的 G1–G4 或卡目标且等 YOUR_OWNER 决策通则；B2 待方案确认、E 待合并批准均 blocked。问题写 `YOUR_OWNER 需决策：…`；等 CI/review/市场只报 milestone 和恢复方。
> summary 用短句分行，技术证据放 evidence；秘密只在本机凭据文件，不写信号、Markdown 或日志。
> 问题使用正常聊天文字；GitHub bot 评论末尾标 `【LLM：…】`；外部动作须已有授权。

本片段是新提炼，不是缺失全局原件的声称副本。具体规则只有安装的 SOP 一处权威来源。

涉及 PR ready、合并授权、评审回应表或 F 验收，人工合并 [生命周期 ①–⑤ 追加稿](LIFECYCLE_AGENTS_APPEND.md)。该稿含 ready 前 R1–R4 全条件（含 mergeable）、head 绑定与 Bot 关单；不是已安装声称。这是未安装草案；各主机均需独立核验；CI_WATCH OQ 与云 E4 仍待批/待核。

## #24 停手前交接（未安装）

执行端每次停手前按 [#24 总纲](../sop/cases/local-automation-design.md) 原子写当前 task/batch 的 DONE/BLOCKED/OUT_OF_SCOPE JSON handoff，默认由 Main 核实交接后按原 helper 协议发本机信号；只有另行提供、核验并授权安装 runner 后，才驱动同一 manifest 的可选本机观察。贴出需要 YOUR_OWNER 回答的问题就写 BLOCKED，保留问句；不能以 working/旧等待掩盖。worker 只原子交给 Main，由 Main 驱动脚本，不越 brief POST；部署前仍由 Main 用原 helper。只有 Bot 读写 Page，合并/部署/生产仍需明确授权，保留 Superpowers 禁用规则。
