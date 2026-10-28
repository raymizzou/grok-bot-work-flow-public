import contextlib
import errno
import http.client
import io
import json
import os
from pathlib import Path
import subprocess
import runpy
import socket
import ssl
import sys
import tempfile
import threading
import unittest
from unittest import mock
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


HELPER = Path(__file__).with_name("board-signal-post")
SIGNAL = {
    "board": "任务流",
    "board_row": "T4",
    "task_id": "test-task",
    "title": "本机看板信号",
    "goal": "先写入再唤醒",
    "status": "wip",
    "question": "",
    "host": "air",
    "pr": "",
    "event": "milestone",
    "as_of": "2026-10-23T12:40:00Z",
    "seq": 1,
    "summary": "T4-smoke: 中文\n第二行",
    "evidence": "本地验证",
    "writer": "Codex",
}


class BoardSignalPostTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.target = self.home / "ray-docs/任务流/test-task/BOARD_SIGNAL.md"
        self.credentials = self.home / ".config/board-wake"
        self.credentials.mkdir(parents=True, mode=0o700)
        self.requests = []

    @contextlib.contextmanager
    def server(self, status=204):
        records, target = self.requests, self.target

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                records.append({
                    "body": json.loads(self.rfile.read(int(self.headers["Content-Length"]))),
                    "auth": self.headers.get("Authorization"),
                    "key": self.headers.get("Idempotency-Key"),
                    "signal": target.read_text(encoding="utf-8"),
                    "path": self.path,
                })
                if status is None:
                    self.wfile.write(b"invalid-response-containing-test-only-token\r\n")
                    self.close_connection = True
                    return
                self.send_response(status)
                if status == 302:
                    self.send_header("Location", "/do-not-follow")
                self.end_headers()

            def log_message(self, *args):
                pass

            def do_GET(self):
                records.append({"method": "GET", "auth": self.headers.get("Authorization")})
                self.send_response(204)
                self.end_headers()

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_port}/private-hook"
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def configure(self, url, auth="test-only-token"):
        for name, value in (("webhook_url", url), ("webhook_auth", auth)):
            path = self.credentials / name
            path.write_text(value + "\n", encoding="utf-8")
            path.chmod(0o600)

    def run_helper(self, signal=None, *args, raw_input=None):
        return subprocess.run(
            [sys.executable, str(HELPER), "--task", "test-task", *args],
            input=(json.dumps(SIGNAL if signal is None else signal, ensure_ascii=False)
                   if raw_input is None else raw_input),
            text=True, capture_output=True, timeout=10,
            env={**os.environ, "HOME": str(self.home)},
        )

    def test_write_then_post_and_stable_retry(self):
        self.target.parent.mkdir(parents=True)
        self.target.write_text("old signal", encoding="utf-8")
        with self.server() as url, self.target.open() as previous:
            self.configure(url)
            first = self.run_helper()
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(previous.read(), "old signal", "replace the file atomically")
            second = self.run_helper()
            self.assertEqual(second.returncode, 0, second.stderr)
            changed = self.run_helper({**SIGNAL, "seq": 2})
            self.assertEqual(changed.returncode, 0, changed.stderr)
        self.assertEqual(len(self.requests), 3)
        posted = self.requests[0]
        fields = dict(line.split(": ", 1) for line in posted["signal"].split("```")[1].splitlines()[1:] if line)
        self.assertEqual({k: json.loads(v) for k, v in fields.items()}, SIGNAL)
        self.assertEqual(posted["auth"], "Bearer test-only-token")
        payload = posted["body"]
        self.assertEqual(set(payload), {"source", "host", "diff_id", "sent_at", "changes"})
        self.assertEqual(payload["source"], "board-signal-post")
        self.assertEqual(payload["host"], "air")
        self.assertEqual(self.target.stat().st_mode & 0o777, 0o644)
        self.assertEqual(payload["changes"], [{
            "path": "任务流/test-task/BOARD_SIGNAL.md", "seq": 1, "board_row": "T4",
            "status": "wip", "event": "milestone", "task_id": "test-task",
            "title": "本机看板信号", "summary": "T4-smoke: 中文\n第二行", "question": "",
            "pr": "", "as_of": "2026-10-23T12:40:00Z",
        }])
        self.assertEqual(payload["diff_id"], self.requests[1]["body"]["diff_id"])
        self.assertNotEqual(payload["diff_id"], self.requests[2]["body"]["diff_id"])
        self.assertEqual(posted["key"], payload["diff_id"])
        self.assertNotIn("test-only-token", first.stdout + first.stderr + json.dumps(payload) + posted["signal"])
        self.assertNotIn(url, first.stdout + first.stderr)

    def test_dry_run(self):
        with self.server() as url:
            self.configure(url)
            result = self.run_helper(None, "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("dry-run", result.stdout)
        self.assertTrue(self.target.is_file())
        self.assertEqual(self.requests, [])
        for path in self.credentials.iterdir():
            path.unlink()
        self.assertEqual(self.run_helper(None, "--dry-run").returncode, 0)

    def test_auth_forms(self):
        with self.server() as url:
            for auth in ("test-only-token", "Bearer test-only-token",
                         "Authorization: test-only-token", "Authorization: Bearer test-only-token"):
                with self.subTest(auth=auth):
                    self.configure(url, auth)
                    result = self.run_helper()
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(self.requests[-1]["auth"], "Bearer test-only-token")
                    self.assertNotIn("test-only-token", result.stdout + result.stderr)

    def test_http_failure(self):
        for status in (400, 401, 500):
            with self.subTest(status=status), self.server(status) as url:
                self.configure(url)
                result = self.run_helper()
                self.assertEqual(result.returncode, 4)
                self.assertIn("signal written; delivery pending", result.stderr)
                self.assertTrue(self.target.is_file())
                self.assertNotIn(url, result.stdout + result.stderr)
                self.assertNotIn("test-only-token", result.stdout + result.stderr)
        self.assertEqual(len(self.requests), 3, "one POST per invocation, no automatic retry")

    def test_mocked_http_error_diagnostics(self):
        url = "https://example.invalid/private-hook?secret=url-canary"
        self.configure(url)
        response = io.BytesIO(b"response-body-canary")
        error = urllib.error.HTTPError(url, 503, "Service Unavailable", {}, response)
        helper = runpy.run_path(str(HELPER))
        stderr = io.StringIO()
        opener = mock.Mock()
        opener.open.side_effect = error
        with mock.patch.dict(os.environ, {"HOME": str(self.home)}), \
                mock.patch.object(sys, "argv", [str(HELPER), "--task", "test-task"]), \
                mock.patch.object(sys, "stdin", io.StringIO(json.dumps(SIGNAL))), \
                mock.patch("urllib.request.build_opener", return_value=opener), \
                contextlib.redirect_stderr(stderr):
            self.assertEqual(helper["main"](), 4)
        output = stderr.getvalue()
        self.assertIn("signal written; delivery pending; retry same input at most once", output)
        self.assertIn("exc_type=HTTPError", output)
        self.assertIn("http_status=503", output)
        self.assertIn("reason=Service Unavailable", output)
        for secret in (url, "url-canary", "test-only-token", "response-body-canary"):
            self.assertNotIn(secret, output)
        self.assertEqual(len(output.splitlines()), 1)
        self.assertTrue(self.target.is_file())
        self.assertTrue(response.closed)
        self.assertEqual(opener.open.call_count, 1, "no automatic retry")

    def test_mocked_transport_error_diagnostics(self):
        url = "https://example.invalid/private-hook?secret=url-canary"
        self.configure(url)
        helper = runpy.run_path(str(HELPER))
        cases = (
            (urllib.error.URLError("timed out"), "URLError", "timed out"),
            (TimeoutError("untrusted timeout text"), "TimeoutError", "timed out"),
            (urllib.error.URLError(ConnectionRefusedError(errno.ECONNREFUSED, "untrusted text")),
             "URLError", "Connection refused"),
            (OSError(errno.ENETUNREACH, "untrusted network text"), "OSError", "Network is unreachable"),
            (urllib.error.URLError(socket.gaierror(socket.EAI_NONAME, "untrusted DNS text")),
             "URLError", "name resolution failed"),
            (urllib.error.URLError(ssl.SSLCertVerificationError(1, "untrusted TLS text")),
             "URLError", "certificate verification failed"),
            (urllib.error.URLError(ssl.SSLError(ssl.SSL_ERROR_SSL, "untrusted TLS text")),
             "URLError", "TLS error"),
            (http.client.BadStatusLine("test-only-token"), "BadStatusLine", "invalid HTTP response"),
        )
        for error, exc_type, reason in cases:
            with self.subTest(exc_type=exc_type, reason=reason):
                stderr = io.StringIO()
                opener = mock.Mock()
                opener.open.side_effect = error
                with mock.patch.dict(os.environ, {"HOME": str(self.home)}), \
                        mock.patch.object(sys, "argv", [str(HELPER), "--task", "test-task"]), \
                        mock.patch.object(sys, "stdin", io.StringIO(json.dumps(SIGNAL))), \
                        mock.patch("urllib.request.build_opener", return_value=opener), \
                        contextlib.redirect_stderr(stderr):
                    self.assertEqual(helper["main"](), 4)
                output = stderr.getvalue()
                self.assertIn("signal written; delivery pending; retry same input at most once", output)
                self.assertIn("exc_type=" + exc_type, output)
                self.assertIn("http_status=-", output)
                self.assertIn("reason=" + reason, output)
                for secret in (url, "url-canary", "test-only-token", "untrusted"):
                    self.assertNotIn(secret, output)
                self.assertEqual(len(output.splitlines()), 1)
                self.assertTrue(self.target.is_file())
                self.assertEqual(opener.open.call_count, 1, "no automatic retry")

    def test_delivery_error_redaction(self):
        url = "https://example.invalid/private-hook?secret=url-canary"
        self.configure(url)
        helper = runpy.run_path(str(HELPER))
        secrets = (url, "url-canary", "test-only-token", "unrelated-header-canary", "body-canary")
        message = (f"{url}\r\nAuthorization: Bearer test-only-token "
                   "Authorization: Bearer unrelated-header-canary\n"
                   '{"secret": "body-canary"} ' + "x" * 10000)
        errors = (
            urllib.error.HTTPError(url, 503, message, {"Authorization": message}, io.BytesIO(message.encode())),
            urllib.error.URLError(message),
            OSError(errno.ECONNRESET, message, url),
            TimeoutError(message),
            http.client.BadStatusLine(message),
        )
        for error in errors:
            with self.subTest(exc_type=type(error).__name__):
                stderr = io.StringIO()
                opener = mock.Mock()
                opener.open.side_effect = error
                with mock.patch.dict(os.environ, {"HOME": str(self.home)}), \
                        mock.patch.object(sys, "argv", [str(HELPER), "--task", "test-task"]), \
                        mock.patch.object(sys, "stdin", io.StringIO(json.dumps(SIGNAL))), \
                        mock.patch("urllib.request.build_opener", return_value=opener), \
                        contextlib.redirect_stderr(stderr):
                    self.assertEqual(helper["main"](), 4)
                output = stderr.getvalue()
                self.assertIn("exc_type=" + type(error).__name__, output)
                self.assertIn("reason=", output)
                for secret in (*secrets, "Authorization", "Bearer", "Traceback"):
                    self.assertNotIn(secret, output)
                self.assertEqual(len(output.splitlines()), 1)
                self.assertLess(len(output), 300)
                self.assertEqual(opener.open.call_count, 1, "no automatic retry")

    def test_non_2xx_response_diagnostics(self):
        url = "https://example.invalid/private-hook?secret=url-canary"
        self.configure(url)
        helper = runpy.run_path(str(HELPER))
        stderr = io.StringIO()
        opener = mock.MagicMock()
        opener.open.return_value.__enter__.return_value.status = 502
        with mock.patch.dict(os.environ, {"HOME": str(self.home)}), \
                mock.patch.object(sys, "argv", [str(HELPER), "--task", "test-task"]), \
                mock.patch.object(sys, "stdin", io.StringIO(json.dumps(SIGNAL))), \
                mock.patch("urllib.request.build_opener", return_value=opener), \
                contextlib.redirect_stderr(stderr):
            self.assertEqual(helper["main"](), 4)
        output = stderr.getvalue()
        self.assertIn("http_status=502", output)
        self.assertIn("reason=Bad Gateway", output)
        self.assertNotIn(url, output)
        self.assertNotIn("test-only-token", output)
        self.assertTrue(self.target.is_file())
        self.assertEqual(opener.open.call_count, 1, "no automatic retry")

    def test_redirect(self):
        with self.server(302) as url:
            self.configure(url)
            result = self.run_helper()
        self.assertEqual(result.returncode, 4)
        self.assertIn("signal written; delivery pending", result.stderr)
        self.assertEqual(len(self.requests), 1, "never follow redirects carrying credentials")

    def test_missing_or_unsafe_credentials(self):
        with self.server() as url:
            missing = self.run_helper()
            self.assertEqual(missing.returncode, 3)
            self.assertIn("signal written; delivery pending", missing.stderr)
            self.assertTrue(self.target.is_file())
            self.configure(url)
            auth = self.credentials / "webhook_auth"
            auth.chmod(0o644)
            self.assertEqual(self.run_helper().returncode, 3)
            auth.chmod(0o600)
            external = self.home / "external-token"
            auth.rename(external)
            auth.symlink_to(external)
            self.assertEqual(self.run_helper().returncode, 3, "reject symlinked credentials")
        self.assertEqual(self.requests, [])

    def test_invalid_input(self):
        self.target.parent.mkdir(parents=True)
        self.target.write_text("preserve this signal", encoding="utf-8")
        bad_inputs = [[], {k: v for k, v in SIGNAL.items() if k != "goal"}]
        bad_inputs += [{**SIGNAL, **patch} for patch in (
            {"seq": True}, {"seq": 0}, {"status": "complete"},
            {"host": "other"}, {"event": "other"}, {"goal": ""}, {"pr": []},
        )]
        for value in bad_inputs:
            with self.subTest(value=value):
                self.assertEqual(self.run_helper(value, "--dry-run").returncode, 2)
                self.assertEqual(self.target.read_text(), "preserve this signal")
        for text in ("{", "", "NaN"):
            with self.subTest(raw_input=text):
                result = self.run_helper(None, "--dry-run", raw_input=text)
                self.assertEqual(result.returncode, 2)
                self.assertIn("signal not written", result.stderr)
                self.assertEqual(self.target.read_text(), "preserve this signal")
        result = self.run_helper(None, "--task", "../outside", "--dry-run")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.home / "ray-docs/outside").exists())

    def test_invalid_configuration(self):
        with self.server() as url:
            cases = [
                ("http://x.invalid/private-hook", "test-only-token"),
                (url + "#private-fragment", "test-only-token"),
                (url.replace("127.0.0.1", "user:test-only-token@127.0.0.1"), "test-only-token"),
                ("http://127.0.0.1:bad/private-hook", "test-only-token"),
                ("http://127.0.0.1:99999/private-hook", "test-only-token"),
                (url + "/中文", "test-only-token"),
                ("", "test-only-token"), (url + "\nsecond-line", "test-only-token"),
                (url, ""), (url, "first-line\nsecond-line"),
                (url, "Bearer two tokens"), (url, "Bearer 中文"),
            ]
            for configured_url, auth in cases:
                with self.subTest(url=configured_url, auth=auth):
                    self.configure(configured_url, auth)
                    result = self.run_helper()
                    self.assertEqual(result.returncode, 3)
                    self.assertIn("signal written; delivery pending", result.stderr)
                    self.assertTrue(self.target.is_file())
                    self.assertNotIn("test-only-token", result.stdout + result.stderr)
                    self.assertNotIn(url, result.stdout + result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(self.requests, [])

    def test_blocked_display_fields(self):
        with self.server() as url:
            self.configure(url)
            result = self.run_helper({**SIGNAL, "status": "blocked", "event": "blocked",
                                      "question": "请选择后续方案", "pr": "https://example.invalid/pr/1"})
        self.assertEqual(result.returncode, 0, result.stderr)
        change = self.requests[0]["body"]["changes"][0]
        self.assertEqual(change["status"], "blocked")
        self.assertEqual(change["event"], "blocked")
        self.assertEqual(change["question"], "请选择后续方案")
        self.assertEqual(change["pr"], "https://example.invalid/pr/1")

    def test_signal_write_failure(self):
        self.target.parent.parent.mkdir(parents=True)
        self.target.parent.write_text("cannot create a directory here", encoding="utf-8")
        with self.server() as url:
            self.configure(url)
            result = self.run_helper()
        self.assertEqual(result.returncode, 1)
        self.assertIn("signal write failed; no POST", result.stderr)
        self.assertEqual(self.requests, [])
        self.assertEqual(self.target.parent.read_text(), "cannot create a directory here")
        self.assertNotIn("Traceback", result.stderr)

    def test_transport_failure(self):
        with self.server(None) as url:
            self.configure(url)
            result = self.run_helper()
        self.assertEqual(result.returncode, 4)
        self.assertTrue(self.target.is_file())
        self.assertNotIn(url, result.stdout + result.stderr)
        self.assertNotIn("test-only-token", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(len(self.requests), 1, "no automatic retry after a transport failure")


if __name__ == "__main__":
    unittest.main()
