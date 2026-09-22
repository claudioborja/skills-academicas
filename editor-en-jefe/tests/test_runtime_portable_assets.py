import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "editor-en-jefe" / "scripts" / "preparar_runtime_portable.py"
spec = importlib.util.spec_from_file_location("preparar_interpretes", SCRIPT)
preparar_interpretes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preparar_interpretes)


class PrepararInterpretesTests(unittest.TestCase):
    def test_selects_the_four_supported_platform_assets(self):
        assets = [
            {"name": "cpython-3.14.7+20260901-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz"},
            {"name": "cpython-3.14.7+20260901-x86_64-pc-windows-msvc-install_only_stripped.tar.gz"},
            {"name": "cpython-3.14.7+20260901-x86_64-apple-darwin-install_only_stripped.tar.gz"},
            {"name": "cpython-3.14.7+20260901-aarch64-apple-darwin-install_only_stripped.tar.gz"},
        ]
        selected = preparar_interpretes.select_assets(assets, "3.14")

        self.assertEqual(set(selected), {
            "linux-x86_64-py314", "windows-x86_64-py314",
            "macos-x86_64-py314", "macos-arm64-py314",
        })
        self.assertTrue(all(item["name"].endswith("install_only_stripped.tar.gz") for item in selected.values()))

    def test_finds_the_windows_python_executable_from_the_target_label(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            interpreter = root / "python" / "python.exe"
            interpreter.parent.mkdir()
            interpreter.write_bytes(b"portable python")
            self.assertEqual(
                preparar_interpretes.python_root(root, "windows-x86_64-py314"),
                interpreter.parent,
            )

    def test_declares_a_wheel_platform_for_every_bundled_interpreter(self):
        self.assertEqual(preparar_interpretes.wheel_platform("linux-x86_64-py314"), ["manylinux_2_28_x86_64", "manylinux_2_17_x86_64"])
        self.assertEqual(preparar_interpretes.wheel_platform("windows-x86_64-py314"), ["win_amd64"])
        self.assertEqual(preparar_interpretes.wheel_platform("macos-x86_64-py314"), ["macosx_10_13_x86_64"])
        self.assertEqual(preparar_interpretes.wheel_platform("macos-arm64-py314"), ["macosx_11_0_arm64"])

    def test_lock_uses_the_lxml_version_available_for_every_supported_platform(self):
        lock = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("lxml==6.0.2", lock)

    def test_lock_uses_the_pymupdf_version_available_for_macos_intel(self):
        lock = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("pymupdf==1.27.2.3", lock)

    def test_lock_uses_the_pillow_version_with_cpython_314_wheels_for_every_target(self):
        lock = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("pillow==11.3.0", lock)

    def test_lock_uses_the_matplotlib_version_with_cpython_314_wheels_for_macos_intel(self):
        lock = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("matplotlib==3.10.9", lock)

    def test_lock_uses_the_kiwisolver_version_with_cpython_314_wheels_for_macos_intel(self):
        lock = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("kiwisolver==1.4.9", lock)

    def test_lock_uses_the_numpy_version_with_cpython_314_wheels_for_macos_intel(self):
        lock = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("numpy==2.3.3", lock)


if __name__ == "__main__":
    unittest.main()
