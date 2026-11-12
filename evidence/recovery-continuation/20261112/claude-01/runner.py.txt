"""CF-08: isolated three-round artifact recovery with a controlled transport."""
from __future__ import annotations

import argparse
import json
import shutil
import uuid
import zipfile
from datetime import UTC, datetime
from pathlib import Path

from evaluations import mcp_asset_case, readiness_case
from evaluations.host_trials import inventory, sha, write_json
from evaluations.native_trial_records import reference
from evaluations.provider_recovery_fixture import PROVIDER, SCHEMAS, RecoveryProvider
from evaluations.request_review_trials import run
from pixl import codec, jobs, service, store
from pixl.readiness import verify_manifest

WORK = 'work/provider-recovery'
STORE = '.pixl/recovery'
KIT = readiness_case.KIT
AUTHORITY = 'RECOVERY-ASSIGNMENT.md'
JOB = 'recoverable-job'
UNRESOLVED = 'unresolved-job'
OUTPUT = 'recovered-avatar'
CANDIDATE = 'recovered-avatar-candidate'


def plan(root: Path) -> codec.Document:
    """A real saved sample plan for recovery mechanics; acceptance remains unperformed."""
    R, Ref, Sym = codec.Record, codec.Ref, codec.Symbol
    source = root / AUTHORITY
    records = [
        R('actor', 'A', {'nm': 'PIXL recovery evaluator', 'rl': Sym('agent')}),
        R('source', 'S', {'ur': AUTHORITY, 'dg': sha(source),
                         'ln': [1, len(source.read_text(encoding='utf-8').splitlines())],
                         'at': datetime.now(UTC).isoformat(), 'au': Sym('local')}),
        R('project', 'P', {'nm': 'Existing avatar recovery evaluation', 'ow': Ref('actor'),
                          'sc': [Ref('source')], 'in': []}),
        R('contract', 'C', {'nm': 'Retained avatar fixture', 'px': [32, 32], 'pl': [],
                           'vw': Sym('side'), 'sa': Sym('nearest'), 'al': Sym('binary'),
                           'li': 'Controlled source pixels; no new aesthetic acceptance.'}),
        R('q.bytes', 'Q', {'nm': 'Complete recovered PNG', 'dm': Sym('mechanical'),
                           'md': Sym('local'), 'ck': 'Complete 32 by 32 PNG matches originating response byte identity.',
                           'wh': Ref('actor'), 'so': [Ref('source')]}),
    ]
    for task, output, label in [('recover-task', OUTPUT, 'Recover the existing avatar request'),
                                ('unresolved-task', 'unresolved-output', 'Preserve unresolved submission uncertainty')]:
        records.extend([
            R(task, 'T', {'nm': label, 'ow': Ref('actor'), 'pr': Ref('project'),
                         'dp': [], 'dc': [], 'kn': [], 'st': Sym('open'), 'ph': Sym('sample'),
                         'ip': [], 'op': [Ref(output)], 'ca': [], 'vr': []}),
            R(output, 'F', {'tk': Ref(task), 'nm': label, 'kd': Sym('sprite'),
                           'ct': Ref('contract'), 'rq': [Ref('q.bytes')]}),
        ])
    return codec.Document(0, {record.id: record for record in records}, format=2)


