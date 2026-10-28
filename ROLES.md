# 四端职责对照表

占位符：`YOUR_BOT`（调度 Bot，参考实现名为「任务流」，跑在 Grok Bot 平台）、`YOUR_CLOUD_HOST`、`YOUR_MINI`、`YOUR_AIR`、`YOUR_PROD_HOST`（默认部署机）、负责人（Owner）。

信号里的 `host` 字段只能取一个**固定枚举**，每台主机一个值。参考实现是 `air` / `mini` / `云电脑`；你换成自己的三个值后，要同时改信号 helper 的校验，不能随手写新名字。

---

## 1. 总表

| 维度 | 调度 Bot（`YOUR_BOT`） | 云端 Claude（`YOUR_CLOUD_HOST`） | Mini Codex（`YOUR_MINI`） | Air Codex（`YOUR_AIR`） |
| --- | --- | --- | --- | --- |
| 一句话职责 | 盯进度、判阶段、派单、核对、汇报、关单 | 写方案、做方案/代码评审 | 实现、测试、开 PR、**默认部署** | 实现、测试、开 PR |
| 跑什么 | Bot 平台 + 定时任务 + webhook | Herdr（default 会话）里的 Claude Code | Herdr 里的 Codex | Herdr 里的 Codex |
| 默认模型/档位 | 平台自带 | Opus 5.5，effort=high，不开 fast | 显式指定模型和 effort；不开 fast/priority 档 | 同 Mini |
| 写进度板 | **唯一写入者** | 不读不写 | 不读不写 | 不读不写 |
| 写 GitHub | issue 记录（【跟进】【方案确认】【合并批准】…）、关单评论、关 issue | 本任务的方案评论、评审结论 | PR、提交、评审回应表、验收回报 | 同 Mini |
| 发信号 | 不发（它是接收方） | 每版方案后发一次 `blocked`；每次评审结论后发一次 `milestone`；在本机发 | 阶段进展 `milestone`、需决策 `blocked`、验收全过 `done`；在本机发 | 同 Mini |
| 可以自己决定 | 按规则推导阶段；在已有授权内派续（修评审意见、修 PR 上的 CI、补完成声明、派复评） | 方案内容、评审结论（P0/P1/P2） | 批次范围内的修复、测试补充 | 同 Mini |
| 必须等负责人 | 派第一次实现（要负责人点名机器）、合并、部署、关单前的偏差接受、改验收口径 | 不直接和负责人讨论；疑问写成 OQ | 超出范围（OUT_OF_SCOPE）、合并、部署、切线上开关 | 同 Mini |
| 禁止 | 自己做重活；用直连 IP 判出口；无证据写 working；替 agent 写完成声明 | 写实现代码；在其他机器运行；写进度板；改出口包装脚本/看门狗 | 启动 Claude；自己合并/关单；写进度板；发 `finished` | 同 Mini |
| Herdr 命名 | — | tab `<issue号>-<短标题>`；agent `<task_id>-review`（方案和代码评审共用，issue 关了才关） | tab `<issue号>-<短标题>`；agent `<task_id>-impl-main`，帮手 `<task_id>-impl-worker` | 同 Mini |
| 停手前必须 | 把本次判定写进 WAKE_/FALLBACK_ 证据 | 贴好 issue 评论 → 读回确认 → 发信号 | 写当前批次交接文件（原子替换）→ 发信号 | 同 Mini |
| GitHub 评论尾标 | `【LLM：<Bot 名/模型>】` | `【LLM：Claude@<主机>｜Opus 5.5｜effort=high｜fast=否】` | `【LLM：Codex@<主机>｜<模型>｜effort=…】` | 同 Mini |

**负责人（Owner）**：读板；回答 `❓ <负责人> 需决策：…？` 问句；只有负责人能批准合并、部署、关单前的偏差、改验收、切线上开关、资金/凭据/外部账号相关动作。负责人在 GitHub 上的评论**不带** `【LLM：…】` 尾标，Bot 靠这一点识别「这是本人说的」。

---

## 2. 派哪台机器

```text
需要的是设计/评审？ ──是──▶ YOUR_CLOUD_HOST 的 Claude（唯一选项）
        │否
需要的是部署到生产？ ──是──▶ YOUR_PROD_HOST（固定，不做负载均衡）
        │否
这张票已经在某台 Mac 上开始实现？ ──是──▶ 原机器原 tab 跑到底
        │否
新开实现 ──▶ 负责人点名哪台；Bot 只能「建议」更空闲的那台
           （空闲 = 该机 Herdr 里 working 的 agent 更少）
```

- 负载均衡只是建议，**第一次派实现必须负责人明确点名机器**；只回答了 OQ 没点名，仍停在 B2。
- 原 tab 已不存在时，才在**同一台机器**新开 `<task_id>-impl-main2`，用新批次号。
- 主机暂时连不上 ≠ tab 丢了，不能据此改派别的机器。

---

## 3. 每个阶段谁动手（RACI 简表）

R = 动手，A = 拍板，C = 被咨询，I = 被通知

| 阶段 | Bot | Claude | Codex | 负责人 |
| --- | --- | --- | --- | --- |
| A 入板 | R | — | — | A（说「跟进」） |
| B1 出方案 | R（开 issue/记录/派单） | R（写方案） | — | I |
| B2 方案拍板 | R（转述 + 问句） | C | — | **A** |
| C 实现 | R（派单/盯 CI 和评审/回派） | R（代码评审） | R（实现） | I |
| D 卡决策 | R（问句） | C | C | **A** |
| E 等合并 | R（核 R1–R4 + 问句） | — | R（声明 ready） | **A** |
| F 合并/部署/验收 | R（派单、核 C1–C6、关单） | — | R（合并/部署/验收） | A（已在 E 批过） |
| G follow-up | R（开票互链） | — | C | I |

---

## 4. 什么算 blocked（只有一种情况）

**卡住了目标，而且必须等负责人决定**，才是 `blocked`。问句必须一句话能回答，例如：

- `❓ <负责人> 需决策：#123 方案 v2 可以实现了，派谁做？（mini Codex / air Codex；建议 air）`
- `❓ <负责人> 需决策：是否批准合并 PR#45（head 0d6fb543）并部署到 YOUR_PROD_HOST？（回滚：回退到上一版本并重启服务）`

**这些都不是 blocked**（写 wip，并写清在等什么、谁来恢复、Bot 最迟什么时候再查）：
等 CI、等外部评审、等已派但还没贴出来的 Claude 评审、等市场/运行时事件、执行端还在自己修。

【LLM：Claude@云电脑｜模型=Opus 5.5｜effort=high｜fast=否】
