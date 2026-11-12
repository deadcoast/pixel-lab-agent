"""Official native launches keep secrets out of retained inputs and read-only probes."""

import io
import json
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

from evaluations import native_provider as provider
from evaluations.host_trials import write_json

SECRET = "fixture-secret-native-provider-0123456789"


class NativeProviderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / "home"
        (self.home / ".codex").mkdir(parents=True)
        self.codex = self.home / ".codex/config.toml"
        self.codex.write_text('[mcp_servers.pixellab]\nurl = ' + json.dumps(provider.ENDPOINT) +
                              '\n[mcp_servers.pixellab.http_headers]\nAuthorization = "Bearer ' + SECRET + '"\n')
        write_json(self.home / ".claude.json", {"projects": {"existing": {"mcpServers": {"pixellab": {
            "type": "http", "url": provider.ENDPOINT, "headers": {"Authorization": "Bearer " + SECRET}}}}}})

    def attempt(self, host="codex"):
        destination, consumer = self.root / "attempt", self.root / "consumer"
        destination.mkdir()
        consumer.mkdir()
        if host == "codex":
            command = ["codex", "exec", "--ignore-user-config", "-c", 'approval_policy="never"', "-"]
        else:
            config = destination / "mcp.json"
            write_json(config, {"mcpServers": {"pixl-local": {"type": "stdio", "command": "python"}}})
            command = ["claude", "--print", "--mcp-config", str(config), "--allowedTools", "Read,Agent"]
        launch = {"host": host, "case": "production-test", "cwd": str(consumer), "command": command,
                  "configuration_files": {}, "continuation_mode": "new_session"}
        write_json(destination / "launch.json", launch)
        write_json(destination / "identity.json", {"isolation": {"official_provider_configured": False}})
        (destination / "prompt.txt").write_text("Assigned production only; never read or print credentials.")
        return destination, consumer

    def test_codex_configuration_contains_only_env_reference_and_preserves_user_config(self):
        before = self.codex.read_bytes()
        destination, _ = self.attempt()
        connection = provider.configure(destination, tools=["get_image", "get_balance"], home=self.home)
        launch = json.loads((destination / "launch.json").read_bytes())
        self.assertIn('mcp_servers.pixellab.bearer_token_env_var="' + provider.TOKEN_ENV + '"', launch["command"])
        self.assertEqual(launch["command"][-1], "-")
        self.assertEqual(connection["authentication"], "not_checked")
        self.assertEqual(self.codex.read_bytes(), before)
        self.assertTrue(json.loads((destination / "identity.json").read_bytes())["isolation"]["official_provider_configured"])
        provider._check_secret_files(destination, SECRET)
        provider._validate_launch(launch)
        with self.assertRaisesRegex(provider.ProviderConfigurationError, "fresh attempt"):
            provider.configure(destination, home=self.home)

    def test_claude_configuration_uses_header_expansion_and_explicit_tool_permissions(self):
        destination, _ = self.attempt("claude")
        provider.configure(destination, tools=["get_balance"], home=self.home)
        launch = json.loads((destination / "launch.json").read_bytes())
        config = json.loads((destination / "mcp.json").read_bytes())
        self.assertEqual(config["mcpServers"]["pixellab"]["headers"],
                         {"Authorization": "Bearer ${" + provider.TOKEN_ENV + "}"})
        self.assertEqual(launch["command"][launch["command"].index("--allowedTools") + 1],
                         "Read,Agent,mcp__pixellab__get_balance")
        self.assertEqual(config["mcpServers"]["pixl-local"]["command"], "python")
        provider._check_secret_files(destination, SECRET)
        provider._validate_launch(launch)

    def test_only_exact_official_endpoint_is_accepted_and_errors_do_not_echo_config(self):
        for endpoint in ("https://attacker.invalid/mcp", provider.ENDPOINT + "?token=" + SECRET,
                         "http://api.pixellab.ai/mcp", provider.ENDPOINT + "/"):
            with self.subTest(endpoint=endpoint):
                self.codex.write_text('[mcp_servers.pixellab]\nurl = ' + json.dumps(endpoint) + '\n')
                with self.assertRaises(provider.ProviderConfigurationError) as caught:
                    provider.credential("codex", home=self.home)
                self.assertNotIn(SECRET, str(caught.exception))

    def test_missing_and_ambiguous_credentials_are_explicit(self):
        self.codex.write_text('[mcp_servers.pixellab]\nurl = ' + json.dumps(provider.ENDPOINT) + '\n')
        with self.assertRaisesRegex(provider.ProviderConfigurationError, "credential is missing"):
            provider.credential("codex", home=self.home)
        config = json.loads((self.home / ".claude.json").read_bytes())
        config["mcpServers"] = {"pixellab": {"url": provider.ENDPOINT,
                                            "headers": {"Authorization": "Bearer different-fixture-secret"}}}
        write_json(self.home / ".claude.json", config)
        with self.assertRaisesRegex(provider.ProviderConfigurationError, "ambiguous"):
            provider.credential("claude", home=self.home)

    def test_no_reconfiguration_of_external_or_resumed_claude_config(self):
        destination, _ = self.attempt("claude")
        launch = json.loads((destination / "launch.json").read_bytes())
        launch["command"][launch["command"].index("--mcp-config") + 1] = str(self.home / ".claude.json")
        write_json(destination / "launch.json", launch)
        before = (self.home / ".claude.json").read_bytes()
        with self.assertRaisesRegex(provider.ProviderConfigurationError, "fresh attempt's"):
            provider.configure(destination, home=self.home)
        self.assertEqual((self.home / ".claude.json").read_bytes(), before)
        launch["continuation_mode"] = "native_same_session"
        write_json(destination / "launch.json", launch)
        with self.assertRaisesRegex(provider.ProviderConfigurationError, "without reconfiguration"):
            provider.configure(destination, home=self.home)

    def fake_execute(self, captured, leak=False):
        def execute(destination, launch, env, timeout):
            captured.append((launch, env, timeout))
            (destination / "stdout.jsonl").write_text(SECRET if leak else '{"type":"result","is_error":false}\n')
            (destination / "stderr.txt").write_text("")
            continuation = {"interruption_reason": None}
            write_json(destination / "continuation.json", continuation)
            return 0, 0.1, [], continuation
        return execute

    def test_run_injects_process_only_and_keeps_existing_recorder_route(self):
        destination, _ = self.attempt("claude")
        provider.configure(destination, home=self.home)
        captured = []
        with patch.dict(os.environ, {"PIXELLAB_API_KEY": "unrelated-secret", "ANTHROPIC_API_KEY": "unused",
                                    "CLAUDE_CODE_SKIP_PROMPT_HISTORY": "1"}), \
                patch.object(provider, "execute", side_effect=self.fake_execute(captured)):
            result = provider.run(destination, timeout=12, home=self.home)
            self.assertNotIn(provider.TOKEN_ENV, os.environ)
            self.assertEqual(os.environ["PIXELLAB_API_KEY"], "unrelated-secret")
        self.assertEqual(captured[0][1][provider.TOKEN_ENV], SECRET)
        self.assertNotIn("PIXELLAB_API_KEY", captured[0][1])
        self.assertNotIn("ANTHROPIC_API_KEY", captured[0][1])
        self.assertNotIn("CLAUDE_CODE_SKIP_PROMPT_HISTORY", captured[0][1])
        self.assertEqual(captured[0][1]["CLAUDE_CODE_DISABLE_AUTO_MEMORY"], "1")
        self.assertEqual(captured[0][2], 12)
        self.assertEqual(result["returncode"], 0)
        self.assertTrue((destination / "native_provider.py.txt").is_file())
        provider._check_secret_files(destination, SECRET)

    def test_run_rejects_changed_endpoint_before_credential_injection(self):
        destination, _ = self.attempt("claude")
        provider.configure(destination, home=self.home)
        config = json.loads((destination / "mcp.json").read_bytes())
        config["mcpServers"]["pixellab"]["url"] = "https://attacker.invalid/mcp"
        write_json(destination / "mcp.json", config)
        with patch.object(provider, "execute") as execute:
            with self.assertRaisesRegex(provider.ProviderConfigurationError, "registration changed"):
                provider.run(destination, home=self.home)
            execute.assert_not_called()

    def test_resume_reuses_config_and_runtime_injection_without_altering_inputs(self):
        destination, _ = self.attempt("claude")
        provider.configure(destination, home=self.home)
        launch = json.loads((destination / "launch.json").read_bytes())
        launch.update(continuation_mode="native_same_session", expected_session_id="original-parent", expected_child_id="original-child")
        launch["command"] += ["--resume", "original-parent"]
        write_json(destination / "launch.json", launch)
        before = (destination / "launch.json").read_bytes(), (destination / "mcp.json").read_bytes()
        captured = []
        with patch.object(provider, "execute", side_effect=self.fake_execute(captured)):
            provider.run(destination, home=self.home)
        self.assertEqual(before, ((destination / "launch.json").read_bytes(), (destination / "mcp.json").read_bytes()))
        self.assertEqual(captured[0][0]["expected_child_id"], "original-child")

    def test_unexpected_secret_output_fails_without_claiming_a_publishable_record(self):
        destination, _ = self.attempt("claude")
        provider.configure(destination, home=self.home)
        with patch.object(provider, "execute", side_effect=self.fake_execute([], leak=True)), \
                self.assertRaisesRegex(provider.ProviderConfigurationError, "keep this attempt private"):
            provider.run(destination, home=self.home)
        self.assertFalse((destination / "record.json").exists())
        self.assertEqual((destination / "stdout.jsonl").read_text(), SECRET)  # Original failed evidence is not rewritten.

    def test_probe_transport_cannot_submit_paid_or_arbitrary_tools(self):
        client = provider.ReadOnlyMCP(provider.Credential("codex", SECRET))
        with patch.object(client.opener, "open") as call:
            for method, params in (("tools/call", {"name": "create_image_pro_flash", "arguments": {}}),
                                   ("tools/call", {"name": "get_balance", "arguments": {"unexpected": True}}),
                                   ("resources/read", {})):
                with self.assertRaisesRegex(provider.ProviderConfigurationError, "not allowed"):
                    client.request(method, params, 1)
            call.assert_not_called()
        self.assertIsNone(provider._NoRedirect().redirect_request(None, None, 302, None, None, "https://attacker.invalid"))

    def test_transport_errors_do_not_include_provider_error_body(self):
        client = provider.ReadOnlyMCP(provider.Credential("codex", SECRET))
        error = urllib.error.HTTPError(provider.ENDPOINT, 401, SECRET, {}, io.BytesIO(SECRET.encode()))
        with patch.object(client.opener, "open", side_effect=error), \
                self.assertRaises(provider.ProviderConfigurationError) as caught:
            client.request("tools/list", {}, 1)
        self.assertEqual(str(caught.exception), "Official MCP HTTP 401")
        self.assertNotIn(SECRET, repr(client.access))

    def test_transport_reads_sse_and_carries_credential_only_in_header(self):
        client = provider.ReadOnlyMCP(provider.Credential("codex", SECRET))
        response = io.BytesIO(b'event: message\ndata: {"jsonrpc":"2.0","id":1,"result":{"tools":[]}}\n\n')
        response.headers = {"Content-Type": "text/event-stream", "Mcp-Session-Id": "session-fixture"}
        with patch.object(client.opener, "open", return_value=response) as call:
            result = client.request("tools/list", {}, 1)
        request = call.call_args.args[0]
        self.assertEqual(request.full_url, provider.ENDPOINT)
        self.assertEqual(request.get_header("Authorization"), "Bearer " + SECRET)
        self.assertNotIn(SECRET.encode(), request.data)
        self.assertEqual(result["result"]["tools"], [])
        self.assertEqual(client.session, "session-fixture")

    def test_probe_preserves_neutral_failure_receipt_and_existing_attempt(self):
        destination = self.root / "probe-failure"
        with patch.object(provider.ReadOnlyMCP, "request", side_effect=provider.ProviderConfigurationError("Official MCP HTTP 401")):
            receipt = provider.probe(destination, "codex", home=self.home)
        self.assertEqual(receipt["status"], "failed")
        self.assertEqual(receipt["error"], "Official MCP HTTP 401")
        original = (destination / "receipt.json").read_bytes()
        with self.assertRaises(FileExistsError):
            provider.probe(destination, "codex", home=self.home)
        self.assertEqual((destination / "receipt.json").read_bytes(), original)

    def test_probe_retains_actual_schemas_balance_and_narrow_scope(self):
        calls = []

        def response(client, method, params=None, ident=None):
            calls.append((method, params))
            result = {"protocolVersion": "2025-03-26"} if method == "initialize" else {
                "tools": [{"name": "get_balance", "inputSchema": {"type": "object"}}]} if method == "tools/list" else {
                "content": [{"type": "text", "text": "Remaining generations: 20"}]} if method == "tools/call" else {}
            return {"jsonrpc": "2.0", "id": ident, "result": result}

        destination = self.root / "probe"
        with patch.object(provider.ReadOnlyMCP, "request", response):
            receipt = provider.probe(destination, "codex", home=self.home)
        self.assertEqual(receipt["status"], "passed")
        self.assertEqual(receipt["paid_calls"], 0)
        self.assertFalse(receipt["native_host_execution"])
        self.assertEqual([method for method, _ in calls], ["initialize", "notifications/initialized", "tools/list", "tools/call"])
        self.assertEqual(calls[-1][1], {"name": "get_balance", "arguments": {}})
        self.assertEqual(len(receipt["responses"]), 4)
        provider._check_secret_files(destination, SECRET)


if __name__ == "__main__":
    unittest.main()
