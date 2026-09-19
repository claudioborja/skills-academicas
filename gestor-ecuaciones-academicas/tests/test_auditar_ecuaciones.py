"""Pruebas funcionales del auditor de ecuaciones académicas."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "auditar_ecuaciones.py"


class AuditarEcuacionesTests(unittest.TestCase):
    def run_audit(self, source: Path, output: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(source), "--out", str(output), *extra],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=20,
        )

    def test_inventories_display_equations_and_resolves_equation_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "capitulo.md"
            output = root / "informe.json"
            source.write_text(
                """# Modelo

$$
E = mc^2
$$

\\begin{equation}
F = ma
\\label{eq:fuerza}
\\end{equation}

Como muestra \\eqref{eq:fuerza}, la fuerza depende de la aceleración.
""",
                encoding="utf-8",
            )

            result = self.run_audit(source, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["summary"], {"equations": 2, "errors": 0, "warnings": 0})
            self.assertEqual(report["references"], ["eq:fuerza"])
            self.assertEqual(report["equations"][1]["labels"], ["eq:fuerza"])

    def test_reports_duplicate_labels_and_missing_equation_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "articulo.tex"
            output = root / "informe.json"
            source.write_text(
                r"""\begin{equation}a=b\label{eq:dup}\end{equation}
\begin{align}c&=d\label{eq:dup}\end{align}
Véase \eqref{eq:ausente}.
""",
                encoding="utf-8",
            )

            result = self.run_audit(source, output)

            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(
                {issue["code"] for issue in report["issues"]},
                {"duplicate_label", "missing_equation_reference", "unreferenced_label"},
            )
            self.assertEqual(report["summary"]["errors"], 2)

    def test_reports_unclosed_display_math(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "borrador.md"
            output = root / "informe.json"
            source.write_text("Texto\n$$\nx + y = z\n", encoding="utf-8")

            result = self.run_audit(source, output)

            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["summary"]["equations"], 0)
            self.assertIn("unclosed_display_math", {issue["code"] for issue in report["issues"]})

    def test_does_not_replace_an_existing_report_without_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "capitulo.md"
            output = root / "informe.json"
            source.write_text("$$x=1$$\n", encoding="utf-8")
            output.write_text("conservar", encoding="utf-8")

            result = self.run_audit(source, output)

            self.assertEqual(result.returncode, 2)
            self.assertIn("ya existe", result.stderr)
            self.assertEqual(output.read_text(encoding="utf-8"), "conservar")


if __name__ == "__main__":
    unittest.main()
