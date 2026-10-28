# #24 看板中心与本机脚本（交付版，未部署）

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

依据：YOUR_OWNER t552u 定案（历史示例，原记录不随公开包分发）。本页是 #24 的操作总纲；旧补丁中 30/day、08/13/19、禁止本机定时脚本、只恢复 guard-stop、无限新 occurrence 恢复的规定废止。历史文件保留历史身份。

## 四个角色

| 角色 | 写/读 Page | GitHub | 恢复 |
| --- | --- | --- | --- |
| 任务流 Bot | 唯一读写者 | 读取完整事实、判断、分发 | 每小时兜底并问 YOUR_OWNER |
| 本机脚本（Air / Mini / 云） | 不读、不写，只推信号 | 仅云脚本发现新动静 | 原任务无本批交接时，本机原会话一次 |
| Claude / Codex 执行端 | 不读、不写 | 按原 brief 发布/修改 | 每次停手写本批交接并驱动本机脚本；worker 只交给 Main |
| YOUR_OWNER | 读板、答问题 | 无须盯 | 只回答 Bot 的明确决策问句 |

唤醒入口只有三种：本机脚本更新、云脚本发现 GitHub 新动静、每小时 H2。三种进入同一套生命周期判断，只有 Bot 写板。每次刷新当前状态、上次更新时间、跟进主机、**待推送**与送达状态。问题保留原选项、推荐项、不回答时停在哪里，同次唤醒聊天提醒，夜间也发。正常停手可交 DONE 并发 wip/milestone；只有贴出需 YOUR_OWNER 回答的实际决策问题才交 BLOCKED，不以仍 working 掩盖问题。

## 本机记录的责任与命令

另批部署后，每台主机只有一个 `~/.local/state/local-board/dispatch.json`，由本机登记 owner 通过下述锁内单条登记接口维护；Bot 派单时要求该 owner 更新当前批身份、投递编号与派前 `state_change_seq`。首次记录须在 agent 仍 working 时核实本机 Herdr 的 tab/pane/terminal/session、前台进程 cwd、显式 model/effort 参数（Codex 还须显式原始 `service_tier="default"`），不能从默认配置猜；同时绑定 `activity_log` 为该原 session 的 native JSONL 绝对路径，加入当前批身份。Bot 将所有开票 issue/PR（含在其他主机做的票）导出到**云本机**该文件的 watches；每次开/关/换 PR 后登记对应记录，脚本不访问 Page。Bot 是导出 owner；本机 Main 是登记 owner。云上直接派 Claude 评审而无该任务本机 Main 时，由云端实际派单 owner（父 Main / 任务流云执行端）负责登记，不得漏记。所有 Main 写入者都用同一接口，禁止先读旧全文件再无锁替换；交接给出实际路径与登记证据。

单条登记输入是 HOME 内一份 task/watch JSON record（不是整个 manifest）。登记在读取现有 manifest **之前**取得同一个 `.lock`，只更新对应 task_id 或 repo+issue+pr，保留其他记录；文件缺失可初始化空 version1，损坏文件拒绝覆盖。不观察、不投递、不启动 agent；不与 `--task/--github/--cloud-egress/--close-event` 混用。

（可选 runner 命令未随公开包提供；本节保留身份、锁、收据与一次预算设计约束。）

