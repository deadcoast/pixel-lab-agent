# Production handoff: Working representative sample

This is the stopping point for the requirements assignment. `plar.txt` records three missing assets shared by both status consumers. No art has been generated, no provider has been called, and no candidate or integration has been accepted.

## Resume context

- Consumer root: `C:\Users\ryanf\.codex\visualizations\2026\11\05\01a1ad70-8a80-7762-a210-de5dbde57aba\plar-forward-20261107`
- Requirements: the consumer root's `plar.txt`; selected asset ID: `queue.working`.
- PLAR skill: `C:\Users\ryanf\github\gh\pixel-lab-agent\plugins\pixl\skills\plar\SKILL.md`.
- Production skill: `C:\Users\ryanf\github\gh\pixel-lab-agent\plugins\pixl\skills\pixl\SKILL.md`; follow its PX2 intake/sample and provider workflow when production is assigned.
- Current authorization covers source analysis and this production handoff. It does not dispatch a provider request. The next production assignment should establish its authorization scope before submission.
- Development runtime: `C:\Users\ryanf\github\gh\pixel-lab-agent\.venv\Scripts\python.exe`; run from `C:\Users\ryanf\github\gh\pixel-lab-agent` using `-B -m pixl plar` and an explicit consumer `--root`. The runtime is not bundled yet. Do not place project artifacts in the skill checkout.

Read the queue and full selected row, checking source bindings before using its claims:

```powershell
& 'C:\Users\ryanf\github\gh\pixel-lab-agent\.venv\Scripts\python.exe' -B -m pixl plar read --root 'C:\Users\ryanf\.codex\visualizations\2026\11\05\01a1ad70-8a80-7762-a210-de5dbde57aba\plar-forward-20261107' --asset queue.working
```

## Source findings and allocation

| Role | Source evidence | Required local artifact |
| --- | --- | --- |
| Start / idle | `statusVisuals.idle`, `assets/start.svg`; brief says preserve it | Existing vector, no new pixel-art row |
| Working / running | `stateAfter("started")`; `statusVisuals.running` | `assets/working.png`, four horizontal frames |
| Ready / succeeded | `stateAfter("ok")`; `statusVisuals.succeeded` | `assets/ready.png`, static |
| Retry / failed | `stateAfter("error")`; `statusVisuals.failed` | `assets/retry.png`, static, noncolor distinction |
| Account badge | `accountBadge(registry, account)` | Server supplied; explicitly outside this request |

Both `statusCell` and `compactStatus` return the same `statusVisuals[state]` object. Each visual role needs one shared asset, not separate compact and regular artwork. The state module has no additional image needs. Text labels and the solid panel background do not call for new raster art.

All four original project files were read: `BRIEF.md`, both TypeScript modules, and the Start SVG definition. The three PNGs are missing. The SVG definition is a 16x16 view box with a triangular path filled `#70b9ed`; this was source inspection, not rendered art review. There is no application entry point, package manifest, image loader, sprite cropper or running UI in this checkout. Scope is the complete supplied project snapshot, not an unseen host application or server.

## Selected next asset and authority

Use Working as the proposed representative sample. It exercises small-scale readability, animation continuity and the distinction between activity and success. Ready and Retry wait for the reviewed style baseline. This choice of sample and dependency order is a proposal; the brief's requirement is to propose a representative sample before expanding the family.

