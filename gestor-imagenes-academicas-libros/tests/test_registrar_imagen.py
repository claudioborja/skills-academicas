"""Pruebas de coherencia académica del manifiesto de imágenes."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/registrar_imagen.py'
SPEC = importlib.util.spec_from_file_location('registrar_imagen_en_pruebas', SCRIPT)
REGISTRAR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REGISTRAR)


class RegistrarImagenTests(unittest.TestCase):
    def traceability_arguments(self, root, identifier):
        asset = root / f'{identifier}.png'
        asset.write_bytes(b'contenido visual')
        return [
            '--id', identifier, '--numero-figura', 'Figura 1', '--capitulo', '1',
            '--ubicacion', 'Después del párrafo 1', '--fecha-creacion', '2026-04-05',
            '--archivo', str(asset),
        ]

    def generated_arguments(self, root, identifier='fig-1'):
        return [
            *self.traceability_arguments(root, identifier),
            '--titulo', 'Ilustración conceptual',
            '--origen', 'generada', '--metodo', 'ia_generativa',
            '--funcion', 'ilustracion', '--necesidad', 'Explicar el proceso',
            '--modelo', 'Modelo', '--prompt', 'Prompt',
            '--razon-generacion', 'Razón', '--busqueda-previa', 'Búsqueda',
            '--anexo', str(root / 'anexo.md'),
        ]

    def run_registrar(self, root, *arguments):
        manifest = root / 'manifiesto.jsonl'
        result = subprocess.run(
            [sys.executable, str(SCRIPT), '--manifest', str(manifest), *arguments],
            capture_output=True, text=True, encoding='utf-8', timeout=20,
        )
        return result, manifest

    def test_rejects_generated_image_classified_as_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result, manifest = self.run_registrar(
                root, *self.traceability_arguments(root, 'fig-1'),
                '--titulo', 'Resultado experimental',
                '--origen', 'generada', '--metodo', 'ia_generativa',
                '--funcion', 'evidencia', '--necesidad', 'Documentar el resultado',
                '--modelo', 'Modelo', '--prompt', 'Prompt',
                '--razon-generacion', 'Razón', '--busqueda-previa', 'Búsqueda',
                '--anexo', str(root / 'anexo.md'),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(manifest.exists())

    def test_rejects_adaptation_without_source_license_and_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result, manifest = self.run_registrar(
                root, *self.traceability_arguments(root, 'fig-2'),
                '--titulo', 'Diagrama adaptado',
                '--origen', 'adaptada', '--metodo', 'manual',
                '--funcion', 'adaptacion', '--necesidad', 'Explicar el proceso',
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(manifest.exists())

    def test_rejects_duplicate_identifier_without_changing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / 'manifiesto.jsonl'
            original = b'{"id":"fig-3","titulo":"Anterior"}\n'
            manifest.write_bytes(original)
            result, _ = self.run_registrar(root, *self.generated_arguments(root, 'fig-3'))
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(manifest.read_bytes(), original)
            self.assertFalse((root / 'anexo.md').exists())

    def test_second_write_failure_restores_manifest_and_annex(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, annex = root / 'manifiesto.jsonl', root / 'anexo.md'
            manifest_before = b'{"id":"anterior"}\r\n'
            annex_before = '# Anexo existente\r\n'.encode('utf-8')
            manifest.write_bytes(manifest_before)
            annex.write_bytes(annex_before)
            real_append = REGISTRAR.atomic_append
            writes = 0

            def fail_second_write(path, data):
                nonlocal writes
                writes += 1
                if writes == 2:
                    raise OSError('fallo simulado en la segunda publicación')
                return real_append(path, data)

            arguments = ['registrar_imagen.py', '--manifest', str(manifest),
                         *self.generated_arguments(root, 'fig-4')]
            with patch.object(REGISTRAR, 'atomic_append', side_effect=fail_second_write), \
                    patch.object(sys, 'argv', arguments), self.assertRaises(OSError):
                REGISTRAR.main()
            self.assertEqual(manifest.read_bytes(), manifest_before)
            self.assertEqual(annex.read_bytes(), annex_before)

    def test_records_complete_traceability_with_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            work, original = root / 'figura-final.png', root / 'figura-original.png'
            png, pdf = root / 'figura-web.png', root / 'figura-impresion.pdf'
            work.write_bytes(b'final')
            original.write_bytes(b'original')
            png.write_bytes(b'derivado png')
            pdf.write_bytes(b'derivado pdf')
            result, manifest = self.run_registrar(
                root, '--id', 'fig-5', '--numero-figura', 'Figura 3.2',
                '--capitulo', '3', '--ubicacion', 'Resultados, después del párrafo 4',
                '--fecha-creacion', '2026-04-05', '--estado-revision', 'aprobada',
                '--titulo', 'Modelo conceptual', '--origen', 'elaboracion_propia',
                '--metodo', 'manual', '--funcion', 'ilustracion',
                '--necesidad', 'Explicar relaciones', '--archivo', str(work),
                '--archivo-original', str(original), '--derivado', str(png),
                '--derivado', str(pdf),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            record = json.loads(manifest.read_text(encoding='utf-8'))
            self.assertEqual(record['numero_figura'], 'Figura 3.2')
            self.assertEqual(record['capitulo'], '3')
            self.assertEqual(record['ubicacion_prevista'], 'Resultados, después del párrafo 4')
            self.assertEqual(record['fecha_creacion'], '2026-04-05')
            self.assertEqual(record['estado_revision'], 'aprobada')
            self.assertEqual(Path(record['archivo_original']['ruta']), original.resolve())
            self.assertEqual(len(record['derivados']), 2)
            self.assertTrue(all(item['sha256'] for item in record['derivados']))

    def test_rejects_missing_required_traceability(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            work = root / 'figura.png'
            work.write_bytes(b'figura')
            result, manifest = self.run_registrar(
                root, '--id', 'fig-6', '--titulo', 'Figura sin ubicación',
                '--origen', 'elaboracion_propia', '--metodo', 'manual',
                '--funcion', 'ilustracion', '--necesidad', 'Explicar',
                '--archivo', str(work),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(manifest.exists())

    def test_rejects_future_creation_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            arguments = self.traceability_arguments(root, 'fig-7')
            arguments[arguments.index('--fecha-creacion') + 1] = '2999-01-01'
            result, manifest = self.run_registrar(
                root, *arguments, '--titulo', 'Figura futura',
                '--origen', 'elaboracion_propia', '--metodo', 'manual',
                '--funcion', 'ilustracion', '--necesidad', 'Explicar',
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(manifest.exists())


if __name__ == '__main__':
    unittest.main()