- 格式见 [JSON 示例](../../templates/LOCAL_BOARD_DISPATCH.json)。`tasks` 是本机执行映射；`watches` 是 Bot 的全板开票导出，和 tasks 无须重合。`active=false` 表示 Bot 暂停；删除 task 表示撤单，均不再恢复。换任务/授权用新 batch；同批不得换 terminal/session/model/effort/service_tier 或删除状态来重试。
- 字段 `brief/worktree/handoff/ack/activity_log` 为当前用户 HOME 内绝对路径，不得指向凭据；不接受任意命令、shell、SSH 或远端目标。每任务一条，name 和 tab label 均须包含 task_id 中首个 issue 编号（数字边界匹配，如 `workflow24-pr25-r3` 与 `24-pr25-r3`）；pane/tab/workspace/terminal 仍须与原记录精确相符。session 由原生 JSONL 的 sessionId/cwd（Claude）或 session_meta（Codex）绑定，Herdr 可选 agent_session 若存在则不得矛盾。身份无法核实推一次「无法核验」、观察失败并保留 UNKNOWN，由 Bot 核查。
- handoff 是 UTF-8 JSON，当前 `task_id+batch_id` 必须匹配：`{"task_id":"workflow24-example","batch_id":"C1","status":"DONE","summary":"实现已交接，等 Main 验收","question":""}`。可选 `evidence` 字符串保留已核实评论 URL/PLAN/详细报告路径，透传到原信号 evidence（不增加 helper 顶层字段）。DONE 的 question 必须空；BLOCKED/OUT_OF_SCOPE 必须有 `YOUR_OWNER 需决策：…` 问句；先写 sibling 临时文件，再 rename。若详细报告是 Markdown，在 summary 写短结论、详细报告路径留在原 brief，JSON 是明确的本批完成凭证；禁止从旧 Markdown 中猜 DONE。当前交接语法/内容不符或不可读时，本批去重报一次 wip/milestone「交接格式不符」，观察失败且不恢复；有效旧批交接仍忽略。
- 原 brief 要求的 GitHub 评论/文件发布完成并核对后才写最终 handoff；部署后旧执行端直接 POST 完成信号步骤废止，由脚本统一发送，不额外双发。脚本不把通用 `DONE:`、旧输出或旧批交接当完成。DONE 仅发 wip/milestone；本脚本从不发整票 done/finished，也不关单。
- 每次 Codex/Claude 停手前，Main/独立执行端必须写本批 handoff，再运行下列立即命令（与定时命令同一文件锁）；worker 仍只原子 handoff 给 Main，由 Main 调脚本。部署前继续现有 helper，由 Main 按既有权限发信号。

（可选 runner 命令未随公开包提供；本节保留身份、锁、收据与一次预算设计约束。）

Mini 改 `--host mini`；云改 `--host 云电脑` 并加 `--github --cloud-egress`。程序为一次运行；[Air](../../scripts/air/README.md)、[Mini](../../scripts/mini/README.md)、[云](../../scripts/cloud/README.md) 的五分钟样例不会自行安装。需 Python 3.12、Herdr、既有 helper，云另需 gh/curl。没有依赖安装器、模型判断或跨机转发。

## 送达与恢复

Bot 在板行持久保留待推送内容、编号、目标主机/原 tab、派前 seq、派出时间和 attempt；不能只存 WAKE 文件。投递后 Main 更新 manifest.dispatch。脚本只认可该编号、当前 task/batch 的 JSON ACK，或原会话在派前 seq 后的新 working；旧 working/旧批 ACK 不作收据。ACK 文件格式：`{"task_id":"workflow24-example","batch_id":"C1","dispatch_id":"delivery-24-C1-1"}`。收到后只报一次「已收到」，Bot 读回后清板行 pending。十分钟未确认报 wip/milestone「未确认」并保留 pending；Bot 下次唤醒重推一次（attempt=2），再次失败则问 YOUR_OWNER，脚本不替 Bot 重发任务。

无当前交接、active、本机身份唯一、没有在途进程且原生工具活动证据完整结束，才考虑恢复。Codex 保留 known idle/done 触发；活着的 Claude 改用下面 Herdr 停态 + 空输入框判定，普通 idle/done 也可在原授权内恢复一次；不按错误文案或无输出时长判断。已观察过该原会话且 shell+精确 resume 提示确认退出时，保留原退出恢复路径。同名 unknown 且无 agent 类型，或报告原 kind+idle/done 但前台已是原 shell，并有精确 resume 提示时，也可按已核验退出处理；仍须先前 verified working、原 shell pid/cwd 和全量命令结束证据。其他 unknown/busy、身份缺失/歧义、活跃/不可核明命令、已交付/暂停/撤单都不提交恢复；本批正常交接一旦观察到，即使文件后来消失也不恢复，旧批/其他任务交接仍分开核对。Claude 只在云电脑；C2 只读核实了 Air 历史 Claude 2.1.70 的真实 sessionId/cwd、tool_use/tool_result 与同步 Bash toolUseResult 格式，并以该原生语法做离线契约；实际云版本/日志兼容性仍待部署另批核实。未知/异步/缺失格式保持 UNKNOWN、零 start/prompt，不能拿 Codex 日志冒充 Claude 证明。精确出口门禁仍保留，且启用出口开关后本次固定 `curl -s -m 8 -x YOUR_PROXY YOUR_IP_ECHO_URL` exit=0、trim 后仅 `YOUR_EGRESS_IP` 才可续；错/空/多值/超时等下一轮，不与 guard 对打，不用别机/直连结果。

