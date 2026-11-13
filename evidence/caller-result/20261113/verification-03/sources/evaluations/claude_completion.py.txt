"""Bind Claude task completion to native events, persisted journals and child text."""

from __future__ import annotations

import re


def blocks(row):
    message = row.get("message", {})
    content = message.get("content", []) if isinstance(message, dict) else []
    return [block for block in content if isinstance(block, dict)] if isinstance(content, list) else []


def mapping(row, key):
    value = row.get(key)
    return value if isinstance(value, dict) else {}


def tag(text, name):
    matches = re.findall(r"<" + name + r">(.*?)</" + name + r">", text, re.DOTALL)
    return matches[0] if len(matches) == 1 else None


def event(row):
    return {key: row.get(key) for key in ("file", "line", "type", "subtype")}


def async_completion(stdout, parent, child, selected, session, *, resumed=False):
    """Require actual delivery; an async launch or a resumed-agent ID is not completion.

    For a continuation, callers must supply only the appended parent/child rows.
    A host may automatically background Agent even without run_in_background.
    SendMessage can complete a resumed task while subagent_stats.completed is 0.
    The bound task events and exact delivered child text establish either case.
    """
    if not selected or not session:
        return []
    finals = [row for row in child if row.get("type") == "assistant" and row.get("agentId") == selected
              and row.get("sessionId") == session and row.get("isSidechain") is True
              and mapping(row, "message").get("stop_reason") == "end_turn"]
    if not finals:
        return []
    final = finals[-1]
    final_text = "\n".join(b["text"] for b in blocks(final) if b.get("type") == "text")
    if not final_text:
        return []

    def successful_result(row, call_id):
        return any(b.get("type") == "tool_result" and b.get("tool_use_id") == call_id
                   and not b.get("is_error", False) for b in blocks(row))

    def launch_matches(value):
        if resumed:
            return value.get("success") is True and value.get("resumedAgentId") == selected
        return value.get("status") == "async_launched" and value.get("isAsync") is True and value.get("agentId") == selected

    for index, call_row in enumerate(stdout):
        if call_row.get("type") != "assistant" or call_row.get("session_id") != session:
            continue
        for call in blocks(call_row):
            if call.get("type") != "tool_use" or not call.get("id"):
                continue
            args = mapping(call, "input")
            if resumed:
                eligible = call.get("name") == "SendMessage" and args.get("to", args.get("recipient")) == selected
            else:
                eligible = call.get("name") == "Agent" and args.get("subagent_type") == "pixl:pixl"
            if not eligible:
                continue
            call_id = call["id"]
            later = stdout[index + 1:]
            launches = [row for row in later if row.get("type") == "user" and row.get("session_id") == session
                        and launch_matches(mapping(row, "tool_use_result")) and successful_result(row, call_id)]
            starts = [row for row in later if row.get("type") == "system" and row.get("subtype") == "task_started"
                      and row.get("session_id") == session and row.get("task_id") == selected
                      and row.get("tool_use_id") == call_id and row.get("subagent_type") == "pixl:pixl"
                      and row.get("is_backgrounded") is True and row.get("run_id")]
            if not launches or not starts:
                continue
            for start in starts:
                run_id = start["run_id"]
                updates = [row for row in later if row.get("type") == "system" and row.get("subtype") == "task_updated"
                           and row.get("session_id") == session and row.get("task_id") == selected
                           and row.get("run_id") == run_id and mapping(row, "patch").get("status") == "completed"]
                notices = [row for row in later if row.get("type") == "system" and row.get("subtype") == "task_notification"
                           and row.get("session_id") == session and row.get("task_id") == selected
                           and row.get("tool_use_id") == call_id and row.get("run_id") == run_id
                           and row.get("status") == "completed" and row.get("summary") == final_text]
                parent_calls = [row for row in parent if row.get("type") == "assistant"
                                and row.get("sessionId") == session and call in blocks(row)]
                parent_launches = [row for row in parent if row.get("type") == "user" and row.get("sessionId") == session
                                   and launch_matches(mapping(row, "toolUseResult")) and successful_result(row, call_id)]
                parent_notices = []
                for row in parent:
                    text = mapping(row, "message").get("content")
                    if (row.get("type") == "user" and row.get("sessionId") == session and row.get("isSidechain") is False
                            and row.get("promptSource") == "system" and row.get("turnOrigin") == "task_notification"
                            and row.get("origin") == {"kind": "task-notification", "producer": "session-task", "runId": run_id}
                            and isinstance(text, str) and text.startswith("<task-notification>\n") and text.endswith("</task-notification>")
                            and tag(text, "task-id") == selected and tag(text, "tool-use-id") == call_id
                            and tag(text, "status") == "completed" and tag(text, "result") == final_text):
                        parent_notices.append(row)
                    attachment = mapping(row, "attachment")
                    text = attachment.get("prompt")
                    if (row.get("type") == "attachment" and row.get("sessionId") == session
                            and row.get("isSidechain") is False and row.get("renderedRole") == "system"
                            and attachment.get("type") == "queued_command" and attachment.get("commandMode") == "task-notification"
                            and attachment.get("origin") == {"kind": "task-notification", "producer": "session-task"}
                            and attachment.get("runId") == run_id and attachment.get("source_uuid") and attachment.get("delivery_id")
                            and isinstance(text, str) and text.startswith("<task-notification>\n") and text.endswith("</task-notification>")
                            and tag(text, "task-id") == selected and tag(text, "tool-use-id") == call_id
                            and tag(text, "status") == "completed" and tag(text, "result") == final_text):
                        enqueued = [r for r in parent[:parent.index(row)] if r.get("type") == "queue-operation"
                                    and r.get("operation") == "enqueue" and r.get("sessionId") == session and r.get("content") == text]
                        delivered = [r for r in parent[parent.index(row) + 1:] if r.get("type") == "queue-operation"
                                     and r.get("operation") == "remove" and r.get("sessionId") == session and r.get("content") == text
                                     and r.get("reason") == "absorbed_mid_turn" and r.get("commandUuid") == attachment["source_uuid"]
                                     and r.get("deliveryId") == attachment["delivery_id"]]
                        if enqueued and delivered:
                            parent_notices.append(row)
                terminals = [row for row in later if row.get("type") == "result" and row.get("subtype") == "success"
                             and row.get("session_id") == session and row.get("terminal_reason") == "completed"
                             and row.get("is_error") is False and mapping(row, "subagent_stats").get("failed", 0) == 0]
                if not all((updates, notices, parent_calls, parent_launches, parent_notices, terminals)):
                    continue
                if not (stdout.index(start) < stdout.index(updates[0]) < stdout.index(notices[0]) < stdout.index(terminals[-1])
                        and stdout.index(launches[0]) < stdout.index(updates[0])
                        and parent.index(parent_calls[0]) < parent.index(parent_launches[0]) < parent.index(parent_notices[0])):
                    continue
                return [{"mechanism": "bound_same_child_async_completion" if resumed else "bound_async_host_completion",
                         "agent_id": selected, "session_id": session, "call_id": call_id, "run_id": run_id,
                         "events": [event(row) for row in (call_row, launches[0], start, updates[0], notices[0], final,
                                                          parent_calls[0], parent_launches[0], parent_notices[0], terminals[-1])]}]
    return []
