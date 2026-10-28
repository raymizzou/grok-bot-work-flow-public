# #17 原会话恢复安全契约与 #24 演员迁移

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

原票 #17（历史示例，原记录不随公开包分发） / PR#23（历史示例，原记录不随公开包分发） 已合入 main `21301ba4d9db5a3cd77748ea90ed8eb0625beb37`。#24 最新定案以本机脚本为主、Bot 每小时兜底、无当前批交接触发、本批/session 一次恢复。旧 guard-only、30/day、三次 H2、无限新 occurrence 预算废止；[总纲](local-automation-design.md) 与 [lifecycle §5.6](../lifecycle.md#56-派续由父代理执行pending_dispatch) 是当前操作定义。#23 的入口发现、真实云覆盖/UNKNOWN、父回执和 guard 归属证据按该节保留。合入 main 不证明安装/激活。

PR#23 精确历史快照（历史材料未分发，不是安装依赖） 保存原 P1–P36、原证据链接及验收边界；其中旧政策仅作历史，不再执行。

## 纸面守卫（PASS 仅指规则一致）

| 场景 | 预期及负断言 | 结果 |
| --- | --- | --- |
| 精确出口 | 真实云本次 `curl -s -m 8 -x YOUR_PROXY YOUR_IP_ECHO_URL`，exit=0，trim 仅 `YOUR_EGRESS_IP` 才清 gate；不由出口产生任务授权 | PASS |
| 错误/空/多值/非零/超时 | 本次不恢复，下个五分钟 tick 重核；不直连、不借别机结果，不与 guard 对打 | PASS |
| 主机/出口 UNKNOWN | 不恢复，真实状态保留 UNKNOWN，不补造成功观测 | PASS |
| 工作中/有活跃命令 | 原身份仍 working、busy 或在途无法核明时不 start/prompt，不覆盖 dirty 工作 | PASS |
| 暂停/撤销/其他任务 | active=false、删除 task、host/task/tab/pane 不匹配均不恢复 | PASS |
| 已交付 | 当前 task+batch handoff DONE/BLOCKED/OUT_OF_SCOPE 均不恢复；旧批 DONE 不当当前完成 | PASS |
| 身份缺失/歧义 | 原 session/model/effort/worktree 缺失、不符或多个候选进程时不猜、不用默认模型、不新建 | PASS |
| 只有 shell/unknown | shell 单独不够；需先前已核实原身份、精确原 session resume 提示且 shell 自身前台无其他命令 | PASS |
| 正常退出缺交接 | #24 视为卡住，不必猜 guard；满足身份/无在途守卫才能原会话一次恢复 | PASS |
| 重复 tick / 不确定提交 | mutation 意图先持久记录；同次停止不重复 start/prompt；超时/结果未知保留现场给 Bot | PASS |
| 续跑后又停 | 仍无交接就给 Bot 问 YOUR_OWNER，不因相同 session 的新 kill 无限恢复，不重置一次预算 | PASS |
| 启动/身份/ready/ACK 失败 | 一次诊断 pane read、发问题，无盲重启；CLI 提交不算成功，十分钟内新 working 或编号 ACK 才证实 | PASS |
| wrapper 再验拒绝 | 不绕过 wrapper/代理，脚本不重复未知启动；Bot 核清未起后依原授权处理，不冒称恢复成功 | PASS |
| 夜间 | 03:40 与白天同一守卫、同次处理；无 08:00 排队，授权内提醒全天 | PASS |
| 停止时间未知 | 不捏造 guard/time；绑定当前 batch/session 与真实停止观察，不从每轮轮询造新恢复额度 | PASS |
| 原名字消失 | 按原 pane + 原任务/tab 映射，原会话先 start；不能向 shell 发自然语言，不新 tab/session | PASS |
| ACK/历史 pending | 只认当前 task/batch/编号，旧 ACK/working 不算；不重发完整 brief、历史 pending 或已贴 GitHub 评论 | PASS |

固定提醒与 CLI/状态格式见 [总纲的送达与恢复](local-automation-design.md#送达与恢复)。#24 离线 CLI 测试通过不等于本机或云已自然杀、重启或证明十分钟时延。

## 集成纸面反例

| 输入 | 当前独立预期 | 纸面结果 |
| --- | --- | --- |
| H1 无关触发行/空 pending、Mac Main working、F PR 已合并 | diff_id 受理后先核实际云当前默认 session/inventory，再行级等待短路；不因此新授恢复权 | PASS |
| 云或部分 pane 不可读、映射缺证据 | 留覆盖/缺口、逐候选处置与零动作原因，UNKNOWN 不当零 eligible；不猜旧 ID | PASS |
| 只有实际云全局 kill 告警 | 告警已观察，归属仍独立核；不宣称该 session 被杀，也不把来源未知当“无 kill” | PASS |
| 三项 guard 归属全真、但当前 DONE/保留指令或原命令仍活跃 | 不恢复；归属不替代交付、授权或 no-inflight | PASS |
| kill 时间/归属无法证明，但完整独立 #24 当前批未交接/身份/无在途/预算可核 | 不宣称 kill、不填未知 kill 时间；只按一般 #24 路径核验，缺任一独立守卫仍不恢复 | PASS |
| 脚本已有意图、失败/已耗预算或 ACK 在途 | Bot 不重复 queue/start/prompt，不因新 occurrence 重置预算 | PASS |
| 仅有 resume 队列、缺父执行/未执行原因或同原身份 ACK | 标未证实，结束 wake 前逐项对账；CLI accepted 不当完成，不盲重发 | PASS |

## 实际证据与当前验收

故意杀父辅助试跑报告（历史示例，原记录不随公开包分发） 已报告同 pane/name/session 恢复并继续写心跳，支持“能恢复原会话”。原记录 `YOUR_TASK_ROOT/YOUR_TASK_EVIDENCE` 明确是父代理直接执行，**未走 H1/H2 自动路径、未触发自然 guard**，还记录一次 post-resume prompt 未 ready。不能把续写当整条提醒/ACK 全过；该 DONE 试跑不再续。

YOUR_OWNER 后续决定（历史示例，原记录不随公开包分发） 保留故意杀结果、先不关单，要求自然路径；t525u 进展（历史示例，原记录不随公开包分发） 报告自然告警与未见自动续跑 ACK。这不证明具体会话资格，也不从缺 wake 日志推断 H2 未执行或某个根因。旧 L1 的父辅助证据已存在，自然 H1/H2 全链仍未证实；旧 L2–L5 仍 DEFERRED；L6 旧版安装报告不证明 B03 新入口/读回已完成。以上是合入源的历史报告，本批未重新访问现场或把它们回填为 #24 PASS。

#24 AC-1–AC-4 时延、AC-5 三种真机演练、AC-6 七天观察仍 **NOT RUN / 部署另批**；八个 #24 纸面场景仍见 [总纲](local-automation-design.md#八个纸面场景)。#17 自然杀验收按 #24 交由本机脚本为主完成，Bot 只兜底；完整证据需发现、资格、本次实际云出口、排队、父执行/未执行原因、原身份 ACK/续写逐层可读。合入 main、旧纸面 PASS 或父辅助结果不替代当前三机安装和自然路径验收。本批没有实际 kill/start、curl、routine 或安装。
