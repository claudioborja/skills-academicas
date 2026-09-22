import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "editor-en-jefe" / "scripts" / "preparar_runtime_portable.py"
spec = importlib.util.spec_from_file_location("runtime_bundle", SCRIPT)
runtime_bundle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime_bundle)


class RuntimePortableBundleTests(unittest.TestCase):
    def test_uses_the_collection_lock_not_a_single_skill_lock(self):
        self.assertEqual(runtime_bundle.LOCK, ROOT / "requirements.txt")
        self.assertEqual(runtime_bundle.BUNDLE_ROOT, ROOT / "editor-en-jefe" / "runtime" / "python")


if __name__ == "__main__":
    unittest.main()
