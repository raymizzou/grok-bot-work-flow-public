import ast
import os
from pathlib import Path
import pty
import re
import select
import unittest


class BootstrapTests(unittest.TestCase):
    def test_credential_prompt_uses_real_nonseekable_terminal(self):
        readme = Path(__file__).with_name('README.md').read_text()
        snippet, = [code for code in re.findall(
            r"python3 - <<'PYCODE'\n(.*?)^PYCODE", readme, re.M | re.S
        ) if 'from getpass import' in code]
        terminal_open, = [node for node in ast.walk(ast.parse(snippet))
                          if isinstance(node, ast.Call)
                          and isinstance(node.func, ast.Name) and node.func.id == 'open'
                          and node.args and isinstance(node.args[0], ast.Constant)
                          and node.args[0].value == '/dev/tty']
        master, slave = pty.openpty()
        try:
            # Use the documented open arguments on an actual nonseekable terminal.
            terminal_open.args[0] = ast.Constant(os.ttyname(slave))
            expression = ast.fix_missing_locations(ast.Expression(terminal_open))
            with eval(compile(expression, '<documented terminal open>', 'eval')) as terminal:
                self.assertTrue(terminal.isatty())
                self.assertFalse(terminal.seekable())
                self.assertTrue(terminal.writable())
                terminal.write('Bootstrap credential prompt\n')
                terminal.flush()
                os.set_blocking(master, False)
                ready, _, _ = select.select([master], [], [], 2)
                self.assertTrue(ready, 'prompt not observed within independent PTY deadline')
                self.assertIn(b'Bootstrap credential prompt', os.read(master, 4096))
        finally:
            os.close(slave)
            os.close(master)


if __name__ == '__main__':
    unittest.main()
