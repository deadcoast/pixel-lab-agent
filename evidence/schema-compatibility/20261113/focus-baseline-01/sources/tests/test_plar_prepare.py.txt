"""Selected-asset plan preparation against the existing queue consumer fixture."""

import copy
import json
import shutil
import subprocess
import sys
import unittest
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import codec, job_history, jobs, plar, service, store
from pixl.codec import PixlError
from pixl.mcp import dispatch

ROOT = Path(__file__).resolve().parents[1]


def write(root, path, value):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return {"path": path, "sha256": sha256(target.read_bytes()).hexdigest()}


def seed(root):
    shutil.copytree(ROOT / "examples/plar-project", root, dirs_exist_ok=True)
    selected = plar.read(root, asset_id="queue.working")
    arguments = {
        "description": "Four-frame working activity loop with cool blue accent and transparent background; no success symbolism.",
        "width": 64,
        "height": 16,
        "no_background": True,
    }
    request = write(root, "work/arguments.json", arguments)
    criteria = []
    for id_, domain, mode, check in [
        (
            "canvas",
            "mechanical",
            "local",
            "64x16 candidate with four horizontal 16x16 frames; packing remains a sample proposal pending loader verification.",
        ),
        (
            "activity",
            "visual",
            "visual",
            "Readable activity without success symbolism at 1x and 3x nearest on the dark panel.",
        ),
        (
            "integration",
            "engine",
            "live",
            "Verify frame timing, alpha and actual full/compact consumer rendering when a runner is available.",
        ),
    ]:
        criteria.append(
            {
                "id": id_,
                "domain": domain,
                "mode": mode,
                "check": check,
                "basis": "Brief and consumer; proposed packing remains scoped to this candidate.",
                "scope": "This working-loop candidate",
                "sources": [{"path": "BRIEF.md", "locator": "Asset brief"}],
            }
        )
    plan = {
        "version": 1,
        "scope": "Prepare the first working-loop candidate for review; no style adoption or renderer acceptance is claimed.",
        "outputs": [
            {
                "id": "working",
                "name": "Working loop",
                "kind": "animation",
                "contract": {
                    "size": [64, 16],
                    "palette": [],
                    "view": "ui",
                    "sampling": "nearest",
                    "alpha": "full",
                    "intent": "Four frames, 100 ms; cool blue accent, transparent background, activity distinct from success.",
                },
                "criteria": criteria,
            }
        ],
    }
    packet = {
        "version": 1,
        "requirements_hash": selected["requirements_hash"],
        "sources": [
            {"path": s["path"], "sha256": s["sha256"], "role": "consumer requirement"}
            for s in selected["sources"]
        ],
        "request": {
            **request,
            "kind": "provider_arguments",
            "tool": "create_image_pro_flash",
        },
        "criteria": write(root, "work/criteria.json", plan),
        "choices": [],
    }
    write(root, "work/request-review.json", packet)
    connection = {
        "provider": "pixellab",
        "schema": {
            "type": "object",
            "properties": {
                "description": {"type": "string"},
                "width": {
                    "type": "integer",
                    "minimum": 16,
                    "maximum": 256,
                    "multipleOf": 4,
                },
                "height": {
                    "type": "integer",
                    "minimum": 16,
                    "maximum": 256,
                    "multipleOf": 4,
                },
                "no_background": {"type": "boolean"},
            },
            "required": ["description", "width", "height", "no_background"],
            "additionalProperties": False,
        },
        "discovery": {
            "source": "Controlled test connection with documented PixelLab argument fields",
            "observed_at": datetime.now(UTC).isoformat(),
            "evidence": {"fixture": True},
        },
        "authorization": {
            "scope": "Local request-preparation regression only",
            "evidence": {"fixture": True},
        },
    }
    write(root, "work/connection.json", connection)
    args = {
        "asset_id": "queue.working",
        "requirements_hash": selected["requirements_hash"],
        "packet": "work/request-review.json",
        "connection": connection,
    }
    return args, packet, plan, arguments


class PLARPrepareTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "consumer"
        self.args, self.packet, self.plan, self.arguments = seed(self.root)

    def prepare(self):
        return service.call("pixl_plar_prepare", self.args, self.root)

    def files(self):
        return {
            p.relative_to(self.root).as_posix(): p.read_bytes()
            for p in self.root.rglob("*")
            if p.is_file()
        }

    def revise(self):
        self.packet["criteria"] = write(self.root, "work/criteria.json", self.plan)
        write(self.root, "work/request-review.json", self.packet)

    def test_reviewed_plan_to_exact_dispatch_without_acceptance_or_schema_defaults(
        self,
    ):
        result = self.prepare()
        self.assertFalse(result["already_prepared"])
        self.assertFalse(result["remote_executed"])
        folder = self.root / result["store"]
        doc = store.load(folder)
        self.assertFalse(any(r.kind in {"V", "D"} for r in doc.records.values()))
        self.assertEqual(doc.records["task"].fields["ca"], [])
        self.assertEqual(doc.records["task"].fields["ph"], codec.Symbol("sample"))
        for criterion in self.plan["outputs"][0]["criteria"]:
            record = doc.records["criterion.working." + criterion["id"]]
            self.assertEqual(record.fields["ck"], criterion["check"])
            self.assertEqual(record.fields["md"], codec.Symbol(criterion["mode"]))
        dispatched = jobs.dispatch(folder, result["hash"], "first_request", self.root)
        self.assertEqual(dispatched["dispatch_request"]["arguments"], self.arguments)
        self.assertEqual(
            dispatched["dispatch_request"]["schema"], self.args["connection"]["schema"]
        )
        self.assertEqual(dispatched["job"]["state"], "unknown")
        self.assertFalse((self.root / "assets/working.png").exists())

    def test_repeated_preparation_after_dispatch_recovers_without_new_job(self):
        result = self.prepare()
        jobs.dispatch(
            self.root / result["store"], result["hash"], "first_request", self.root
        )
        before = self.files()
        resumed = self.prepare()
        self.assertTrue(resumed["already_prepared"])
        self.assertEqual(resumed["job"]["state"], "unknown")
        self.assertEqual(resumed["job"]["next_action"], "reconcile")
        self.assertEqual(before, self.files())

    def test_queue_progress_and_relocation_preserve_the_prepared_identity(self):
        result = self.prepare()
        document = json.loads((self.root / "plar.txt").read_text(encoding="utf-8"))
        document["assets"][0].update(
            status="in_progress",
            next="Dispatch the prepared request",
            production={
                "store": result["store"],
                "task": "task",
                "output": "output.working",
            },
        )
        plar.save(self.root, document, plar.read(self.root)["hash"])
        self.assertEqual(self.prepare()["hash"], result["hash"])
        moved = self.root.parent / "moved"
        shutil.copytree(self.root, moved)
        self.assertEqual(
            service.call("pixl_plar_prepare", self.args, moved)["hash"], result["hash"]
        )

    def test_stale_selection_and_packet_bytes_fail_before_state(self):
        before = self.files()
        self.args["requirements_hash"] = "0" * 64
        with self.assertRaisesRegex(PixlError, "requirements changed"):
            self.prepare()
        self.assertEqual(before, self.files())
        self.args["requirements_hash"] = self.packet["requirements_hash"]
        (self.root / "work/arguments.json").write_text("{}", encoding="utf-8")
        before = self.files()
        with self.assertRaisesRegex(PixlError, "changed artifact"):
            self.prepare()
        self.assertEqual(before, self.files())

    def test_source_drift_is_not_blessed_by_a_fresh_requirements_hash(self):
        (self.root / "src/queue.ts").write_text("changed backend", encoding="utf-8")
        self.args["requirements_hash"] = plar.read(self.root, asset_id="queue.working")[
            "requirements_hash"
        ]
        before = self.files()
        with self.assertRaisesRegex(PixlError, "sources are changed"):
            self.prepare()
        self.assertEqual(before, self.files())

    def test_schema_or_secret_failure_does_not_create_a_store(self):
        self.args["connection"]["schema"]["properties"]["width"]["maximum"] = 32
        with self.assertRaises(PixlError):
            self.prepare()
        self.assertFalse((self.root / ".pixl/assets").exists())
        self.args["connection"]["schema"]["properties"]["width"]["maximum"] = 256
        self.args["connection"]["authorization"]["evidence"] = {
            "Authorization": "Bearer fixture-secret"
        }
        with self.assertRaises(PixlError):
            self.prepare()
        self.assertFalse((self.root / ".pixl/assets").exists())

    def test_invalid_criteria_do_not_pin_an_unusable_bootstrap(self):
        self.plan["outputs"][0]["criteria"][1]["mode"] = "local"
        self.revise()
        with self.assertRaises(PixlError):
            self.prepare()
        self.assertFalse(list(self.root.rglob("state.px")))
        self.assertFalse(list(self.root.rglob("plans/*.json")))
        self.plan["outputs"][0]["criteria"][1]["mode"] = "visual"
        self.revise()
        self.assertEqual(self.prepare()["job"]["state"], "prepared")

    def test_interrupted_intent_publication_resumes_the_saved_plan(self):
        with (
            patch(
                "pixl.plar_prepare.jobs.prepare",
                side_effect=OSError("simulated storage interruption"),
            ),
            self.assertRaises(OSError),
        ):
            self.prepare()
        state = self.root / ".pixl/assets/queue.working"
        self.assertEqual(store.load(state).revision, 0)
        resumed = self.prepare()
        self.assertEqual(resumed["revision"], 1)
        self.assertEqual(resumed["job"]["state"], "prepared")

    def test_resumption_does_not_adopt_a_different_job_with_the_same_id(self):
        with (
            patch(
                "pixl.plar_prepare.jobs.prepare", side_effect=OSError("interruption")
            ),
            self.assertRaises(OSError),
        ):
            self.prepare()
        folder = self.root / ".pixl/assets/queue.working"
        changed = {**self.arguments, "description": "Different unreviewed intent"}
        jobs.prepare(
            folder,
            codec.digest(store.load(folder)),
            "first_request",
            "task",
            ["output.working"],
            tool="create_image_pro_flash",
            arguments=changed,
            root=self.root,
            **self.args["connection"],
        )
        before = self.files()
        with self.assertRaisesRegex(PixlError, "differs from the reviewed intent"):
            self.prepare()
        self.assertEqual(self.files(), before)

    def test_resumption_requires_the_same_complete_output_context(self):
        second = copy.deepcopy(self.plan["outputs"][0])
        second["id"] = "alternate"
        self.plan["outputs"].append(second)
        self.revise()
        with (
            patch(
                "pixl.plar_prepare.jobs.prepare", side_effect=OSError("interruption")
            ),
            self.assertRaises(OSError),
        ):
            self.prepare()
        folder = self.root / ".pixl/assets/queue.working"
        jobs.prepare(
            folder,
            codec.digest(store.load(folder)),
            "first_request",
            "task",
            ["output.working"],
            tool="create_image_pro_flash",
            arguments=self.arguments,
            root=self.root,
            **self.args["connection"],
        )
        before = self.files()
        with self.assertRaisesRegex(PixlError, "different task/output bindings"):
            self.prepare()
        self.assertEqual(self.files(), before)

    def test_source_update_blocks_dispatch_but_keeps_history_readable(self):
        result = self.prepare()
        folder = self.root / result["store"]
        original = (self.root / "BRIEF.md").read_bytes()
        (self.root / "BRIEF.md").write_text(
            "Changed consumer requirements", encoding="utf-8"
        )
        report = jobs.report(store.load(folder), self.root)
        self.assertEqual(
            report["jobs"][0]["selection_bindings"][0]["status"], "changed"
        )
        self.assertEqual(report["jobs"][0]["next_action"], "resolve_context")
        self.assertEqual(
            (self.root / result["retained_inputs"]["BRIEF.md"]["path"]).read_bytes(),
            original,
        )
        with self.assertRaisesRegex(PixlError, "plar_selection"):
            jobs.dispatch(folder, result["hash"], "first_request", self.root)
        self.assertEqual(store.load(folder).revision, result["revision"])

    def test_generic_publication_also_rechecks_the_live_selection(self):
        result = self.prepare()
        folder = self.root / result["store"]
        current = store.load(folder)
        journal = jobs._get(current, "first_request", self.root)
        event = job_history.append(
            journal, "dispatch", {"fixture": "generic publication path"}
        )
        (self.root / "BRIEF.md").write_text(
            "Changed before generic dispatch", encoding="utf-8"
        )
        candidate = copy.deepcopy(current)
        jobs._project(candidate, folder, self.root, event)
        candidate.revision += 1
        with self.assertRaisesRegex(PixlError, "job_blocked"):
            store.commit(folder, candidate, result["hash"], self.root)
        self.assertEqual(codec.digest(store.load(folder)), result["hash"])

    def test_unknown_submission_remains_reconcilable_after_consumer_change(self):
        result = self.prepare()
        folder = self.root / result["store"]
        dispatched = jobs.dispatch(folder, result["hash"], "first_request", self.root)
        (self.root / "BRIEF.md").write_text(
            "Changed after submission", encoding="utf-8"
        )
        observed = jobs.observe(
            folder,
            dispatched["hash"],
            "first_request",
            "submitted",
            {"fixture": "Actual response placeholder"},
            remote_id="controlled-job",
            root=self.root,
        )
        self.assertEqual(observed["job"]["state"], "submitted")
        self.assertEqual(observed["job"]["selection_bindings"][0]["status"], "changed")
        self.assertEqual(observed["job"]["request"]["arguments"], self.arguments)

    def test_existing_work_is_not_overwritten_by_a_new_contract(self):
        result = self.prepare()
        before = (self.root / result["store"] / "state.px").read_bytes()
        self.plan["scope"] = "A different proposed scope"
        self.revise()
        with self.assertRaises(PixlError):
            self.prepare()
        self.assertEqual(
            (self.root / result["store"] / "state.px").read_bytes(), before
        )

    def test_binary_reference_and_empty_source_prepare_with_exact_byte_bindings(self):
        shutil.copyfile(
            ROOT / "examples/delegation/assets/robot-base.png",
            self.root / "assets/style.png",
        )
        (self.root / "empty.txt").write_bytes(b"")
        document = json.loads((self.root / "plar.txt").read_text(encoding="utf-8"))
        document["sources"].extend(
            [
                {"id": "style", "path": "assets/style.png"},
                {"id": "empty", "path": "empty.txt"},
            ]
        )
        document["assets"][0]["references"] = [
            {
                "source": "style",
                "role": "style",
                "instructions": "Byte-binding fixture; no generated fidelity claim.",
            }
        ]
        document["assets"][0]["requirements"].append(
            {
                "property": "empty_source",
                "value": "binding fixture",
                "authority": "observation",
                "sources": ["empty"],
                "reason": "Empty source remains a valid byte-bound file.",
            }
        )
        plar.save(self.root, document, plar.read(self.root)["hash"])
        selected = plar.read(self.root, asset_id="queue.working")
        self.args["requirements_hash"] = self.packet["requirements_hash"] = selected[
            "requirements_hash"
        ]
        self.packet["sources"] = [
            {"path": r["path"], "sha256": r["sha256"], "role": "test source"}
            for r in selected["sources"]
        ]
        self.revise()
        result = self.prepare()
        doc = store.load(self.root / result["store"])
        bound = {r.fields["ur"]: r for r in doc.records.values() if r.kind == "S"}
        self.assertEqual(
            bound[result["retained_inputs"]["assets/style.png"]["path"]].fields["ln"],
            [],
        )
        self.assertEqual(
            bound[result["retained_inputs"]["empty.txt"]["path"]].fields["ln"], []
        )
        reference = doc.records["reference.0"]
        self.assertEqual(
            reference.fields["dg"],
            sha256((self.root / "assets/style.png").read_bytes()).hexdigest(),
        )
        self.assertIn(codec.Ref("reference.0"), doc.records["task"].fields["ip"])
        self.assertEqual(self.prepare()["hash"], result["hash"])

    def test_multiple_outputs_are_planned_without_fabricated_artifacts(self):
        second = copy.deepcopy(self.plan["outputs"][0])
        second["id"] = "alternate"
        second["name"] = "Alternative candidate"
        self.plan["outputs"].append(second)
        self.revise()
        result = self.prepare()
        self.assertEqual(result["outputs"], ["output.working", "output.alternate"])
        self.assertEqual(
            result["job"]["context"]["outputs"], ["output.alternate", "output.working"]
        )
        doc = store.load(self.root / result["store"])
        self.assertFalse(
            any(r.kind == "X" and "of" in r.fields for r in doc.records.values())
        )

    def test_cli_and_mcp_prepare_the_same_saved_operation(self):
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "pixl",
                "plar",
                "prepare",
                "--root",
                str(self.root),
                "--asset",
                "queue.working",
                "--requirements",
                self.args["requirements_hash"],
                "--packet",
                "work/request-review.json",
                "--connection",
                "work/connection.json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        cli = json.loads(result.stdout)
        response = dispatch(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "pixl_plar_prepare", "arguments": self.args},
            },
            self.root,
        )
        self.assertFalse(response["result"].get("isError", False), response)
        self.assertEqual(response["result"]["structuredContent"]["hash"], cli["hash"])
        tools = dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, self.root)
        declaration = next(
            t for t in tools["result"]["tools"] if t["name"] == "pixl_plar_prepare"
        )
        self.assertFalse(declaration["annotations"]["readOnlyHint"])


if __name__ == "__main__":
    unittest.main()
