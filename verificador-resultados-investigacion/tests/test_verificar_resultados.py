"""Pruebas funcionales del verificador mecánico de resultados."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verificar_resultados.py"


class VerificarResultadosTests(unittest.TestCase):
    def run_audit(self, payload: dict, output_exists: bool = False):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        source = root / "resultados.json"
        output = root / "informe"
        source.write_text(json.dumps(payload), encoding="utf-8")
        if output_exists:
            output.mkdir()
            (output / "conservar.txt").write_text("original\n", encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--input", str(source), "--out-dir", str(output)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=20,
        )
        return completed, source, output

    def test_percentage_is_recalculated_and_verified(self):
        completed, _, output = self.run_audit(
            {
                "proyecto": "tesis-demo",
                "tolerancia": 0.01,
                "resultados": [
                    {
                        "id": "RES-001",
                        "ubicacion": "Tabla 4",
                        "afirmacion": "El 75 % respondió sí.",
                        "tipo": "porcentaje",
                        "reportado": 75,
                        "numerador": 30,
                        "denominador": 40,
                        "fuente": "base.csv:respuesta",
                    }
                ],
            }
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads((output / "informe-consolidado.json").read_text(encoding="utf-8"))
        self.assertEqual(report["resumen"], {"verificado": 1, "incorrecto": 0, "inconsistente": 0, "no_verificable": 0})
        self.assertEqual(report["resultados"][0]["esperado"], 75.0)
        self.assertFalse((output / "hallazgos").exists())

    def test_incorrect_percentage_gets_an_individual_explanation(self):
        completed, source, output = self.run_audit(
            {
                "proyecto": "tesis-demo",
                "resultados": [
                    {
                        "id": "RES-002",
                        "ubicacion": "Capítulo 5, p. 88",
                        "afirmacion": "El 70 % respondió sí.",
                        "tipo": "porcentaje",
                        "reportado": 70,
                        "numerador": 30,
                        "denominador": 40,
                        "fuente": "Tabla 4",
                    }
                ],
            }
        )

        self.assertEqual(completed.returncode, 1, completed.stderr)
        report = json.loads((output / "informe-consolidado.json").read_text(encoding="utf-8"))
        result = report["resultados"][0]
        self.assertEqual(result["estado"], "incorrecto")
        self.assertEqual(result["esperado"], 75.0)
        self.assertEqual(result["diferencia"], -5.0)
        self.assertIn("30 / 40", result["verificacion"])
        self.assertIn("corregir", result["intervencion_propuesta"].lower())
        individual = (output / "hallazgos" / "RES-002.md").read_text(encoding="utf-8")
        self.assertIn("Por qué está mal", individual)
        self.assertIn("Intervención propuesta", individual)
        self.assertIn("75", individual)
        self.assertIn('"reportado": 70', source.read_text(encoding="utf-8"))

    def test_sum_mean_and_group_total_use_hand_checked_values(self):
        completed, _, output = self.run_audit(
            {
                "proyecto": "tesis-demo",
                "resultados": [
                    {"id": "RES-010", "ubicacion": "T1", "afirmacion": "Total 15", "tipo": "suma", "reportado": 15, "componentes": [4, 5, 6], "fuente": "T1"},
                    {"id": "RES-011", "ubicacion": "T2", "afirmacion": "Media 4", "tipo": "media", "reportado": 4, "valores": [2, 4, 6], "fuente": "datos.csv"},
                    {"id": "RES-012", "ubicacion": "Método", "afirmacion": "n = 20", "tipo": "total_grupos", "reportado": 20, "grupos": [8, 7, 5], "fuente": "muestra.csv"},
                ],
            }
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads((output / "informe-consolidado.json").read_text(encoding="utf-8"))
        self.assertEqual([item["esperado"] for item in report["resultados"]], [15.0, 4.0, 20.0])
        self.assertTrue(all(item["estado"] == "verificado" for item in report["resultados"]))

    def test_repeated_values_are_flagged_as_inconsistent(self):
        completed, _, output = self.run_audit(
            {
                "proyecto": "tesis-demo",
                "resultados": [
                    {
                        "id": "RES-020",
                        "ubicacion": "Resumen",
                        "afirmacion": "Participaron 120 personas.",
                        "tipo": "consistencia",
                        "reportado": 120,
                        "apariciones": [
                            {"ubicacion": "Resultados", "valor": 118},
                            {"ubicacion": "Tabla 1", "valor": 120},
                        ],
                        "fuente": "manuscrito",
                    }
                ],
            }
        )

        self.assertEqual(completed.returncode, 1, completed.stderr)
        result = json.loads((output / "informe-consolidado.json").read_text(encoding="utf-8"))["resultados"][0]
        self.assertEqual(result["estado"], "inconsistente")
        self.assertIsNone(result["esperado"])
        self.assertIn("118", result["motivo"])
        self.assertIn("120", result["motivo"])

    def test_missing_inputs_are_not_guessed(self):
        completed, _, output = self.run_audit(
            {
                "proyecto": "tesis-demo",
                "resultados": [
                    {
                        "id": "RES-030",
                        "ubicacion": "Tabla 7",
                        "afirmacion": "El 42 % mejoró.",
                        "tipo": "porcentaje",
                        "reportado": 42,
                        "numerador": 21,
                        "fuente": "Tabla 7",
                    }
                ],
            }
        )

        self.assertEqual(completed.returncode, 1, completed.stderr)
        result = json.loads((output / "informe-consolidado.json").read_text(encoding="utf-8"))["resultados"][0]
        self.assertEqual(result["estado"], "no_verificable")
        self.assertIsNone(result["esperado"])
        self.assertIn("denominador", result["motivo"])
        self.assertNotIn("corregir a", result["intervencion_propuesta"].lower())

    def test_invalid_or_duplicate_ids_stop_before_writing_reports(self):
        completed, _, output = self.run_audit(
            {
                "proyecto": "tesis-demo",
                "resultados": [
                    {"id": "RES-001", "ubicacion": "A", "afirmacion": "x", "tipo": "suma", "reportado": 1, "componentes": [1], "fuente": "A"},
                    {"id": "RES-001", "ubicacion": "B", "afirmacion": "y", "tipo": "suma", "reportado": 2, "componentes": [2], "fuente": "B"},
                ],
            }
        )

        self.assertEqual(completed.returncode, 2)
        self.assertIn("duplicado", completed.stderr.lower())
        self.assertFalse(output.exists())

    def test_existing_output_directory_is_preserved(self):
        completed, _, output = self.run_audit(
            {"proyecto": "tesis-demo", "resultados": []}, output_exists=True
        )

        self.assertEqual(completed.returncode, 2)
        self.assertIn("ya existe", completed.stderr.lower())
        self.assertEqual((output / "conservar.txt").read_text(encoding="utf-8"), "original\n")


if __name__ == "__main__":
    unittest.main()
