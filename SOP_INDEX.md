# SOP 索引：哪些规则要带走

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

「SOP」= 写成文件的操作规则。本页告诉你：参考实现有哪些 SOP、各管什么、移植时哪些**必带**。链接指向本仓 `sop/` 下的源文件；摘要只抽关键条款，不复制长历史。

> 版本提醒：本仓 `sop/` 是交付快照。参考实现的运行副本（在每台主机的 `<SOP_DIR>`）后来又更新过几处，见 §4。移植时以「本页摘要 + 本仓源文件」为准，缺的按 §4 补。

---

## 1. 文件清单

| 文件 | 管什么 | 移植 |
| --- | --- | --- |
| [sop/bot-global-rules.md](sop/bot-global-rules.md) | 全体 Bot 通用规则：所有权、人话信号、角色、Claude 续跑、生产只读排查、CI 硬规则、Herdr 清理、安全 | **必带**，并按 §2 补齐硬规则 |
| [sop/board-state-machine.md](sop/board-state-machine.md) | 看板四状态怎么判、身份/命名、各阶段完成条件 | **必带** |
| [sop/board-signal.md](sop/board-signal.md) | 信号 15 字段、退出码、凭据边界 | **必带** |
| [sop/bot-progress-board-sop_2026-10-26.md](sop/bot-progress-board-sop_2026-10-26.md) | 进度板：一 Bot 一板、八列定义、G1–G4、每行判定顺序、早报 | **必带**（当前版） |
| [sop/lifecycle.md](sop/lifecycle.md) | A–G 阶段操作细则、R1–R4、C1–C6、等待与无人跟进、派续、纠偏码 X14–X19 | **必带**（H1/H2 每次读） |
| [sop/claude-discipline.md](sop/claude-discipline.md) | Claude 出口检查的唯一命令与判定（E1–E5） | **必带**（把具体数值换成你的私有值） |
| [sop/herdr.md](sop/herdr.md) | Herdr 归属核对、派工回收、续跑、清理 | **必带** |
| [sop/cases/](sop/cases/) | 纸面推演用例：出口、自动恢复、空闲判定、PR 评审闭环 | 推荐（用于自测理解） |
| 旧版 SOP（历史材料未分发，不是安装依赖） | 旧版 SOP | 不带（只用于追溯） |
| [templates/CLAUDE_SNIPPET.md](templates/CLAUDE_SNIPPET.md)、[AGENTS_SNIPPET.md](templates/AGENTS_SNIPPET.md) | 合并进 agent 个人指令的指针 | **必带** |
| [H1/H2 生命周期追加稿](templates/H1_H2_LIFECYCLE_APPEND.md)、[出口补丁](templates/H1_H2_PROMPT_PATCH.md)、[routine.md](templates/routine.md)、[profile.yaml](templates/profile.yaml) | Bot 定时任务与 profile 的追加稿/模板 | **必带**（人工填写） |
| [templates/PR_REVIEW_BRIEF.md](templates/PR_REVIEW_BRIEF.md) | 派 Claude 做 PR 评审的模板 | 推荐 |
| [templates/BOARD_SIGNAL.json](templates/BOARD_SIGNAL.json) | 信号示例 | 推荐 |
| [scripts/common/board-signal-post](scripts/common/board-signal-post) + 测试 | 信号 helper | **必带** |
| [scripts/common/codex-herdr](scripts/common/codex-herdr) | 在 Herdr 里启动 Codex 的小包装 | 可选 |
| 旧独立扫描器（历史材料未分发，不是安装依赖） | 历史的独立评审扫描器 | **不带**（已决定统一由看板在常驻评审 tab 派评审，不保留独立扫描） |
| [bootstrap/README.md](bootstrap/README.md) | 新机器手工安装步骤（helper、SOP、凭据、dry-run） | **必带**（照着做） |

---

## 2. 必带的硬规则摘要

参考实现早期的全局规则按 §1–§11 编号；后来全局规则文件被重新整理，部分条款不在新版正文里了。下面是**必须继续生效**的条款（已改成通用说法），迁移时写进你的全局规则文件。

### 2.1 LLM 来源标注
所有用到模型额度的汇报、所有 bot 写的 GitHub 评论，末尾标 `【LLM：<来源>@<主机>｜模型=…｜effort=…｜fast=是/否】`。查不到写「未知」，不猜。负责人本人的评论不带这个尾标——这是识别「负责人原话」的唯一依据。

