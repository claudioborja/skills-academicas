from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from dependencias import check_dependencies


class DependencyTests(unittest.TestCase):
    def test_missing_and_different_versions_are_not_approved(self):
        with tempfile.TemporaryDirectory() as tmp:
            lock = Path(tmp) / 'lock.txt'
            lock.write_text('paquete-inexistente-de-prueba==1.0\n', encoding='utf-8')
            result = check_dependencies(lock)
            self.assertFalse(result['ok'])
            self.assertEqual(result['packages'][0]['status'], 'missing')
            with patch('dependencias.metadata.version', return_value='2.0'):
                result = check_dependencies(lock)
            self.assertEqual(result['packages'][0]['status'], 'version_mismatch')

    def test_unpinned_requirement_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            lock = Path(tmp) / 'lock.txt'
            lock.write_text('pypdf>=5\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                check_dependencies(lock)

    def test_installed_but_broken_import_is_not_approved(self):
        with tempfile.TemporaryDirectory() as tmp:
            lock = Path(tmp) / 'lock.txt'
            lock.write_text('pypdf==1.0\n', encoding='utf-8')
            with patch('dependencias.metadata.version', return_value='1.0'), \
                 patch('dependencias.importlib.import_module', side_effect=ImportError('roto')):
                result = check_dependencies(lock)
            self.assertFalse(result['ok'])
            self.assertEqual(result['packages'][0]['status'], 'import_error')
