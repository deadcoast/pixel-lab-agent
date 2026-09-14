"""Probe native skills and selected model without sending an inference turn."""

from pathlib import Path
import json
import queue
import subprocess
import threading
import time


HERE = Path(__file__).resolve().parent


def main() -> None:
    diagnostic = json.loads((HERE / "codex-loader-probe.json").read_text())
    executable = (
        "C:/nvm4w/nodejs/node_modules/@openai/codex/node_modules/@openai/"
        "codex-win32-x64/vendor/x86_64-pc-windows-msvc/bin/codex.exe"
    )
    command = [executable, "app-server", "--stdio"]
    for override in diagnostic["overrides"]:
        command += ["-c", override]
    process = subprocess.Popen(
        command, cwd=diagnostic["project"], stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        encoding="utf-8", creationflags=subprocess.CREATE_NO_WINDOW,
    )
    output: queue.Queue[str] = queue.Queue()
    diagnostics: list[str] = []
    notifications: list[str] = []
    results = {}
    assert process.stdout is not None and process.stderr is not None
    assert process.stdin is not None
    threading.Thread(target=lambda: [output.put(line) for line in process.stdout], daemon=True).start()
    threading.Thread(target=lambda: diagnostics.extend(process.stderr.readlines()), daemon=True).start()

    def request(identifier: int, method: str, params: dict) -> dict:
        process.stdin.write(json.dumps({"id": identifier, "method": method, "params": params}) + "\n")
        process.stdin.flush()
        deadline = time.monotonic() + 35
        while time.monotonic() < deadline:
            item = json.loads(output.get(timeout=max(0.01, deadline - time.monotonic())))
            if item.get("id") == identifier:
                return item
            notifications.append(item.get("method", "other_response"))
        raise TimeoutError(method)

    try:
        results["initialize"] = request(1, "initialize", {
            "clientInfo": {"name": "pixl_discovery", "version": "1.0.0"},
            "capabilities": {"experimentalApi": True},
        })
        process.stdin.write(json.dumps({"method": "initialized"}) + "\n")
        process.stdin.flush()
        results["skills_list"] = request(2, "skills/list", {
            "cwds": [diagnostic["project"]], "forceReload": True,
        })
        results["thread_start"] = request(3, "thread/start", {
            "cwd": diagnostic["project"], "model": "gpt-6-astra",
            "ephemeral": True, "approvalPolicy": "never", "sandbox": "read-only",
            "config": {"model_reasoning_effort": "xhigh"},
        })
    except Exception as error:
        results["probe_error"] = {"type": type(error).__name__, "message": str(error)}
    finally:
        process.terminate()
        process.wait(timeout=10)
    skill_result = results.get("skills_list", {}).get("result", {})
    entries = skill_result.get("data", [])
    skill_summary = []
    for entry in entries:
        skill_summary.append({
            "cwd": entry.get("cwd"), "errors": entry.get("errors"),
            "skills": [
                {key: skill.get(key) for key in ("name", "path", "scope", "enabled")}
                for skill in entry.get("skills", [])
            ],
        })
    thread = results.get("thread_start", {}).get("result", {})
    record = {
        "purpose": "Native app-server discovery and thread configuration; no turn/start sent.",
        "initialize": results.get("initialize"),
        "skills_list": skill_summary,
        "thread_start": {key: thread.get(key) for key in (
            "model", "modelProvider", "reasoningEffort", "cwd", "approvalPolicy",
            "instructionSources", "sandbox",
        )},
        "thread_turn_count": len(thread.get("thread", {}).get("turns", [])),
        "errors": {key: result for key, result in results.items() if isinstance(result, dict) and "error" in result},
        "probe_error": results.get("probe_error"),
        "notifications": notifications,
        "stderr": "".join(diagnostics),
        "model_inference_executed": False,
    }
    (HERE / "codex-appserver-probe.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
