# 本机信号与 wake 协议

> 路径约定：`~/ray-docs` 仅为 helper 默认的参考布局；`YOUR_` 值须由部署者填写，涉及真实主机/出口/凭据的值只留本机私有配置。

> 可选自动化说明：本公开包仅支持手工交接 + `board-signal-post`；下文本机 runner/恢复设计仅供参考，代码与定时安装样例未分发，未安装时由 Main 按原 helper 协议执行。不得直接运行设计中的命令，也不得宣称自动恢复已生效。

导出源为 Air 当前安装 helper 和 exit-4 版本测试；helper 字节不改。
它从 stdin 读取 JSON，先用同目录临时文件 + fsync + rename 原子替换
`~/ray-docs/任务流/<task>/BOARD_SIGNAL.md`，再 POST 一次。
`--task` 为单目录名，建议与 task_id 相同；禁止 `.`、`..` 和路径分隔符。

## #24 操作入口（未部署）

四角色、三种唤醒、每小时 H2、共享 Bot 每日 100 次 admission、持久待推送/编号收据与本机一次恢复，统一见 [#24 总纲](cases/local-automation-design.md)。旧 30/day、三次 H2 和禁止本机定时恢复的冲突补丁废止。执行端停手前写当前批交接并立即驱动脚本；worker 只交 Main；只有 Bot 读写 Page。

## 输入与载荷

必须恰好 15 字段：`board, board_row, task_id, title, goal, status, question, host, pr, event, as_of, seq, summary, evidence, writer`。
除 seq 为正整数外均为字符串；pr/question 可以空，其他字符串必须非空。
host 固定 `air|mini|云电脑`；status 固定 `wip|blocked|finished`；event 固定 `start|milestone|done|blocked`。
要部署其他 host 标签必须另行批准修改 helper，不能假装当前支持任意名称。
as_of 由发送者给带时区时间，helper 不解析时间。seq 为现有信号 seq（不存在为 0）+1。
已有文件必须先核对且保留必要备份，dry-run 也会替换目标信号文件。

产物是 fenced YAML，值使用 JSON 标量编码，保留中文、换行和冒号。
POST 含 source、host、diff_id、sent_at、changes。
changes 含 path、seq、board_row、status、event、task_id、title、summary、question、pr、as_of；
goal/evidence/writer 不在 webhook 展示载荷中，不能依赖它们从 Mac 同步到云。
所有字段都不得含秘密。接收端仅用这些展示字段更新 owner 的板。

## 退出和重试

| 退出码 | 已发生 | 下一步 |
| --- | --- | --- |
| 0 | 已写，POST 2xx；dry-run 时只写 | dry-run 不是真实投递证据 |
| 1 | 写失败，未 POST | 修复访问；不宣称已写 |
| 2 | 输入无效，未写 | 修正输入；不要原样重试 |
| 3 | 已写，凭据/配置不合格 | 保留信号；修复本机配置再尝试 |
| 4 | 已写，HTTP/网络失败 | 相同输入最多重试一次，仍失败停止并报告投递待补 |

同任务路径与完整信号内容生成稳定 SHA256 diff_id 和 Idempotency-Key。
重试保留 seq、as_of 和全部输入，禁止重新生成新信号冒充重试；helper 自身无重试。
同输入再次调用仍 POST，不承诺接收端 exactly-once；接收 routine 必须独立验证去重。
20 秒超时，拒绝重定向。错误仅输出异常类型、有效 HTTP 状态和受信任短原因，不输出原始异常/URL/token/响应正文。

## 本机安全与边界

只读本机 `~/.config/board-wake/{webhook_url,webhook_auth}`，所属用户普通文件、0600、非符号链接；目录设 0700。
支持 raw token、Bearer、Authorization: 形式。生产 HTTPS，只有 loopback 测试可 HTTP。
`--dry-run` 完全不读取凭据、不联网，但会写本机信号。
Air、Mini、云各自执行；无跨主机 POST relay、同步等待或统一 watcher。
2xx 只证明接收；routine 执行、去重、全天授权内提醒、实际 Page 更新均需另外取证。
首次安装按 [bootstrap](../bootstrap/README.md)，仅人工授权后做真实 smoke，本仓库默认只给 dry-run。

## #24 runner 投递

本机 `local_board.py`（可选设计，代码未分发） 使用原 helper；定时/立即调用共享一个 manifest 锁，intent/seq/完整输入先原子保存。退出 4 跨运行仅重试原输入一次；3/1/2 与未知提交保留待处理不盲重试；新事件独立入队。DONE handoff 只发 wip/milestone，脚本从不关单或发 finished。共享 100/day admission 在 Bot 接收端执行，不是各机计数。
