#!/usr/bin/env python3
"""Install the portable skill without overwriting existing files."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]

def install(base, terminal=False):
    source = ROOT / 'skills/colors'
    targets = [base / '.agents/skills/colors', base / '.claude/skills/colors']
    # Cursor and Codex both discover .agents/skills; avoid duplicate Cursor skills.
    if terminal:
        targets.append(base / '.local/bin/colors')
    for target in targets:
        if target.exists() or target.is_symlink():
            raise FileExistsError(f'Refusing to overwrite {target}; remove your previous installation explicitly first.')
    for target in targets[:2]:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        print(f'Installed {target}')
    if terminal:
        target = targets[2]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('#!/usr/bin/env python3\nfrom pathlib import Path\nimport runpy\nrunpy.run_path(str(Path.home() / ".agents/skills/colors/scripts/colors.py"), run_name="__main__")\n')
        target.chmod(0o755)
        print(f'Installed {target}; ensure ~/.local/bin is on PATH.')

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--global', dest='global_install', action='store_true')
    g.add_argument('--project', type=Path)
    a=p.parse_args()
    try:
        install(Path.home() if a.global_install else a.project.resolve(), a.global_install)
    except FileExistsError as e:
        p.error(str(e))
