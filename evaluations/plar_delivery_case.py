"""Cold retrieval/review and source-consumer integration of the selected generation."""

import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngInfo

from evaluations.host_trials import write_json
from evaluations.plar_delivery_fixture import SCHEMAS

GUIDANCE = """This is an isolated native continuation evaluation. Work only in this consumer.
Use the packaged PLAR/PIXL skills under .agents/skills/pixl-kit/skills/ and the current
assignment in STAGE.md; previous OWNER.md describes the completed request stage.
The same controlled pixellab-test connection now supplies retrieval of retained work;
its images and observations are evaluator fixtures, not upstream PixelLab generation.
Download only its returned loopback result; do not manufacture a replacement image.
No new generation, credentials, package installs or host settings changes are assigned.
The caller owns independent comparison and final consumption. The selected Python is
supplied below; Node is available for the actual consumer-module integration check.
"""
PROMPT = """You are the calling agent continuing STAGE.md. Delegate the retained selected
generation to PIXL using the installed workflow. Recover its actual current provider
status, retrieve and inspect the existing result, retain justified reviews and integrate
the exact candidate into the assigned source consumers. Independently open the delivered
artifact and verify the retained contract/state and integration evidence. Save
DELIVERY-RESULT.json with exact paths/hashes, reviews, original/current job and task
identity, fresh production continuation and remaining family/renderer obligations.
"""
INTEGRATION = """// Execute the actual source consumers; this is not a renderer.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { stateAfter } from './src/queue.ts';
import { statusCell, compactStatus, display } from './src/queue-view.ts';
const expected = process.argv[2];
assert.ok(expected, 'Pass the selected PLAR delivery path');
const state = stateAfter('ok');
assert.equal(state, 'succeeded');
const consumers = [statusCell(state), compactStatus(state)];
for (const consumer of consumers) {
  assert.equal(consumer.path, expected);
  assert.equal(consumer.frames, 1);
}
const data = readFileSync(new URL(expected, import.meta.url));
assert.equal(data.subarray(0,8).toString('hex'), '89504e470d0a1a0a');
assert.deepEqual([data.readUInt32BE(16), data.readUInt32BE(20)], display.cell);
assert.equal(display.filter, 'nearest');
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
console.log(JSON.stringify({state, consumers, display, file: expected,
  sha256: hash(data), sources: Object.fromEntries(['src/queue.ts','src/queue-view.ts'].map(
    p => [p, hash(readFileSync(new URL(p, import.meta.url)))])),
  scope: 'Executed backend-to-view mapping and actual file/header lookup; no renderer, alpha compositing or artistic acceptance.'}, null, 2));
"""


def fixture_png(path):
    image = Image.new("RGBA", (16, 16))
    draw = ImageDraw.Draw(image)
    draw.line([(3, 8), (6, 11), (13, 4)], fill="#70b9ed", width=2)
    metadata = PngInfo()
    metadata.add_text(
        "purpose", "Controlled retrieval fixture, not PixelLab-generated art"
    )
    image.save(path, pnginfo=metadata)


def setup(project, destination, python, resume):
    if resume is None:
        raise ValueError("Delivery requires an existing submitted request attempt")
    state = json.loads((resume / "provider-state.json").read_bytes())
    pending = [j for j in state["jobs"] if j["status"] in ("queued", "processing")]
    if len(pending) != 1:
        raise ValueError("Expected one selected pending request")
    write_json(destination / "provider-state.json", state)
    fixture_png(destination / "provider-result.png")
    write_json(project / "retrieval-provider-schemas.json", SCHEMAS)
    (project / "verify-integration.mjs").write_text(INTEGRATION, encoding="utf-8")
    (project / "STAGE.md").write_text(
        """# Continue the existing Ready generation through delivery
The reviewed current queue.ready generation was submitted in the retained request
stage. Continue that same provider job and saved plan through actual retrieval, local
candidate import, mechanical/visual review and justified task finalization. Deliver the
reviewed PNG to the current PLAR destination and verify both real source consumers via
node verify-integration.mjs PATH (PATH is the selected PLAR delivery path).
The existing renderer obligations and family/style adoption are not silently completed
by this bounded Ready delivery. No runnable graphical renderer is supplied. Preserve
old source, plan, job, rejected-candidate and review history and all unrelated asset rows.
The controlled connection now exposes get_image and serves an actual synthetic PNG;
retain its identity/provenance and do not create another request. Inspect the downloaded
artifact itself. If a required candidate check fails, retain that result and report the
remaining correction instead of weakening criteria to pass. No upstream image or live
renderer acceptance is claimed by this assignment. STAGE.md extends the earlier OWNER
request-stage scope without rewriting the request's original bound source bytes.
""",
        encoding="utf-8",
    )
    for name in (
        "plar_delivery_fixture.py",
        "plar_request_fixture.py",
        "pixellab_mcp_fixture.py",
    ):
        shutil.copyfile(Path(__file__).parent / name, destination / name)
    return {
        "command": str(python),
        "args": [
            str(destination / "plar_delivery_fixture.py"),
            "--folder",
            str(destination),
        ],
    }