def seed(root: Path, provider_folder: Path) -> None:
    provider = RecoveryProvider(provider_folder, provider_folder / 'provider-negative.png',
                                provider_folder / 'provider-positive.png')
    source = provider.upload((root / 'input.png').read_bytes())['ref']
    anchor = provider.upload((root / 'reference.png').read_bytes())['ref']
    folder = root / STORE
    store.initialize(folder, plan(root), root)
    for ident, task, output, description in [
        (JOB, 'recover-task', OUTPUT, 'Recover existing avatar identity; original accepted controlled edit.'),
        (UNRESOLVED, 'unresolved-task', 'unresolved-output', 'Separate uncertain request with no sufficient provider observation.'),
    ]:
        arguments = {'method': 'reference', 'description': description, 'image_url': source,
                     'reference_image': {'url': anchor}}
        jobs.prepare(folder, codec.digest(store.load(folder)), ident, task, [output], PROVIDER,
                     'edit_image_pro_flash', arguments, SCHEMAS['edit_image_pro_flash'],
                     {'source': 'Controlled recovery fixture tools/list', 'observed_at': datetime.now(UTC).isoformat(),
                      'evidence': {'provider_simulated': True, 'schema_path': 'provider-schemas.json'}},
                     {'scope': 'Only original controlled preparation; native rounds recover without new submissions.',
                      'evidence': {'provider_simulated': True, 'assignment': AUTHORITY}}, root=root)
        claim = jobs.dispatch(folder, codec.digest(store.load(folder)), ident, root=root)
        if ident == JOB:
            response, is_error, _ = provider.call('edit_image_pro_flash', claim['dispatch_request']['arguments'])
            assert is_error and 'job_id' not in response
            evidence = {'provider_simulated': True, 'response': response}
        else:
            evidence = {'provider_simulated': True,
                        'observation': 'No response or identifier is available. This does not establish acceptance or non-acceptance.'}
        jobs.observe(folder, codec.digest(store.load(folder)), ident, 'unknown', evidence, root=root)


def guidance(root: Path, host: str, python: Path) -> str:
    return f'''Explicit CF-08 controlled native recovery evaluation, not a new art assignment.
Consumer root: {root.as_posix()}. Kit: {(root / KIT).as_posix()}.
Selected Python: {python.as_posix()}. Read {AUTHORITY} and the assigned phase file.
The actual named {'pixl' if host == 'codex' else 'pixl:pixl'} specialist is required.
The local PIXL server and originating pixellab-recovery-test fixture are separate.
Only that controlled fixture is configured; no real provider or paid work is assigned.
Work only inside this consumer. Do not inspect evaluator backing files outside it,
credentials, host settings or memory; do not install packages or modify the kit.
Keep provider_simulated=true. Human acceptance and artistic/engine acceptance are
separate and unperformed; do not let a generic human-approval gate halt recovery.
'''


def assignment() -> str:
    return f'''# Continue the existing avatar request without duplicate submission

This later CF-08 recovery addendum supersedes only OWNER.md's instruction to start
a new edit. Preserve that original brief, src/avatar.ts, input.png and reference.png.
The existing consumer expects a 32x32 PNG at assets/robot.png. These images and the
provider are controlled fixtures, not real PixelLab generation or human acceptance.

The saved store is {STORE}. Job {JOB} has a lost submission response; recover it
using exact originating-connection observations. Job {UNRESOLVED} is a separate
unknown attempt with insufficient observations; absence in a listing cannot prove
non-acceptance. Keep that job unknown unless actual matching evidence resolves it.
There is no authorization for a new request, paid or simulated. Do not dispatch,
prepare, generate, upload, replace provider identity or abandon unknown work to
bypass it. Original local journal/state evidence remains immutable.

Use ordinary jobs/workflow reports, job-observe and job-import. Read the installed
shared skill/profile and provider-recovery reference; use actual tool schemas/help.
Choose the correct current expected hash for each mutation. Provider success is
not complete retrieval, and imported bytes are not visual/engine acceptance.
Do not fabricate candidate reviews, nominate, complete tasks or alter criteria.

The experiment has three separately launched artifact-recovery phases. A fresh
caller and named child consume the SAME root/store/kit each round; these are not
same-session or same-child native continuations. Follow only the assigned phase.
Phase1 reconciles identity, observes progress and preserves the interrupted HTTP
retrieval as a useful partial handoff. Phase2 cold-recovers complete bytes/imports
and gives the caller a useful file. Phase3 cold-consumes that exact retained
candidate and confirms current state without another dispatch or import.

Caller: delegate to the actual named specialist, supply this root, kit, Python and
phase assignment, retain its real child ID and wait for its result. Codex uses
agent_type='pixl', fork_turns='none'. Do not substitute a generic child. Independently
read the specialist's exact report and current jobs/state, inspect actual returned
files/diagnostics and verify src/avatar.ts's path mapping. Report partial recovery
honestly; do not require unrelated artistic or human acceptance for this assignment.

All new work belongs under {WORK}/phase-N or this existing {STORE}; assets/robot.png
may first be created in phase2 as an exact byte copy, clearly unaccepted for art.
Keep earlier phase files unchanged. Retain actual stdout/errors rather than making
up observations. Capture timestamps from the clock when needed, never from memory.
'''


