import json, hashlib, io
from pathlib import Path
def get(d, path):
    for k in path.split('.'):
        d = d[int(k)] if isinstance(d, list) else d[k]
    return d
P = 'request.request.discovery.evidence.declaration_text'
old_raw_b = Path('work/criteria-review-01/request-review-raw.txt').read_bytes()
old_fmt_b = Path('work/criteria-review-01/request-review.json').read_bytes()
new_raw_b = Path('work/export-review-01/request-review-raw.txt').read_bytes()
new_fmt_b = Path('work/export-review-01/request-review.json').read_bytes()
res = {}
res['old_formatted_bytes'] = {'non_ascii_bytes': sum(1 for x in old_fmt_b if x>127), 'contains_utf8_em_dash': '\u2014'.encode() in old_fmt_b, 'contains_utf8_ellipsis': '\u2026'.encode() in old_fmt_b, 'contains_json_escape_u2014': b'\u2014' in old_fmt_b, 'contains_mojibake_a_circumflex_euro': 'â€'.encode('utf-8') in old_fmt_b, 'contains_replacement_char': '\ufffd'.encode() in old_fmt_b, 'crlf': old_fmt_b.count(b'\r\n')}
for label, b in [('prior_raw', old_raw_b), ('prior_formatted', old_fmt_b), ('fresh_raw', new_raw_b), ('fresh_formatted', new_fmt_b)]:
    d = json.loads(b.decode('utf-8'))
    t = get(d, P)
    res[label] = {'declaration_text_len': len(t), 'declaration_text_sha256_utf8': hashlib.sha256(t.encode()).hexdigest(), 'non_ascii_codepoints': sorted({'U+%04X' % ord(c) for c in t if ord(c) > 127}), 'non_ascii_count': sum(1 for c in t if ord(c)>127)}
    # where in whole doc non-ascii occurs
    locs = []
    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items(): walk(v, path + '.' + k if path else k)
        elif isinstance(o, list):
            for i, v in enumerate(o): walk(v, path + '.%d' % i)
        elif isinstance(o, str) and any(ord(c) > 127 for c in o):
            locs.append(path)
    walk(d, '')
    res[label]['paths_with_non_ascii'] = locs
# hypothesis: a Windows cp1252 decode of the raw bytes
tg = get(json.loads(old_raw_b.decode('utf-8')), P)
try:
    tb = get(json.loads(old_raw_b.decode('cp1252')), P)
    res['cp1252_decode_hypothesis_on_prior_raw'] = {'decodes': True, 'declaration_text_differs_from_utf8': tb != tg, 'cp1252_len': len(tb), 'utf8_len': len(tg), 'cp1252_non_ascii_codepoints': sorted({'U+%04X' % ord(c) for c in tb if ord(c) > 127})}
except Exception as e:
    res['cp1252_decode_hypothesis_on_prior_raw'] = {'decodes': False, 'error': str(e)}
res['prior_formatted_equals_prior_raw_parsed'] = json.loads(old_fmt_b.decode('utf-8')) == json.loads(old_raw_b.decode('utf-8'))
res['prior_formatted_declaration_equals_prior_raw_declaration'] = get(json.loads(old_fmt_b.decode('utf-8')), P) == tg
res['fresh_raw_declaration_equals_prior_raw_declaration'] = get(json.loads(new_raw_b.decode('utf-8')), P) == tg
json.dump(res, io.open('work/export-review-01/decoder-observation.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=True)
print(json.dumps(res, indent=1, ensure_ascii=True))
