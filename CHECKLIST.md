# 移植验收清单

逐项勾选。每项后面写证据（文件路径、命令输出位置、GitHub 链接）。**没有证据就不勾**；查不清写 UNKNOWN，不猜。

主机：`YOUR_CLOUD_HOST` = C，`YOUR_MINI` = M，`YOUR_AIR` = A。

---

## 0. 准备

- [ ] [MIGRATION §0](MIGRATION.md#0-移植前先定下来填表) 占位符表已填完
- [ ] 私人数值（代理地址、出口 IP、webhook、看板 ID）只在私有笔记里，`git grep` 本仓查不到
- [ ] （公司电脑）网络/代理/外部 webhook/AI 服务政策已确认允许
- [ ] Bot 平台能在 C、M、A 各自执行本机 shell（不靠主机间 SSH）

## 1. 依赖

- [ ] C：git / python3 / gh（已登录）/ curl / herdr / claude 均有版本输出
- [ ] M：git / python3 / gh / curl / herdr / codex 均有版本输出
- [ ] A：同 M
- [ ] M、A 上**没有**安装或登录 Claude Code

## 2. 规则文件

- [ ] C、M、A 的 `<SOP_DIR>` 都有 [SOP_INDEX §1](SOP_INDEX.md#1-文件清单) 的全部「必带」文件
- [ ] 三台 `<SOP_DIR>` 的 sha256 列表一致
- [ ] 全局规则文件包含 [README 十一条硬规则](README.md#十一条硬规则移植时必须原样带走) 和 [SOP_INDEX §2](SOP_INDEX.md#2-必带的硬规则摘要) 全部条款
- [ ] `~/.claude/CLAUDE.md`（仅 C）、`~/.codex/AGENTS.md`（M、A）已备份并合并指针；原有禁用规则保留

## 3. Herdr

- [ ] 三台 `herdr --version` 正常，各只用 default 会话（脚本里搜不到写死的会话名）
- [ ] 在 C 上 `herdr` 进入后能看到 Bot 派出的 tab（人看到的和 Bot 派的是同一会话）
- [ ] 命名演练：建一个 `999-naming-test` tab，agent `t999-naming-review`，`herdr agent list` 能看到，然后 `herdr tab close` 关掉

## 4. Claude 主机

- [ ] C 上出口检查命令输出恰为登记出口 IP（退出码 0、单个值）
- [ ] 人为让代理不可用时（或在测试环境模拟），`claude` 包装脚本拒绝启动并写告警
- [ ] 看门狗在跑（单实例），出口异常时会停 Claude、包装脚本被替换时会恢复
- [ ] 在 Herdr tab 启动的 Claude 读回模型 = Opus 5.5、effort = high、fast = 否
- [ ] 续跑演练：对在跑的 Claude 用 `pane send-text` + `Enter` 注入一句话，读屏确认开始执行

## 5. Codex 主机

- [ ] M、A 在 Herdr tab 启动的 Codex 读回：显式模型、effort、普通服务档（非 fast/priority）
- [ ] M、A 已记录授权内本机诊断的实际观测；`netcheck` 仅为可选、已安装接口，默认不依赖该命令；未核验项标 UNKNOWN，不据单次 CLI 错误断言网络或模型故障
- [ ] `YOUR_PROD_HOST` 已写进规则，作为默认部署机

## 6. 信号与凭据（每台各自）

- [ ] C / M / A：`~/.local/bin/board-signal-post` sha256 与仓内一致
- [ ] C / M / A：`~/.config/board-wake/` 目录 0700，两个凭据文件 0600、属本人、非链接（只看元数据）
- [ ] helper 的 host 枚举 = 你的三台主机值；15 个回归测试通过
- [ ] 隔离 HOME dry-run 产出 15 字段信号文件，退出码 0
- [ ] （已授权后）每台各发一次真实 smoke 信号：HTTP 2xx，且 Bot 实际被唤醒、实际刷新了「上次更新」

## 7. Bot 与进度板

- [ ] Bot profile 已写入，含：只调度不做重活、额度先批后用、出口只认代理结果、失败两次就停
- [ ] 进度板八列顺序正确：任务 / 当前状态 / 上次更新 / 目标 / 验收 / 跟进方 / Issue / PR
- [ ] 只有 Bot 能写进度板
- [ ] H1（webhook）、H2（每小时）、早报三个定时任务已建，各自留下一次 WAKE_/FALLBACK_ 证据
- [ ] H2 能发现「wip 一小时没动静」并写进证据

## 8. 纸面票全流程（[MIGRATION §9](MIGRATION.md#9-首次验收走一张纸面票)）

- [ ] A→B1：负责人说「跟进」后，同一回合出现 issue【跟进】记录 + 出口检查记录 + Claude tab + 板面 wip
- [ ] B1→B2：issue 出现格式合格的【方案 v1】（六块、首行/末行格式、时间晚于【跟进】），板面 blocked + 问句
- [ ] B2→C：负责人确认 + 点名机器后才派 Codex；brief 有批次号与交接路径；10 分钟内看到 ACK
- [ ] C：PR 开出后同一个 `-review` tab 评审当前 head；回应表 PR 评论存在
- [ ] C→E：执行端发 ready，Bot 进 E 并发合并问句（含 head 与部署/回滚说明）
- [ ] E→F：负责人批准后 issue 有【合并批准】head=…；合并后主分支 CI 绿
- [ ] F：逐条验收 PASS 回报；执行端发 `event=done,status=wip`（不是 finished）
- [ ] 关单：Bot 核 C1–C6 后评论并关 issue；下一次检查读到 CLOSED 才 finished
- [ ] 清理：issue 关闭后相关 Herdr tab 已关

## 9. 反例自检（都应被拦下）

- [ ] 在 M 或 A 上派 Claude → 被拒
- [ ] 用直连 IP 判断出口 → 不放行
- [ ] 负责人只回答了 OQ、没点名机器 → 仍停在 B2
- [ ] PR 合并了但 issue 没关 → 不显示 finished
- [ ] 执行端 idle → 不自动降 todo
- [ ] 新提交推上来后用旧批准合并 → 被拦（批准失效）
- [ ] 信号退出码 4 → 只用同一输入重试一次

全部勾完，才把真实任务迁过来。

【LLM：Claude@云电脑｜模型=Opus 5.5｜effort=high｜fast=否】
