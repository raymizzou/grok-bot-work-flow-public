# Claude 出口纪律（workflow#12 限定补充）

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

版本：2026-10-27；依据 workflow#12（历史示例，原记录不随公开包分发） 的已批准出口口径。
这是新写的限定补充，不是恢复的历史原件；只约束 Claude 派单的出口检查，不替代已有 Claude 纪律。
文档交付不表示已安装、已修改 routine 或已完成真实出口验证。

东京/生产只读排查按 [全局规则：东京与生产只读排查（YOUR_OWNER t529u）](bot-global-rules.md#东京与生产只读排查) 走云电脑本机 Shell SSH，独立于 Claude/Herdr；本文件的 YOUR_PROXY 出口检查不作为 SSH 前置条件。§8 的 Claude/Claude Code 云电脑限定、既有云 Herdr 及下述出口纪律不变；不得为拿日志复活 #21 FIX-01/R2 wrapper 修复或重放其历史 pending。

## #24 操作入口（未部署）

四角色、三种唤醒、每小时 H2、共享 Bot 每日 100 次 admission、持久待推送/编号收据与本机一次恢复，统一见 [#24 总纲](cases/local-automation-design.md)。旧 30/day、三次 H2 和禁止本机定时恢复的冲突补丁废止。执行端停手前写当前批交接并立即驱动脚本；worker 只交 Main；只有 Bot 读写 Page。

## 1. 检查位置与唯一命令

Claude 只在云电脑 Herdr 运行。父代理在本次 Claude 派单前，须核实**将实际运行 Claude 的云主机**，在该主机执行：

```sh
curl -s -m 8 -x YOUR_PROXY YOUR_IP_ECHO_URL
```

`YOUR_PROXY` 是该云主机本机代理。Mini/Air 上执行同样命令不能代替云主机观测；不能借用另一主机、旧记录或未核实来源的结果。
直连公网 IP 为 `YOUR_DIRECT_IP` 正常，与此门禁无关；直连 IP 无论是什么都不得作 Claude 出口闸门，也不得在代理失败时改用直连重试来放行。

## 2. 出口判定

- **E1 / egress_ok**：上述命令 curl 退出码为 `0`，输出去掉首尾空白后是单个 IP，且整串恰为 `YOUR_EGRESS_IP`。只有这一条件能清除此项出口检查。
- **E2 / blocked_now**：代理返回其他 IP、空输出、格式错误或多值，或 curl 超时、连接失败、其他非零退出码，一律阻止**本次 Claude 派单的出口门禁**。即使直连返回 `YOUR_EGRESS_IP` 也不放行。
- **E3 / blocked_now（出口未核验）**：不能核实实际云主机，只有 Mac 上的结果、过期结果或根本没有可验证的本次云端观测时，不得声称 egress_ok；未知事实保留 UNKNOWN。

`blocked_now` 是本次派单的出口门禁结果，**不是新增板状态**，不能据此自动把板项改为 blocked。板面仍按 [新版 SOP §3](bot-progress-board-sop_2026-10-26.md) 与 [lifecycle](lifecycle.md) 判断；确实卡目标且必须等 YOUR_OWNER 决策才写 blocked 和正常聊天问句。

## 3. 证据与派单边界

本次 WAKE_/FALLBACK_ 或派单证据记录：经核实的执行主机身份、带时区观测时间、§1 的完整代理命令、curl 退出码、代理结果（或脱敏短错误）。可选直连诊断须标「不参与门禁」，不得让它覆盖代理结果。不记录凭据；没有观测就写未核验，不补造成功证据。

**E4 / egress_ok 仅通过出口检查**：出口正常本身不授权任意启动、恢复或重放；其他授权、安全、容量约束仍分别核验。#24 / t597u 已批恢复仍要求 active、无本批交接、原身份及无在途证明。活 Claude 用 Herdr idle/done + 空输入框判断停住，不匹配错误/耗时/页脚，不计无输出时长；普通停住也走同一规则。有名由 list+explain 复核，已登记的精确同 pane Claude 无名记录由 `herdr agent explain <原pane> --json` 判定，只认顶层 agent=claude。名单完全缺该 pane 时 Herdr 0.9.5 返回 agent_not_found，判不了、零动作并去重交 Bot。working 不动；blocked/unknown/判不了/草稿零动作，去重信号交 Bot。完整规则见 [Herdr 停输出 v2](herdr.md#claude-停输出恢复-v2your_owner-t597u)。

实际云本次 §1 出口通过后，注入前第二次原身份/停态序号/原生活动须与第一次一致，无在途且仍无交接、输入为空，才原 pane send-text + Enter，不先 agent prompt，不 start 活进程。输入框仅用于防夹带草稿，不能代替 Herdr 状态；可选元数据缺失不新增必填字段，但实际 kind/session/name/pane 冲突仍拒绝。确认退出路径及 Codex 原路由不变。t588u 的 API 中断停空框是历史例子，不是必须出现的错误串。

每 batch/session 一次，与确认退出恢复共用预算；已有交接后来消失也不重开。意图先落盘，任一步未知不重试；活 Claude 的原十分钟窗口只认游标后真实同 session assistant 输出/工具活动或精确 ACK，输入/徽标/元数据不算。没有干活证明但原身份仍可核时保留 pending，不另起窗口；超时或续后再次停住仍无交接，让 Bot 问 YOUR_OWNER。Bot 漏报兜底也共用记录；固定提醒保留原只读/任务边界，不新增合并/部署/关单权。旧恢复状态不自动清空换预算，处置见 [#24 总纲](cases/local-automation-design.md#送达与恢复)。本段及测试不表示已做云上真实恢复。

**E5 / 不回放历史 pending**：代理恢复不等于历史 `pending_dispatch` 获准执行，不自动清空、冲刷或重放积压列表；只按当前任务已有授权及本次核验处理，不凭出口恢复产生新授权。上述原会话恢复只处理当前批已核实的一次无交接停止，不重送完整 brief、不恢复已交付工作，也不借此重派历史评审。

不修改或削弱 `~/.local/bin/claude` wrapper 与 `YOUR_GUARD_SCRIPT`，不改代理、网络、SSH 或信任配置。本补充不启动 Claude，不派任何历史评审。

## 4. 消费与交付

H1（任务流看板唤醒）、H2（看板兜底）及父代理的 Claude `pending_dispatch` 都使用上述规则。owner 的可粘贴交付见 [H1/H2 出口补丁](../templates/H1_H2_PROMPT_PATCH.md)，纸面反例见 [T1–T7](cases/claude-egress.md) 与 [原会话恢复用例](cases/claude-auto-resume.md)，三端人工对齐见 [bootstrap §2](../bootstrap/README.md#2-复制-helper-和-sop)。所有安装与真实运行状态均须另取证，本批未完成。
