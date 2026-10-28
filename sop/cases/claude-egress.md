# Claude 出口纸面自检（workflow#12）

依据：批准任务（历史示例，原记录不随公开包分发） 的输入/预期；判据为 [Claude 出口纪律](../claude-discipline.md) §1–§3。
本批只对假设输入推演规则，不执行 curl、不连接云端、不启 Claude、不运行 routine、不派单。表中「观察结果」是文案推演所得，PASS 仅指纸面一致性。
共同命令为 `curl -s -m 8 -x YOUR_PROXY YOUR_IP_ECHO_URL`，除 T5 外假设已核实本次观测来自将实际运行 Claude 的云主机。

| 用例 | 纸面输入 | 独立预期（批准 brief） | 规则落点 | 本次观察结果 |
|---|---|---|---|---|
| T1 | 直连 `YOUR_DIRECT_IP`；代理 `YOUR_EGRESS_IP`；curl exit=0 | egress_ok | [§1](../claude-discipline.md#1-检查位置与唯一命令) 直连无关；[§2 E1](../claude-discipline.md#2-出口判定) 精确代理成功 | 推演为 egress_ok；PASS（纸面） |
| T2 | 直连任意，含直连为 `YOUR_EGRESS_IP`；代理为另一 IP；exit=0 | blocked_now | [§2 E2](../claude-discipline.md#2-出口判定) 错误代理 IP 不放行 | 两种直连输入均为 blocked_now；PASS（纸面） |
| T3 | 代理空输出、非 IP 或多值；exit=0 | blocked_now；无直连回退 | [§2 E2](../claude-discipline.md#2-出口判定)；[§1](../claude-discipline.md#1-检查位置与唯一命令) 禁止直连回退 | 三种输出均为 blocked_now；PASS（纸面） |
| T4 | 代理超时/连接失败/其他非零退出码；即使直连为 `YOUR_EGRESS_IP` | blocked_now；不改走直连 | [§2 E2](../claude-discipline.md#2-出口判定)；[§1](../claude-discipline.md#1-检查位置与唯一命令) | 各错误均为 blocked_now；PASS（纸面） |
| T5 | 未核实云主机，或只有 Mini/Air 结果，或只有过期结果 | blocked_now / 出口未核验；不得声称通过 | [§1](../claude-discipline.md#1-检查位置与唯一命令) 主机限定；[§2 E3](../claude-discipline.md#2-出口判定) | 各场景均为 blocked_now，未知保留 UNKNOWN；PASS（纸面） |
| T6 | 代理为预期 IP 且 exit=0；另有安全/容量门禁或任务授权不通过 | 仅 egress_ok；不得自动派单 | [§3 E4](../claude-discipline.md#3-证据与派单边界)；[lifecycle §5.6](../lifecycle.md#56-派续由父代理执行pending_dispatch) | 出口通过但仍不派；PASS（纸面） |
| T7 | 本次代理恢复为预期 IP、exit=0；存在历史 pending_dispatch | 不自动重放历史 pending | [§3 E5](../claude-discipline.md#3-证据与派单边界) | 仅清本次出口检查，历史列表不自动冲刷；PASS（纸面） |

附加边界核对：blocked_now 不是板状态，未以出口失败自动判板面 blocked；证据必须有实际云主机、带时区时间、原命令、退出码与代理结果/脱敏短错误；H1/H2 的 [共同补丁](../../templates/H1_H2_PROMPT_PATCH.md) 同样保留 ACK、去重及其他安全门禁；夜间不构成延后条件。#17 已批 guard-stop 原会话例外须全部满足 [独立恢复用例](claude-auto-resume.md)，不能用出口通过替代任务授权，T6 不因此放行任意新派单。

本次纸面结果：T1–T7 均与批准预期一致。真实云端代理出口、H1/H2 安装/读回/执行与三端安装均 **未执行、未验证**；这些结果不能当 live egress 或 routine 验收证据。
