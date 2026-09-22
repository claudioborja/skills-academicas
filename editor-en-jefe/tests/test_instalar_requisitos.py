import importlib.util
import ast
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/instalar_requisitos.py'
spec = importlib.util.spec_from_file_location('installer', SCRIPT)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def test_flat_requirements_cover_all_profiles_and_direct_imports(self):
        root = SCRIPT.parents[2]
        packaged = SCRIPT.with_name('requirements.txt')
        source = root / 'requirements.txt'
        if source.exists():
            self.assertEqual(source.read_bytes(), packaged.read_bytes())
        def entries(path):
            lines = [line.strip() for line in path.read_text().splitlines()
                     if line.strip() and not line.lstrip().startswith('#')]
            self.assertTrue(all('==' in line and not line.startswith('-') for line in lines))
            return set(lines)
        full = entries(packaged)
        self.assertEqual(len(full), 17)
        for relative in ['preprocesador-documentos/scripts/requirements-lock.txt',
                         'gestor-imagenes-academicas-libros/scripts/requirements-lock.txt',
                         'explorador-temas-articulos/scripts/requirements-graficos-lock.txt',
                         'editor-en-jefe/scripts/requirements-mantenimiento.txt']:
            self.assertTrue(entries(root / relative) <= full, relative)
        mapping = {'PIL': 'pillow', 'docx': 'python-docx', 'pymupdf': 'pymupdf',
                   'pypdf': 'pypdf', 'matplotlib': 'matplotlib', 'yaml': 'pyyaml'}
        names = {line.split('==')[0].lower() for line in full}
        catalog = (root / 'editor-en-jefe/references/mapa-responsabilidades.md').read_text()
        collection = set(re.findall(r'`([a-z0-9-]+)`', catalog)) | {'editor-en-jefe'}
        scripts = [path for name in collection for path in (root / name / 'scripts').glob('*.py')]
        local = {path.stem for path in scripts}
        for path in scripts:
            for node in ast.walk(ast.parse(path.read_text(encoding='utf-8-sig'))):
                imports = ([alias.name for alias in node.names] if isinstance(node, ast.Import)
                           else [node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
                for module in imports:
                    module = module.split('.')[0]
                    if module not in sys.stdlib_module_names and module not in local:
                        self.assertIn(mapping.get(module, module.lower()), names, f'{path}: {module}')

    def test_default_checks_current_python_without_creating_environment(self):
        completed = subprocess.CompletedProcess([], 0, stdout='3 14')
        with patch.object(sys, 'argv', [str(SCRIPT), '--comprobar']), \
             patch.object(installer, 'probe', return_value=[{'packages': [{'name': 'x', 'status': 'ok'}]}]) as probe, \
             patch.object(installer.subprocess, 'run', return_value=completed) as run:
            self.assertEqual(installer.main(), 0)
        self.assertEqual(probe.call_args.args[0], Path(sys.executable))
        commands = [call.args[0] for call in run.call_args_list]
        self.assertFalse(any('venv' in command or 'install' in command for command in commands))

    def test_complete_environment_does_not_install(self):
        self.assertFalse(installer.installation_needed([{'packages': [{'name': 'x', 'status': 'ok'}]}]))

    def test_missing_dependency_needs_install(self):
        self.assertTrue(installer.installation_needed([{'packages': [{'name': 'x', 'status': 'missing'}]}]))

    def test_incompatible_or_broken_dependency_is_not_overwritten(self):
        for status in ['version_mismatch', 'import_error']:
            with self.subTest(status=status), self.assertRaises(RuntimeError):
                installer.installation_needed([{'packages': [{'name': 'x', 'status': status}]}])

    def test_check_from_another_directory_does_not_create_environment(self):
        with tempfile.TemporaryDirectory(prefix='requisitos á ') as tmp:
            target = Path(tmp) / 'entorno nuevo'
            result = subprocess.run([sys.executable, str(SCRIPT), '--comprobar', '--entorno', str(target)],
                                    cwd=tmp, capture_output=True, text=True, encoding='utf-8',
                                    env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertFalse(target.exists())


if __name__ == '__main__':
    unittest.main()
