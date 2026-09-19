"""Evitar entornos incompletos cuando falta el soporte de instalación."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import runtime_portable


class RuntimeTests(unittest.TestCase):
    def test_prepare_refuses_version_drift_without_replacing_existing_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp)
            (scripts / 'dependencias.py').write_text(
                'import json\nprint(json.dumps({"ok": False, "packages": [{"status": "version_mismatch"}]}))\nraise SystemExit(1)\n',
                encoding='utf-8')
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
