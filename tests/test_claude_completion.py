"""Synthetic traces exercise native proof rejection, not Claude qualification."""

from __future__ import annotations

import copy
import unittest

from evaluations.claude_completion import async_completion
from tests.test_grade_domain_consumers import async_fixture


def resumed_fixture():
    stdout, parent, children, child, session = async_fixture()
    send = {"type": "tool_use", "name": "SendMessage", "id": "agent-call", "input": {"to": child}}
    resumed = {"success": True, "resumedAgentId": child, "revivedAgentId": child}
    stdout[0]["message"]["content"] = [send]
    parent[0]["message"]["content"] = [copy.deepcopy(send)]
    stdout[2]["tool_use_result"] = resumed
    parent[1]["toolUseResult"] = copy.deepcopy(resumed)
    # Current Claude counts spawned agents separately from resumed tasks.
    stdout[-1]["subagent_stats"]["completed"] = 0
    return stdout, parent, children[0], child, session


def queued_fixture():
    args = resumed_fixture()
    parent, session = args[1], args[4]
    text = parent.pop()["message"]["content"]
    parent.extend([
        {"type": "queue-operation", "operation": "enqueue", "sessionId": session, "content": text},
        {"type": "attachment", "sessionId": session, "isSidechain": False, "renderedRole": "system", "attachment": {
            "type": "queued_command", "commandMode": "task-notification", "runId": "background-run",
            "origin": {"kind": "task-notification", "producer": "session-task"}, "source_uuid": "command-id",
            "delivery_id": "delivery-id", "prompt": text}},
        {"type": "queue-operation", "operation": "remove", "sessionId": session, "content": text,
         "reason": "absorbed_mid_turn", "commandUuid": "command-id", "deliveryId": "delivery-id"},
    ])
    return args


class ClaudeCompletionTests(unittest.TestCase):
    def test_host_automatic_background_without_requested_flag_qualifies(self):
        stdout, parent, children, child, session = async_fixture()
        del stdout[0]["message"]["content"][0]["input"]["run_in_background"]
        del parent[0]["message"]["content"][0]["input"]["run_in_background"]
        self.assertTrue(async_completion(stdout, parent, children[0], child, session))

    def test_same_child_sendmessage_completion_with_no_spawn_counter_qualifies(self):
        proof = async_completion(*resumed_fixture(), resumed=True)
        self.assertEqual(proof[0]["mechanism"], "bound_same_child_async_completion")
        self.assertEqual(proof[0]["agent_id"], "selected-child")

    def test_queued_system_attachment_requires_actual_enqueue_and_delivery(self):
        self.assertTrue(async_completion(*queued_fixture(), resumed=True))
        for missing in (2, 3, 4):
            args = queued_fixture()
            del args[1][missing]
            with self.subTest(missing=missing):
                self.assertEqual(async_completion(*args, resumed=True), [])
        for field, wrong in (("runId", "other"), ("commandMode", "user"), ("source_uuid", "other"),
                             ("delivery_id", "other"), ("origin", {"kind": "user"})):
            args = queued_fixture()
            args[1][3]["attachment"][field] = wrong
            with self.subTest(field=field):
                self.assertEqual(async_completion(*args, resumed=True), [])

    def test_spawn_completion_cannot_substitute_for_same_child_continuation(self):
        stdout, parent, children, child, session = async_fixture()
        self.assertEqual(async_completion(stdout, parent, children[0], child, session, resumed=True), [])

    def test_resume_acknowledgement_without_complete_bound_delivery_never_qualifies(self):
        for missing in range(6):
            args = resumed_fixture()
            del args[0][missing]
            with self.subTest(stdout_row=missing):
                self.assertEqual(async_completion(*args, resumed=True), [])
        for missing in range(3):
            args = resumed_fixture()
            del args[1][missing]
            with self.subTest(parent_row=missing):
                self.assertEqual(async_completion(*args, resumed=True), [])
        args = resumed_fixture()
        args[2].clear()
        self.assertEqual(async_completion(*args, resumed=True), [])

    def test_wrong_child_session_role_run_and_return_identity_are_rejected(self):
        changes = [(0, 0, "session_id", "other"), (0, 1, "task_id", "other"),
                   (0, 1, "subagent_type", "general-purpose"), (0, 1, "tool_use_id", "other"),
                   (0, 3, "run_id", "other"), (0, 4, "tool_use_id", "other"),
                   (0, 4, "summary", "Invented final text"), (1, 2, "promptSource", "user"),
                   (1, 2, "isSidechain", True), (2, 0, "agentId", "other"), (2, 0, "sessionId", "other")]
        for journal, row, field, value in changes:
            args = resumed_fixture()
            args[journal][row][field] = value
            with self.subTest(journal=journal, row=row, field=field):
                self.assertEqual(async_completion(*args, resumed=True), [])
        for journal, row, key in ((0, 2, "tool_use_result"), (1, 1, "toolUseResult")):
            args = resumed_fixture()
            args[journal][row][key]["resumedAgentId"] = "replacement-child"
            self.assertEqual(async_completion(*args, resumed=True), [])

    def test_parent_prose_duplicate_tags_wrong_event_order_and_failure_are_rejected(self):
        for mode in ("prose", "duplicate", "wrong-result", "order", "wrong-origin", "failed"):
            args = resumed_fixture()
            if mode == "prose":
                args[1][2].update(type="assistant", promptSource="assistant")
            elif mode == "duplicate":
                args[1][2]["message"]["content"] = args[1][2]["message"]["content"].replace("<status>", "<status>completed</status><status>")
            elif mode == "wrong-result":
                args[1][2]["message"]["content"] = args[1][2]["message"]["content"].replace("Bound final child result", "Invented")
            elif mode == "order":
                args[0][3], args[0][4] = args[0][4], args[0][3]
            elif mode == "wrong-origin":
                args[1][2]["origin"]["runId"] = "other"
            else:
                args[0][-1]["subagent_stats"]["failed"] = 1
            with self.subTest(mode=mode):
                self.assertEqual(async_completion(*args, resumed=True), [])


if __name__ == "__main__":
    unittest.main()
