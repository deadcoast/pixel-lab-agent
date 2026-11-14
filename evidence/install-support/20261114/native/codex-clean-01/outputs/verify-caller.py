import hashlib, json
from pathlib import Path

root = Path.cwd()
out = root / 'work/readiness'
kit = root / 'installed pixl'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name): return json.loads((out / name).read_text(encoding='utf-8-sig'))
def ref(name): return {'path': 'work/readiness/' + name, 'sha256': digest(out / name)}
r, s, lib, child = (read(n) for n in ('readiness.json','source.json','library.json','SPECIALIST-RESULT.json'))
checks = {
 'source_hash_matches_actual_brief': s['sha256'] == digest(root / 'BRIEF.md'),
 'source_text_matches_actual_brief': s['text'] == (root / 'BRIEF.md').read_bytes().decode('utf-8'),
 'source_lines': s['start'] == 1 and s['end'] == 3,
 'readiness_root_matches_consumer': Path(r['project']['root']).resolve() == root.resolve(),
 'installation_root_matches_copied_kit': Path(r['installation']['root']).resolve() == kit.resolve(),
 'installation_files_match': all(digest(kit / v['path']) == v['sha256'] for v in r['installation']['files'].values()),
 'manifest_hash_matches': digest(kit / 'bundle-manifest.json') == r['installation']['bundle_manifest']['sha256'],
 'library_root_matches': Path(lib['root']).resolve() == (kit / 'resources').resolve(),
 'library_source_hashes_match': all(digest(kit / 'resources' / d['path']) == d['sha256'] for d in lib['documents']),
 'supplied_observations_match_return': read('observations.json') == r['caller_supplied_observations'],
 'specialist_artifact_identities_match': all(digest(root / a['path']) == a['sha256'] for a in child['artifacts']),
 'specialist_brief_matches': child['brief']['sha256'] == digest(root / 'BRIEF.md'),
 'specialist_root_matches': Path(child['root']).resolve() == root.resolve(),
 'specialist_installation_matches': Path(child['installation']).resolve() == kit.resolve(),
 'specialist_runtime_matches_caller': all(child['runtime']['report'][k] == r[k] for k in ('project','reporter','installation','dependencies')),
 'specialist_native_identity_matches_spawn': child['native_identity']['task_name'] == '/root/readiness_specialist' and child['native_identity']['selected_role'] == 'pixl',
}
report = {
 'host': 'codex', 'status': 'completed_scoped_readiness_evaluation', 'root': str(root),
 'target_role': 'pixl', 'role_observation': 'available', 'native_child': '/root/readiness_specialist',
 'observations_file': ref('observations.json'), 'readiness': ref('readiness.json'),
 'source': ref('source.json'), 'library': ref('library.json'), 'specialist_result': ref('SPECIALIST-RESULT.json'),
 'role_evidence': {'declaration': 'collaboration.spawn_agent explicitly declares pixl as an available agent_type', 'invocation': {'agent_type':'pixl','fork_turns':'none','task_name':'readiness_specialist'}, 'returned_child_id':'/root/readiness_specialist', 'completion':'Actual child completion observed; result read and compared separately from self-description', 'registration_route':'Actual exposed collaboration role route; no inference that project role file caused registration'},
 'checks': checks,
 'inventory_evidence': ref('tool-inventory.json'),
 'limitations': ['Host version 0.167.2 comes from assignment executable observation, not independently executed by caller.', 'Instruction loading is not verified by host trace; child file identities are compared separately.', 'Only local PIXL MCP is configured for this isolated invocation; official tools not listed, authentication not verified, provider execution not attempted.', 'Manifest byte verification does not establish publisher authenticity.', 'No artwork, production state, renderer or engine acceptance was assigned or established.'],
 'next_action': 'Readiness evaluation complete. Before future authorized provider work, inspect the official PixelLab tools in that work session; no setup changes are needed for this evaluation.'
}
(out / 'CALLER-RESULT.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(checks, indent=2))
assert all(checks.values())
