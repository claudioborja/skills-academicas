from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validar_coleccion import compare_collections, discover_skills, run_tests, validate_collection


class CollectionTests(unittest.TestCase):
    def fixture(self, root):
        skill = root / 'prueba'
        skill.mkdir(parents=True)
        (skill / 'SKILL.md').write_text('---\nname: prueba\ndescription: Prueba\n---\n', encoding='utf-8')
        return skill

    def test_empty_collection_is_not_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                discover_skills(Path(tmp))

    def test_comparison_detects_changed_missing_and_extra_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, other = Path(tmp)/'local', Path(tmp)/'instalado'
            a, b = self.fixture(root), self.fixture(other)
            (a/'changed.txt').write_text('nuevo')
            (b/'changed.txt').write_text('viejo')
            (a/'missing.txt').write_text('falta')
            (b/'extra.txt').write_text('sobra')
            self.fixture(other/'ajenas')
            (b/'.runtime').mkdir()
            (b/'.runtime/ignorar').write_text('entorno')
            result = compare_collections(root, other, ['prueba'])
            self.assertEqual({x['kind'] for x in result['differences']}, {'changed', 'missing', 'extra'})
            self.assertEqual(len(result['differences']), 3)

    def test_same_root_is_not_a_valid_comparison(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.fixture(Path(tmp))
            with self.assertRaises(ValueError):
                compare_collections(Path(tmp), Path(tmp), ['prueba'])

    def test_real_failing_and_skipped_tests_are_not_green(self):
        with tempfile.TemporaryDirectory() as tmp:
            suite = self.fixture(Path(tmp))/'tests'
            suite.mkdir()
            file = suite/'test_sample.py'
            file.write_text('import unittest\nclass T(unittest.TestCase):\n def test_bad(self): self.fail("fallo real")\n', encoding='utf-8')
            result = run_tests(Path(sys.executable), suite, 20)
            self.assertEqual(result['status'], 'failed')
            self.assertEqual(result['count'], 1)
            file.write_text('import unittest\nclass T(unittest.TestCase):\n @unittest.skip("pendiente")\n def test_skip(self): pass\n', encoding='utf-8')
            result = run_tests(Path(sys.executable), suite, 20)
            self.assertEqual(result['status'], 'partial')
            self.assertEqual(result['skipped'], 1)

    def test_zero_tests_is_not_green(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_tests(Path(sys.executable), Path(tmp), 20)
            self.assertNotEqual(result['status'], 'passed')

    def test_tests_and_children_use_selected_python_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            suite = Path(tmp)
            (suite/'test_environment.py').write_text(
                'import os, sys, unittest\n'
                'class T(unittest.TestCase):\n'
                ' def test_environment(self):\n'
                '  self.assertEqual(os.environ.get("SKILLS_RUNTIME_DIR"), sys.prefix)\n',
                encoding='utf-8')
            result = run_tests(Path(sys.executable), suite, 20)
            self.assertEqual(result['status'], 'passed', result['output'])

    def test_collection_validation_checks_image_dependency_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, other = Path(tmp) / 'local', Path(tmp) / 'instalado'
            for collection in (root, other):
                skill = self.fixture(collection)
                tests = skill / 'tests'
                tests.mkdir()
                (tests / 'test_ok.py').write_text(
                    'import unittest\nclass T(unittest.TestCase):\n def test_ok(self): self.assertTrue(True)\n',
                    encoding='utf-8')
                probe = collection / 'preprocesador-documentos/scripts/dependencias.py'
                probe.parent.mkdir(parents=True)
                probe.write_text(
                    'import argparse\nfrom pathlib import Path\n'
                    'p=argparse.ArgumentParser(); p.add_argument("--lock"); a=p.parse_args()\n'
                    'raise SystemExit(0 if not a.lock or Path(a.lock).is_file() else 1)\n',
                    encoding='utf-8')
                for lock in (
                    collection / 'explorador-temas-articulos/scripts/requirements-graficos-lock.txt',
                    collection / 'gestor-imagenes-academicas-libros/scripts/requirements-lock.txt',
                    collection / 'workflow-maestro-academico-editorial/scripts/requirements-mantenimiento.txt',
                ):
                    lock.parent.mkdir(parents=True, exist_ok=True)
                    lock.write_text('paquete==1\n', encoding='utf-8')
            validator = Path(tmp) / 'validator.py'
            validator.write_text('raise SystemExit(0)\n', encoding='utf-8')
            report = validate_collection(root, other, validator, sys.executable, sys.executable, 20)
            profiles = [item['profile'] for item in report['dependencies']]
            self.assertEqual(profiles.count('images'), 2)
