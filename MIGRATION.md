# 迁移手册（可逐步执行）

> 路径约定：`~/ray-docs` 仅为 helper 默认的参考布局；`YOUR_` 值须由部署者填写，涉及真实主机/出口/凭据的值只留本机私有配置。

给「要在自己机器上搭同款工作流的人」和「照着执行的 Claude Opus」用。每节分三块：**要懂的**（概念）、**要做的**（步骤）、**不要做的**。做完一节就到 [CHECKLIST.md](CHECKLIST.md) 勾一节。

> 执行者须知（给 agent）：本手册里的安装、配置凭据、新建定时任务、第一次真实 POST，都属于「外部动作或不可逆动作」。**每一步动手前先确认部署者已授权**；没有授权就只做只读检查并记录。不要把本手册当成授权。

---

## 0. 移植前先定下来（填表）

**要懂的**：这套系统由「一个调度 Bot + 一台 Claude 主机 + 若干台 Codex 主机 + 一位负责人」组成。先把你的环境对上号，后面所有占位符都从这张表来。

| 占位符 | 含义 | 你的值 | 参考实现 |
| --- | --- | --- | --- |
| `YOUR_BOT` | 调度 Bot 名与平台 | | 「任务流」，Grok Bot 平台 |
| `YOUR_CLOUD_HOST` | 常开 Linux 主机，跑 Claude、Herdr default 会话 | | 一台云 Linux |
| `YOUR_MINI` / `YOUR_AIR` | Codex 执行机 | | Mac mini / MacBook Air |
| `YOUR_PROD_HOST` | 默认部署机（固定） | | Mac mini |
| 信号 host 枚举 | 每台主机一个固定值 | | `air` / `mini` / `云电脑` |
| `YOUR_WORKFLOW_REPO` | 流程仓（本仓或你的 fork） | | 私有流程仓 |
| `YOUR_BUSINESS_REPO` | 业务仓（可多个） | | 私有业务仓 |
| `<SOP_DIR>` | 规则文件目录，**每台主机同路径** | | `~/ray-docs/YOUR_COORDINATOR/sop` |
| `<TASK_ROOT>` | 任务记录目录 | | `~/ray-docs/任务流` |
| `YOUR_PROXY` | Claude 主机本机代理地址 | 写在私有文件 | 私有 |
| `YOUR_IP_ECHO_URL` | 返回调用方公网 IP 的服务 | | 公共 IP 回显服务 |
| `YOUR_EGRESS_IP` | Claude 必须使用的出口 IP | 写在私有文件 | 私有 |
| 负责人称呼 | 问句前缀 `<负责人> 需决策：` | | 负责人名字 |
| 时区 / 早报时间 | | | 美西时间，08:00 早报 |

**要做的**

1. 填上表。`YOUR_PROXY`、`YOUR_EGRESS_IP`、真实 webhook、看板 ID 这类值**只写进你自己的私有笔记**（不进本仓、不进聊天、不进信号）。
2. 如果是在公司电脑上搭：先确认公司的网络、代理、外部 webhook、第三方 AI 服务政策是否允许。不允许的部分不要搭。
3. 确认每台机器能被 Bot 平台执行本机 shell（参考实现靠平台自带的机器连接，而不是主机间 SSH）。

**不要做的**

- 不要把参考实现的私人路径、IP、仓名当成你的值直接用。
- 不要一上来就迁移「已在跑的任务」；先用一张纸面演练票走通（§9）。

---

## 1. 每台主机的基础依赖

**要做的**（每台都跑一遍，只读检查）：

```sh
git --version
python3 --version        # 3.8+
gh --version && gh auth status   # GitHub CLI，本人登录
curl --version | head -1
herdr --version          # 没装见 §3
```

额外：

| 主机 | 还需要 |
| --- | --- |
| `YOUR_CLOUD_HOST` | Claude Code CLI（`claude --version`）；本机代理（固定出口）；出口包装脚本与看门狗（§4） |
| `YOUR_MINI` / `YOUR_AIR` | Codex CLI（`codex --version`）；按本机授权执行只读诊断（§5） |

**不要做的**：不在 Mac 上安装或登录 Claude Code（硬规则 1）。

---