Codex typed idle/done 仍按原路先 `herdr agent explain <name> --json` 复核原顶层 agent/state；只认同值 idle/done，working 抑制，失败/未知/不符零动作。Codex 和确认退出路径、参数、原 ACK/seq 语义不改。活 Claude 有名时 list 与顶层 explain 都须 idle/done；若同一精确 pane 已登记为 Claude、name 缺失/为空，则 `herdr agent explain <原pane> --json` 只认顶层 agent=claude 的状态。名单完全缺 pane 时 Herdr 0.9.5 返回 agent_not_found，判不了、零动作并去重交 Bot，不能靠预存 explain JSON 续跑。不从框或字幕猜状态；有冲突 name/kind/session、重复映射或原身份不符仍拒绝。pane 明确 working/busy/blocked 也抑制。working 安静多久都不动；blocked/unknown/判不了/草稿发一次去重 milestone 交 Bot，不回答权限问题。

输入安全条件保留 P1-1：空 `❯`（NBSP 可 trim）下一行必须紧接关闭分隔线，框内任何续行（包括空行/空格/NBSP）都零注入，页脚可任意。它只判断能否安全输入，绝不决定 idle。过本次云出口后、第一次提交前再观察：同一个原身份仍 idle/done、状态及序号一致，原生活动未变、没有子进程/未完工具、仍无交接、框仍空。命名任务比 Herdr state_change_seq；已登记无名任务使用完整解析 explain 对象的稳定摘要核同一个停，摘要不是 provider 整数序号。fallback 派单收据仍只认精确 ACK，不拿摘要和整数比较。

符合上述条件才直接 `herdr pane send-text <原pane> '<固定提醒及 ACK>'`，然后 `herdr pane send-keys <原pane> Enter`。不先 agent prompt、不 start 活进程；`interactive_ready=null` 不替代完整证据，也不是额外阻碍。历史 t588u 中 Claude 说「P2 已修到位」，随后显示 `API Error: The response stopped arriving. The response above may be incomplete.` 停空框、无交接；这个反例说明漏报，不再作为文案门禁。任意既往输出、统计行或其它错误，都用同一 Herdr 停态规则。

每 batch/session 只自动恢复一次，活进程与退出路径共用；不按 occurrence/错误次数重开。意图和原生内容身份/游标在第一条文字前原子保存；文字失败/未知不 Enter，Enter 失败/未知不重发。活 Claude 只认游标后的真实同 session assistant 输出/工具活动或精确 ACK，结构化 isApiErrorMessage 不作干活；不按文本前缀排除输出。用户输入、徽标/seq、页脚/元数据不能 ACK 工作。原身份仍可核但没新证明/暂时 explain 不可判时保持原十分钟 pending，不重置窗口；超时、或确认开始后又停且仍无交接，发一次可行动的 YOUR_OWNER 问句，即使 fallback 摘要未变也不再注入。

