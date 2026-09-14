import sys
from pathlib import Path
if '--version' in sys.argv:
 print('fake-host recorder-fixture 1.0')
else:
 sys.stdin.read()
 if sys.argv[1] == 'null':
  print('null')
 else:
  package=Path.cwd()/'.agents'/'skills'/'pixl-kit'
  (package/'sample.txt').write_text('changed sample\n',encoding='utf-8')
  (package/'added.txt').write_text('new fixture file\n',encoding='utf-8')
  (package/'remove.txt').unlink()
  print('{"type":"turn.completed"}')