def phase_prompt(root: Path, host: str, python: Path, phase: int) -> str:
    out = f'{WORK}/phase-{phase}'
    tasks = {
        1: f'''Read saved unknown attempts and actual originating list/status responses.
Match the recoverable request's full tool/arguments/input identity before binding
its observed ID. Save real provider responses under {out}; record actual running
and succeeded observations using public job-observe. Keep {UNRESOLVED} unknown.
Retrieve the completed result through the returned loopback URL, ONCE this round.
The controlled transport deliberately truncates its first HTTP response. Preserve
the actual partial file at {out}/download.part and exact exit/error diagnostics at
{out}/download-error.json. curl.exe --fail --show-error --output PATH URL retains
partial bytes and returns a failure code for this short body; Python clients must
preserve IncompleteRead.partial when using response.read(). Do not suppress the
error, copy reference pixels, import the partial file, or retry in this phase.
Return status='partial' with the same observed resource ID and an actionable cold
retrieval continuation. This scheduled phase boundary is the trial's interruption,
not a request for human permission. Save current full jobs and workflow reports.''',
        2: f'''Cold-read the previous partial handoff and actual saved jobs/state.
Keep {UNRESOLVED} unknown. The old download URL belonged to an ended connection;
re-query the SAME saved provider/job ID for this connection's fresh result URL.
Download the complete returned PNG to {out}/retrieved.png. Verify actual byte length,
SHA-256 and PNG decoding against the originating response. Do not copy reference
pixels as recovered output. Preserve phase1's partial bytes and error untouched.
Import through public job-import using job={JOB}, output={OUTPUT}, candidate={CANDIDATE}.
Retain the import evidence you supplied in {out}/import-evidence.json and full return
in {out}/import-result.json. Obtain its actual retained candidate path/hash from
current public state/job reports; no acceptance is granted by import. Return that
file to the caller. Caller independently reads/hashes the actual candidate, opens
it with an available image tool, checks src/avatar.ts, and copies exact bytes to
assets/robot.png. Return status='recovered' with visual/engine acceptance unperformed.''',
        3: f'''Cold-read prior handoffs and current public state/jobs. Obtain the existing
{CANDIDATE} path/hash and actual assets/robot.png. Do not observe, import, prepare,
dispatch, poll or mutate production state in this read-only round. Keep {UNRESOLVED}
unknown and recover its exact next action. Caller independently reads/hashes the
actual retained candidate and delivered file, opens the returned PNG, verifies the
consumer path and consumes the result. Return status='recovered' with the SAME
candidate/job/remote identity and explicit next inspection/unresolved-job action.
No new provider call or file copy is needed. Write new reports only under {out}.''',
    }
    return guidance(root, host, python) + f'''
# Assigned recovery phase {phase}

{tasks[phase]}

Both participants must read the full current public jobs report, saved as
{out}/jobs-before.json by the specialist and {out}/jobs-after.json after its work.
The caller independently retrieves its own current report as {out}/caller-jobs.json.
The specialist writes {out}/SPECIALIST-RESULT.json; caller writes
{out}/CALLER-RESULT.json after actual child completion and independent consumption.
Each report includes phase, status, provider_simulated=true, job, remote_id,
unresolved_job, unresolved_state, candidate (null or {{id,output,path,sha256}}),
state ({{path,sha256,canonical_hash,revision}}), evidence_refs (actual path/sha256),
limitations and next_action. The caller also includes native_child and a file
reference to specialist_result. File paths are consumer-relative; hashes are actual
SHA-256. Preserve supplied schema/value meanings. Do not claim live PixelLab,
new artistic quality, target-engine or human acceptance. M1/M2 and broader M3/M4
remain open. Return useful exact files and recovery status, not just a plan.
'''


