import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('colors',ROOT/'skills/colors/scripts/colors.py')
c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)

class ColorsTest(unittest.TestCase):
    def cli(self,*args):
        return subprocess.run([sys.executable,str(ROOT/'bin/colors'),*args],text=True,capture_output=True)
    def test_data_integrity(self):
        colors,combos=c.load()
        self.assertEqual(len(colors),159)
        self.assertEqual(set(combos),set(range(1,349)))
        self.assertEqual(len({x['slug'] for x in colors}),159)
        for n,cs in combos.items():
            self.assertEqual(len(cs),2 if n<=120 else 3 if n<=240 else 4)
            for x in cs: c.rgb(x['hex'])
    def test_contrast_reference_cases(self):
        self.assertAlmostEqual(c.contrast('#000000','#ffffff'),21)
        self.assertAlmostEqual(c.contrast('#417777','#417777'),1)
        self.assertLess(c.contrast('#777777','#ffffff'),4.5)
        self.assertGreater(c.contrast('#767676','#ffffff'),4.5)
    def test_recommend_exact_anchor_and_size(self):
        out=json.loads(self.cli('recommend','--hex','#ffb3f0','--size','3').stdout)
        self.assertEqual(out['palettes'][0]['id'],176)
        self.assertTrue(all(len(x['colors'])==3 for x in out['palettes']))
        self.assertIn('#ffb3f0',[x['hex'] for x in out['palettes'][0]['colors']])
    def test_invalid_inputs(self):
        for args in [('show','349'),('contrast','red','#ffffff'),('recommend','--limit','0'),('recommend','--hex','#xyzxyz')]:
            r=self.cli(*args); self.assertNotEqual(r.returncode,0); self.assertNotIn('Traceback',r.stderr)
    def test_export(self):
        r=self.cli('show','176','--format','css')
        self.assertEqual(r.returncode,0)
        self.assertIn('--wada-hermosa-pink: #ffb3f0;',r.stdout)
    def test_install_is_portable_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            cmd=[sys.executable,str(ROOT/'scripts/install.py'),'--project',d]
            subprocess.run(cmd,check=True,capture_output=True)
            for host in ('.agents','.claude'):
                skill=Path(d)/host/'skills/colors'
                r=subprocess.run([sys.executable,str(skill/'scripts/colors.py'),'show','176'],capture_output=True,text=True,check=True)
                self.assertEqual(json.loads(r.stdout)['id'],176)
            marker=Path(d)/'.agents/skills/colors/SKILL.md'
            marker.write_text('user changes')
            self.assertNotEqual(subprocess.run(cmd,capture_output=True).returncode,0)
            self.assertEqual(marker.read_text(),'user changes')
    def test_archive(self):
        with tempfile.TemporaryDirectory() as d:
            archive=Path(d)/'plugin.zip'
            subprocess.run([sys.executable,str(ROOT/'scripts/package.py'),str(archive)],check=True,capture_output=True)
            with zipfile.ZipFile(archive) as z:
                self.assertIsNone(z.testzip())
                self.assertTrue(all(n.startswith('sanzo-colors/') for n in z.namelist()))
                self.assertFalse(any('__pycache__' in n for n in z.namelist()))
                m=json.loads(z.read('sanzo-colors/plugin.json'))
                self.assertLessEqual(len(m['extensions']['com.openai']['interface']['shortDescription']),30)
                z.extractall(d)
            r=subprocess.run([sys.executable,str(Path(d)/'sanzo-colors/skills/colors/scripts/colors.py'),'show','176'],capture_output=True,check=True)
            self.assertEqual(json.loads(r.stdout)['id'],176)

if __name__=='__main__': unittest.main()
