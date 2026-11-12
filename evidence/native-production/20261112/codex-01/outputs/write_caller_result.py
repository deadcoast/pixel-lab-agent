exec(compile(open('work/native-production/caller_audit.py',encoding='utf-8').read(),'caller_audit.py','exec'))
from datetime import datetime, timezone
viewed=['assets/ready-confirmed.png','work/native-production-inputs/original-ready.png','assets/working.png','assets/error-retry.png','assets/paused.png','work/native-production/ready-generated-01.png','work/native-production/render-01/destination.png','work/native-production/destination-gray-01.png']
viewed += ['work/native-production/render-01/view-%03d.png'%n for n in (12,13,14,15)]
viewed += ['work/native-production/gray-view-%03d.png'%n for n in (4,5,8,9,12,13,14,15,16,17)]
viewed += ['.pixl/assets/queue.ready/inspections/adb5f69b48f880a2113a2c8c8a6ea89e09947409a12a325bd16c2c6469f36450/views/%04d.png'%n for n in (1,2,4,5)]
checks_report=read('work/native-production/caller-renderer-check-01.json')
audit=read('work/native-production/caller-identity-audit.json')
result={
 'version':1,'observed_at':datetime.now(timezone.utc).isoformat(),'status':'delivered',
 'scope':'Complete NATIVE-PRODUCTION.md Ready-only official replacement and caller consumption. No broader milestone closure.',
 'native_child':{'identity':'/root/pixl','agent_type':'pixl','fork_turns':'none','invoked':True,'waited_for_completion':True,'same_child_feedback':True,'final_status':'delivered'},
 'specialist_result':ref('work/native-production/SPECIALIST-RESULT.json','complete specialist result independently consumed'),
 'comparison_ref':ref('work/native-production/COMPARISON.json','independent pre-dispatch every-criterion comparison'),
 'provider_operations':s['provider_operations'],'delivered_files':s['delivered_files'],'reused_files':s['reused_files'],
 'viewed_images':[ref(p,'Actually opened with host view_image by caller') for p in viewed],
 'renderer_report_ref':s['renderer_report_ref'],'renderer_check_ref':ref('work/native-production/caller-renderer-check-01.json','independent full supplied checker stdout'),
 'handoff_ref':s['handoff_ref'],
 'handoff_consumption':{'compact':True,'full_details':True,'full_resume':True,'full_delivery':True,'source_ranges':'Full immutable handoff read, including details lines3-154 and resume/delivery157-326. Fresh selected PLAR read afterward; state and requirements match.','refresh_ref':ref('work/native-production/caller-final-selection.json','exact fresh focused public selection')},
 'independent_checks':{
  'identity_audit':ref('work/native-production/caller-identity-audit.json','155 passing file/provider/source/grayscale checks'),
  'renderer':{'status':checks_report['status'],'observations':len(checks_report['observations']),'failures':checks_report['failures'],'missing':checks_report['missing']},
  'request':'Reviewed original sources and each of nine literal criteria. Saved dispatch arguments equal reviewed and actual submitted arguments, including real upload handle and style controls.',
  'provider':'Real official MCP submission/completion IDs match saved durable claim and import. Provider returned PNG bytes match downloaded candidate, local artifact and Ready destination; one charge5, balance4984 to4979.',
  'visual':'Caller opened exact final destination and generated PNG, original reference and native/3x panel composites; blue asymmetric tick reads success. White roundel is deliberate subject with transparent exterior, allowed by contract. Stronger white emphasis remains coherent with blue stepped queue family.',
  'non_color':'Actual color/grayscale destination plus native/3x cells distinguish check/solid roundel from open activity arcs, circular retry arrow and paired pause bars. Both consumers show identical Ready bytes. Grayscale source derivations independently recomputed and matched.',
  'acceptance_scope':'Agree with all nine current passing verdicts for this one Ready replacement. No new family manifest, generated sibling, recipe restriction or historical simulated execution inferred.',
  'state':'Fresh PLAR requirements e0f3f9cc941fbff42793106774c5a786290c348957ce7853acd4f29f19f8e3c3 and canonical state586fe65d3720eb8a8edbeafb9b51c56c872ae3761482bf3ff70d0e6d8d8c9ed3 match full handoff; task done,9pass,no pending,delivery complete.'},
 'preservation':{'baseline_ref':ref('work/native-production/caller-preservation-baseline.json','independent starting protected hashes'),'check_ref':ref('work/native-production/caller-preservation-check.json','independent protected file match report'),'origin_closure':'Every original origin.json entry except authorized Ready destination independently matched. Original Ready snapshot and original plar unchanged. Fresh work confined to assigned work/store and production-plar progress plus Ready destination.'},
 'guided_recovery':{'contract':'Same child corrected citation34-38 to34-39 before dispatch; originals retained.','local_failures_ref':s['failures_and_recovery'],'other_observed_failure':ref('work/native-production/platform-docs.html.failure.json','official platform docs HTTP403 retained'),'caller_output_limits':'Some full discovery and duplicate text/structured output displays truncated; exact reports saved, specific relevant fields retrieved and full immutable handoff read. No paid resubmission.'},
 'limitations':s['limitations']+['Host image payloads were native16px and nearest48px; physical monitor zoom/DPI unknown.','Official platform docs URL returned HTTP403. Actual connected declarations, current MCP docs/help and free capabilities were used; failure retained.','Generic local lineage projection does not authenticate remote execution and leaves upload resolution unknown; host official receipts and exact upload source/hash/handle transport are separate retained evidence.'],
 'next_action':'None for this scoped assignment. M1/M2 and broader M3 remain open; no additional paid work needed.'}
assert audit['status']=='pass' and checks_report['status']=='pass'
(root/'work/native-production/CALLER-RESULT.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'status':result['status'],'path':'work/native-production/CALLER-RESULT.json','sha256':sha('work/native-production/CALLER-RESULT.json')}))
