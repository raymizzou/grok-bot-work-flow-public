# 新 routine 人工配置清单（非可导入 API 载荷）

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

所有 `<...>` 都必须人工替换；未填写/未核对时不启动。不要修改现有 routine。

- owner Bot：`<OWNER_BOT>`；唯一 Page：`<PAGE_URL>`；板名：`<BOARD_NAME>`。
- 平台生成新 webhook 后，只在各机本地隐藏交互输入凭据，不粘贴到此文件。
- 时区：`<IANA_TIMEZONE>`；自检间隔：`<APPROVED_INTERVAL>`。
- 提醒政策：`<OWNER_CONFIRMED_POLICY>`；任务流按 YOUR_OWNER t462u 定案，授权内通知和聊天提醒 24h 同回合发送，包括决策问题/合并请求。
- 触发：接收本机 helper payload。只消费 changes 展示字段，不能等待文件同步。
- 每台机器分别配置授权、执行、核对；host 仅 air/mini/云电脑，不能假定三端已有安装。
- 接收端按 diff_id 去重；相同输入最多一次调用方重试，禁止无限重试。
- 状态判断先读 [当前状态机](../sop/board-state-machine.md) 与 [lifecycle](../sop/lifecycle.md)，idle 不自动降 todo，todo 只等 YOUR_OWNER 跟进。
- 现有任务流 H1/H2 使用 [共同追加稿](H1_H2_LIFECYCLE_APPEND.md)，父代理先备份平台完整原 prompt 再追加、读回；这不创建新 routine，也不声称已修改。新 owner 若采用此生命周期也须先确认授权。
- 任务流 H2 每小时、08:00 PT 早报，共享 Bot 每日 admission 100 次（含 H2）；已批 PR 下一手全天派，其他工作按已有授权；不伪称 working。旧暂停 30 分钟自检条文废止，以每小时 H2 取代。
- CI_WATCH OQ、云 E4 检测仍待批/待核；不凭本文部署断链恢复、watcher 或跨主机 relay。
- 仅 owner Bot 更新自己的 Page；其他 Bot 和 helper 不直接调用 Canvas API。
- 人工验收：触发记录、展示字段、重复输入处理、全天提醒与去重、Page 实际状态与 owner。

本仓库不提供 routine ID、Page ID、账号资料、实际 webhook 或自动建板脚本。

#24 四角色、manifest/交接/ACK、持久待推送与一次恢复的操作来源：[看板中心总纲](../sop/cases/local-automation-design.md)。本模板未安装；三机调度、routine 和七天观察另批。
