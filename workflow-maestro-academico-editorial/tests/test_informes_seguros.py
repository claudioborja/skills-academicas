"""Regresiones de conservación al invocar los informes sin el lanzador."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = [
    'preprocesador-documentos/scripts/documento_a_markdown.py',
    'preprocesador-documentos/scripts/segmentar_manuscrito.py',
    'preprocesador-documentos/scripts/proteger_bloques.py',
    'explorador-temas-articulos/scripts/clasificar_literatura.py',
    'explorador-temas-articulos/scripts/matriz_estado_arte.py',
    'explorador-temas-articulos/scripts/proponer_temas.py',
    'explorador-temas-articulos/scripts/seleccionar_metodologia.py',
    'explorador-temas-articulos/scripts/cribar_fuentes_revision.py',
    'humanizar-redaccion-academica/scripts/documento_a_perfil_estilo.py',
    'auditor-articulo-imryd/scripts/auditar_imryd.py',
    'auditor-articulo-imryd/scripts/check_envio_revista.py',
    'auditor-articulo-imryd/scripts/matriz_objetivo_metodo_resultados.py',
    'auditor-documental-academico/scripts/analizar_repeticiones.py',
    'auditor-documental-academico/scripts/auditar_terminologia.py',
    'auditor-documental-academico/scripts/check_preentrega.py',
    'auditor-documental-academico/scripts/inventariar_documento.py',
    'auditor-documental-academico/scripts/inventariar_tablas_figuras.py',
    'automatizador-referencias/scripts/auditar_citas_bibliografia.py',
    'automatizador-referencias/scripts/normalizar_referencias.py',
    'respondedor-observaciones-academicas/scripts/observaciones_a_matriz.py',
]
ORIGINAL = '# Introducción\nTexto de prueba [1].\n\n# Referencias\n[1] A. Autor, Libro, 2024.\n'


class DirectReportSafetyTests(unittest.TestCase):
    def run_case(self, mode):
        for script in SCRIPTS:
            with self.subTest(script=script, mode=mode), tempfile.TemporaryDirectory(prefix='informes con espacios ') as tmp:
                source = Path(tmp) / 'original.md'
                out = Path(tmp) / 'informe.md'
                data = Path(tmp) / 'datos.json'
                source.write_text(ORIGINAL, encoding='utf-8')
                extra = []
                if mode in ('source', 'source_force'):
                    data = source
                    if mode == 'source_force':
                        extra = ['--overwrite']
                elif mode == 'existing':
                    data.write_text('Conservar', encoding='utf-8')
                elif mode == 'duplicate':
                    data = out
                elif mode == 'overwrite':
                    out.write_text('Anterior', encoding='utf-8')
                    extra = ['--overwrite']
                result = subprocess.run([sys.executable, str(ROOT / script), str(source),
                                         '--out', str(out), '--json-out', str(data), *extra],
                                        capture_output=True, text=True)
                self.assertEqual(source.read_text(encoding='utf-8'), ORIGINAL)
                if mode in ('fresh', 'overwrite'):
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertTrue(out.read_text(encoding='utf-8').startswith('#'))
                    json.loads(data.read_text(encoding='utf-8'))
                else:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn('salida', result.stderr.lower())
                    self.assertFalse(out.exists())
                    if mode == 'existing':
                        self.assertEqual(data.read_text(encoding='utf-8'), 'Conservar')

    def test_new_reports_are_generated(self):
        self.run_case('fresh')

    def test_json_cannot_replace_source_before_first_output(self):
        self.run_case('source')

    def test_existing_second_output_prevents_first_write(self):
        self.run_case('existing')

    def test_overwrite_never_authorizes_replacing_source(self):
        self.run_case('source_force')

    def test_outputs_cannot_share_a_path(self):
        self.run_case('duplicate')

    def test_explicit_overwrite_replaces_reports(self):
        self.run_case('overwrite')
