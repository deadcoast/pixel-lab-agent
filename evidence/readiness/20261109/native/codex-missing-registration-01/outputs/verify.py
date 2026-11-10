import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
out = root / 'work/readiness'
kit = root / 'installed pixl'
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):
    return json.loads((out / name).read_text(encoding='utf-8'))
def ref(name):
    return {'path': 'work/readiness/' + name, 'sha256': digest(out / name)}
source = read('source.json')['structuredContent']
library = read('library.json')['structuredContent']
ready = read('readiness.json')['structuredContent']
manifest = json.loads((kit / 'bundle-manifest.json').read_text(encoding='utf-8'))
issues = []
entries = manifest['files'] + manifest['generated_files']
for item in entries:
    path = kit / item['path']
    if not path.is_file() or digest(path) != item['sha256']:
        issues.append(item['path'])
checks = {
    'source_text_matches_actual_brief': source['text'] == (root / 'BRIEF.md').read_bytes().decode('utf-8'),
    'source_hash_matches_actual_brief': source['sha256'] == digest(root / 'BRIEF.md') == 'c79556d9a2ad6eb6b05685974bd2bd7410ceefc31e49a6ae1e8eb19bf75bec3d',
    'source_range': [source['start'], source['end']],
    'readiness_root_matches_consumer': Path(ready['project']['root']).resolve() == root,
    'library_root_matches_copied_resources': Path(library['root']).resolve() == (kit / 'resources').resolve(),
    'library_document_hashes_match': all(digest(kit / 'resources' / d['path']) == d['sha256'] for d in library['documents']),
    'readiness_installation_matches_copied_kit': Path(ready['installation']['root']).resolve() == kit.resolve(),
    'readiness_identity_hashes_match': all(digest(kit / d['path']) == d['sha256'] for d in ready['installation']['files'].values()),
    'manifest_hash_matches': digest(kit / 'bundle-manifest.json') == ready['installation']['bundle_manifest']['sha256'],
    'manifest_entries_checked': len(entries),
    'manifest_issues': issues,
    'selected_python_matches': Path(ready['reporter']['python_executable']) == Path('C:/github/pixel-lab-agent/build/readiness-setup-01/runtime/Scripts/python.exe'),
    'reporter_module_matches_copied_kit': Path(ready['reporter']['module']).resolve() == (kit / 'runtime/pixl/readiness.py').resolve(),
    'supplied_observations_match_returned': read('observations.json') == ready['caller_supplied_observations'],
    'consumer_role_file_exists': (root / '.codex/agents/pixl.toml').exists(),
    'actual_local_calls': ['pixl_source', 'pixl_sources', 'pixl_readiness'],
}
report = {
    'host': 'codex', 'host_version': '0.167.0',
    'status': 'completed_readiness_evaluation_with_setup_limits',
    'root': str(root), 'target_role': 'pixl', 'role_observation': 'not_observed',
    'native_child': None, 'observations_file': ref('observations.json'),
    'readiness': ref('readiness.json'), 'source': ref('source.json'), 'library': ref('library.json'),
    'specialist_result': None,
    'role_evidence': {
        'native_delegation': 'The actual collaboration.spawn_agent declaration exposes task_name, message, fork_turns, model and reasoning_effort; it has no agent_type or registered-role selector and advertises no pixl role. No alternative pixl invocation route is exposed in the full deferred-tool catalog.',
        'interpretation': 'Exact native role availability cannot be observed through this surface. This is not a definitive claim of host-wide unavailability.',
        'invocation': 'Not attempted: exact pixl role is not selectable from the observed declarations; no generic replacement was created.',
        'static_files': 'Installed agents/pixl.md and shared skill exist; the readiness result reports .codex/agents/pixl.toml missing. Static adapters do not prove registration or instruction loading.',
        'inventory': ref('tool-inventory.json'),
        'inventory_completeness': 'All entries in the session ALL_TOOLS metadata catalog were captured, not just the three invoked tools. All 39 mcp__pixl_local__ declarations are included as bare local operation names. No official PixelLab connector is advertised in that full catalog or direct tool declarations. Completeness applies only to this isolated session capture.',
        'host_version_basis': 'READINESS-ASSIGNMENT.md supplies observed executable version codex-cli 0.167.0; numeric component supplied to readiness. No independent executable version probe was performed.'
    },
    'checks': checks,
    'limitations': [
        'No exact named specialist was invoked, so there is no child identity or specialist result to compare.',
        'Successful calls establish execution of the three required local operations, not every advertised operation.',
        'Official PixelLab tools are not listed in this isolated invocation; no conclusion about other sessions, provider account status or an authentication failure follows.',
        'Provider authentication is not_verified; execution was not_attempted. No remote availability or authentication probe was made.',
        'Manifest identity verifies copied bytes, not publisher authenticity, host loading, production readiness or host reliability.',
        'No artwork, production state, renderer or engine acceptance was assigned or evaluated.'
    ],
    'next_action': 'If native specialist execution is needed, expose the exact pixl role in a future host invocation and retain its actual child/result identity. Before authorized provider work, discover the separately connected official PixelLab declarations. No registration or global configuration was changed in this evaluation.'
}
(out / 'CALLER-RESULT.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(checks, indent=2))
assert all(v for k, v in checks.items() if isinstance(v, bool) and k != 'consumer_role_file_exists')
assert not issues
