import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / 'workflow-maestro-academico-editorial/scripts/ejecutar.py'
sys.path.insert(0,str(LAUNCHER.parent))
from archivos_seguros import atomic_write, validate_outputs


class LauncherSafetyTests(unittest.TestCase):
    def test_output_cannot_be_parent_directory_of_another_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)/'informe'
            with self.assertRaises(ValueError):
                validate_outputs([], [parent, parent/'datos.json'])

    def test_parent_file_is_rejected_before_any_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)/'archivo'
            parent.write_bytes(b'Conservar')
            with self.assertRaises(ValueError):
                validate_outputs([], [Path(tmp)/'nuevo', parent/'datos.json'])
    def test_atomic_replace_failure_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'salida.txt'
            target.write_text('Original',encoding='utf-8')
            with patch('archivos_seguros.os.replace',side_effect=OSError('simulated disk failure')):
                with self.assertRaises(OSError):
                    atomic_write(target,'Nuevo',overwrite=True)
            self.assertEqual(target.read_text(encoding='utf-8'),'Original')
            self.assertEqual(list(Path(tmp).iterdir()),[target])

    def test_atomic_new_file_refuses_existing_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'salida.txt'
            atomic_write(target,'Uno')
            with self.assertRaises(ValueError):
                atomic_write(target,'Dos')
            self.assertEqual(target.read_text(encoding='utf-8'),'Uno')

    def test_hardlink_alias_is_an_input_collision(self):
        import os
        with tempfile.TemporaryDirectory() as tmp:
            source,target=Path(tmp)/'original.txt',Path(tmp)/'alias.txt'
            source.write_text('Uno',encoding='utf-8')
            try:
                os.link(source,target)
            except OSError:
                self.skipTest('Este sistema de archivos no permite enlaces duros')
            with self.assertRaises(ValueError):
                validate_outputs([source],[target],overwrite=True)

    def test_report_rejects_input_alias_before_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)/'original.md'
            source.write_text('# Texto\nContenido.\n',encoding='utf-8')
            result = subprocess.run([sys.executable,str(LAUNCHER),
                                     'auditor-documental-academico/scripts/check_preentrega.py',
                                     str(source),'--out='+str(source)],capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(source.read_text(encoding='utf-8'),'# Texto\nContenido.\n')

    def test_existing_report_needs_explicit_permission(self):
        with tempfile.TemporaryDirectory() as tmp:
            source,dest=Path(tmp)/'fuente.md',Path(tmp)/'reporte.md'
            source.write_text('Texto.\n',encoding='utf-8')
            dest.write_text('Anterior.\n',encoding='utf-8')
            args=['auditor-documental-academico/scripts/check_preentrega.py',str(source),'--out',str(dest)]
            denied=subprocess.run([sys.executable,str(LAUNCHER),*args],capture_output=True)
            self.assertNotEqual(denied.returncode,0)
            self.assertEqual(dest.read_text(encoding='utf-8'),'Anterior.\n')
            allowed=subprocess.run([sys.executable,str(LAUNCHER),'--permitir-sobrescritura',*args,'--overwrite'],capture_output=True)
            self.assertEqual(allowed.returncode,0,allowed.stderr)
            self.assertIn('Checklist',dest.read_text(encoding='utf-8'))
