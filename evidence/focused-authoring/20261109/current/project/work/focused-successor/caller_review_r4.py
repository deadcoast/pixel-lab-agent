from pathlib import Path
s=Path('work/focused-successor/caller_review.py').read_text(encoding='utf-8')
s=s.replace('proposal-r3','proposal-r4').replace('render-02','render-03').replace('pixel-check-02','pixel-check-03')
s=s.replace('    assert times[-1]-times[0]>=800', '''    assert all(not x['errors'] for x in phase['samples'])
    assert len(phase['samples'][-1]['changes']) == {'normal-before':0,'reduced-live':1,'normal-after':2}[phase['name']]
    if phase['reduced']:
        assert all(c['frame']==0 for x in phase['samples'] for c in x['matrixWorking'])
    assert times[-1]-times[0]>=800''')
exec(compile(s,'caller_review_r4_generated','exec'))