def snapshot(root: Path, destination: Path, *, prefix: str) -> dict:
    folder = destination / 'snapshots'
    folder.mkdir(exist_ok=True)
    doc = store.load(root / STORE)
    state = folder / f'{prefix}-state.px'
    shutil.copyfile(root / STORE / 'state.px', state)
    write_json(folder / f'{prefix}-jobs.json', jobs.report(doc, root))
    write_json(folder / f'{prefix}-workflow.json', service.workflow(root / STORE / 'state.px', root))
    return {'path': str(state.resolve()), 'file_sha256': sha(state),
            'canonical_hash': codec.digest(doc), 'revision': doc.revision}


def metadata(destination: Path, root: Path, phase: int, host: str, provider_folder: Path,
             previous: Path | None = None) -> dict:
    baseline = snapshot(root, destination, prefix='baseline')
    provider_state = json.loads((provider_folder / 'provider-state.json').read_bytes())
    path = destination / 'snapshots/baseline-provider-state.json'
    shutil.copyfile(provider_folder / 'provider-state.json', path)
    launch = json.loads((destination / 'launch.json').read_bytes())
    return {'version': 1, 'phase': phase, 'host': host, 'consumer': str(root), 'store': STORE,
            'job_id': JOB, 'unresolved_job_id': UNRESOLVED, 'output_id': OUTPUT,
            'candidate_id': CANDIDATE, 'provider': PROVIDER,
            'expected_png_sha256': sha(provider_folder / 'provider-positive.png'),
            'expected_remote_id': provider_state['jobs'][0]['job_id'],
            'baseline_state': baseline,
            'baseline_provider': {'accepted_submissions': provider_state['accepted_submissions'],
                                  'record': reference(path)},
            'provider_folder': str(provider_folder),
            'previous_attempt': str(previous) if previous else None,
            'configuration': {name: reference(Path(path)) for name, path in launch['configuration_files'].items()},
            'frozen_kit': reference(root / KIT / 'bundle-manifest.json'),
            'provider_simulated': True,
            'continuation_mode': 'new_session' if phase == 1 else 'artifact_based_restart'}


def prepare(destination: Path, host: str, python: Path, *, package: Path | None = None,
            consumer: Path | None = None) -> Path:
    destination, python = destination.resolve(), python.resolve()
    root = readiness_case.prepare(destination, host, 'clean', python, package=package, consumer=consumer)
    provider_folder = destination / 'provider'
    provider_folder.mkdir()
    mcp_asset_case.setup(root, provider_folder, python)
    write_json(root / 'provider-schemas.json', SCHEMAS)
    write_json(root / 'current-provider-schemas.json', SCHEMAS)
    fixture = provider_folder / 'provider_recovery_fixture.py'
    shutil.copyfile(__file__.replace('provider_recovery_case.py', 'provider_recovery_fixture.py'), fixture)
    (root / AUTHORITY).write_text(assignment(), encoding='utf-8')
    for name in ('AGENTS.md', 'SESSION.md'):
        (root / name).write_text(guidance(root, host, python), encoding='utf-8')
    phase_file = root / WORK / 'phase-1/ASSIGNMENT.md'
    phase_file.parent.mkdir(parents=True)
    phase_file.write_text(phase_prompt(root, host, python, 1), encoding='utf-8')
    (destination / 'prompt.txt').write_text(phase_file.read_text(encoding='utf-8'), encoding='utf-8')
    seed(root, provider_folder)
    server = {'command': str(python), 'args': ['-B', str(fixture), '--folder', str(provider_folder),
              '--negative', str(provider_folder / 'provider-negative.png'),
              '--positive', str(provider_folder / 'provider-positive.png')]}
    launch = json.loads((destination / 'launch.json').read_bytes())
    if host == 'codex':
        for key, value in server.items():
            launch['command'][-1:-1] = ['-c', f'mcp_servers.pixellab_recovery.{key}=' + json.dumps(value)]
    else:
        config = json.loads((destination / 'mcp.json').read_bytes())
        config['mcpServers']['pixellab-recovery'] = {'type': 'stdio', **server}
        write_json(destination / 'mcp.json', config)
        index = launch['command'].index('--allowedTools') + 1
        launch['command'][index] += ',mcp__pixellab-recovery__*'
        launch['configuration_files']['provider_mcp'] = str(destination / 'mcp.json')
    launch.update(case='provider-recovery', phase=1, runtime_python=str(python),
                  artifact_roots=[WORK, STORE, 'assets/robot.png'])
    launch['configuration_files'].update(provider_fixture=str(fixture),
        provider_fixture_base=str(provider_folder / 'pixellab_mcp_fixture.py'))
    write_json(destination / 'launch.json', launch)
    identity = json.loads((destination / 'identity.json').read_bytes())
    identity.update(case='provider-recovery', inputs=inventory(root, ('__pycache__',)),
                    assignment=reference(root / AUTHORITY), runner=reference(Path(__file__)),
                    authorized_changes=[STORE + '/state.px'],
                    authorized_new_prefixes=[WORK + '/', STORE + '/'],
                    authorized_new_files=['assets/robot.png'])
    write_json(destination / 'identity.json', identity)
    write_json(destination / 'recovery-case.json', metadata(destination, root, 1, host, provider_folder))
    with zipfile.ZipFile(destination / 'input-state.zip', 'x', zipfile.ZIP_DEFLATED) as archive:
        for name in identity['inputs']:
            if name.startswith(STORE + '/') or name in (AUTHORITY, 'OWNER.md', 'src/avatar.ts', 'input.png', 'reference.png', 'provider-schemas.json'):
                archive.write(root / name, name)
    (destination / 'runner.py.txt').rename(destination / 'setup-runner.py.txt')
    shutil.copyfile(__file__, destination / 'runner.py.txt')
    return root


