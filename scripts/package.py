#!/usr/bin/env python3
from pathlib import Path
import sys
import zipfile
ROOT=Path(__file__).resolve().parents[1]
with zipfile.ZipFile(Path(sys.argv[1]).resolve(), 'w', zipfile.ZIP_DEFLATED) as z:
    for name in ('plugin.json','LICENSE','skills','assets'):
        p=ROOT/name
        for f in ([p] if p.is_file() else sorted(p.rglob('*'))):
            if f.is_file() and '__pycache__' not in f.parts and f.suffix != '.pyc':
                z.write(f, 'sanzo-colors/'+str(f.relative_to(ROOT)))
print(sys.argv[1])
