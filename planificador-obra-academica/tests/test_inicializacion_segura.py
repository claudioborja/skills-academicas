from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1]/'scripts/inicializar_proyecto_libro.py'


class InitializationTests(unittest.TestCase):
    def test_initializes_editorial_register_for_session_continuity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proyecto'
            result = self.run_init(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            register = root / '01_planificacion_editorial/03_registro_editorial.md'
            self.assertTrue(register.is_file())
            content = register.read_text(encoding='utf-8')
            self.assertIn('## Decisiones vigentes', content)
            self.assertIn('## Estado de capítulos', content)
            self.assertIn('## Requisitos y controles', content)
            self.assertIn('## Pendientes y próxima acción', content)

    def run_init(self, root, *options):
        return subprocess.run([sys.executable, str(SCRIPT), str(root), '--title', 'Obra de prueba', *options], capture_output=True, text=True)

    def test_merge_rejects_linked_directory_before_creating_anything(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, outside = Path(tmp)/'proyecto', Path(tmp)/'ajeno'
            root.mkdir()
            outside.mkdir()
            link = root/'01_planificacion_editorial'
            try:
                link.symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest('Enlaces simbólicos no disponibles')
            result = self.run_init(root, '--merge')
            self.assertEqual(list(outside.iterdir()), [])
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(root.iterdir()), [link])

    def test_merge_rejects_directory_in_place_of_file_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'proyecto'
            conflict = root/'estado_proyecto.json'
            conflict.mkdir(parents=True)
            result = self.run_init(root, '--merge')
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(root.iterdir()), [conflict])

    def test_merge_preserves_user_files_and_dry_run_creates_nothing(self):
        with tempfile.TemporaryDirectory(prefix='proyecto con espacios ') as tmp:
            root = Path(tmp)/'obra'
            result = self.run_init(root, '--dry-run')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(root.exists())
            result = self.run_init(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            source = root/'00_indice_maestro.md'
            source.write_bytes(b'Contenido del usuario\r\n')
            state = (root/'estado_proyecto.json').read_bytes()
            result = self.run_init(root, '--merge')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(source.read_bytes(), b'Contenido del usuario\r\n')
            self.assertEqual((root/'estado_proyecto.json').read_bytes(), state)
