import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('installer', ROOT/'scripts/install.py')
i=importlib.util.module_from_spec(spec);spec.loader.exec_module(i)

class InstallTest(unittest.TestCase):
    def test_legacy_global_upgrade(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d)
            for host in ('.agents','.claude'):
                target=base/host/'skills/colors'
                shutil.copytree(ROOT/'skills/colors',target)
            wrapper=base/'.local/bin/colors';wrapper.parent.mkdir(parents=True);wrapper.write_text(i.WRAPPER)
            i.install(base,terminal=True)
            self.assertTrue(os.access(wrapper,os.X_OK))
            self.assertTrue((base/'.agents/skills/colors'/i.MARKER).exists())
            self.assertEqual(len(list(base.rglob('previous'))),3)

    def test_foreign_and_symlink_refused(self):
        for symlink in (False,True):
            with tempfile.TemporaryDirectory() as d:
                base=Path(d);target=base/'.claude/skills/colors';target.parent.mkdir(parents=True)
                if symlink: target.symlink_to(base/'missing')
                else: target.mkdir();(target/'SKILL.md').write_text('unrelated')
                with self.assertRaises(FileExistsError):i.install(base)
                self.assertFalse((base/'.agents/skills/colors').exists())
                self.assertTrue(target.is_symlink() if symlink else (target/'SKILL.md').read_text()=='unrelated')

    def test_failed_replacement_rolls_back_all_targets(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);i.install(base,True)
            original=base/'.agents/skills/colors/SKILL.md';original.write_text('keep my edits')
            real=i.os.replace
            def failing(src,dst):
                if Path(src).name=='new' and Path(dst)==base/'.local/bin/colors':
                    raise OSError('simulated replacement failure')
                return real(src,dst)
            with patch.object(i.os,'replace',side_effect=failing):
                with self.assertRaises(OSError):i.install(base,True)
            self.assertEqual(original.read_text(),'keep my edits')
            self.assertEqual((base/'.local/bin/colors').read_text(),i.WRAPPER)
            self.assertTrue((base/'.claude/skills/colors/SKILL.md').exists())
            self.assertFalse((base/'.sanzo-colors-install.lock').exists())
            self.assertFalse(list(base.rglob('.sanzo-colors-*')))

    def test_concurrent_install_refused(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);(base/'.sanzo-colors-install.lock').mkdir()
            with self.assertRaises(FileExistsError):i.install(base)
            self.assertTrue((base/'.sanzo-colors-install.lock').is_dir())