### 2.2 重活一律交给 Codex（Bot 红线）
Bot 自身额度（含它派出的子代理）只允许：对话、派单、只读核对（单条命令能看完）、写汇报、启动已经写好的命令。以下任何一条都是重活，必须交给 Mac 上的 Codex：
1. 改代码：超过 5 行，或任何逻辑改动（哪怕 1 行）；新写脚本超过 20 行。
2. 写一次性处理脚本超过 20 行。
3. 数据处理/分析、根因分析。
4. 跑测试、复现 bug、同一问题连续 3 条以上诊断命令。
5. 多步部署/运维、盯 smoke 判断是否回滚。
判断不清按重活处理。记录里的执行者要写真实身份（`Codex@mini` 等）。例外只有负责人当场明说「这次让 Bot 直接做」。

### 2.3 Bot 额度先批后用
超出「对话、派单、只读核对（≤2 条命令）、写汇报」的 Bot 额度使用（后台子任务、浏览器操作、新建定时任务或提高频率、§2.2 的例外），先发卡片请负责人批准，写清做什么、为什么不能交给 Codex、规模大小。没批就交 Codex 或排队。已批准在跑的定时任务照常。

### 2.4 Claude 只在一台主机
Claude / Claude Code（含方案、评审）只在 `YOUR_CLOUD_HOST` 跑。禁止在 Mac 上启动，禁止写「等本机 Claude」，板面问句里不出现「本机 Claude 还是云端 Claude」二选一。

### 2.5 Codex / Claude 一律走 Herdr
必须在对应主机的 Herdr 里开 tab 跑，禁止无 tab 的后台进程。tab 标题 `<issue号>-<短标题>`；同一 issue 多角色在标题里区分（`123-fixplan-main`、`123-fixplan-review`），不另造前缀体系。声称「在跟」时必须能在 `herdr agent list` 看到该 tab。

### 2.6 方案写法：只准六块
1. 问题（大白话）　2. 原因（不确定就写清还不确定什么）　3. 修复方案　4. 当前架构图　5. 修复后架构图　6. Open Question（只在需要负责人澄清时，放末尾）。
不自造术语/缩写/口号（说「开始挂单」，不说内部代号）；不另加「影响范围」「风险」「时间表」等章节，细节塞进对应块。缺块或不是大白话 → 打回重写，不算交付。

### 2.7 验收失败必须点名
凡验收未全过，必须写明**哪几条**没过（编号或原文 + 一句「差在哪」），已过的也标出（例：「TA-2 过；TA-1、TA-3 未过」）。不准只写「部分失败」「未齐」。

### 2.8 负载均衡与同机跑完
新开实现时可建议更空闲的 Mac（working agent 更少）；已在一台开跑的票必须同机跑完。生产部署固定 `YOUR_PROD_HOST`。设计/评审固定 Claude 主机。

### 2.9 Claude 默认档位
Opus 5.5 + effort=high。例外：负责人点名；恢复原会话沿用原档位；已在跑的不中途改。

### 2.10 Claude 续跑先注入
在跑 → `pane send-text` + `Enter`；确认进程已死才 `agent start --resume`。禁止因「未就绪」报错或徽标异常就新开 tab、重发整份 brief 或杀掉仍在跑的 Claude。

### 2.11 Herdr 会话唯一
Claude 主机只用 Herdr default 会话；脚本不写死其他会话名。

### 2.12 issue CLOSED 就关 tab
关联 issue 关闭 → 对应 tab/pane 自动关。只有「仍 working 且在为另一张 OPEN 票干活」或「负责人明说保留」才留。

### 2.13 生产只读排查不依赖 Claude
需要看生产日志时，由 Bot 在已登记的主机上用只读、限时、限条数的命令（如 `journalctl --since … -n 200`）执行；不要求先起 Claude，也不把 Claude 的出口检查当前置条件。不 dump 环境变量/密钥，不重启服务。

### 2.14 PR 必须在合并前跑正式 CI
CI 必须在 PR 上运行（至少 `pull_request` 到主分支），不能改成「合并后才跑」。改 CI 触发条件的 PR，验收要证明 PR 上实际出现了必需检查。PR 绿是合并前证据；部署还要合并后主分支那个提交的 CI 绿。CI 绿从不等于授权。