| Property | Value | Authority and exact source |
| --- | --- | --- |
| Visual treatment | Coherent pixel art; readable silhouettes; existing cool blue accent | Requirement: `BRIEF.md:3` |
| Cell | 16x16 logical pixels | Requirement: `BRIEF.md:3`; observed agreement in `display.cell`, `src/queue-view.ts:8` |
| Working animation | Four horizontal frames, 100 ms each | Requirement: `BRIEF.md:3`; observed `statusVisuals.running.frames` and `display.frameMs`, `src/queue-view.ts:4,8` |
| Sheet packing | 64x16 PNG, tightly packed 16x16 frames, no padding | Proposed interpretation of the frame/cell contract; no loader is available to verify crop behavior |
| Alpha and palette | Transparent background; no fixed palette required | Requirement: `BRIEF.md:3`; partial alpha is not prohibited |
| Accent color | Existing SVG uses `#70b9ed` | Observation: `assets/start.svg:1`; color context, not exclusive palette membership |
| Review setting | 1x and 3x nearest on `#172336` | Requirement: `BRIEF.md:3`; actual configured panel color in `src/queue-view.ts:8` |
| Working semantics | Activity must not look like success | Requirement: `BRIEF.md:3` |
| Style motif | Four-step open orbit with a moving dash | Proposed experiment only; no approved style reference exists (`BRIEF.md:5`) |
| Retry family constraint | Distinguishable without color alone | Requirement: `BRIEF.md:3`; retain for later comparison |
| Delivery and consumers | `assets/working.png`; both status selectors for `running` | Requirement to use existing paths: `BRIEF.md:5`; bindings: `src/queue-view.ts:4,9-10`, `src/queue.ts:2-4` |

No exact palette, hue threshold, binary-alpha-only rule, component count, stroke width or motif is an adopted rejection rule. The current source supplies no pivot, renderer import setting or atlas margin contract. Keep those unknown where relevant instead of inventing engine behavior.

## Focused production task

1. Read the selected row and source bindings. In a production assignment, initialize or resume consumer-owned PX2 state and save choices, planned output and criteria before making or judging a candidate. Discover the actual official PixelLab operation schema; confirm how its supported canvas and animation output can satisfy the selected contract. No provider operation or reliability is asserted by this handoff.
2. Propose one Working sample using the explicit requirements above. A possible creative brief follows; the motif and zero-padding packing remain proposals at the point of use:

   > Create a readable pixel-art Working/activity indicator for a 16x16 status cell on the dark #172336 panel. Use transparent background and the existing UI's cool blue accent, with #70b9ed supplied as color context; no fixed palette is required. Produce four horizontal frames played at 100 ms each. The loop must communicate ongoing work without looking like success. Proposed experiment: a four-step open orbit with a moving dash. Proposed package: four tightly packed 16x16 frames in a 64x16 PNG. Neither the motif nor the zero-padding convention has been approved; retain the proposal label in its review. Inspect the result at 1x and 3x nearest on the panel before extending the style to Ready and Retry.

3. Retain candidates, requests and review evidence under the consumer project, using distinct candidate paths. The final destination is `assets/working.png`. Do not overwrite the existing Start SVG. Link real PX2 store/task/output IDs into PLAR only after they exist.
4. Check valid PNG encoding, transparency, actual dimensions and frame layout. Inspect each frame at 16x16 and 48x48 nearest on the configured dark background. Play the 400 ms loop at the required cadence and review the wraparound transition and activity semantics. Record mechanical, visual and temporal results separately.
5. Obtain the representative style review before extending Ready and Retry. When the host renderer is supplied, verify cropping, path loading, frame timing and appearance in both regular and compact consumers. Missing renderer evidence must stay unavailable; a local preview is not proof of actual integration.
6. Update the selected PLAR row with the actual artifact/evidence and next action. Keep it `todo` until production starts, use `review` when a candidate awaits review, and claim `integrated` only with actual consumer integration evidence.

## Remaining choices and workflow limits

- No style reference is approved. The proposed Working motif is a useful experiment, not an artistic decision already made. Its review will determine the baseline for the static family members.
- Confirm whether the intended renderer consumes the proposed tightly packed 64x16 sheet and where its runnable entry point is. This is not needed to save requirements; it is needed to close import and display acceptance.
- Ready and Retry motifs remain open until the representative sample is reviewed. Retry must remain distinguishable without color alone regardless of motif.
- The PLAR schema has no dedicated ready-for-handoff status. All three rows remain `todo`; this document and each `next` field express the production boundary without implying work has started.
- The first runtime attempt misrouted `plar read` into the save parser and failed with a missing `--expect` argument. The maintainer fixed parser-variable shadowing; subsequent validation results are in `plar-validation.json`. This agent made no changes in the skill checkout.

The source hashes and CLI validation establish document shape, references, dependency consistency and source binding. They do not establish artistic quality, runtime display, provider execution or user acceptance.
