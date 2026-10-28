# 新机器手工 bootstrap

> 路径约定：`~/ray-docs` 仅为 helper 默认的参考布局；`YOUR_` 值须由部署者填写，涉及真实主机/出口/凭据的值只留本机私有配置。

只给人工步骤，不会运行安装器。开始前读 [主 README](../README.md) 和目标清单：
[Air](../scripts/air/README.md) / [Mini](../scripts/mini/README.md) / [云电脑](../scripts/cloud/README.md)。
本批只在隔离 HOME 演练复制/dry-run，没有在真实 HOME 安装、读凭据或 POST。

## 1. 依赖与 Herdr

先按主 README 装好 Git、Python3、gh、curl 并 clone 公开模板仓，以下复制步骤在仓库根执行。
Herdr 官方 [安装页](https://herdr.dev/docs/install/)（2026-10-24 核对）给 macOS/Linux 的安装入口如下。
由人下载、阅读后决定执行；不能在未授权的现网主机直接跑，也不要升级正在使用的 server：

```sh
curl -fsSL https://herdr.dev/install.sh -o herdr-install.sh
less herdr-install.sh
sh herdr-install.sh
export PATH="$HOME/.local/bin:$PATH"
herdr --version
```

`herdr-install.sh` 是临时下载的官方安装文件，不提交本仓库；不会在本批执行。
参考版本 0.9.1 不是最低版本保证，跨版本操作先读 `herdr --help`。
已安装 Herdr 的机器先核对版本和 owner，跳过重复安装；本手册不停止/清理 server。

## 2. 复制 helper 和 SOP

现有路径先比较，以下命令遇到已有文件会停止；更新已有安装应由人备份并另行核对，不能直接覆盖。
SOP 会复制到 `~/ray-docs/YOUR_COORDINATOR/sop`；先将下方代码和指令模板中的 `YOUR_COORDINATOR` 统一填成自己的目录名。
配套模板、说明、样例与脚本按仓内相对布局一起复制，确保安装后的相对链接仍可用。

```sh
python3 - <<'PYCODE'
from pathlib import Path
import shutil
source = Path.cwd()
target = Path.home()
pairs = [(source / 'scripts/common/board-signal-post', target / '.local/bin/board-signal-post')]
support = [p for name in ('sop', 'templates', 'bootstrap', 'scripts', 'examples')
           for p in (source / name).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
support += list(source.glob('*.md'))
pairs += [(p, target / 'ray-docs/YOUR_COORDINATOR' / p.relative_to(source)) for p in support]
if any(dst.exists() or dst.is_symlink() for _, dst in pairs):
    raise SystemExit('已有目标文件：先由人比较/备份，不覆盖')
for src, dst in pairs:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    dst.chmod(src.stat().st_mode & 0o777)
print('helper/配套文档模板已复制；未配置凭据，未 POST')
PYCODE
"$HOME/.local/bin/board-signal-post" --help
python3 - <<'PYCODE'
from pathlib import Path
import hashlib
source = Path('scripts/common/board-signal-post').read_bytes()
installed = (Path.home()/'.local/bin/board-signal-post').read_bytes()
assert source == installed, '安装副本不同'
print('source/installed SHA256:', hashlib.sha256(installed).hexdigest())
PYCODE
```

可一直用绝对路径；当前终端需要简短命令才执行 `export PATH="$HOME/.local/bin:$PATH"`。
不自动改 shell profile。配套树内的可选 codex-herdr wrapper 仅作为参考副本，不加入 PATH 或自动启用；使用前核对其 Codex CLI 兼容性。

### workflow#12 三端 Claude 出口文档对齐（人工，尚未执行）

继续使用本节已有的比较 → 本机备份 → 人工复制/合并 → 独立读回路线，不运行新同步器。云电脑、Mini、Air 各自由 owner 在本机核对，不靠文件同步推断完成。

| 仓内交付 | 各主机的目标/用法 |
|---|---|
| `sop/claude-discipline.md` | 各机 `~/ray-docs/YOUR_COORDINATOR/sop/claude-discipline.md`；若已有其他纪律，先备份全文，只合并本次限定补充，不能用新文件覆盖已有规则 |
| `sop/bot-progress-board-sop_2026-10-26.md`、`sop/lifecycle.md`、`sop/bot-global-rules.md` | 分别对齐各机 `~/ray-docs/YOUR_COORDINATOR/sop/` 同名文件，仅合并本次出口条款，保留其他本地/全局规则 |
| `sop/cases/claude-egress.md` | 各机 `~/ray-docs/YOUR_COORDINATOR/sop/cases/claude-egress.md`，随同相对链接依赖供纸面读回 |
| `templates/H1_H2_PROMPT_PATCH.md`、`templates/CLAUDE_SNIPPET.md` | 保留为 owner 的交付文件；分别按文内步骤应用，不复制成 SOP，不当作已安装 prompt/个人配置 |

每台机先比较对应文件，备份完整已有副本到本机任务备份目录（带时区时间，敏感内容不入仓、不同步），再人工合并。已有目标不得直接跑上方首次安装复制块。保留所有无关纪律与 Superpowers 插件/skill 禁用规则，不修改 `~/.local/bin/claude` wrapper、`YOUR_GUARD_SCRIPT` 或任何脚本/配置。
每机分别读回目标全文、核对链接与本次条款，并记录主机、时间、路径及未完成项；H1/H2 的完整 prompt 备份与分别读回另按 [出口补丁](../templates/H1_H2_PROMPT_PATCH.md) 办理。

**本批没有安装或验证云电脑/Mini/Air 的副本。** 三端文案一致也不能证明出口已通过：唯一有效的 Claude 出口检查仍在将实际运行 Claude 的云主机，用其本机 `YOUR_PROXY`；Mini/Air 的 localhost 观测不得代替。不在本批启动 Claude、改 routine、改调度或重放历史 pending。

## 3. 指令与 profile

将 `templates/profile.yaml` 复制到**新 Bot 的非秘密配置位置**，人工填 Bot 名、owner、职责、Page、host、时区、静默时间和 issue repo。
它不是平台导入文件，不填真实 webhook URL/auth。
读取 templates/AGENTS_SNIPPET.md 与 CLAUDE_SNIPPET.md，先给已有个人指令做带时间戳备份，再人工合并指针；
保留 Superpowers 及其他原有禁用规则。这里不提供覆盖整个控制文件的命令。
完成标准：指针的三个 SOP 路径真实存在，owner 与主机身份经人工核对。

## 4. 本机凭据：仅真实交互终端、隐藏输入、不覆盖

安装不是配置成功。先由 owner 在新 routine 的平台面板取得真实 webhook URL/auth。
不要把值发进聊天、Markdown、命令参数、shell history、Git 或截图；关闭 shell trace 和终端录制。
以下代码拒绝非 TTY，getpass 不能隐藏时直接失败，不回退到 echo 输入；只创建缺失文件。
已有文件（包括链接）不读取、不覆盖；需要修复时单独找 owner。

```sh
python3 - <<'PYCODE'
from getpass import getpass, GetPassWarning
from pathlib import Path
import os, stat, warnings
from urllib.parse import urlsplit
warnings.simplefilter('error', GetPassWarning)
with open('/dev/tty', 'w') as tty:
    if not tty.isatty():
        raise SystemExit('需要真实交互终端')
    directory = Path.home() / '.config/board-wake'
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    info = directory.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid():
        raise SystemExit('凭据目录必须属于本用户且不是链接')
    directory.chmod(0o700)
    for name in ('webhook_url', 'webhook_auth'):
        path = directory / name
        if path.exists() or path.is_symlink():
            raise SystemExit('已有凭据文件：停止，不读取或覆盖')
    values = {}
    for name in ('webhook_url', 'webhook_auth'):
        value = getpass(name + '（隐藏输入）: ', stream=tty).strip()
        if not value or any(c in value for c in ('\r', '\n', '<', '>', '$', '{', '}')):
            raise SystemExit('空值、多行或占位符：未写入')
        try:
            value.encode('ascii')
            if name == 'webhook_url':
                parts = urlsplit(value)
                if (parts.scheme != 'https' or not parts.hostname or parts.username or parts.password
                        or parts.fragment or parts.port == 0 or any(c.isspace() for c in value)
                        or parts.hostname.endswith(('.invalid', '.example'))):
                    raise ValueError
            else:
                token = value
                if token.lower().startswith('authorization:'):
                    token = token.split(':', 1)[1].strip()
                if token.lower().startswith('bearer '):
                    token = token[7:].strip()
                if not token or any(c.isspace() for c in token) or token.lower() in ('token', 'your-token', 'webhook_key', 'replace-me'):
                    raise ValueError
        except ValueError:
            raise SystemExit('凭据格式不合格或仍为示例：未写入') from None
        values[name] = value
    for name, value in values.items():
        descriptor = os.open(directory / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(descriptor, 'w') as stream:
            stream.write(value + '\n')
            stream.flush()
            os.fsync(stream.fileno())
print('本机新凭据已创建；未输出内容，未 POST；尚需另行授权真实 smoke')
PYCODE
```

目录 0700；新文件属于当前用户、0600、普通文件、非链接。凭据输入与文件保护用合成输入自检；真实 PTY 回归另验证提示流可写，不验证实际隐藏凭据输入。
如中途失败可能已创建部分文件，停止请 owner 核对，不循环覆盖。
只查看元数据的检查（不读取内容）：

```sh
python3 - <<'PYCODE'
from pathlib import Path
import os, stat
for name in ('webhook_url', 'webhook_auth'):
    path = Path.home() / '.config/board-wake' / name
    if not path.exists() and not path.is_symlink():
        print(name + ': MISSING')
        continue
    info = path.lstat()
    ok = stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o600 and info.st_uid == os.getuid()
    print(name + (': OK metadata only' if ok else ': CHECK TYPE/OWNER/MODE'))
PYCODE
```

## 5. 无凭据隔离 dry-run

在仓库根执行；仅覆盖新建临时 HOME 中示例任务，不写真实任务目录，不读凭据、不联网。
模板中的 issue URL 是无效演示域名，不能用来声称真实板项验收。

```sh
mkdir -p .seed-evidence
workflow_demo_home=$(mktemp -d "$PWD/.seed-evidence/demo-home.XXXXXX")
HOME="$workflow_demo_home" python3 scripts/common/board-signal-post --task task123 --dry-run < templates/BOARD_SIGNAL.json
cat "$workflow_demo_home/ray-docs/任务流/task123/BOARD_SIGNAL.md"
```

正常输出 dry-run 且返回 0。检查 15 字段后，由人确认变量仍指这个临时目录，再清理该演示目录。
不要把 dry-run 退出 0 当 POST 2xx。另可按主 README 跑 15 个 loopback 测试，不连接真实 webhook。

## 6. 手工配新 routine 与实际验收

按 templates/routine.md 在平台**新建**配置，替换 owner/Page/时区/静默时间/间隔占位符；不改现有 routine。
凭据只在各机执行第 4 步。每台机本地验证 helper 哈希、权限、版本和映射，不依赖同步文件或跨机代理 POST。
实际任务输入须替换演示 issue/标题/task_id/host/writer/evidence，使用当前带时区 as_of、读取现有 seq 后 +1。
真实 POST 需该任务已有授权，本手册没有自动真实 POST 步骤。
授权 smoke 后另记录 HTTP 接收、routine 运行、去重、静默和实际 Page 结果；任何未验证项保留 UNKNOWN。