### 2.15 安全
凭据只在每台主机本机的非同步目录；信号、文档、Git、命令参数、日志都不含秘密。每台主机自己写、自己 POST；不建统一轮询或跨主机转发。个人指令文件人工合并、先备份。

---

## 3. 关键 SOP 的一屏摘要

### 3.1 看板状态怎么判（state machine）
- `todo`：入板但没人干，也不卡负责人。只有负责人说「跟进」才变 wip。
- `wip`：Herdr 里有匹配的 tab 且 agent 是 working；或派单后 10 分钟宽限内；或核实过的合法等待（等的东西确实还没发生、有明确恢复方、Bot 最迟下个 H2 再核）。
- `blocked`：卡目标且必须负责人决定。B2（方案待拍板）和 E（等合并批准）都是 blocked。
- `finished`：issue 已 CLOSED 且验收全勾（或负责人接受偏差）。PR 合并不算。
- idle/done 不等于完成，不自动降回 todo；wip→todo 需负责人明确同意。

### 3.2 每次唤醒的判定顺序
1. 负责人取消 → finished。2. CLOSED 且验收齐 → finished；CLOSED 但验收不齐 → blocked 问「接受偏差还是重开」。3. 没 issue / 没【跟进】→ todo。4. 有方案交付 → B2。5. 方案已确认且点名 → C；R1–R4 齐 → E。6. 有有效合并批准 → F。7. 任一未答的 G1–G4 → D（覆盖 4–6）。8. 和板不一致就纠偏，写证据。

### 3.3 G1–G4（必须等负责人的四类门）
- G1 架构：新组件/服务/定时任务/常驻进程/持久状态、跨端契约、实盘/资金/凭据/生产拓扑、和负责人既有决定冲突、评审留有未解决的 P0/P1 架构问题。
- G2 验收：首次定口径、改/删/放宽、接受偏差。
- G3 中途改架构：实现中冒出的范围外变化命中 G1。
- G4 只有负责人能给的授权：实盘、资金、凭据、生产切换、提权、外部账号、合并、合并后主分支 CI 红怎么处理。

### 3.4 纠偏码（Bot 发现板面和事实不符时）
X14 无人跟进 → 当回合派续；X15 R1–R4 齐还挂 wip → 进 E；X16a/b E 缺条件 → 能补回 C / 补不了进 D；X17 没批准就合并了 → 记录违规、不自动回滚；X18 已关但验收不齐 → blocked；X19 全员停手且没有合法等待 → 按顺序给出一个结果（E / D / 派续 / 问负责人）。每次纠偏写 `行, 从→到, 码, 依据`。

### 3.5 出口检查（claude-discipline）
- E1 通过：Claude 主机上经代理查到的 IP 恰为登记值。
- E2/E3 不通过：其他一切情况，或无法核实是在 Claude 主机上测的。
- E4：通过只清掉这一项检查，不授权派单。
- E5：出口恢复不等于可以重放历史积压的派单。

---

## 4. 本仓快照 vs 参考实现运行副本（已知差异）

| 项 | 状态 | 移植怎么办 |
| --- | --- | --- |
| `bot-global-rules.md`、`herdr.md`、`claude-discipline.md` | 运行副本多了「Claude 续跑直接 pane 注入」「issue CLOSED 关 tab」等节；公开包仅提供固定提交的脱敏快照 | 以 §2.10、§2.12 为准 |
| [可选自动化设计](sop/cases/local-automation-design.md) | 仅设计文档，runner 代码与定时安装样例未分发 | 可选进阶，未部署；需要时由部署者另行提供并核验，不是默认搭建依赖 |
| 可选 runner `local_board.py` 及各主机定时样例（均未分发） | 可选实现未随本公开包提供 | 同上 |
| 旧全局规则 §1–§11 | 不在新版正文 | 已在 §2 摘要补齐 |
| 负载均衡、Claude 默认档位两条更新 | 有变更记录，但运行副本正文里找不到 | 已在 §2.8、§2.9 补齐 |
| 历史夜间静默（07:00–22:30 才打扰负责人） | 已废止，改为问句全天当次发 | 按需自定，但要写进规则 |

【LLM：Claude@云电脑｜模型=Opus 5.5｜effort=high｜fast=否】
