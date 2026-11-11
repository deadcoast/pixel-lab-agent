from operations import *
plan=read('work/integration-change/delivery-plan-result.json')
op('delivery-request-review.json','request-review',STATE,'--plan',plan['plan'],'--root',ROOT)
op('delivery-build.json','family-snapshot',STORE,plan['delivery']['output'],'working.delivery150','--expect',state(),'--root',ROOT)
op('delivery-context.json','review-context',STATE,'working.delivery150','--root',ROOT)
command=['node','renderer-integration/capture.mjs','--project',str(ROOT),'--out',str(OUT/'delivery-capture')]
r=subprocess.run(command,cwd=ROOT,capture_output=True)
(OUT/'delivery-capture.stdout').write_bytes(r.stdout);(OUT/'delivery-capture.stderr').write_bytes(r.stderr)
save('delivery-capture.execution.json',{'command':command,'exit_code':r.returncode,'helper_sha256':sha('work/integration-change/build-delivery.py')})
print(r.stdout.decode(),r.stderr.decode())
command=[PY,'renderer-integration/check.py','--project',str(ROOT),'--capture','work/integration-change/delivery-capture']
r=subprocess.run(command,cwd=ROOT,capture_output=True)
(OUT/'renderer-check.json').write_bytes(r.stdout);(OUT/'renderer-check.stderr').write_bytes(r.stderr)
save('renderer-check.execution.json',{'command':command,'exit_code':r.returncode,'helper_sha256':sha('work/integration-change/build-delivery.py')})
context=read('work/integration-change/delivery-context.json')
mapping=save('destinations.json',{m['output']:'assets/working.png' for m in context['members']})
command=[PY,'renderer-integration/observation.py','--project',str(ROOT),'--capture','work/integration-change/delivery-capture','--context','work/integration-change/delivery-context.json','--renderer','renderer-integration','--destinations',mapping,'--out','work/integration-change/destination-report.json']
r=subprocess.run(command,cwd=ROOT,capture_output=True)
(OUT/'destination-report.stdout').write_bytes(r.stdout);(OUT/'destination-report.stderr').write_bytes(r.stderr)
save('destination-report.execution.json',{'command':command,'exit_code':r.returncode,'helper_sha256':sha('work/integration-change/build-delivery.py')})
print(r.stdout.decode(),r.stderr.decode())
op('destination-import.json','destination-import',STATE,'working.delivery150','work/integration-change/destination-report.json','--out','work/integration-change/destination-bundle','--root',ROOT)