## 2. 取流程仓并安装规则文件

**要懂的**：规则（SOP）只在 `<SOP_DIR>` 一处生效，每台主机同路径、同内容。agent 的个人指令文件（`~/.claude/CLAUDE.md`、`~/.codex/AGENTS.md`）只放「指针」，指向 `<SOP_DIR>`，不复制整份规则。

**要做的**

```sh
mkdir -p ~/projects && cd ~/projects
gh repo clone YOUR_GH_OWNER/YOUR_WORKFLOW_REPO     # 已有目录就先 git status 检查，不覆盖
cd YOUR_WORKFLOW_REPO
ls sop templates scripts bootstrap
```

1. 读 [SOP_INDEX.md](SOP_INDEX.md)，按「必带」清单把 SOP 放到 `<SOP_DIR>`。首次安装可用 [bootstrap §2](bootstrap/README.md#2-复制-helper-和-sop) 的复制脚本（遇到已有文件会停）。
2. 把 [README 的十一条硬规则](README.md#十一条硬规则移植时必须原样带走) 写进你的全局规则文件（参考实现叫 `bot-global-rules.md`）。**注意**：参考实现的当前全局规则文件是重新整理过的版本，旧版里的几条硬规则（LLM 尾标、Bot 重活红线、Claude 只走一台、Herdr 必用、方案六块、验收失败点名等）不在新版正文里，迁移时要按 [SOP_INDEX §2](SOP_INDEX.md#2-必带的硬规则摘要) 补齐。
3. 每台主机读回 `<SOP_DIR>` 文件列表和 sha256，三台一致才算完成。

```sh
cd <SOP_DIR> && find . -name '*.md' -type f | sort | xargs sha256sum
```

**不要做的**：不要直接覆盖已有的个人指令文件；先带时间戳备份，再人工合并指针。保留你原有的插件/skill 禁用规则。

---

## 3. Herdr（所有 agent 的运行容器）

**要懂的**：Herdr 让每个 agent 都跑在一个看得见的终端 tab 里。Bot 用 `herdr agent list` 看状态，人随时 `herdr` 进去看。没有 tab 的后台 agent 一律禁止。

**要做的**

1. 安装（先下载、阅读，再由人执行；见 [Herdr 官方安装页](https://herdr.dev/docs/install/)）：

   ```sh
   curl -fsSL https://herdr.dev/install.sh -o herdr-install.sh
   less herdr-install.sh
   sh herdr-install.sh
   herdr --version
   ```

2. **会话**：每台主机只用 Herdr 的 default 会话（直接敲 `herdr` 进入的那个）。脚本里不写 `--session <别的名字>`，也不设 `HERDR_SESSION`。参考实现曾因用了第二个会话，导致 Bot 派的 tab 和人看到的 tab 不一致。
3. **命名**（硬规则 5）：
   - tab 标题：`<issue号>-<短标题>`，如 `123-login-timeout`
   - agent 名：`<task_id>-<角色>`，task_id 必须含 issue 号，如 `fe123-login-review`、`fe123-login-impl-main`
   - 看板只认「名字里含该行 task_id 或 issue 号、且状态为 working」的 agent 为在跟。
4. 常用命令（以 `herdr <组> --help` 的实际输出为准，不要照抄示例 ID）：

   ```sh
   herdr agent list                         # 所有 agent 与状态
   herdr agent get <name>                   # 核对 cwd / tab / pane
   herdr tab create --label "123-login-timeout" --cwd ~/projects/YOUR_BUSINESS_REPO --no-focus
   herdr pane process-info --pane <PANE_ID> # 前台是什么进程
   herdr pane read <PANE_ID>                # 读屏
   herdr pane send-text <PANE_ID> '<一行指令>'
   herdr pane send-keys <PANE_ID> Enter
   herdr tab close <TAB_ID>                 # 关 tab（连同其 pane）
   ```

5. **清理规则**：关联 issue 一旦 CLOSED，对应 tab/pane 直接关，不用再问。只有两种例外才留：该 pane 仍 working 且在为另一张仍 OPEN 的票干活；负责人当场明说保留。关之前用 `gh issue view <N> --json state` 核对。

**不要做的**：不要操作不属于当前任务的 pane；不要因为徽标显示奇怪就新开 tab、重发整份 brief 或杀掉还在跑的 agent。

---

## 4. Claude 主机：出口闸门与默认档位

**要懂的**：Claude 只在 `YOUR_CLOUD_HOST` 跑，而且只能从你指定的出口上网。这是「某些模型/账号只能从固定网络位置使用」时的通用做法：**自备合规的出口/代理，然后把检查做成闸门**。

**要做的**

1. **派单前检查命令**（Bot 每次派 Claude 前，在 Claude 主机上跑）：

   ```sh
   curl -s -m 8 -x YOUR_PROXY YOUR_IP_ECHO_URL
   ```

   判定：curl 退出码为 0，且输出去掉首尾空白后是**单个** IP，且**恰好等于** `YOUR_EGRESS_IP` → 通过。其他一切（别的 IP、空、超时、多行、非零退出）→ 本次不派，记录原因，下次唤醒再试。

2. **启动包装脚本**（`~/.local/bin/claude` 位置放包装脚本，真正的二进制放别处），必须做到：
   - 设置代理环境变量指向 `YOUR_PROXY`，关闭自动更新；
   - 启动前用同一条命令查出口，不等于 `YOUR_EGRESS_IP` 就打印 `BLOCKED` 并拒绝启动、写一条告警；
   - 通过后 `exec` 真正的 Claude 二进制。

3. **看门狗**（常驻，每 60 秒一轮），必须做到：
   - 查出口，不对就停掉所有 Claude 进程并写告警（带时区时间）；
   - 发现包装脚本被替换，就从只读的安全副本恢复并写告警；
   - 用文件锁保证只有一个实例。

   > 包装脚本和看门狗属于「实现」，按本工作流应由 Codex 按你的方案实现、由负责人批准后部署。参考实现的这两个文件位置记在私有文件里。

4. **默认档位**（硬规则 7）：在 Herdr tab 里启动：

   ```sh
   herdr agent start <task_id>-review --kind claude --pane <PANE_ID> -- --model opus --effort high
   ```

   不开 fast。只有负责人点名其他模型，或恢复原会话时沿用原档位。

5. **合并 Claude 指令指针**：备份 `~/.claude/CLAUDE.md` 后，人工合并 [templates/CLAUDE_SNIPPET.md](templates/CLAUDE_SNIPPET.md) 的指针（把其中路径换成 `<SOP_DIR>`），再加上一句：「Claude 只设计/评审，不写实现；方案只写六块」。

**不要做的**

- 不在其他主机上跑这条检查来代替 Claude 主机的结果。
- 不用直连 IP 判断出口；代理失败时不改走直连。
- 不为了让 Claude 跑起来去改包装脚本、看门狗、换进程名绕过。
- 出口通过 ≠ 可以派单。还要有任务授权。

---

## 5. Codex 主机（`YOUR_MINI` / `YOUR_AIR`）

**要做的**

1. 备份 `~/.codex/AGENTS.md`，人工合并 [templates/AGENTS_SNIPPET.md](templates/AGENTS_SNIPPET.md) 的指针（路径换成 `<SOP_DIR>`）。
2. 在 Herdr tab 里启动 Codex，**显式**写模型、effort 和普通服务档（不要依赖默认值，不要 fast/priority 档）：

   ```sh
   herdr agent start <task_id>-impl-main --kind codex --pane <PANE_ID> -- \
     -m YOUR_CODEX_MODEL -c model_reasoning_effort="high" -c service_tier="default"
   ```

   启动后读回 agent 实际的模型/effort/档位，对不上就不派活。
3. 网络诊断由部署者按自己的授权环境执行并记录实际错误。`netcheck` 只是可选的本机诊断接口，本包不依赖或提供私有诊断脚本；未验证就保留 UNKNOWN，不从一次 CLI 错误推断网络或模型已故障。
4. 可选：[scripts/common/codex-herdr](scripts/common/codex-herdr) 是在 Herdr 里启动 Codex 的小包装，启用前先核对你的 Codex CLI 版本兼容。

**不要做的**：不在 Mac 上启动 Claude；Codex 不自己合并、不关 issue、不写进度板、不发 `finished`。

---

## 6. 调度 Bot

**要懂的**：Bot 是唯一写进度板的人，也是唯一能把「负责人的话」变成 GitHub 记录、再变成派单的人。它不做重活。

**要做的**

1. **Bot 说明（profile）**，可按下面改写后填进你的 Bot 平台：

   ```text
   你是 YOUR_BOT，负责人的任务流 Bot。默认中文，务实直接。
   目标：管理负责人所有电脑上正在跑的大模型任务和 repo，及时发现状态、报告问题和卡点。
   数据来源：
   - YOUR_MINI / YOUR_AIR 上的 Herdr：`zsh -lc 'herdr agent list'` 看状态，`herdr agent read` 看输出。
     未经负责人要求只读，不 send-keys、不 prompt（派单除外）。
   - YOUR_CLOUD_HOST：Claude Code（只走固定出口，出口保护不可削弱）、负载。
   - GitHub：PR、issue、CI，只读核对。
   工作方式：
   - 定时自检 + 信号唤醒；只有发现问题才报告：卡住/报错/等输入、CI 失败或待评审、待验收、机器闲置。
   - 报告 ≤200 字结论 + 证据文件路径；完整材料存 <TASK_ROOT>。
   - 只调度和汇报，重活交给空闲 Mac 的 Codex。同一步失败两次就停，报告负责人。
     本机诊断仅按已有授权记录实际观测；`netcheck` 仅为可选、已安装接口，不要求安装或运行未提供的命令。未核验则保留 UNKNOWN，不从一次 CLI 错误推断网络或模型故障。
   - 自身额度只用于对话、派单、只读核对（最多 2 条命令）、写汇报；其他先发卡片请负责人批准。
   - Claude 出口闸门只认 Claude 主机经代理查到的出口 IP；直连 IP 不作数。
   - 不擅自停止、重启或改动负责人的任务和 repo；任何不可逆操作先问。
   ```

2. **进度板**：建一张只有 Bot 能写的表，固定八列，顺序不变：

   | 任务 | 当前状态 | 上次更新 | 目标 | 验收 | 跟进方 | Issue | PR |
   | --- | --- | --- | --- | --- | --- | --- | --- |

   - 「当前状态」第一行只能是 `todo` / `wip` / `blocked` / `finished`，下面 1 条短 bullet（blocked 可再加 1 条 `❓` 问句）。
   - 「目标」只有负责人能改；「跟进方」只能是你的 host 枚举值；Issue/PR 只填核对过的真实链接。
   - 技术细节（CI 编号、完整提交号、进程号）不上板，放证据文件。

3. **定时任务**（按 [templates/routine.md](templates/routine.md) 新建，不改已有的）：
   - **H1**：webhook 唤醒入口。收到信号 → 读 [lifecycle](sop/lifecycle.md) → 重算所有开发中的行 → 派续/改板/发问句 → 写 `WAKE_<时间>.md`。
   - **H2**：每小时一次，同 H1，外加全量健康检查，写 `FALLBACK_<时间>.md`。
   - **早报**：每天一次，列出待「跟进」的 todo、无法核验项、疑似卡住项。
   - H1/H2 的规则追加稿见 [templates/H1_H2_LIFECYCLE_APPEND.md](templates/H1_H2_LIFECYCLE_APPEND.md) 和 [H1_H2_PROMPT_PATCH.md](templates/H1_H2_PROMPT_PATCH.md)。

**不要做的**：不建跨主机的统一轮询/转发服务；每台主机自己写信号、自己 POST。Bot 不直接调用看板平台的私有 API 以外的东西去改别的 Bot 的板。

---

## 7. 信号 helper 与本机凭据（每台主机各做一次）

**要懂的**：信号是一个 15 字段的小文件，helper 把它原子写到 `<TASK_ROOT>/<task>/BOARD_SIGNAL.md`，再 POST 给 Bot 的 webhook 叫醒 Bot。

**要做的**

1. 安装 helper：把 [scripts/common/board-signal-post](scripts/common/board-signal-post) 放到 `~/.local/bin/`，核对 sha256 与仓内一致。如果你的 host 枚举不是 `air|mini|云电脑`，要先改 helper 的校验并跑它的测试：

   ```sh
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/common -p test_board_signal_post.py -v
   ```

2. 凭据：按 [bootstrap §4](bootstrap/README.md#4-本机凭据仅真实交互终端隐藏输入不覆盖) 在**真实交互终端**隐藏输入，生成 `~/.config/board-wake/webhook_url` 和 `webhook_auth`（目录 0700，文件 0600，不同步、不进 Git、不出现在命令参数和日志里）。
3. 无凭据演练（只写临时目录，不联网）：按 [bootstrap §5](bootstrap/README.md#5-无凭据隔离-dry-run)。
4. 15 个字段：`board, board_row, task_id, title, goal, status, question, host, pr, event, as_of, seq, summary, evidence, writer`。
   - `status` ∈ `wip|blocked|finished`；`event` ∈ `start|milestone|done|blocked`；`as_of` 带时区；`seq` = 同一信号文件已有 seq + 1。
   - `summary` 每行一个人话结论；技术证据放 `evidence`。
   - issue 还开着就不准发 `finished`；验收全过发 `event=done, status=wip`。
5. 退出码处理：

   | 退出码 | 意思 | 下一步 |
   | --- | --- | --- |
   | 0 | 已写、已投递（dry-run 时只写） | 无 |
   | 1 | 写失败，没投递 | 修文件权限 |
   | 2 | 输入不合法，没写 | 改输入，不原样重试 |
   | 3 | 已写，本机凭据缺失/不合格 | 修本机配置，保留信号 |
   | 4 | 已写，网络/HTTP 失败 | **完全相同的输入**（含 seq、as_of）最多重试一次，仍失败就报告「待投递」 |

**不要做的**：不循环重试；不换新 seq 冒充重试；不跨主机代发；不把 dry-run 的 0 当作投递成功。

---

## 8. 派单规则（Bot 照做）

### 8.1 派 Claude 出方案（B1）

前提：负责人明确说了「跟进」。同一回合完成四步：

1. 没有 issue 就开 issue；在 issue 写 `【跟进】` + 负责人原话 + 时间（带 `【LLM：…】` 尾标）。
2. 在 `<TASK_ROOT>/<task-dir>/` 写 `BRIEF_CLAUDE_*.md`（样例 [examples/BRIEF_DESIGN.example.md](examples/BRIEF_DESIGN.example.md)）。brief 必须含：板行名（逐字）、task_id、issue 链接、负责人原话、旧方案和修改意见、六块格式要求、交付方式、禁止事项。
3. 在 Claude 主机：出口检查通过 → 建 tab → `agent start`（§4.4）→ 注入：

   ```sh
   herdr pane send-text <PANE_ID> '请读取并严格执行 <TASK_ROOT>/<task-dir>/BRIEF_CLAUDE_xxx.md'
   herdr pane send-keys <PANE_ID> Enter
   ```

   若 `agent start` 报未就绪，但读屏已看到 Claude 的输入提示，直接按上面注入，不要重开。
4. 写 `DISPATCH.md`（时间、tab/pane、启动参数、出口检查结果），板改 wip。

**Claude 的交付格式**：issue 评论第一行 `【方案 vN】#M <标题>`；正文只有六块（问题、原因、修复方案、当前架构图、修复后架构图、需要时的 Open Question）+ 验收草案 + 架构门（G1）初判；结尾 `Open Question：k 条` 或 `无 Open Question`；最后一行 `【LLM：…】`。然后发一次 `blocked` 信号。评论时间必须晚于最近的【跟进】/【跟进修改】才算本轮交付。

### 8.2 B2 → 派 Codex 实现（C）

三样齐了才派：负责人确认了最新方案、确认了验收口径、**点名了实现机器**。

1. issue 记 `【方案确认】` + 原话。
2. 写 `BRIEF_CODEX_*.md`（样例 [examples/BRIEF_IMPL.example.md](examples/BRIEF_IMPL.example.md)），含：方案链接、负责人定案表、必做/不做、批次号、隔离 worktree、交接文件绝对路径、验收、「不合并、不部署、不关单」。
3. 在被点名的 Mac：建 tab → `agent start`（§5.2）→ 注入「读 brief」。
4. brief 要求 agent 第一行回 `ACK: …`。派出后**等一次**（最多 10 分钟）看 ACK 或开始干活的证据；没开始就读屏一次、记录原因，下一次唤醒再推一次，仍不行才问负责人。不自动重启。

### 8.3 实现中（C）的循环

- 每次开 PR/推新提交 → Bot 在同一个 `<task_id>-review` tab 派 Claude 评审**当前 head**。
- 评审结论贴出后 → 能修的（P0/P1、决定要修的 P2、范围内 CI 红、冲突）同回合回派原 Codex；需要负责人决定的同回合改 D 问。
- 执行端维护一条「评审回应表」PR 评论：每条意见 → 已修（提交号）/ 不改（理由）/ 转 follow-up。P0/P1 修完要 Claude 复核一次。同一 PR 修到第 3 轮还有 P0/P1，停下问负责人。
- R1–R4 全满足 → 执行端发 `blocked` + `ready: pr=#N head=<sha8>` → Bot 进 E 问合并。

### 8.4 续跑与恢复

- Claude 还在跑：直接 `pane send-text` + `Enter`（硬规则 6）。不要先走 `agent prompt` 失败了再改。
- 进程确认已死（前台是 shell、看到「Resume this session with: claude --resume …」、没有在途命令）：在**原 pane、原名字**`herdr agent start … --resume`，只恢复一次；失败就问负责人。
- 恢复时只发通用续写提示：「从停下的地方继续原 brief；先检查已写的文件和已贴的评论，不要重复贴。」不重发完整 brief。

### 8.5 交接（每个执行端停手前）

- 交接文件：`<TASK_ROOT>/<task-dir>/handoffs/<batch-id>-<worker>.md`（样例 [examples/HANDOFF.example.json](examples/HANDOFF.example.json)）。
- 状态只有三种：DONE（批次全部完成）、BLOCKED（权限/授权/需要负责人决定）、OUT_OF_SCOPE（范围要扩大，先报再做）。新冒出的范围内失败不算 BLOCKED，继续修。
- 写法：先写临时同目录文件，再 rename（原子替换）；然后发信号通知。
- worker 只交给 Main；Main 核对改动路径在批准范围内再接受。

---

## 9. 首次验收：走一张纸面票

在正式迁移任务前，用一张无害的 issue（例如「给流程仓 README 加一行说明」）完整走一遍：

1. 负责人说「跟进」→ Bot 开/补 issue、记【跟进】、出口检查、派 Claude。
2. Claude 贴【方案 v1】、发信号 → Bot 板改 B2 并发问句。
3. 负责人确认 + 点名机器 → Bot 派 Codex → PR → Claude 评审 → 回应表。
4. Codex 发 ready → Bot 问合并 → 负责人批准 → 合并 → 主分支 CI 绿 → 验收 → Bot 关单 → finished。

每一步都在 [CHECKLIST.md](CHECKLIST.md) 勾选并保留证据路径。任一步不符合，不进入正式迁移。

---

## 10. 参考实现示例（只作对照）

| 项 | 参考实现 |
| --- | --- |
| Bot | Grok Bot 平台上的「任务流」Bot；进度板是平台画布页；靠平台机器连接在 Mac 上执行本机 shell |
| Claude 主机 | 一台云 Linux；Herdr default 会话；本机代理 + 包装脚本 + 每 60 秒看门狗；Claude Code 2.x |
| Codex 主机 | Mac mini（默认部署机）+ MacBook Air；各自 Herdr |
| 规则目录 | 三台都在 `~/ray-docs/YOUR_COORDINATOR/sop/` |
| 任务目录 | `~/ray-docs/任务流/<task-dir>/`，唤醒证据在 `board-wake/` |
| 唤醒 | 信号 webhook（H1）+ 每小时兜底（H2）+ 每天 08:00 早报；问句全天当次发送 |
| 未部署项 | 每台主机 5 分钟本机脚本自动推信号/恢复一次（文档与脚本已交付，未部署） |

私人数值（出口 IP、代理端口、私有仓地址、主机别名、文件位置）在部署者自己的私有文件里，不在本仓。

【LLM：Claude@云电脑｜模型=Opus 5.5｜effort=high｜fast=否】
