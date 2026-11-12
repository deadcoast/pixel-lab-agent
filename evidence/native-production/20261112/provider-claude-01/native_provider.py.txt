"""Run an explicitly configured native trial with the existing official MCP account.

Credentials are read from the selected host's local registration only at execution.
Saved launches contain an environment-variable reference, never its secret value.
The optional probe performs initialize, tools/list and get_balance only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import tomllib
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from evaluations.host_trials import inventory, outcome, sha, write_json
from evaluations.native_trial_records import (
    atomic_json,
    codex_journals,
    execute,
    now,
    reference,
)
from evaluations.request_review_trials import retain_journals

ENDPOINT = "https://api.pixellab.ai/mcp"
TOKEN_ENV = "PIXL_NATIVE_PROVIDER_TOKEN"
MAX_RESPONSE = 16 * 1024 * 1024


class ProviderConfigurationError(ValueError):
    """A neutral diagnostic; never include credential values or HTTP bodies."""


@dataclass(frozen=True)
class Credential:
    host: str
    token: str = field(repr=False)


def credential(host: str, *, home: Path | None = None) -> Credential:
    """Read only the named existing pixellab registration, without changing it."""
    home = Path(home) if home is not None else Path.home()
    try:
        if host == "codex":
            data = tomllib.loads((home / ".codex/config.toml").read_text(encoding="utf-8-sig"))
            rows = [data.get("mcp_servers", {}).get("pixellab")]
        elif host == "claude":
            data = json.loads((home / ".claude.json").read_bytes())
            rows = [data.get("mcpServers", {}).get("pixellab")]
            rows += [row.get("mcpServers", {}).get("pixellab") for row in data.get("projects", {}).values()]
        else:
            raise ProviderConfigurationError("Unsupported native host")
    except (OSError, ValueError) as error:
        if isinstance(error, ProviderConfigurationError):
            raise
        raise ProviderConfigurationError("Existing provider registration is missing or unreadable") from None
    rows = [row for row in rows if row is not None]
    if not rows:
        raise ProviderConfigurationError("Existing pixellab registration is missing")
    tokens = set()
    for row in rows:
        if not isinstance(row, dict) or row.get("url") != ENDPOINT:
            raise ProviderConfigurationError("Only the exact official PixelLab MCP endpoint is allowed")
        headers = row.get("http_headers", row.get("headers", {}))
        if not isinstance(headers, dict) or any(not isinstance(key, str) for key in headers):
            raise ProviderConfigurationError("Existing provider headers are invalid")
        authorization = next((value for key, value in headers.items() if key.lower() == "authorization"), "")
        if host == "codex" and row.get("bearer_token_env_var"):
            variable = row["bearer_token_env_var"]
            if not isinstance(variable, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", variable):
                raise ProviderConfigurationError("Existing provider credential variable is invalid")
            token = os.environ.get(variable, "")
        elif isinstance(authorization, str) and authorization.startswith("Bearer "):
            token = authorization[7:]
        else:
            token = ""
        if not token or re.search(r"\s|\$\{", token):
            raise ProviderConfigurationError("Existing provider bearer credential is missing or invalid")
        tokens.add(token)
    if len(tokens) != 1:
        raise ProviderConfigurationError("Existing provider registrations have ambiguous credentials")
    return Credential(host, tokens.pop())


def _names(names):
    if names is None:
        return None
    if not names or any(not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_]+", name) for name in names):
        raise ProviderConfigurationError("Supply explicit MCP tool names or omit the filter")
    return sorted(set(names))


def _codex_settings(names):
    result = {"url": ENDPOINT, "bearer_token_env_var": TOKEN_ENV}
    if names is not None:
        result["enabled_tools"] = names
    return [f"mcp_servers.pixellab.{key}=" + json.dumps(value) for key, value in result.items()]


def _claude_server():
    return {"type": "http", "url": ENDPOINT, "headers": {"Authorization": "Bearer ${" + TOKEN_ENV + "}"}}


def configure(destination: Path, *, tools: list[str] | None = None, home: Path | None = None) -> dict:
    """Add the official connection to an unlaunched prepared trial; no remote call."""
    destination = Path(destination).resolve()
    if any((destination / name).exists() for name in ("stdout.jsonl", "continuation.json", "provider-connection.json")):
        raise ProviderConfigurationError("Configure a fresh attempt once; do not alter retained launches")
    launch = json.loads((destination / "launch.json").read_bytes())
    host, command, names = launch["host"], list(launch["command"]), _names(tools)
    credential(host, home=home)  # Fail before writing a misleading configured receipt.
    if launch.get("continuation_mode") == "native_same_session":
        raise ProviderConfigurationError("Resume the original configured launch without reconfiguration")
    if host == "codex":
        if any("mcp_servers.pixellab." in arg for arg in command):
            raise ProviderConfigurationError("Provider overrides already exist")
        at = len(command) - 1 if command[-1:] == ["-"] else len(command)
        command[at:at] = [arg for setting in _codex_settings(names) for arg in ("-c", setting)]
    else:
        path = Path(command[command.index("--mcp-config") + 1]).resolve()
        if not path.is_relative_to(destination):
            raise ProviderConfigurationError("Only this fresh attempt's MCP configuration may be changed")
        config = json.loads(path.read_bytes())
        if "pixellab" in config["mcpServers"]:
            raise ProviderConfigurationError("Provider registration already exists")
        config["mcpServers"]["pixellab"] = _claude_server()
        index = command.index("--allowedTools") + 1
        permission = ["mcp__pixellab__" + name for name in names] if names else ["mcp__pixellab__*"]
        command[index] += "," + ",".join(permission)
        write_json(path, config)
    connection = {"host": host, "endpoint": ENDPOINT, "transport": "streamable-http",
                  "credential_environment": TOKEN_ENV, "tools": names,
                  "credential_source": "Existing host-local pixellab registration; loaded only in memory",
                  "credentials_retained": False, "authentication": "not_checked", "remote_calls": []}
    write_json(destination / "provider-connection.json", connection)
    launch.update(command=command, official_provider=connection)
    launch.setdefault("configuration_files", {})["provider_connection"] = str(destination / "provider-connection.json")
    write_json(destination / "launch.json", launch)
    identity_path = destination / "identity.json"
    if identity_path.is_file():
        identity = json.loads(identity_path.read_bytes())
        identity.setdefault("isolation", {})["official_provider_configured"] = True
        identity["provider_connection"] = reference(destination / "provider-connection.json")
        write_json(identity_path, identity)
    return connection


def _validate_launch(launch):
    connection = launch.get("official_provider", {})
    if connection.get("host") != launch["host"] or connection.get("endpoint") != ENDPOINT or connection.get("credential_environment") != TOKEN_ENV:
        raise ProviderConfigurationError("Launch lacks the explicit official provider configuration")
    names, command = _names(connection.get("tools")), launch["command"]
    if launch["host"] == "codex":
        actual = [arg for arg in command if "mcp_servers.pixellab." in arg]
        if actual != _codex_settings(names):
            raise ProviderConfigurationError("Provider launch overrides changed")
    elif launch["host"] == "claude":
        config = json.loads(Path(command[command.index("--mcp-config") + 1]).read_bytes())
        if config.get("mcpServers", {}).get("pixellab") != _claude_server():
            raise ProviderConfigurationError("Provider launch registration changed")
    else:
        raise ProviderConfigurationError("Unsupported native host")


def _check_secret_files(root, token):
    """Fail before publication if an unexpected host output disclosed the credential."""
    encoded = token.encode()
    for path in Path(root).rglob("*"):
        if path.is_file() and encoded in path.read_bytes():
            raise ProviderConfigurationError("Credential detected in trial files; keep this attempt private")


def run(destination: Path, *, timeout: float | None = None, home: Path | None = None) -> dict:
    """Use the existing recorder/retention route with a process-local credential."""
    destination = Path(destination).resolve()
    launch = json.loads((destination / "launch.json").read_bytes())
    _validate_launch(launch)
    access = credential(launch["host"], home=home)
    _check_secret_files(destination, access.token)
    env = {key: value for key, value in os.environ.items()
           if not any(word in key.upper() for word in ("PIXELLAB", "PIXEL_LAB", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"))}
    env.pop("PYTHONPATH", None)
    env.update(PYTHONDONTWRITEBYTECODE="1", **{TOKEN_ENV: access.token})
    removed_history_override = False
    if launch["host"] == "claude" and "--no-session-persistence" not in launch["command"]:
        removed_history_override = env.pop("CLAUDE_CODE_SKIP_PROMPT_HISTORY", None) is not None
    overrides = {"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"} if launch["host"] == "claude" else {}
    env.update(overrides)
    write_json(destination / "execution-environment.json", {
        "scope": "Evaluation subprocess only; no persistent host configuration changed",
        "overrides": overrides, "removed_history_override": removed_history_override,
        "provider": {"endpoint": ENDPOINT, "credential_environment": TOKEN_ENV, "credential_retained": False},
        "limit": "Native tools receive this process environment; arbitrary shell access is not credential isolation."})
    (destination / "native_provider.py.txt").write_bytes(Path(__file__).read_bytes())
    returncode, elapsed, events, continuation = execute(destination, launch, env, timeout)
    if launch["host"] == "codex":
        retain_journals(destination, events)
        continuation = codex_journals(destination, continuation)
        atomic_json(destination / "continuation.json", continuation)
    _check_secret_files(destination, access.token)
    _check_secret_files(Path(launch["cwd"]), access.token)
    output = (destination / "stdout.jsonl").read_text(encoding="utf-8", errors="replace")
    record = {"host": launch["host"], "case": launch["case"], "returncode": returncode,
              "execution_status": outcome(returncode, continuation["interruption_reason"] == "timeout", output),
              "elapsed_seconds": elapsed, "behavioral_verdict": "ungraded",
              "continuation": {"path": "continuation.json", "sha256": sha(destination / "continuation.json"),
                               "interruption_reason": continuation["interruption_reason"]},
              "artifacts": inventory(Path(launch["cwd"]), ("pixl-kit", "__pycache__")),
              "recorded_files": inventory(destination, ("project", "input-project", "record.json")),
              "credential_scan": "Exact credential absent from retained attempt and consumer files"}
    write_json(destination / "record.json", record)
    return record


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class ReadOnlyMCP:
    """Small bounded transport for discovery/balance; never accepts a paid tool."""

    def __init__(self, access: Credential):
        self.access, self.session, self.protocol = access, None, "2025-03-26"
        self.opener = urllib.request.build_opener(_NoRedirect())

    def request(self, method, params=None, ident=None):
        if method not in {"initialize", "notifications/initialized", "tools/list", "tools/call"} or (
            method == "tools/call" and params != {"name": "get_balance", "arguments": {}}
        ):
            raise ProviderConfigurationError("Read-only probe method is not allowed")
        payload = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        if ident is not None:
            payload["id"] = ident
        headers = {"Authorization": "Bearer " + self.access.token, "Content-Type": "application/json",
                   "Accept": "application/json, text/event-stream", "MCP-Protocol-Version": self.protocol}
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        request = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(), headers=headers, method="POST")
        try:
            with self.opener.open(request, timeout=45) as response:
                raw = response.read(MAX_RESPONSE + 1)
                self.session = response.headers.get("Mcp-Session-Id", self.session)
                content_type = response.headers.get("Content-Type", "")
        except urllib.error.HTTPError as error:
            raise ProviderConfigurationError(f"Official MCP HTTP {error.code}") from None
        except (OSError, TimeoutError):
            raise ProviderConfigurationError("Official MCP transport failed") from None
        if len(raw) > MAX_RESPONSE:
            raise ProviderConfigurationError("Official MCP response exceeded the probe bound")
        if self.access.token.encode() in raw:
            raise ProviderConfigurationError("Official MCP unexpectedly returned a credential")
        if ident is None and not raw:
            return {"notification": "accepted"}
        try:
            if "text/event-stream" in content_type:
                values = [json.loads(line[5:].strip()) for line in raw.decode().splitlines() if line.startswith("data:")]
                result = next(value for value in values if value.get("id") == ident)
            else:
                result = json.loads(raw)
            if result.get("id") != ident or "result" not in result or "error" in result:
                raise ValueError
        except (ValueError, StopIteration, UnicodeError, AttributeError):
            raise ProviderConfigurationError("Official MCP returned an invalid or failed RPC response") from None
        return result


def probe(destination: Path, host: str, *, home: Path | None = None) -> dict:
    """Retain live discovery and balance only, independently of model qualification."""
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=False)
    receipt = {"host": host, "endpoint": ENDPOINT, "started_at": now(), "status": "incomplete",
               "paid_calls": 0, "native_host_execution": False, "responses": []}
    try:
        client = ReadOnlyMCP(credential(host, home=home))

        def save(name, method, params=None, ident=None):
            response = client.request(method, params, ident)
            write_json(destination / name, response)
            receipt["responses"].append({"method": method, "observed_at": now(), **reference(destination / name)})
            return response

        initial = save("initialize.json", "initialize", {"protocolVersion": client.protocol, "capabilities": {},
                       "clientInfo": {"name": "pixl-native-readonly-probe", "version": "1"}}, 1)
        client.protocol = initial["result"]["protocolVersion"]
        save("initialized.json", "notifications/initialized")
        cursor, names = None, []
        for page in range(16):
            result = save(f"tools-{page + 1:02}.json", "tools/list", {"cursor": cursor} if cursor else {}, page + 2)
            names.extend(item["name"] for item in result["result"]["tools"])
            cursor = result["result"].get("nextCursor")
            if not cursor:
                break
        if cursor:
            raise ProviderConfigurationError("Official tool inventory exceeded the probe bound")
        if "get_balance" not in names:
            raise ProviderConfigurationError("Official get_balance tool was not advertised")
        balance = save("balance.json", "tools/call", {"name": "get_balance", "arguments": {}}, 100)
        if balance["result"].get("isError"):
            raise ProviderConfigurationError("Official get_balance returned an error")
        receipt.update(status="passed", tool_count=len(names), tool_names=names,
                       authentication="Authenticated read-only tools/list and get_balance returned successfully")
    except ProviderConfigurationError as error:
        receipt.update(status="failed", error=str(error))
    finally:
        receipt["finished_at"] = now()
        write_json(destination / "receipt.json", receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    configure_parser = sub.add_parser("configure")
    configure_parser.add_argument("destination", type=Path)
    configure_parser.add_argument("--tool", action="append")
    run_parser = sub.add_parser("run")
    run_parser.add_argument("destination", type=Path)
    run_parser.add_argument("--timeout", type=float)
    probe_parser = sub.add_parser("probe")
    probe_parser.add_argument("destination", type=Path)
    probe_parser.add_argument("--host", choices=("codex", "claude"), required=True)
    args = parser.parse_args()
    if args.action == "configure":
        result = configure(args.destination, tools=args.tool)
    elif args.action == "probe":
        result = probe(args.destination, args.host)
    else:
        record = run(args.destination, timeout=args.timeout)
        result = {"attempt": str(args.destination.resolve()), "returncode": record["returncode"]}
    print(json.dumps(result))


if __name__ == "__main__":
    main()