def prepare_cold(previous: Path, destination: Path, python: Path) -> Path:
    previous, destination, python = previous.resolve(), destination.resolve(), python.resolve()
    if destination.exists():
        raise ValueError('Use a fresh cold attempt directory')
    old = json.loads((previous / 'recovery-case.json').read_bytes())
    if old['phase'] >= 3:
        raise ValueError('The three-phase recovery case is already prepared')
    preserved = json.loads((previous / 'preservation.json').read_bytes())
    root = Path(old['consumer'])
    if inventory(root, ('__pycache__',)) != preserved['final_inventory']:
        raise ValueError('Previous retained consumer changed before cold preparation')
    if verify_manifest(root / KIT)['status'] != 'verified' or sha(root / KIT / 'bundle-manifest.json') != old['frozen_kit']['sha256']:
        raise ValueError('Cold recovery requires the exact frozen kit')
    launch = json.loads((previous / 'launch.json').read_bytes())
    for recorded in old['configuration'].values():
        path = Path(recorded['path'])
        if not path.is_file() or sha(path) != recorded['sha256']:
            raise ValueError('Retained host configuration changed or is unavailable')
    if str(python) != launch['runtime_python']:
        raise ValueError('Use the same selected runtime Python for cold recovery')
    destination.mkdir(parents=True)
    phase = old['phase'] + 1
    phase_file = root / WORK / f'phase-{phase}/ASSIGNMENT.md'
    phase_file.parent.mkdir(parents=True)
    phase_file.write_text(phase_prompt(root, old['host'], python, phase), encoding='utf-8')
    (destination / 'prompt.txt').write_text(phase_file.read_text(encoding='utf-8'), encoding='utf-8')
    if launch['host'] == 'claude':
        launch['command'][launch['command'].index('--session-id') + 1] = str(uuid.uuid4())
    launch.update(phase=phase, continuation_mode='artifact_based_restart')
    write_json(destination / 'launch.json', launch)
    identity = json.loads((previous / 'identity.json').read_bytes())
    identity.update(inputs=inventory(root, ('__pycache__',)), runner=reference(Path(__file__)),
                    predecessor={'attempt': str(previous), 'preservation': reference(previous / 'preservation.json'),
                                 'state': preserved['final_state']})
    if phase == 3:
        identity.update(authorized_changes=[], authorized_new_prefixes=[WORK + '/'], authorized_new_files=[])
    write_json(destination / 'identity.json', identity)
    write_json(destination / 'recovery-case.json', metadata(destination, root, phase, old['host'],
                                                          Path(old['provider_folder']), previous))
    shutil.copyfile(__file__, destination / 'runner.py.txt')
    return root


