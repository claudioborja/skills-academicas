"""Evitar entornos incompletos cuando falta el soporte de instalación."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import runtime_portable


class RuntimeTests(unittest.TestCase):
    def test_compatible_current_python_avoids_virtual_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp)
            (scripts / 'dependencias.py').write_text('raise SystemExit(0)\n', encoding='utf-8')
            (scripts / 'requirements-lock.txt').write_text('python-docx==1.2.0\n', encoding='utf-8')
            with patch.dict(os.environ, {}, clear=True), \
                 patch.object(runtime_portable, 'SCRIPTS', scripts), \
                 patch.object(runtime_portable, 'runtime_directory', side_effect=AssertionError('No debe crear entorno')):
                self.assertEqual(runtime_portable.select_python(prepare=True), sys.executable)

    def test_uses_the_script_lock_instead_of_the_complete_pdf_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp)
            dependency_probe = scripts / 'dependencias.py'
            dependency_probe.write_text('raise SystemExit(0)\n', encoding='utf-8')
            lock = scripts / 'codigo-lock.txt'
            lock.write_text('python-docx==1.2.0\n', encoding='utf-8')
            completed = subprocess.CompletedProcess([], 0, stdout='{}', stderr='')
            with patch.dict(os.environ, {}, clear=True), \
                 patch.object(runtime_portable, 'SCRIPTS', scripts), \
                 patch.object(runtime_portable.subprocess, 'run', return_value=completed) as run:
                self.assertEqual(runtime_portable.select_python(prepare=True, lock=lock), sys.executable)
            self.assertEqual(run.call_args.args[0][-2:], ['--lock', str(lock)])

    def test_explicit_runtime_uses_its_own_python_not_the_system_interpreter(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / 'shared-scripts'
            scripts.mkdir()
            (scripts / 'dependencias.py').write_text('raise SystemExit(0)\n', encoding='utf-8')
            lock = scripts / 'codigo-lock.txt'
            lock.write_text('python-docx==1.2.0\n', encoding='utf-8')
            runtime = Path(tmp) / 'skill' / '.runtime' / 'linux-x86_64-py314'
            isolated_python = runtime / 'bin' / 'python'
            completed = subprocess.CompletedProcess([], 0, stdout='{}', stderr='')
            with patch.object(runtime_portable, 'SCRIPTS', scripts), \
                 patch.object(runtime_portable, 'runtime_python', return_value=isolated_python), \
                 patch.object(runtime_portable, 'usable', return_value=True), \
                 patch.object(runtime_portable.subprocess, 'run', return_value=completed) as run:
                self.assertEqual(
                    runtime_portable.select_python(prepare=True, lock=lock, directory=runtime),
                    str(isolated_python),
                )
            self.assertEqual(run.call_args.args[0][0], str(isolated_python))

    def test_identifies_the_linux_bundled_interpreter_label(self):
        with patch.object(runtime_portable.sys, 'platform', 'linux'), \
             patch.object(runtime_portable.platform, 'machine', return_value='x86_64'):
            self.assertEqual(runtime_portable.bundled_label(), 'linux-x86_64-py314')

    def test_prefers_the_bundled_interpreter_over_creating_a_venv(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / 'shared-scripts'
            scripts.mkdir()
            (scripts / 'dependencias.py').write_text('raise SystemExit(0)\n', encoding='utf-8')
            lock = scripts / 'codigo-lock.txt'
            lock.write_text('python-docx==1.2.0\n', encoding='utf-8')
            directory = Path(tmp) / 'skill' / '.runtime' / 'linux-x86_64-py314'
            bundled = Path(tmp) / 'editor-en-jefe' / 'runtime' / 'python' / 'linux-x86_64-py314' / 'bin' / 'python'
            completed = subprocess.CompletedProcess([], 0, stdout='{}', stderr='')
            with patch.object(runtime_portable, 'SCRIPTS', scripts), \
                 patch.object(runtime_portable, 'bundled_python', return_value=bundled), \
                 patch.object(runtime_portable, 'usable', return_value=True), \
                 patch.object(runtime_portable.subprocess, 'run', return_value=completed) as run:
                self.assertEqual(runtime_portable.select_python(prepare=True, lock=lock, directory=directory), str(bundled))
            self.assertEqual(run.call_args.args[0][0], str(bundled))

    def test_uses_the_collection_bundle_instead_of_a_single_skill_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundled = root / 'editor-en-jefe/runtime/python/linux-x86_64-py314/bin/python'
            bundled.parent.mkdir(parents=True)
            bundled.write_bytes(b'python')
            directory = root / 'gestor-codigo-tecnico-editorial/.runtime/linux-x86_64-py314'
            with patch.object(runtime_portable, 'COLLECTION_ROOT', root), \
                 patch.object(runtime_portable.sys, 'platform', 'linux'), \
                 patch.object(runtime_portable.platform, 'machine', return_value='x86_64'):
                self.assertEqual(runtime_portable.bundled_python(directory), bundled)

    def test_prepare_refuses_version_drift_without_replacing_existing_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp)
            (scripts / 'dependencias.py').write_text(
                'import json\nprint(json.dumps({"ok": False, "packages": [{"status": "version_mismatch"}]}))\nraise SystemExit(1)\n',
                encoding='utf-8')
            (scripts / 'requirements-lock.txt').write_text('python-docx==1.2.0\n', encoding='utf-8')
            with patch.object(runtime_portable, 'SCRIPTS', scripts), \
                 patch.object(runtime_portable, 'runtime_python', return_value=Path(sys.executable)):
                with self.assertRaisesRegex(RuntimeError, 'versiones'):
                    runtime_portable.select_python(prepare=True)

    def test_missing_ensurepip_does_not_leave_partial_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'entorno nuevo'
            with patch.dict(os.environ, SKILLS_RUNTIME_DIR=str(target)):
                with patch('importlib.util.find_spec', return_value=None):
                    with self.assertRaisesRegex(RuntimeError, 'ensurepip'):
                        runtime_portable.select_python(prepare=True)
            self.assertFalse(target.exists())


if __name__ == '__main__':
    unittest.main()
