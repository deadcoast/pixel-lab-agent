from operations import *
ctx=read('work/integration-change/delivery-context.json')
review=read('work/integration-change/delivery-review-observation.json')
d=read('work/integration-change/final-integrated-document.json')
a=next(a for a in d['assets'] if a['id']=='queue.working')
a['evidence']=[{'path':e,'note':'Fresh current controlled150ms integration evidence; scoped exact-art reuse only.'} if isinstance(e,str) else e for e in a['evidence']]
fp=save('final-integrated-document-corrected.json',d)
sel=op('status-recovery-selection.json','plar','read','--path','integration-plar.txt','--asset','queue.working','--root',ROOT)
op('integration-status-save-corrected.json','plar','save',fp,'--root',ROOT,'--path','integration-plar.txt','--expect',sel['hash'])
# Execute only the remaining handoff/result portion; original helper remains immutable.
source=(OUT/'finish.py').read_text()
tail=source[source.index("sel=op('final-selection.json'"):]
exec(compile(tail,str(OUT/'finish.py')+'#handoff-result','exec'))
