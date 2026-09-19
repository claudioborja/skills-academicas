import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import contextlib
import io

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'humanizar-redaccion-academica/scripts'))
import documento_a_perfil_estilo as profiler


class RemainingReportsTests(unittest.TestCase):
    def test_csv_collision_prevents_markdown_publication(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, out = root/'fuentes.csv', root/'informe.md'
            source.write_bytes(b'title,year\r\nPrueba,2024\r\n')
            for script in ('clasificar_literatura.py','matriz_estado_arte.py','cribar_fuentes_revision.py'):
                with self.subTest(script=script):
                    result = subprocess.run([sys.executable,str(ROOT/'explorador-temas-articulos/scripts'/script),str(source),'--out',str(out),'--csv-out',str(source),'--overwrite'],capture_output=True)
                    self.assertNotEqual(result.returncode,0)
                    self.assertFalse(out.exists())
                    self.assertEqual(source.read_bytes(),b'title,year\r\nPrueba,2024\r\n')

    def test_watchlist_cannot_be_replaced(self):
        watchlist = ROOT/'filtro-editoriales-depredadoras/references/watchlist.json'
        # Invocar main con el publicador interceptado evita arriesgar el recurso real en una regresión.
        from unittest.mock import patch
        sys.path.insert(0,str(ROOT/'filtro-editoriales-depredadoras/scripts'))
        import check_editorial_risk as risk
        cmd = ['risk','Revista de prueba','--out',str(watchlist),'--overwrite']
        with patch.object(sys,'argv',cmd), patch.object(risk,'atomic_write',side_effect=AssertionError('Intento de escribir la fuente')), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                risk.main()
    def cases(self, folder):
        source, profile = folder/'original.md', folder/'perfil.json'
        source.write_text('# Texto\nContenido de prueba sin DOI.', encoding='utf-8')
        profile.write_text(json.dumps(profiler.build_profile([source])), encoding='utf-8')
        manifest = folder/'fuentes.json'
        manifest.write_text('[]', encoding='utf-8')
        import pymupdf
        pdf = folder/'informe.pdf'
        doc = pymupdf.open()
        doc.new_page().insert_text((72,72), 'Reporte de prueba')
        doc.save(pdf)
        doc.close()
        return [
            ('automatizador-referencias/scripts/doi_a_referencia.py', [str(source),'--from-file'], [source]),
            ('automatizador-referencias/scripts/inventario_fuentes.py', [str(source)], [source]),
            ('filtro-editoriales-depredadoras/scripts/check_editorial_risk.py', ['--file',str(source)], [source]),
            ('explorador-temas-articulos/scripts/generar_protocolo_revision.py', ['--topic','Educación'], []),
            ('humanizar-redaccion-academica/scripts/comparar_con_perfil_estilo.py', [str(source),'--profile',str(profile)], [source,profile]),
            ('humanizar-redaccion-academica/scripts/analizar_reporte_compilatio.py', [str(pdf)], [pdf]),
            ('humanizar-redaccion-academica/scripts/resumir_alertas_respaldo_citas.py', [str(source)], [source]),
            ('humanizar-redaccion-academica/scripts/auditar_respaldo_citas_pdf.py', [str(folder),'--book',str(source),'--manifest',str(manifest)], [source,manifest]),
            ('gestor-tablas-figuras-pies/scripts/exportar_tablas_html.py', [str(source)], [source]),
        ]

    def test_reports_create_refuse_existing_and_allow_explicit_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            for script, args, inputs in self.cases(Path(tmp)):
                with self.subTest(script=script):
                    out = Path(tmp)/(Path(script).stem+'.out')
                    cmd = [sys.executable,str(ROOT/script),*args,'--out',str(out)]
                    fresh = subprocess.run(cmd, capture_output=True)
                    self.assertEqual(fresh.returncode,0,fresh.stderr)
                    self.assertTrue(out.read_bytes())
                    out.write_bytes(b'Conservar')
                    denied = subprocess.run(cmd,capture_output=True)
                    self.assertNotEqual(denied.returncode,0)
                    self.assertEqual(out.read_bytes(),b'Conservar')
                    allowed = subprocess.run([*cmd,'--overwrite'],capture_output=True)
                    self.assertEqual(allowed.returncode,0,allowed.stderr)
                    self.assertNotEqual(out.read_bytes(),b'Conservar')

    def test_every_input_is_protected_even_with_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            for script,args,inputs in self.cases(Path(tmp)):
                for source in inputs:
                    with self.subTest(script=script,source=source):
                        before = source.read_bytes()
                        result = subprocess.run([sys.executable,str(ROOT/script),*args,'--out',str(source),'--overwrite'],capture_output=True)
                        self.assertNotEqual(result.returncode,0)
                        self.assertIn(b'salida',result.stderr.lower())
                        self.assertEqual(source.read_bytes(),before)
