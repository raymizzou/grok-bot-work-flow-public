# 多机 Agent 工作流：一个 Bot 调度 + 云端 Claude 设计 + 多台 Mac Codex 实现

> 这是公开工作流模板，与私有实现仓库分开维护。
> 不包含真实私人路径、出口值、凭据或私有仓地址；所有 `YOUR_` 均须替换。
> 本包可独立克隆并执行本地测试和隔离 bootstrap dry-run；真实部署仍需单独授权。

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

> English one-liner: a portable playbook for running a multi-host AI-agent workflow — one scheduler bot owns a progress board, one gated cloud host runs Claude for design/review, and two Macs run Codex for implementation, all inside Herdr terminal tabs, with a human owner approving every merge/deploy.

这是一份**通用、可公开**的移植手册。读者可以是任何想搭同款「多机 agent 工作流」的人，也可以是一台新电脑上的 Claude Opus——照着 [MIGRATION.md](MIGRATION.md) 一步一步做就能搭起来。

文中所有 `YOUR_…` 都是占位符，换成你自己的值。真实部署者的私人数值（出口 IP、端口、私有仓地址）**不在本目录**，由部署者自己保存在不公开的地方。

---

## 30 秒看懂

一句话：**人只回答问题，Bot 管进度，Claude 出方案和评审，Codex 写代码，所有 agent 都在看得见的终端 tab 里跑。**

| 角色 | 跑在哪 | 干什么 | 不干什么 |
| --- | --- | --- | --- |
| **负责人（Owner）** | 手机/任意设备 | 看进度板，回答板上的「需决策」问句，批准合并/部署/关单 | 不用盯终端、不用盯 CI |
| **调度 Bot** | 一个支持定时任务 + webhook 唤醒 + 能在各主机跑 shell 的 Bot 平台（参考实现：Grok Bot） | 唯一写进度板的人；派单、核对、汇报；判断每个任务现在在哪个阶段 | 不写代码、不跑测试、不排障（这些叫「重活」，交给 Codex） |
| **云端 Claude** | `YOUR_CLOUD_HOST`（一台常开的 Linux 云主机） | 写方案、做架构/代码评审，结论贴到 GitHub issue/PR | 不写实现代码；不在其他机器上跑 |
| **Mac Codex** | `YOUR_MINI`、`YOUR_AIR`（两台 Mac） | 改代码、跑测试、开 PR、按批准部署、逐条验收 | 不自己合并、不自己关单、不写进度板 |

四端怎么连：

```text
           负责人 ── 读板 / 回答问句 ──┐
                                      ▼
   GitHub(issue/PR/CI) ◀──读写──  调度 Bot ──写── 进度板 Page
        ▲   ▲   ▲                  │  ▲
        │   │   │       派单 brief  │  │ 信号（webhook 唤醒）
        │   │   │     ┌────────────┼──┼──────────────┐
        │   │   │     ▼            ▼  │              ▼
        │   │  YOUR_CLOUD_HOST   YOUR_MINI         YOUR_AIR
        │   │  Herdr: Claude     Herdr: Codex      Herdr: Codex
        │   │  (方案/评审)        (实现/默认部署)    (实现)
        └───┴──────── 方案评论 / PR / 验收回报 ───────┘
```

详细架构和数据流见 [ARCHITECTURE.md](ARCHITECTURE.md)；每端的权限边界见 [ROLES.md](ROLES.md)。

---

## 十一条硬规则（移植时必须原样带走）

这些是参考实现里踩过坑之后定下的规则。换成你的主机名即可，**规则本身别删**。

