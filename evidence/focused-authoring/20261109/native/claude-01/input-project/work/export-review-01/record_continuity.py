import json, io
from pathlib import Path
new = json.loads(Path('work/export-review-01/request-review-raw.txt').read_bytes().decode('utf-8'))
old = json.loads(Path('work/criteria-review-01/request-review-raw.txt').read_bytes().decode('utf-8'))
cmp = json.loads(Path('work/criteria-review-01/caller-comparison.json').read_bytes().decode('utf-8'))
rows = {}
for c in new['criteria']:
    rows[c['id']] = {'report_record_sha256': c['record_sha256'], 'report_current_record_sha256': c['current_record_sha256'], 'record_status': c['record_status']}
for c in old['criteria']:
    rows[c['id']]['prior_report_record_sha256'] = c['record_sha256']
for r in cmp['criterion_comparisons']:
    rows.setdefault(r['criterion'], {})['prior_caller_comparison_record_sha256'] = r['record_sha256']
ok = all(v.get('report_record_sha256') == v.get('report_current_record_sha256') == v.get('prior_report_record_sha256') == v.get('prior_caller_comparison_record_sha256') and v.get('record_status') == 'current' for v in rows.values())
summary = {'criteria_in_fresh_report': len(new['criteria']), 'criteria_in_prior_report': len(old['criteria']), 'rows_in_prior_caller_comparison': len(cmp['criterion_comparisons']),
  'criterion_ids_identical_in_order': new['criterion_ids'] == old['criterion_ids'] == [r['criterion'] for r in cmp['criterion_comparisons']],
  'all_record_hashes_identical_and_current': ok,
  'criteria_section_identical': new['criteria'] == old['criteria'], 'controls_identical': new['controls'] == old['controls'], 'decisions_identical': new['decisions'] == old['decisions'], 'selections_identical': new['selections'] == old['selections'], 'baseline_identical': new['baseline'] == old['baseline'], 'plan_identical': new['plan'] == old['plan'], 'state_identical': new['state'] == old['state'], 'diagnostics_identical': new['diagnostics'] == old['diagnostics'],
  'request_identical_including_lifecycle': new['request'] == old['request'],
  'request_request_sha256': new['request']['request']['request_sha256'], 'prior_request_request_sha256': old['request']['request']['request_sha256'],
  'intent_sha256': new['request']['intent_sha256'], 'prior_intent_sha256': old['request']['intent_sha256'],
  'job_state': new['request']['state'], 'remote_id': new['request']['remote_id'], 'blockers': new['request']['blockers'], 'next_action': new['request']['next_action'],
  'sources_identical_excluding_absolute_path': [{k: v for k, v in s.items() if k != 'absolute_path'} for s in new['sources']] == [{k: v for k, v in s.items() if k != 'absolute_path'} for s in old['sources']],
  'source_excerpt_fields_present': sorted(set().union(*[set(s.keys()) for s in new['sources']])),
  'rows': rows}
json.dump(summary, io.open('work/export-review-01/record-continuity.json', 'w', encoding='utf-8'), indent=1)
print(json.dumps({k: v for k, v in summary.items() if k != 'rows'}, indent=1))
print('row check sample', json.dumps(rows['authoring-01.working.q.geometry'], indent=1))
