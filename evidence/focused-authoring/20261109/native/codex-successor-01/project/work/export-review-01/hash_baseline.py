import hashlib, os, sys, json
root = sys.argv[1]
out = {}
targets = ['EXPORT-REVIEW.md','CRITERIA-RESULT.json','AUTHORING-REVIEW.md','AUTHORING-RESULT.json','AUTHORING-STAGE.md','AUTHORING-UPDATE.md','authoring-plar.txt','plar.txt','.pixl/assets/queue.ready/state.px','BRIEF.md','src/queue.ts','src/queue-view.ts','assets/working.png','assets/ready-confirmed.png','assets/error-retry.png','assets/paused.png','assets/start.svg','AGENTS.md','SESSION.md',
 '.pixl/assets/queue.ready/production-plans/b025e867d863f5ad28b47127d3384ea5f191d459573394521504243abd95d826.json',
 '.pixl/assets/queue.ready/stage-requests/84dcf243f2cd22b69fa7ac906bfc33e7abd55bf113c2cc6db7566cb87bd4b1f8.json',
 '.pixl/assets/queue.ready/jobs/d9badc9cf64c04f7adc812f2e245d4af8caf38bb63f102e4304c4e83bed1290d.json',
 'work/authoring-01/plan.json','work/authoring-01/stage-packet.json','work/authoring-01/working-rotation-policy.json','work/authoring-01/specialist-report.json']
for p in targets:
    fp = os.path.join(root, p)
    if os.path.exists(fp):
        b = open(fp,'rb').read()
        out[p] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
    else:
        out[p] = None
for f in sorted(os.listdir(os.path.join(root,'work/criteria-review-01'))):
    p = 'work/criteria-review-01/'+f
    b = open(os.path.join(root,p),'rb').read()
    out[p] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
print(json.dumps(out, indent=1))
