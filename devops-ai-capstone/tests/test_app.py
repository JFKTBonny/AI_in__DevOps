import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from unittest.mock import patch
from urllib.request import Request, urlopen
from urllib.error import HTTPError

import app


SNAPSHOT = {
    "incident": {"id": "test-1", "service": "checkout-api"},
    "timeline": [{"time": "14:00", "event": "Deployment completed"}],
    "metrics": [
        {"time": "14:05", "p95_latency_ms": 900, "pod_restarts": 1}
    ],
    "log_samples": [
        {"time": "14:04", "level": "ERROR", "message": "database timeout"}
    ],
}


class TriageApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), app.TriageHandler)
        cls.server_thread = threading.Thread(
            target=cls.server.serve_forever, daemon=True
        )
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def post_json(self, path, payload):
        request = Request(
            self.base_url + path,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        return urlopen(request, timeout=2)

    def test_health_endpoint(self):
        with urlopen(self.base_url + "/healthz", timeout=2) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(json.loads(response.read()), {"status": "ok"})

    def test_invalid_snapshot_is_rejected(self):
        with self.assertRaises(HTTPError) as raised:
            self.post_json("/triage", {"incident": {}})
        self.assertEqual(raised.exception.code, 400)

    @patch.dict("os.environ", {"GROQ_API_KEY": "test-key"})
    @patch("app.analyze_snapshot", return_value="Evidence-based report.")
    def test_triage_returns_report_and_no_actions(self, analyze):
        with self.post_json("/triage", SNAPSHOT) as response:
            result = json.loads(response.read())
        self.assertEqual(result["triage"], "Evidence-based report.")
        self.assertEqual(result["actions_taken"], [])
        analyze.assert_called_once()

    def test_log_search_reads_only_matching_sample(self):
        matches = app.run_read_only_tool(
            "search_log_samples", {"query": "DATABASE"}, SNAPSHOT
        )
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["time"], "14:04")

    def test_unlisted_tool_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "not allowed"):
            app.run_read_only_tool("run_shell_command", {}, SNAPSHOT)

    @patch("app._request_completion")
    def test_agent_uses_read_only_tool_then_returns_report(self, request_model):
        request_model.side_effect = [
            {
                "tool_calls": [
                    {
                        "id": "call-1",
                        "function": {
                            "name": "get_metric_trend",
                            "arguments": '{"metric":"p95_latency_ms"}',
                        },
                    }
                ]
            },
            {"content": "Latency increased at 14:05."},
        ]
        report = app.analyze_snapshot(SNAPSHOT, "test-key")
        self.assertEqual(report, "Latency increased at 14:05.")
        tool_result = request_model.call_args_list[1].args[0][-1]
        self.assertEqual(tool_result["role"], "tool")
        self.assertIn("900", tool_result["content"])


if __name__ == "__main__":
    unittest.main()
