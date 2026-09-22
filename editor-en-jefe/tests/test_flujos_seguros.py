from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import importlib.util
import os
import contextlib
import io

ROOT = Path(__file__).resolve().parents[2]


class PipelineSafetyTests(unittest.TestCase):
    def test_nonempty_chart_export_creates_readable_pngs(self):
        if importlib.util.find_spec('matplotlib') is None:
            self.skipTest('matplotlib opcional no instalado')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, out = root/'datos.json', root/'salida'
            source.write_text('[{"year":2024,"topic":"Educación","article_type":"original"}]',encoding='utf-8')
            env = dict(os.environ, MPLCONFIGDIR=str(root/'matplotlib'), MPLBACKEND='Agg')
            result = subprocess.run([sys.executable,str(ROOT/'explorador-temas-articulos/scripts/tabular_visualizar.py'),str(source),'--out-dir',str(out)],capture_output=True,env=env)
            self.assertEqual(result.returncode,0,result.stderr)
            import pymupdf
            pngs = list(out.glob('*.png'))
            self.assertEqual(len(pngs),3)
            for png in pngs:
                pix = pymupdf.Pixmap(str(png))
                self.assertGreater(pix.width,0)
                self.assertGreater(pix.height,0)
    def test_preprocessing_refuses_late_collision_before_first_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp)/'fuente.txt', Path(tmp)/'salida'
            source.write_text('Texto de prueba.', encoding='utf-8')
            out.mkdir()
            existing = out/'fuente-protegidos.json'
            existing.write_bytes(b'Conservar')
            cmd = [sys.executable,str(ROOT/'preprocesador-documentos/scripts/preprocesar_documento.py'),str(source),str(out)]
            result = subprocess.run(cmd,capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(list(out.iterdir()),[existing])
            self.assertEqual(existing.read_bytes(),b'Conservar')
            result = subprocess.run([*cmd,'--overwrite'],capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(len(list(out.iterdir())),6)

    def test_chart_reports_validate_all_outputs_and_prefix(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp)/'fuente.json', Path(tmp)/'salida'
            source.write_text('[]',encoding='utf-8')
            out.mkdir()
            existing = out/'exploracion_reporte.md'
            existing.write_bytes(b'Conservar')
            cmd = [sys.executable,str(ROOT/'explorador-temas-articulos/scripts/tabular_visualizar.py'),str(source),'--out-dir',str(out)]
            result = subprocess.run(cmd,capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(list(out.iterdir()),[existing])
            result = subprocess.run([*cmd,'--prefix','../escape'],capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse((Path(tmp)/'escape_tablas.json').exists())
            result = subprocess.run([*cmd,'--overwrite'],capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)

    def test_profile_pipeline_refuses_collision_without_partial_reports(self):
        sys.path.insert(0,str(ROOT/'humanizar-redaccion-academica/scripts'))
        import perfilar_y_comparar_estilo as pipeline
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root/'fuente.txt'
            source.write_text('Texto académico de prueba.',encoding='utf-8')
            out = root/'styles/prueba'
            out.mkdir(parents=True)
            existing = out/'manifest.json'
            existing.write_bytes(b'Conservar')
            argv = ['program','--model',str(source),'--draft',str(source),'--style-name','prueba']
            with patch.object(pipeline,'skill_root',return_value=root), patch.object(sys,'argv',argv), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises((SystemExit,ValueError)):
                    pipeline.main()
            self.assertEqual(list(out.iterdir()),[existing])
            self.assertEqual(existing.read_bytes(),b'Conservar')
            with patch.object(pipeline,'skill_root',return_value=root), patch.object(sys,'argv',argv+['--overwrite']), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(pipeline.main(),0)
            self.assertEqual(len(list(out.iterdir())),6)