新恢复记录不写 interruption/occurrence/attempts；activity/cursor 必须一起有效。本实现读到这些旧 API 状态键时失败保留原文件，交 owner 核验；不自动迁移、删状态、清预算或再给一次。通用 since/seq 校验沿用 Codex/退出路径原语义，活 Claude 游标架构另做字段完整性核验。安装/真实恢复需另批取证；[Herdr 操作说明](../herdr.md#claude-停输出恢复-v2your_owner-t597u)。

退出成 shell 时，先原 pane/name 用原 session/model/effort start（Codex 必须带原始 `-c service_tier="default"`，fast/priority、缺失、矛盾或重复 tier override 一律拒绝），保留既有 wrapper 再验；Herdr start 在原生 `--` 前带 `--timeout 25000`，外层命令超时仍为 30 秒，不重试未知启动；读回原身份 ready 后才固定提醒：

> Continue the unfinished original brief delivery. First check files already written and issue/PR comments already posted; do not post duplicates. Preserve the original read-only and task scope. No new authority to merge, deploy, or close issues.

所有路径共用上述固定提醒，尾部附 `ACK recovery:<batch_id>:<session>`，ACK JSON 同上。上述退出路径及 Codex 仍按原规则：CLI 提交不是成功，十分钟内新 working/seq 或精确编号 ACK 才报续跑；活 Claude 按前述游标后干活证明。脚本把 mutation 意图先原子记录；不确定 start/prompt/pane 提交不重试。一次失败、未 ACK，或续跑后再次停下仍无交接，报问句让 Bot 问 YOUR_OWNER，不无限重启。出口未通过尚未提交时下轮可重核。wrapper 拒绝/启动失败一律不绕过，交给 Bot 核验是否确实未起再按原授权处理，脚本不重复未知启动。

#17 的身份、no replay、一次 ACK、wrapper/代理安全边界保留，演员改本机脚本，触发改缺交接，不再猜 guard 原因。PR#23（历史示例，原记录不随公开包分发） 已合入 main `21301ba4d9db5a3cd77748ea90ed8eb0625beb37`；本批按 #24 优先级集成其 Bot 兜底文档，不声称已安装/部署。其发现先于行级短路、实际云 inventory/UNKNOWN、零动作和父执行回执，以及具体 guard 归属证据，统一见 [lifecycle §5.6](../lifecycle.md#56-派续由父代理执行pending_dispatch)；历史快照（历史材料未分发，不是安装依赖） 保留实际父辅助续写及自然路径未证实边界，不抹成全部 live 未跑。#17 自然杀验收改由本机脚本通过；Bot H1/H2 只在脚本漏报且核清没有在途恢复时兜底一次，共用本机状态/交接核对，不能另开无限恢复预算。

## 云 GitHub 提示与信号

watches 全量分页读 issue 正文/评论、PR conversation（`/issues/<pr>/comments`，PR 与 issue 同号时复用）、inline/reviews、当前 PR head checks/statuses，MERGED 后另读准确 merge main SHA。第一轮仅建基线，之后新/编辑评论、评审和 CI 变化只报「有新动静」，不解释严重性或宣称 PASS。忽略明确末尾 `【LLM：任务流 Bot…】` / `【LLM：Grok Bot…】` / 实际 `【LLM：Grok｜任务流 Bot】` 标记，保留同账号无尾标 YOUR_OWNER 与 Claude/Codex。Bot 读回所有来源和精确 head 事实再判断；不能把提示当 R3/ready。任一 API/分页不完整不推进该 watch 游标，下轮仍能捕捉。

每台只调用本机原 helper，15 字段/退出码与凭据边界不变。manifest 相邻 `.state.json` 保存游标、待投递事件、恢复状态和一次重试额度；`.lock` 串行立即/定时调用。manifest 由锁内单条登记更新，handoff、ACK 原子替换；不要手删 state/锁另开进程绕过意图。损坏状态直接失败并保留，不自动初始化覆盖。stdout 只有脱敏结果；无原始命令错误、凭据或 pane 输出。新事件不会被旧待投递事件吞掉。

序号取本机同路径 BOARD_SIGNAL、runner 历史和 `applied.json.signals["任务流/<signal_task>/BOARD_SIGNAL.md"].seq` 的最大值加一；无文件按零，已有不可读/格式坏则失败，不借别路径或别机 floor。`signal_task` 是安全单目录组件（支持实际大写 `YOUR_TASK_DIRECTORY`），不是 agent/task 小写名字规则，不接受分隔符、`.`/`..` 或路径越界。退出 4：下次运行仅对完整相同输入（含 seq/as_of）重试一次；这一次重试未决前，后来的同路径事件留队，不得先发新 seq 再用旧 retry 覆盖；不同路径独立。重试成功或额度耗尽后继续较新事件，耗尽项仍保留 delivery_pending。退出 3/1/2 或提交结果未知不盲重试，修复由 Main/Bot 按现有协议处理。runner 非零表示观察错误或有未送达事件；失败期间仍由 H2 兜底，不能将退出 0/POST 2xx 等同 Page 已更新。运行期间不要让其他发送者同时写同一个 signal_task；云 review 独立目录规则保留。

未解决的失败/待投递事件保持 `delivery_pending` 非零，不因新 seq、过期、新批或重试耗尽自动结案。人工核验处置后可单独运行：

（可选 runner 命令未随公开包提供；本节保留身份、锁、收据与一次预算设计约束。）

该 operator 模式只在同一锁内追加 closed.reason/as_of，不观察、投递、重试或恢复；拒绝未知、未尝试、result=None 在途、成功或已结案事件，原 result/attempts/payload/seen/预算全保留。结案是人工处置，不等于送达成功；后续轮次跳过已结案项，出现任何新未解决失败仍非零。新字段可选，已有状态继续兼容；不手删状态或改 result 伪造送达。

## 每小时与共享预算

H2 改每小时（原 08/13/19 和暂停 30 分钟自检条文废止）；08:00 仍出早报。只对 wip 行上次更新超过一小时的行核本机 Herdr/GitHub，给出仍在跑/已拉起/blocked；主机一小时无推送且有 wip，查脚本/睡眠/可达性并写早报。所有主机、GitHub 提示与 H2 **共用 Bot 每日 100 次 admission**，不是各机 100；Bot 在现有 WAKE/FALLBACK 去重记录计数，超限事件保留待处理，早报/H2报告，不发额外无限 wake，不增跨机计数器或 relay。时延承诺需主机在线、出口正常且预算未耗尽；睡眠/不可达明确例外。

## 八个纸面场景

以下 PASS 是规则推演，支撑离线 CLI 测试见 本批记录（`YOUR_TASK_ROOT/YOUR_TASK_EVIDENCE`）；不是 live 时延证明。

| 例子 | 流程 / 独立预期 | 纸面结果 |
| --- | --- | --- |
| #473 main CI 红 | 云 watch 读准确 main SHA CI 变化→提示→Bot 核 CI 并 blocked 问 YOUR_OWNER；≤10 分钟 | PASS |
| #475 扫描失败停下 | 当前 BLOCKED handoff→立即/五分钟脚本→Bot 同次转述问题；≤10 分钟 | PASS |
| #475 Claude 提待定问题 | 新 issue 评论 + 停手交接 BLOCKED→Bot 核问题并提问；≤10 分钟 | PASS |
| #17 外审 P1 | 新 PR review→Bot 回派原主机/原 tab→精确编号或新 working 回执；≤10 分钟送出 | PASS |
| 17:16 未送进去 | 十分钟未 ACK 留板行 pending→下一 wake 重推一次→再失败问 YOUR_OWNER；≤1 小时 | PASS |
| #17 guard 杀 Claude | 无本批交接且证实原会话退出→出口恢复后下一五分钟 tick 原会话一次；再次失败问 YOUR_OWNER | PASS |
| done tab 无人续 | 无交接的 known done→本机续一次并推更新；脚本漏报由每小时 H2 核；≤10 分钟/最迟一小时 | PASS |
| 关单靠 YOUR_OWNER 开口 | Bot 核合并、准确 main CI、验收/部署门禁；只剩另批部署时同 wake 问现在关还是等部署，不自动关 | PASS |

AC-1/2/3/4 live 时延、AC-5 三种真机演练、AC-6 七天观察：**NOT RUN / 部署另批**。AC-5 八纸面 PASS；AC-7 本地离线边界检查 PASS，真实三机仍 NOT RUN。#2 已并入关闭，试跑无幻觉由 #24 AC-6 覆盖，不能回填七天 PASS。合并、部署、实盘、资金/凭据授权独立；本批不安装 routine、scheduler 或个人指令。

## C2 无在途证明的可核边界

Herdr 0.9.1 的 foreground_processes 不覆盖模型工具的独立 PGID，不能单独证明命令结束。runner 用本机 `ps -axo pid=,ppid=,pgid=,lstart=,comm=` 递归原 agent 后代，保存 PID+出生时间，退出后已观察过的孤儿仍可识别；不读环境/凭据。当前前台以外的任务后代存活、ps 缺失/不完整均 UNKNOWN，不能恢复。

同时解析当前 manifest 绑定原 session/worktree 的真实 Codex `session_meta.payload.id/cwd` 与 response_item 工具 call_id/匹配 output。完整同步命令或 yielded exec_command 随后 matching write_stdin 完结才算 settled；外层 functions.exec 返回不清除未结束 session_id。日志无匹配输出、局部写入、错 session、不可读、未知 provider/语法、无法归属的 wrapper 结果、显式 detached/background 不确定性均保留 UNKNOWN。仅观察支持的命令结果格式，不能据 shell 空前台补造无在途。日志上限 32 MiB，超限不截断猜完成。此限制会保守拒绝复杂/不支持的原生记录；没有部署或真实恢复 PASS。

shell 恢复前还须 pane cwd 与实际 shell cwd 都等于原 worktree；start 后原身份已新 working 则承认开始，不再 prompt；busy/unknown 或命令未明均不 prompt。此 shell 启动后的 idle/done+ready 也须再次核无在途才发固定提醒；活 Claude 只按上文 Herdr 停态与空输入框条件处理。Bot 兜底同样不能拿 foreground/interactive_ready 替代这些守卫。

Claude 同一 session 可有历史 cwd 变化，但最后显式 session cwd 必须是原 worktree，当前前台 cwd 仍精确匹配；外来 session、sidechain、缺少当前 cwd 绑定仍拒绝。完整历史所有工具调用/结果都扫描，不能截掉旧 pending/background。

Claude 支持同步 Bash（无后台/中断、已匹配结果）与 Read/Write/Edit/Glob/Grep 成对结果；匹配 Bash error tool_result（is_error=true）的字符串错误结果可判结束。字典继续要求 interrupted=false、stdout/stderr，只增加 persistedOutputPath/persistedOutputSize/gitOperation/returnCodeInterpretation；不读输出文件。backgroundTaskId/timedOutAfterMs 只要出现就拒绝，未知字段、Agent/未知工具、不完整和 detached/background 仍 UNKNOWN。云引用字段/字符串类型 fixture 不是整份实采原文。原生格式来源与脱敏字段证据见 C2 格式核验（`YOUR_TASK_ROOT/YOUR_TASK_EVIDENCE`）。

## C3：原生返回必须可归属，stdout 不是完成证明

Codex `functions.exec` 只接受**一次单工具完整结果透传**，参数必须是 JSON object；以下各为独立的一次调用，不合到一个 wrapper：

```javascript
text(await tools.exec_command({"cmd":"pwd"}));
```

若命令真实返回 session_id，则后续独立调用：

```javascript
text(await tools.write_stdin({"session_id":123}));
```

原生日志中的完整 passthrough 记录须有匹配 call_id、真实 Script completed 外层块和**一个**完整工具返回 object（chunk_id / wall_time_seconds / output，以及 exit_code 或运行中的 session_id）。`output` 是程序 stdout，始终只作数据，不递归解析里面的 JSON 当完成证明。受信的运行中 session_id 只有匹配的完整 write_stdin 完结返回才能清除。direct native exec_command/write_stdin 也只接受其完整原生返回 envelope；Claude 已核实的原生 tool-use/result 规则不变。

`text(r.output)`、变量/projection、手写 summary、任意变换、多工具/额外副作用、pragma/comment wrapper、缺字段或额外未归属 output block 均保持 UNKNOWN。即使 stdout 刚好长得像完整工具 JSON 也不放行；形状和块数量不证明来源。这里只识别上面小语法，不做通用 JS/dataflow 推断，不加 daemon/hooks。很多旧 Codex wrapper 因而不能自动证明无在途；不要改写旧 native 日志或清状态伪造完成，交 Bot 按已有权限核验。

真实、无秘密的单条 canonical call/return 由 Main 的无副作用 probe 留证：C3 envelope（`YOUR_TASK_ROOT/YOUR_TASK_EVIDENCE`）。它证明上述 envelope 格式，不能当 live 恢复、三机兼容性或七天验收。