1. **Claude 只在一台主机跑**：Claude / Claude Code 只在 `YOUR_CLOUD_HOST` 上跑；`YOUR_MINI`、`YOUR_AIR` 上禁止启动 Claude，也不准写「等本机 Claude」。
2. **重活交给 Codex**：改代码、测试、排障、数据分析、部署脚本 → `YOUR_MINI` 或 `YOUR_AIR` 的 Codex。Bot 只调度、核对、汇报。
3. **已开跑的票同机跑完**：一张票已经在某台 Mac 上开始实现，就在那台跑到底。「挑空闲机器」只用于还没有执行主机的新实现。
4. **生产部署默认一台固定机器**：默认 `YOUR_PROD_HOST`（参考实现是 Mini），不随负载均衡漂移。
5. **Herdr 必用**：所有 Codex/Claude 都在 Herdr 的 tab 里跑，禁止无 tab 的后台 agent。tab 标题 `<GitHub issue 号>-<短标题>`（如 `123-login-timeout`）；agent 名 `<task_id>-<角色>`，task_id 含 issue 号。Claude 主机只用 Herdr 的 **default** 会话，脚本不写死别的会话名。
6. **Claude 续跑**：Claude 还在跑 → 直接 `herdr pane send-text <pane> '…'` 再 `herdr pane send-keys <pane> Enter`；只有确认进程已死，才在原 pane 用原名字 `herdr agent start … --resume`。
7. **Claude 默认档位**：Opus 5.5、effort=high，不开 fast。只有负责人点名，或恢复原会话（保持原档位），才例外。
8. **出口闸门**：每次派 Claude 前，在 Claude 主机上跑一次「经代理查出口 IP」，结果必须**恰好**等于你预先登记的出口 IP 才放行。直连 IP 不算数，失败不准改走直连。（命令模板见 [MIGRATION §4](MIGRATION.md#4-claude-主机出口闸门与默认档位)；具体数值属私人配置。）
9. **方案只写六块**：问题、原因、修复方案、当前架构图、修复后架构图、（需要时才加）Open Question。大白话，不自造术语，不另加章节。
10. **四件事必须负责人明文批准**：合入默认分支、部署、关 issue、切换线上开关。CI 绿不等于批准；批准绑定具体 PR 和具体提交（head）。
11. **Bot 额度先批后用**：Bot 自己的模型额度只用于对话、派单、只读核对（每次最多 2 条命令）和写汇报；超出这些（后台子任务、浏览器操作、新增定时任务等）先发卡片请负责人批准。

---

## 从哪开始

| 你是谁 | 先读 | 再做 |
| --- | --- | --- |
| 想了解这套系统的人 | 本页 → [ARCHITECTURE.md](ARCHITECTURE.md) | — |
| 要动手搭的人 / 新电脑上的 Claude Opus | 本页 → [ROLES.md](ROLES.md) → [MIGRATION.md](MIGRATION.md) | 逐步执行，最后用 [CHECKLIST.md](CHECKLIST.md) 验收 |
| 要写或改规则的人 | [SOP_INDEX.md](SOP_INDEX.md) | 只改对应 SOP 一处，别在多份文件里各写一遍 |

样例：[examples/](examples/) 里有脱敏后的一份「方案派单 brief」、一份「实现派单 brief」和一份交接文件。

---

## 名词小词典（第一次见就查这里）

| 词 | 人话解释 |
| --- | --- |
| **Herdr** | 一个终端工作区管理器（[herdr.dev](https://herdr.dev)），能在一台机器上开很多 tab/pane 跑 AI agent，并用命令行列出每个 agent 的状态（working/idle/done）。人可以随时进去看、插手。 |
| **tab / pane** | Herdr 里的标签页 / 标签页里的一个终端格子。一个任务一个 tab。 |
| **进度板（Page）** | Bot 自己维护的一张表，每个任务一行，是「进度」的唯一事实来源；聊天只报异常。 |
| **brief（派单说明）** | Bot 给 agent 的任务书：做什么、不做什么、怎么交付、验收标准。放在任务目录里的一个 Markdown 文件。 |
| **handoff（交接文件）** | agent 停手时写的结果文件：DONE / BLOCKED / OUT_OF_SCOPE + 证据。 |
| **信号（BOARD_SIGNAL）** | agent 或本机脚本写的一份 15 字段小文件，同时 POST 给 Bot 的 webhook，用来「叫醒」Bot 去重新核对。信号只叫醒，不直接改板。 |
| **H1 / H2** | Bot 的两种定时/唤醒检查：H1 = 收到信号就立刻查；H2 = 每小时兜底查一遍。另有每天早上一次早报。 |
| **出口闸门** | 派 Claude 前检查「这台机器访问外网时用的是不是指定的出口」。不对就不派。 |
| **Main / worker** | 一张票的主 agent（Main）和它分出去的帮手（worker）。worker 只向 Main 交接。 |
| **OQ（Open Question）** | 方案里需要负责人拍板的问题，每版最多 5 条。 |
| **G1–G4** | 必须停下来等负责人决定的四类门：架构、验收口径、中途改架构、只有负责人能给的授权（合并/部署/资金/凭据等）。 |
| **A–G 阶段** | 一张票从「入板」到「关单」的固定阶段，详见 [ARCHITECTURE §3](ARCHITECTURE.md#3-一张票的一生ag-阶段)。 |

---

## 现状说明（诚实声明）

- 本包提供**看板唤醒协议、Herdr 派单规则、出口闸门要求及方案/评审/实现分工**；不证明任何新主机、平台或真实任务已运行。
- 「每台机器五分钟本机脚本自动推信号 + 自动恢复一次」的设计（参考实现内部编号 #24）**已写成文档和脚本，但尚未部署**。本手册把它列为可选进阶项，不当作已生效。
- 本包包含文档、模板、信号 helper 与测试，不包含任何凭据、真实 webhook、真实看板 ID 或私有仓地址。

【LLM：Claude@云电脑｜模型=Opus 5.5｜effort=high｜fast=否】

## 公开克隆与本地验证

`YOUR_GH_OWNER` 填公开仓或公开 fork 的 owner；无需访问私有实现仓。以下命令在公开仓根目录执行：

```sh
git clone https://github.com/YOUR_GH_OWNER/grok-bot-work-flow-public.git
cd grok-bot-work-flow-public
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/common -p test_board_signal_post.py -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s bootstrap -p test_bootstrap.py -v
mkdir -p .seed-evidence
workflow_demo_home=$(mktemp -d "$PWD/.seed-evidence/demo-home.XXXXXX")
HOME="$workflow_demo_home" python3 scripts/common/board-signal-post --task task123 --dry-run < templates/BOARD_SIGNAL.json
```

完整的首次复制与无凭据 dry-run 见 [bootstrap](bootstrap/README.md#5-无凭据隔离-dry-run)。`.seed-evidence/` 只保存本地演练与检查产物，不发布。loopback 单测使用动态本机端口与合成凭据，不连接真实 webhook。

默认路径不包含本机自动恢复 runner、定时安装或网络出口 wrapper/watchdog 的实现。前者仅保留[设计约束](sop/cases/local-automation-design.md)，后者按 [MIGRATION §4](MIGRATION.md#4-claude-主机出口闸门与默认档位) 由部署者按自己的授权环境实现；未具备出口闸门时不得派 Claude。Bot 平台、GitHub 登录、agent CLI 与主机访问由部署者提供，本包不创建账号或变更生产。
