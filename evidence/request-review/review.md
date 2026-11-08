# Independent review findings

The evaluator read the original assignments, complete proposed contracts, native parent/specialist execution, actual submitted arguments, retained images and final results. Process exit and a producer's self-audit were not acceptance. Original attempts remain in the adjacent hash-verified archives.

## Corrected planning failures

- **claude-drone-01:** caller-driven revisions removed an unsupported one-frame rule, but also weakened the owner's general reference-matching outcome to report-only. **claude-drone-02** preserves the required outcome while keeping a particular construction recipe optional. Actual correction exchange and separate final review: native stdout lines 125, 132, 195, 201, 208.
- **claude-save-indicator-01:** the contract was usable, but the caller reported partial because future generation was absent from an explicitly planning-only assignment. **claude-save-indicator-02** reports the completed planning scope correctly; separate correction/review at stdout 99, 103, 153, 157, 163.
- **codex-drone-01 / codex-save-indicator-01:** both bounded planning handoffs preserve original requirements and perform separate caller comparison.

## Delivery defects that a correct final fixture would hide

### claude-mcp-edit-01

The corrective request used incorrect eye coordinates (x16–18 rather than the reference's x18–20, inclusive), and the caller repeated the incorrect measurement. See project/work/criteria.json:119, work/request-edit-02.json:11, caller-review-02.json:24, provider-calls.jsonl:10 and native stdout:454. Original source/reference bytes were correct. The controlled provider returned a positive fixture independently of that erroneous request.

Claude opened all 15 inspection views, but its file viewer supplied no usable dimensions. It retained null delivered sizes and correctly failed to publish visual passes (stdout:580,585). The caller ultimately delivered and inspected the actual downloaded PNG (632,634,636,638,646), but the durable task and three acceptance criteria remained open. PARENT-RESULT.json accurately says delivered_with_limitations. Independent decoding confirmed the 15 native image blocks exactly matched the prepared images; the failure was metadata/workflow support, not absence of image access.

The runtime now supplies optional exact-color region measurements from the same hashed snapshot, and optional selected inspection image blocks together with dimensions and hashes. These add no automatic verdict or saved-state schema.

### claude-mcp-edit-02

Two distinct failures prevent acceptance:

1. The specialist required the downloaded output hash to differ from the reference, and the caller incorrectly adopted that rule as sourced. The original instruction prohibits substituting a local reference for the provider download; it does not reject an authentic provider result with identical bytes. See project/criteria/robot-criteria.json:84, caller-review.json:29, initial adoption stdout:180/185 and false second-candidate rejection:510. Final reporting still defends this unsupported rule at PARENT-RESULT.json:91,93,101.
2. The actual second edit arguments differ from the reviewed artifact: image_base64 character 95 (zero-based) changed B to D, corrupting decoded byte 71. Actual input SHA-256 is 5b1652a6193fec8a4c23df2c45fb2eb944c5d59f484a4cd03ff6dc3d5a3f2115; the reviewed original is d28f90f619400f8a770741b23bb5c1da995e6b6dd017ebab30eac934892c8d8d. Actual dispatch is provider-calls.jsonl:10 / stdout:461; the image fails full decoding. The specialist later detected this from provider observations and honestly disclosed it at PARENT-RESULT.json:46–48. A terminal job correction was rejected (stdout:634–635), leaving the discrepancy in external retained receipts and the caller result. No destination asset was delivered; status blocked is accurate.

The new image-delivery interface itself passed this run: all 33 native MCP image blocks across calls 296,314,504,518,521,649 exactly matched prepared bytes and payload dimensions. Both candidates received complete specialist viewing coverage. 108 artifact hashes, 13 recorded evidence hashes and 53 linked hashes matched; original inputs were unchanged.

The shared handoff now requires a short source comparison for every rejection rule and distinguishes process requirements, output requirements and diagnostic proxies. Production guidance uses the official upload-handle path for local image files, avoiding model transcription of encoded bytes.

## Successful controlled operations already reviewed

**codex-mcp-edit-01:** two reviewed requests, recovered unknown submission without duplication, retained failed candidate, corrective inspection, durable completion and actual parent image/source consumption. 76 artifact hashes, 13 evidence hashes and 35 linked hashes matched.

**codex-mcp-cold-01:** parent and specialist recovered completed revision 18, original/revised reviews and delivered file; both opened images, and no provider call was made. 77 artifact hashes, 12 evidence hashes and 49 linked hashes matched. A guessed image path failed first, then the actual retained path was opened. No unresolved access blocker remained.

**codex-mcp-edit-02:** both actual requests exactly match the reviewed arguments and original decoded image bytes. Separate parent comparisons precede dispatch; both agents receive actual prepared image blocks. The first failed candidate remains retained and final revision 18 marks the task complete. 85 artifact hashes, 13 evidence hashes and 41 linked hashes matched. The parent independently downloads, opens and verifies the final asset and consumer mapping. The old fixture's separate-connection lookup failed for an existing job; the parent used the actual returned download URL and accurately disclosed the limitation. The new fixture shares current state across parent/specialist connections.

## Evaluation infrastructure corrections

The earlier controlled server checked only the PNG signature, so it accepted the corrupt second input in Claude02. It also cached state separately in each native MCP process. Both are preserved limitations of those attempts. The current server fully verifies and decodes input/reference PNGs before job creation and uses atomic state publication with a process lock and fresh reads for each operation.

Official get_upload_url discovery returned multipart upload instructions and a JSON upload:<id> reference for image-URL fields. The sanitized declaration/result shape is retained in evaluations/fixtures/pixellab-upload-20261108.json; the temporary signed URL is not retained and no image was uploaded to the upstream service. The controlled surface now implements this interaction with actual loopback uploads, exact stored bytes and persistent handle/hash bindings. Cold setup preserves older discovery artifacts already bound by saved packets and records current connection schemas separately.

The upload and cold outcomes below extend these earlier findings. The fresh Claude full-run findings are recorded below. These fixtures establish operation behavior; they do not establish PixelLab-generated art quality or live renderer acceptance.

## Qualified Claude03 result

**claude-mcp-edit-03:** the request/review, exact submitted bytes, uncertain-job recovery, candidate rejection/revision, image viewing, durable completion and actual consumer delivery pass. Both requests match reviewed arguments; original image/reference hashes decode exactly. Caller reviews stdout172/432 precede dispatch218/486. Parent re-queries629, re-downloads631, measures637/639 and opens enlarged641→642/native643→644 images. Revision19 completes repair_robot with all seven required criteria passed. 106 artifact hashes, 30 evidence hashes and 58 linked hashes matched.

**Overall workspace scope fails:** the original instruction restricts work to project/, but the specialist wrote sibling scratch/ helpers and state exports (stdout462,502,578,598,603), and the caller wrote sibling caller-verify/ downloads/previews (631,637). These are retained attempt-local files, with no observed production/host mutation, but they exceed the assigned consumer root. The correct delivered file does not erase that failure. Shared delegation guidance now explicitly keeps helper scripts, scratch and previews under the consumer root and asks the caller to verify returned path scope.

## Upload-based operation and completed handoff

**codex-mcp-upload-01 passes controlled delivery.** Actual uploads (provider-calls:3–4) retain exact original input/reference bytes; both edits5/10 equal reviewed requests and use those handles. Unknown submission is reconciled without duplicate edits, the failed candidate remains retained, and the parent actually opens and consumes the final file. Revision19 completes the task with all eight criteria passed. All writes stay inside the consumer (service-owned uploads are separate evaluator storage). 79 artifact hashes, 16 evidence hashes and 49 linked hashes match. This run does not itself exercise a parent-side provider re-query; it does not claim that additional behavior.

**claude-mcp-upload-01 delivers the correct reviewed file, but does not complete the durable task.** All source uploads and actual requests match; caller reviews223/430 precede edits278/470. All 30 specialist inspection payloads match prepared views. The caller opens the final image568→569, re-queries the provider590 and independently downloads592. However, revision17 still has t_robot=open and no nominated output; PARENT-RESULT.json:55 acknowledges this. The state reports output criteria as unperformed although x_robot_02 has all eight candidate-level passes. 105 artifact hashes, 16 evidence hashes and 64 linked hashes match.

That Claude run also writes an unauthorized helper under the host Temp directory (stdout23/25, reused572); its exact bytes are retained separately in supplements/claude-upload-temp-helper.py.txt with a retrospective capture record. It creates an unsupported future observed_at in evidence/uploads.json:5: 02:05Z is written at02:02:30.708Z (stdout139). Correct hashes and actual native timing remain available. These scope and metadata defects are preserved, not upgraded by a later repair.

The new task-complete CLI / pixl_task_complete MCP operation removes handwritten nomination/lifecycle scripts. It selects explicit existing candidates, preflights all existing acceptance/activation requirements, and publishes the legal active/done transitions. It preserves criteria, evidence, failures and provider jobs; no acceptance or generation is manufactured. Independent semantic probes reject a failed candidate, missing prerequisite and missing production adoption before publication. Tests also cover interruption, CAS, file drift, all-output selection, idempotence and CLI/MCP parity. OS hard-termination lock cleanup retains the existing explicit recovery procedure.

**claude-upload-cold-01 and codex-cross-host-completion-01 both pass local continuation of the same incomplete Claude handoff.** Each starts from exact revision17 and reaches identical revision19 SHA-256 35cea0fdcc0e47f8d1100f456898ecf6b895d2dfb6a6b309eef8cd17460d5412. The state changes only revision and t_robot.ca/st: x_robot_02 is selected and the task is done. All 16 verdicts, both jobs and the failed candidate remain unchanged. Neither run generates, uploads, prepares or dispatches again. Claude observes existing jobs; Codex observes/retrieves the existing result and downloads it once. Both keep new files inside the consumer root.

Claude uses the completion tool at stdout50→51, independently validates72→73 and receives the actual final native PNG81→82. Its cold review relies on retained enlarged inspection/provenance rather than claiming a new enlarged viewing or download. Codex's parent independently verifies complete contracts, bytes and source mapping, retrieves/opens the existing final result and receives prepared enlarged views; its child completes the same selection. Claude's109 artifact/16 evidence/114 linked hashes and Codex's115/16/132 hashes match. Original Claude upload files still match their original record. These repairs complete the remaining local work; they do not erase the original scope or timestamp defects.

**codex-upload-cold-01** also passes resumption of Codex's own completed upload run: state and originals unchanged, no provider calls, parent and child open actual retained images and recover existing acceptance. 81 artifact hashes, 14 evidence hashes and 63 linked hashes match. Generic inspect_candidates guidance is recognized as already satisfied by the completed task.

## Fresh full Claude operation: delivery passes with retained conformance defects

**claude-mcp-upload-02** completes in 760.128 seconds. Both on-wire requests (provider-calls:5,12) exactly match the independently reviewed argument artifacts. Actual uploads preserve the original input/reference bytes. Caller comparisons stdout172/180→201 and339→365 precede the edits246/432. The first unknown submission is recorded251 and reconciled253/259 without duplication; exactly two edits occur.

Both candidates receive all 30 prepared image payloads with exact bytes/dimensions (stdout281,295,459,476). The failed candidate remains unnominated with its identity failure. Accepted reviews482/500 precede task-complete504→505. The caller independently retrieves537→538, downloads and checks source/pixels542, opens the actual final PNG546→547 and checks durable state554/556/557. Revision 19, SHA-256 0817120d2a4bed4763fecb88bca7eb3dbc7f70b14fd18e8746716ad2beeaafbf, marks repair done with x_edit_2 nominated and all eight output criteria passing. All 124 artifact hashes, 16 evidence hashes and 78 checked path/hash references match; original inputs are unchanged.

**Consumer scope fails:** stdout224 writes /tmp/jobs.json, resolving to C:/Users/ryanf/AppData/Local/Temp/jobs.json. The subsequent Python path read fails231→232 and the agent recovers inside work/reports at234. The exact 8,837-byte outside file is retained in supplements/claude-upload-02-temp-jobs.json with a retrospective capture receipt; its original remains unchanged. Final reporting does not disclose this scope breach. This is a bounded helper-file deviation, not evidence of unrelated destructive behavior.

**Timestamp assertion is unsupported:** stdout403/408 supplies 02:40:00Z as the second discovery observation; prepared_at is 02:34:40.499Z. PARENT-RESULT.json:58 later calls it an estimate, but the published intent originally carried no such qualification. The inspection-review operation separately rejects a future time463→464 and incomplete viewing coverage470→471; corrected evidence then permits the actual reviews. Those rejections do not repair the earlier discovery assertion.

The runtime now rejects future discovery observations when preparing new requests, before publishing intent/blobs; callers must capture actual host time. Historical version1 receipts remain readable with their original assertions. Two regression tests cover preparation/history compatibility and unchanged files on rejection. These completed native attempts predate that final runtime correction; no fresh native verification of it is claimed. Delivery success, remaining host conformance defects and real-provider qualification are separate findings.

## What supports ordinary production

- **Keep on the everyday path:** exact request/criteria exchange, original reference bytes and roles, official upload handles, unknown-job reconciliation, actual candidate images, retained failed revisions, independent caller consumption and explicit completion. These mechanisms each resolved or exposed a concrete observed problem.
- **Simplify next:** specialists still construct numerous low-level plan records and helper scripts before the first operation. Derive that deterministic plan from the selected PLAR asset and reviewed contract while retaining traceable requirements. Task completion already has a single operation; initial plan authoring does not.
- **Keep available on demand:** source archives, method reference proofs, serialization benchmarks, broad catalogs and maintenance evaluators support diagnosis/research. Load only the relevant knowledge and complete selected dependencies for an assignment. These mechanisms are preserved; they are not all prerequisites for every asset.

The controlled workflow now reaches actual caller-consumed files in both hosts. Generated art quality, consistency across asset families and live renderer acceptance remain unverified. Neither a reference-identical fixture nor this runtime suite closes those outcomes.
