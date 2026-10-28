# Herdr 操作指引（新整理，非缺失的旧 SOP 原件）

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

参考文档基于 CLI `herdr 0.9.1`；不代表新部署者任何主机的安装版本，也不是最新版声明。
安装步骤参考 [Herdr 官方安装页](https://herdr.dev/docs/install/)，2026-10-24 已在线核对。
官方 macOS/Linux 安装入口为 `https://herdr.dev/install.sh`；先下载审阅再由人执行，具体命令见 bootstrap。
[官方 agent automation](https://herdr.dev/docs/agent-automation/) 是动态参考，使用已安装 CLI 的 help 核对语法。
不复制 #437 下载中的二进制、会话状态、源码或日志。

## 每个任务先核对归属

在 Herdr 内执行：

```sh
test "${HERDR_ENV:-}" = 1
herdr --version
herdr --help
herdr agent
herdr agent list
```

从 live 列表取得名字后才 `herdr agent get <name>`，核对 session、cwd、workspace、tab、pane。
继承环境和焦点只是线索，不能证明归属。tab/agent 命名遵循 [状态机](board-state-machine.md)。
不要操作非任务所属窗格；Mini/远端资源需单独授权，不修改 SSH trust 作为绕过。

## 派工与回收

Main 先取得范围批准，在持久目录放唯一 brief，指定唯一隔离 worktree、批次 ID、验证命令、排除项和原子交接路径。
worker 先读 brief，向 live 核对的 Main ACK ID/目标/步骤/边界，然后只改授权工作树；Git 元数据由 Main 管理。
worker 不额外启动代理；reviewer 只读。明确批准的 scope-local 修复可以继续，架构/风险/模块扩张先交 Main 决策。
交接 DONE 只表示批准批次完成；BLOCKED/OUT_OF_SCOPE 写清条件与所需决定，原子写临时 sibling 再 rename。
Main 核对当前批次 handoff、路径/身份/实际命令，保存原始失败与日志，不把工作徽标当进展。

每次 launch/prompt 前读当前 CLI 组帮助，使用返回的真实 ID；不要复制文档中的示例 ID 当实际目标。
保留用户焦点；启动成功不等于读过 brief，需观察 ACK。
容量/连接错误先查活跃命令与最后实际进展，再按部署者批准的有界恢复政策处理，不能复制运行中的测试或提交。

## #24 本机恢复与 #17 Bot 兜底

PR#23 已合入 main `21301ba`，其旧 Bot-only/guard-only/每次 occurrence 可重启的演员与预算规定由 #24 废止；保留发现先于行级短路、实际云 inventory、UNKNOWN、父回执和归属证据。当前完整规范见 [lifecycle §5.5/§5.6](lifecycle.md#56-派续由父代理执行pending_dispatch) 与 [#24 总纲](cases/local-automation-design.md)，历史原文/实际父辅助证据见 PR#23 快照（历史材料未分发，不是安装依赖）。源码合入不证明本机/云安装与 live 验收。

每个非重复 H1/每次 H2 先核实际云当前默认 Herdr session 和真实 agent/tab/pane，再续期 wait/行短路；空 pending、无 open PR、跟进方 Mini/Air、Mac Main working 或 F PR 已合并都不能省略同任务云候选。名字消失核同任务历史映射，不猜旧 ID。扫描时间/覆盖缺口/逐候选处置/空队列原因即使零动作也写现有 WAKE_/FALLBACK_，UNKNOWN 不是零 eligible；本次 resume 要有父执行或未执行原因、原身份 ACK/续写回执，CLI accepted 不等于开始。

执行仍须当前原授权任务无本批交接、精确原 task/tab/pane/name/session/model/effort/worktree、完整原生命令/后代进程无在途证明和同一 batch/session 未用预算。脚本为主，父代理驱动同一恢复记录/锁；已有意图/已耗预算/失败/未知或 ACK 在途就不再提交恢复。Claude 仍只在实际云核新鲜 YOUR_PROXY 精确出口并走未改 wrapper。确认退出成 shell 才先原会话 start，新 working 不再 prompt，busy/unknown 不 prompt；此退出路径仍只在原身份 idle/done+ready 且命令证据完整后通用提醒。活着的 Claude 按下面 Herdr 停态与空输入框判断；Codex 原有恢复不变。恢复只一次，失败问 YOUR_OWNER，不借普通投递重推增加恢复次数。

若具体声称 guard kill，必须按 lifecycle 的独立三项 AND 核实际云 `YOUR_GUARD_ALERT_LOG` 精确杀线、北京时间/唯一主 transcript 的秒级对齐和之后无写入、同原 pane 精确 hint；UNKNOWN 不猜。#24 一般缺交接路径不要求编造 kill 归属，归属也不授权恢复 DONE 或活跃命令。H2 每小时/共享 100/day 依 #24，旧三次/30 次规定废止；本批不改线上频率。

## Claude 停输出恢复 v2（YOUR_OWNER t597u）

当前任务 `active=true`、本批没有交接（见过后文件消失也算已交）、原身份及无在途核验通过时，活 Claude 是否已停由 Herdr 判，不读报错、耗时或页脚文案，也不用「多久没出字」。有名任务要求 `agent list` 与 `herdr agent explain <原name> --json` 都是 idle/done。同一精确 pane 已登记为 Claude、name 缺失/为空时，用 `herdr agent explain <原pane> --json`，只认顶层 agent=claude、state=idle/done。名单完全没有该 pane 时，真实 Herdr 0.9.5 返回 agent_not_found，判不了、零动作并去重交 Bot；不把预存 explain 结果当作登记证明。活 pane explain 保留标题判态，不改成 pane read 后 `--file`；`--agent` 仅用于离线 `--file`。冲突名字、kind/session、重复映射及任何原身份不符仍拒绝。

空输入框只表示能否安全打字：空 `❯`（含 NBSP）下一行必须就是关闭分隔线，框内文字、空行、空格行或 NBSP 续行都拒绝；分隔线下页脚不影响判空。框本身不判 idle。Herdr 或 pane 明确 working/busy/blocked 时不注入，working 安静多久都一样；blocked/unknown、explain 失败或有草稿时零动作，发一次去重 milestone 给 Bot 核查，不替 YOUR_OWNER 答权限弹窗。

只在实际云本次 YOUR_PROXY 精确出口通过后，注入前再核一次原身份、仍是同一停态/序号、原生进展未变、无后代/在途工具且仍无交接，才原 pane 提交：

```sh
herdr pane send-text <原pane> '<继续原 brief 未完交付、先查文件和评论去重、保留原只读/任务边界的固定提醒及 ACK 编号>'
herdr pane send-keys <原pane> Enter
```

不先 agent prompt、不 start 活进程，`interactive_ready=null` 不代替也不阻止完整停态/空框证明。固定提醒不新增合并/部署/关单权，不重放整份 brief；Codex 与确认退出恢复保留原路由、参数及 ACK/seq 语义，只共用这一提醒文案。完整核验见 [#24 总纲](cases/local-automation-design.md#送达与恢复)。

每 batch/session 只恢复一次，与退出路径共用预算；不按报错次数另计。先原子存意图和原生游标再提交，文字或 Enter 失败/未知都不补发。十分钟内只认游标后真实同 session assistant 输出/工具活动或精确 ACK；用户输入、徽标/seq、元数据不是开始证明。原身份仍可核时，缺少证明或 explain 暂不可判保持原 pending 窗口；超时或续上后再停仍无交接，发一次 YOUR_OWNER 问句。旧状态含 interruption 或 occurrence/attempts 时本实现失败保留，交 owner 核验，不自动清空或重新给预算；新 activity/cursor 必须配对有效。

历史反例：Claude 曾说「P2 已修到位」，随后 `API Error: The response stopped arriving. The response above may be incomplete.`，停在空框且无交接。这是例子，不再是触发条件；换一种错误、普通结束或换统计行都按同一停态规则。离线测试不证明云安装或真实恢复已验收。

## busy / 利用率

working 需要与实际任务身份及最新读写/命令证据一致；idle 只描述观察时点，不代表任务完成或允许降为 todo。
本次没有找到独立 busy/利用率采集脚本，也没有可安全导出的安装/清理脚本。
不凭徽标算利用率，不新造监控或清理器，不杀活跃 session。实际需要时另行定义范围与授权。

可选 [codex-herdr](../scripts/common/codex-herdr) 是本机现有标准库 wrapper 的原样副本：
查找 PATH 中的 codex，在 Herdr 环境转发窗格上下文并用 --no-daemon 启动。
它不安装 Codex、不切模型、不修改配置。本批只语法核对，未启动额外 agent；新环境启用前核对其 Codex CLI 兼容性。
