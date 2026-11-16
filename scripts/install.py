#!/usr/bin/env python3
"""Install or update Sanzo Colors, preserving previous installations as backups."""
import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MARKER = '.sanzo-colors.json'
WRAPPER = '#!/usr/bin/env python3\nfrom pathlib import Path\nimport runpy\nrunpy.run_path(str(Path.home() / ".agents/skills/colors/scripts/colors.py"), run_name="__main__")\n'


def owned(path, terminal=False):
    if path.is_symlink():
        return False
    if terminal:
        return path.is_file() and path.read_text() == WRAPPER
    if not path.is_dir():
        return False
    marker = path / MARKER
    if marker.is_file():
        try:
            return json.loads(marker.read_text()).get('package') == 'teodorik/sanzo-colors'
        except (ValueError, AttributeError):
            return False
    # Recognize v0.1.x installations created before ownership markers existed.
    script, sources = path / 'scripts/colors.py', path / 'references/sources.md'
    return (script.is_file() and sources.is_file() and (path / 'data/colors.json').is_file()
            and 'Offline Sanzo Wada palette lookup' in script.read_text()
            and 'https://sanzo-wada.dmbk.io/assets/colors.json' in sources.read_text())


def install(base, terminal=False):
    base = Path(base)
    base.mkdir(parents=True, exist_ok=True)
    lock = base / '.sanzo-colors-install.lock'
    try:
        lock.mkdir()
    except FileExistsError:
        raise FileExistsError(f'Another installation may be running: {lock}. Remove this lock only if no installer is running.')
    stages = []
    try:
        targets = [base / '.agents/skills/colors', base / '.claude/skills/colors']
        if terminal:
            targets.append(base / '.local/bin/colors')
        for i, target in enumerate(targets):
            if (target.exists() or target.is_symlink()) and not owned(target, i == 2):
                raise FileExistsError(f'Refusing to replace unrecognized installation or symlink: {target}. Move it aside explicitly first.')
        version = json.loads((ROOT / 'plugin.json').read_text())['version']
        # Prepare all new files before changing any current installation.
        for i, target in enumerate(targets):
            target.parent.mkdir(parents=True, exist_ok=True)
            stage = Path(tempfile.mkdtemp(prefix='.sanzo-colors-', dir=target.parent))
            record = {'target': target, 'stage': stage, 'installed': False, 'backed_up': False}
            stages.append(record)
            new = stage / 'new'
            if i == 2:
                new.write_text(WRAPPER)
                new.chmod(0o755)
            else:
                shutil.copytree(ROOT / 'skills/colors', new, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
                (new / MARKER).write_text(json.dumps({'package': 'teodorik/sanzo-colors', 'version': version}) + '\n')
        for record in stages:
            target, stage = record['target'], record['stage']
            if target.exists():
                os.replace(target, stage / 'previous')
                record['backed_up'] = True
            os.replace(stage / 'new', target)
            record['installed'] = True
    except BaseException:
        # Restore every previous target if staging or replacement fails.
        for record in reversed(stages):
            target, stage = record['target'], record['stage']
            if record['installed']:
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            if record['backed_up']:
                os.replace(stage / 'previous', target)
            shutil.rmtree(stage)
        raise
    else:
        for record in stages:
            target, stage = record['target'], record['stage']
            print(f'Installed {target}')
            if record['backed_up']:
                print(f'Previous installation backed up at {stage / "previous"}')
            else:
                stage.rmdir()
        if terminal:
            print('Ensure ~/.local/bin is on PATH.')
    finally:
        lock.rmdir()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--global', dest='global_install', action='store_true')
    g.add_argument('--project', type=Path)
    a = p.parse_args()
    try:
        install(Path.home() if a.global_install else a.project.resolve(), a.global_install)
    except (OSError, ValueError) as e:
        p.error(str(e))
