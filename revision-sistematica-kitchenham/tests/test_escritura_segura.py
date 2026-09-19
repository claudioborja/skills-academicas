from pathlib import Path
import subprocess
import contextlib
import io
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import kitchenham_workspace as workspace


class BrokenValue:
    def __str__(self):
        raise ValueError('Dato CSV no serializable')


class StateWritesTests(unittest.TestCase):
    def test_bad_append_does_not_rewrite_or_extend_existing_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'registro.csv'
            original = b'old\r\nconservar\r\n'
            target.write_bytes(original)
            with self.assertRaises(ValueError):
                workspace.append_csv(target, ['id'], {'id': BrokenValue()})
            self.assertEqual(target.read_bytes(), original)
    def test_copy_failure_preserves_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp)/'original', Path(tmp)/'copia'
            source.write_bytes(b'Original completo')
            def fail(origin, output):
                output.write(b'Parcial')
                raise OSError('fallo al copiar')
            with patch.object(workspace.shutil, 'copyfileobj', side_effect=fail):
                with self.assertRaises(OSError):
                    workspace.copy_source(source, target)
            self.assertFalse(target.exists())
            self.assertEqual(source.read_bytes(), b'Original completo')
            target.write_bytes(b'Anterior')
            with self.assertRaises(ValueError):
                workspace.copy_source(source, target)
            self.assertEqual(target.read_bytes(), b'Anterior')

    def test_snapshot_is_valid_and_manifest_does_not_include_itself(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'proyecto'
            args = workspace.build_parser().parse_args(['init', '--project-dir', str(root), '--title', 'Prueba', '--topic', 'Software', '--question', 'Evidencia'])
            with contextlib.redirect_stdout(io.StringIO()):
                workspace.create_project(args)
            result = workspace.create_snapshot(root, 'planificacion')
            manifest = Path(result['manifest'])
            rows = workspace.read_csv(manifest)
            self.assertNotIn(manifest.relative_to(root).as_posix(), [r['path'] for r in rows])
            with workspace.zipfile.ZipFile(result['snapshot']) as archive:
                self.assertIsNone(archive.testzip())
                self.assertEqual(archive.read(manifest.relative_to(root).as_posix()), manifest.read_bytes())

    def test_snapshot_failure_does_not_publish_partial_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'proyecto'
            args = workspace.build_parser().parse_args(['init', '--project-dir', str(root), '--title', 'Prueba', '--topic', 'Software', '--question', 'Evidencia'])
            with contextlib.redirect_stdout(io.StringIO()):
                workspace.create_project(args)
            with patch.object(workspace.zipfile.ZipFile, 'write', side_effect=OSError('fallo al leer fuente')):
                with self.assertRaises(OSError):
                    workspace.create_snapshot(root, 'planificacion')
            self.assertEqual(list((root/'10_respaldo/02_snapshots').iterdir()), [])

    def test_project_rejects_linked_internal_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, outside = Path(tmp)/'proyecto', Path(tmp)/'externo'
            args = workspace.build_parser().parse_args(['init', '--project-dir', str(root), '--title', 'Prueba', '--topic', 'Software', '--question', 'Evidencia'])
            with contextlib.redirect_stdout(io.StringIO()):
                workspace.create_project(args)
            outside.mkdir()
            try:
                (root/'enlace').symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest('Enlaces no disponibles')
            with self.assertRaises(ValueError):
                workspace.require_project(root)

    def test_publication_failure_preserves_state_and_cleans_temporary_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'estado.json'
            target.write_bytes(b'{"fase":"original"}')
            with patch('archivos_seguros.os.replace', side_effect=OSError('disco no disponible')):
                with self.assertRaises(OSError):
                    workspace.write_json(target, {'fase': 'nuevo'})
            self.assertEqual(target.read_bytes(), b'{"fase":"original"}')
            self.assertEqual(list(Path(tmp).iterdir()), [target])

    def test_init_then_phase_update_persists_without_snapshot(self):
        with tempfile.TemporaryDirectory(prefix='revisión con espacios ') as tmp:
            root = Path(tmp)/'proyecto'
            command = [sys.executable, workspace.__file__]
            result = subprocess.run([*command, 'init', '--project-dir', str(root), '--title', 'Prueba', '--topic', 'Software', '--question', '¿Qué evidencia existe?'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = subprocess.run([*command, 'phase', '--project-dir', str(root), '--phase', 'preguntas', '--status', 'in_progress', '--note', 'Revisión inicial', '--no-snapshot'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            state = workspace.read_json(root/workspace.PROJECT_PATHS['state'])
            self.assertEqual(state['phases']['preguntas']['status'], 'in_progress')
            self.assertEqual(state['phases']['preguntas']['note'], 'Revisión inicial')
            self.assertFalse(list(root.rglob('*.zip')))

    def test_bad_csv_row_preserves_previous_matrix(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'matriz.csv'
            target.write_bytes(b'id\r\noriginal\r\n')
            with self.assertRaises(ValueError):
                workspace.write_csv(target, ['id'], [{'id': 'nuevo'}, {'id': BrokenValue()}])
            self.assertEqual(target.read_bytes(), b'id\r\noriginal\r\n')

    def test_state_updates_do_not_follow_symbolic_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            original, link = Path(tmp)/'original', Path(tmp)/'enlace'
            original.write_bytes(b'Conservar')
            try:
                link.symlink_to(original)
            except OSError:
                self.skipTest('Enlaces simbólicos no disponibles')
            for writer in (lambda: workspace.write_json(link, {'new': True}),
                           lambda: workspace.write_csv(link, ['id'], [{'id': 'nuevo'}])):
                with self.subTest(writer=writer):
                    try:
                        writer()
                    except ValueError:
                        pass
                    self.assertEqual(original.read_bytes(), b'Conservar')
                    self.assertTrue(link.is_symlink())

    def test_successful_state_updates_preserve_unicode_and_csv_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            state, matrix = Path(tmp)/'estado.json', Path(tmp)/'matriz.csv'
            workspace.write_json(state, {'fase': 'inicio'})
            workspace.write_json(state, {'fase': 'revisión'})
            self.assertEqual(workspace.read_json(state), {'fase': 'revisión'})
            rows = [{'id': '1', 'nota': 'Línea 1\nLínea 2, "cita"'}]
            workspace.write_csv(matrix, ['id', 'nota'], [])
            workspace.write_csv(matrix, ['id', 'nota'], rows)
            self.assertEqual(workspace.read_csv(matrix), rows)
