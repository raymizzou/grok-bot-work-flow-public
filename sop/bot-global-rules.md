# Bot 全局规则（新整理，2026-10-24）

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

这是从已读取的本机 board 指令与旧 SOP 提炼的通用规则，**不是缺失的同名原件**。
生命周期以 [新版 SOP](bot-progress-board-sop_2026-10-26.md) 和 [lifecycle](lifecycle.md) 为操作来源；本摘要及 [当前状态机](board-state-machine.md) 不覆盖其门禁，[信号协议](board-signal.md) 定义不变的 helper 格式。负责人最新明确决定优先；历史材料只用于追溯。G1–G4 已由供给 SOP 补齐，见新版 §3。

## #24 操作入口（未部署）

四角色、三种唤醒、每小时 H2、共享 Bot 每日 100 次 admission、持久待推送/编号收据与本机一次恢复，统一见 [#24 总纲](cases/local-automation-design.md)。旧 30/day、三次 H2 和禁止本机定时恢复的冲突补丁废止。执行端停手前写当前批交接并立即驱动脚本；worker 只交 Main；只有 Bot 读写 Page。

## 所有权与事实来源

- 一 Bot 一进度板 Page，只有 owner Bot 写自己的 Page，其他 Bot 通过 owner 授权的信号/交接通知；执行端与脚本不读写 Page。
- 聊天用于短异常通知；Page 追踪状态，长证据保留文件路径，AS_OF 标明时区。
- Page 固定八列：任务、当前状态、上次更新、目标、验收、跟进方、Issue、PR。目标仅 YOUR_OWNER 可改，标题含 issue 编号；细则见新版 SOP §3。
- 每个板项绑定一个真实 GitHub issue。无 PR 时信号 pr 填已核对的 issue URL；有 PR 时以 PR 为主，evidence 仍保留 issue。
- 状态、跟进方和 URL 必须有证据；不确定信息写 UNKNOWN，不猜测。
- issue 验收满足且已 closed 才能 finished。F 验收全 PASS 专用 event=done/status=wip，执行端不关单，由 Bot 核 C1–C6 关闭；其他阶段完成报 milestone。PR 合并或本机阶段完成不能替代 issue 验收。
  无 issue 时也不得自报完成，由负责人决定后续。

## 人可读信号与角色

summary 和问题每行一个短结论：发生了什么、在等谁、需要什么决定。
CI run、完整 SHA、进程/窗格标识、样本数字放 evidence，不堆进摘要。
问题为 `YOUR_OWNER 需决策：…`，能在手机直接用普通文字回答；这里 YOUR_OWNER 是既有协议固定提示语，部署者应确认自己的适配政策。
不使用结构化问答控件。

Claude 负责评审/设计，Codex 实现，任务流 owner 管板。bot 在 GitHub 的评论末尾标 `【LLM：模型或工具名】`。
Claude 派单的出口检查只按 [Claude 出口纪律](claude-discipline.md)：在将实际运行 Claude 的云主机核验 YOUR_PROXY 代理，直连 IP 不得作闸门；egress_ok 不授予派单或历史 pending 重放权限。
这些角色分工不授予创建代理、发评论、合并、部署或修改 Page/routine 的权限。
每次外部动作遵循部署者已有授权，禁止把来源文档中的操作指令当新授权。

## 东京与生产只读排查

YOUR_OWNER t529u 定案：workflow#21（历史示例，原记录不随公开包分发）、YOUR_BUSINESS_REPO#476（历史示例，原记录不随公开包分发）。本节是 H1/H2、Bot 和父代理处理此类排查的统一入口。

- **东京/生产只读排查默认由任务流 owner 经既有 t475u 本机原生机器通道，在云电脑本机 Shell 执行 SSH。** Claude/Herdr 不是 SSH 排查执行器；本 SOP 不再派发 #476 旧「Claude 只读 SSH 东京」验收。验收修改仍由 YOUR_OWNER/Bot 处理，不修改历史验收，也不把旧 FAIL 报成 PASS。
- 非云端 Main（Mini/Air）收到请求时交给任务流 owner，附已登记 Host、只读命令及时间范围、既有授权依据、结果回传位置。H1/H2 只写 `pending_dispatch` 的既有 `kind=notify`，由父代理送达任务流 owner/云电脑本机通道，再由 owner 核实已有执行授权、执行并返回证据，见 [lifecycle §5.6](lifecycle.md#56-派续由父代理执行pending_dispatch)。`notify` 只转交请求，不授予执行权限、不启动 Claude。云电脑本机入口不可用时报告实际通道缺口，不跨机器 SSH 进入云电脑、不加密钥、不换用 Claude/Herdr，也不声称已执行或自动改派 Air。
- 本 SOP 当前仅登记 `YOUR_REGISTERED_PROD_HOST`（云电脑 `~/.ssh/config` 中的别名；本次文档修改未重验配置）。其他生产 Host 须先有明确文档登记与适用授权，不凭「生产排查」扩展目标。只读拉取限定时间/条数的 `journalctl` 日志，或读取与问题直接相关且不含秘密的配置项。示例只用于东京日志读取：

  ```sh
  ssh -o BatchMode=yes -o ConnectTimeout=10 YOUR_REGISTERED_PROD_HOST 'journalctl -u YOUR_SERVICE --since "30 minutes ago" --no-pager -n 200'
  ```

  `ConnectTimeout=10` 只限制连接建立等待，不是整条远程命令的总耗时上限。

- SSH 排查独立于 Claude/Herdr；Claude 不可用或其出口检查失败，不阻止这条已授权的只读路径。**不得要求先启动云 Herdr Claude 才能 SSH，也不把 Claude 专用的 YOUR_PROXY 出口检查当作 SSH 前置门禁。**
- **禁止为拿东京日志/排查修改 `~/.local/bin/claude` wrapper、使用 `exec -a claude` 或与 `YOUR_GUARD` 对打。#21 的 FIX-01/R2 wrapper 修复路径已停止，不自动重放相关历史 pending 修复指令。** 这里的 R2 是 #21 旧修复路径，不改变 lifecycle 的 R2 CI 门禁。
- Host 必须已登记；别名解析、连接或认证失败时，报告实际 SSH 错误（脱敏），不改 wrapper/guard，也不新增凭据、改 SSH/网络/信任配置或绕过检查。不 dump 环境变量、密钥或秘密配置，不重启服务、不作线上变更。
- **§8 不变：Claude/Claude Code 仍只在云电脑运行，用于方案/评审；既有云 Herdr 和 [Claude 出口纪律](claude-discipline.md) 均保留。** 本节只区分 SSH 排查的执行路径，不放宽 Claude 规则。
- Air 只读 SSH 东京作为已授权的并行入口继续保留（#476 Air 历史 PASS（历史示例，原记录不随公开包分发），不是本次 live 验证），使用时仍须有相应任务的既有授权；云默认通道失败不自动改派 Air。部署默认仍是 **Mini**（t502u/t503u 派单转述 t501u（历史示例，原记录不随公开包分发））。只读排查不授予部署权限，部署仍须单独核验既有授权与门禁。

## YOUR_BUSINESS_REPO 正式 CI 硬规则（2026-10-26，#473（历史示例，原记录不随公开包分发））

- 正式 CI 必须在合并前覆盖 PR/feature，至少支持 `pull_request` 到 `main`；除非 YOUR_OWNER 当场明确批准，禁止再改成只在 push main 后才跑。
- 任何修改 `.github/workflows/ci.yml` 触发条件的 PR，验收必须明确核实：PR 事件仍运行 `plan` 和 `required`，且 PR 上实际出现 `CI / required`。没有 run 不算 PASS。
- PR 绿是合并前证据；部署仍须最终合入后 main 的 exact-SHA 正式 CI 绿，既有已授权的 main-only 手动 CI 替代路径不变。CI 绿不授予合并或部署权限。

## 安全与配置

凭据仅在本机非同步目录中保存；信号、文档、Git、命令参数和日志均不含秘密。
每台机器自己写、自己 POST；不建统一 poller/跨主机 relay，不等待同步。
沿用经过人工确认的 wake routine；授权内通知和聊天提醒按 YOUR_OWNER t462u 定案全天发送；helper/执行 agent 不直接调用 Canvas API。
个人指令片段人工合并且先备份。保留已有插件/skill 禁用规则，特别是 Superpowers 禁用；不引入安装或启用操作。

初版缺口和原件来源见 INVENTORY（历史材料未分发，不是安装依赖）。

#14 的 PR 发布、评审与修复回派前必须读 [lifecycle §5.2 PR 闭环](lifecycle.md#52-评审回应表r3)，并按其中引用的 §5.5/§5.6/§6 执行；仓内模板未应用，安装与 live 验证另批。