def retain(destination: Path) -> None:
    destination = destination.resolve()
    if (destination / 'preservation.json').exists():
        raise ValueError('Retain each attempt once; prior receipts remain immutable')
    case = json.loads((destination / 'recovery-case.json').read_bytes())
    root = Path(case['consumer'])
    identity = json.loads((destination / 'identity.json').read_bytes())
    current = inventory(root, ('__pycache__',))
    changed = [p for p, digest in identity['inputs'].items() if current.get(p) != digest]
    new = {p: digest for p, digest in current.items() if p not in identity['inputs']}
    unexpected = [p for p in changed if p not in identity['authorized_changes']]
    unexpected += [p for p in new if p not in identity.get('authorized_new_files', [])
                   and not p.startswith(tuple(identity['authorized_new_prefixes']))]
    with zipfile.ZipFile(destination / 'consumer-delta.zip', 'x', zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(set(changed) | set(new)):
            if (root / name).is_file():
                archive.write(root / name, name)
    shutil.copytree(root / WORK / f"phase-{case['phase']}", destination / 'outputs')
    final_state = snapshot(root, destination, prefix='final')
    for name in ('provider-state.json', 'provider-calls.jsonl'):
        shutil.copyfile(Path(case['provider_folder']) / name, destination / name)
    write_json(destination / 'preservation.json', {'changed': changed, 'new': new,
               'removed': [p for p in identity['inputs'] if p not in current], 'unexpected': unexpected,
               'final_inventory': current, 'final_state': final_state,
               'delta': reference(destination / 'consumer-delta.zip'),
               'provider_state': reference(destination / 'provider-state.json'),
               'provider_calls': reference(destination / 'provider-calls.jsonl'),
               'scope': 'Exact retained artifact-recovery phase; no art or human acceptance inferred.'})


def verify_ready(destination: Path) -> None:
    """Reject consumer/configuration drift between phase preparation and launch."""
    destination = destination.resolve()
    case = json.loads((destination / 'recovery-case.json').read_bytes())
    identity = json.loads((destination / 'identity.json').read_bytes())
    root = Path(case['consumer'])
    if inventory(root, ('__pycache__',)) != identity['inputs']:
        raise ValueError('Prepared consumer inputs changed before native launch')
    for row in case['configuration'].values():
        path = Path(row['path'])
        if not path.is_file() or sha(path) != row['sha256']:
            raise ValueError('Prepared host configuration changed before native launch')
    current_provider = Path(case['provider_folder']) / 'provider-state.json'
    if sha(current_provider) != case['baseline_provider']['record']['sha256']:
        raise ValueError('Prepared provider state changed before native launch')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    prep = sub.add_parser('prepare')
    prep.add_argument('destination', type=Path)
    prep.add_argument('--host', choices=('codex', 'claude'), required=True)
    prep.add_argument('--python', type=Path, default=readiness_case.DEFAULT_PYTHON)
    prep.add_argument('--package', type=Path)
    cold = sub.add_parser('cold')
    cold.add_argument('previous', type=Path)
    cold.add_argument('destination', type=Path)
    cold.add_argument('--python', type=Path, default=readiness_case.DEFAULT_PYTHON)
    execute = sub.add_parser('run')
    execute.add_argument('destination', type=Path)
    execute.add_argument('--timeout', type=float, default=1200)
    args = parser.parse_args()
    if args.action == 'prepare':
        root = prepare(args.destination, args.host, args.python, package=args.package)
        print(json.dumps({'consumer': str(root), 'launched': False}))
    elif args.action == 'cold':
        root = prepare_cold(args.previous, args.destination, args.python)
        print(json.dumps({'consumer': str(root), 'launched': False, 'mode': 'artifact_based_restart'}))
    else:
        verify_ready(args.destination)
        run(args.destination.resolve(), timeout=args.timeout)
        retain(args.destination.resolve())


if __name__ == '__main__':
    main()
