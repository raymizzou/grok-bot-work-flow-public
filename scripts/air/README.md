# Air / macOS 主机清单

本公开模板不证明本机或其他主机已安装；所有实际状态为 UNKNOWN，须逐机取证。

- 依赖：Git、Python 3.8+；真实派单另需已授权的 Herdr、对应 agent CLI 与 gh/curl。
- 来源：[公共 helper](../common/board-signal-post)；按 [bootstrap](../../bootstrap/README.md) 人工复制并比较 source/installed SHA256、权限与版本。
- helper：`~/.local/bin/board-signal-post`；凭据：本机 `~/.config/board-wake/`，仅当前用户、普通文件、0600、非链接，不复制或同步。
- 信号 host：`air`；task_id、逐字板标题、issue 与本机身份须核对。
- 隔离 HOME dry-run 仅证明写入；真实 POST、routine 去重/提醒、Page 和三端部署各自另取证，不能互相替代。
- SSH/身份或访问失败保留 UNKNOWN，不改 trust/凭据，不重启生产。
- [可选本机自动化设计](../../sop/cases/local-automation-design.md) 不在默认安装路径；runner、launchd/cron 安装样例未分发，不得直接启用或声称已运行。
