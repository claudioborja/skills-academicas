import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "diagnosticar_tesis.py"


class DiagnosticarTesisTest(unittest.TestCase):
    def test_json_reports_marker_location_context_and_section(self):
        source = """# Introducción\nTexto de contexto.\n## Resultados\nLos resultados obtenidos muestran un cambio.\nLa preresultados no es un marcador.\n"""
        with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as file:
            file.write(source)
            source_path = Path(file.name)
        self.addCleanup(source_path.unlink)

        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(source_path), "--json"],
            check=True,
            capture_output=True,
            text=True,
        )
        report = json.loads(completed.stdout)

        findings = [item for item in report["findings"] if item["marker"] == "resultados"]
        self.assertEqual(len(findings), 2)
        self.assertEqual(
            findings[0],
            {
                "category": "estructura_tesis",
                "marker": "resultados",
                "line": 3,
                "section": "Resultados",
                "excerpt": "## Resultados",
            },
        )
        self.assertEqual(findings[1]["line"], 4)
        self.assertEqual(findings[1]["section"], "Resultados")
        self.assertEqual(report["source"]["format"], "markdown")


if __name__ == "__main__":
    unittest.main()
