"""Pruebas funcionales del selector de control editorial para libros."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "seleccionar_control.py"


class SeleccionarControlTests(unittest.TestCase):
    def run_selector(self, payload: dict, *extra: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "contexto.json"
            source.write_text(json.dumps(payload), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(source), *extra],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=20,
            )

    def parse_success(self, payload: dict) -> dict:
        result = self.run_selector(payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_thesis_book_with_integral_authorship_uses_complete_work_front_matter(self):
        report = self.parse_success(
            {
                "tipo_obra": "tesis-convertida",
                "autoria_capitulos": "integral",
                "etapa": "prepublicacion",
                "objetivo_bkci": False,
            }
        )

        self.assertEqual(report["perfil_front_matter"], "obra-completa")
        self.assertEqual(report["estado"], "PERFIL_RECOMENDADO")
        self.assertIn("control-tecnico-prepublicacion", report["controles"])
        self.assertNotIn("preevaluacion-bkci", report["controles"])
        self.assertTrue(report["recursos"]["plantilla"].endswith("04_Plantilla_front_matter_obra_completa_EUC.docx"))

    def test_edited_book_with_independent_chapters_adds_bkci_when_requested(self):
        report = self.parse_success(
            {
                "tipo_obra": "volumen-editado",
                "autoria_capitulos": "independiente",
                "etapa": "pre-revision",
                "objetivo_bkci": True,
            }
        )

        self.assertEqual(report["perfil_front_matter"], "libro-por-capitulos")
        self.assertIn("control-admisibilidad", report["controles"])
        self.assertIn("preevaluacion-bkci", report["controles"])
        self.assertIn("no garantiza", " ".join(report["advertencias"]).lower())
        self.assertTrue(report["recursos"]["perfil_bkci"].endswith("03_Guia_18_criterios_BKCI_EUC.docx"))

    def test_unknown_chapter_authorship_requires_a_decision_instead_of_guessing(self):
        report = self.parse_success(
            {
                "tipo_obra": "monografia",
                "autoria_capitulos": "por-determinar",
                "etapa": "recepcion",
                "objetivo_bkci": False,
            }
        )

        self.assertIsNone(report["perfil_front_matter"])
        self.assertEqual(report["estado"], "REQUIERE_DECISION_EDITORIAL")
        self.assertIn("autoría", " ".join(report["decisiones_pendientes"]).lower())

    def test_rejects_invalid_stage(self):
        result = self.run_selector(
            {
                "tipo_obra": "monografia",
                "autoria_capitulos": "integral",
                "etapa": "publicada",
                "objetivo_bkci": False,
            }
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("etapa", result.stderr)

    def test_existing_output_is_preserved_without_explicit_permission(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "contexto.json"
            output = Path(tmp) / "reporte.json"
            source.write_text(
                json.dumps(
                    {
                        "tipo_obra": "obra-colectiva",
                        "autoria_capitulos": "independiente",
                        "etapa": "aceptada",
                        "objetivo_bkci": False,
                    }
                ),
                encoding="utf-8",
            )
            output.write_text("conservar\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(source), "--out", str(output)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=20,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("ya existe", result.stderr)
            self.assertEqual(output.read_text(encoding="utf-8"), "conservar\n")


if __name__ == "__main__":
    unittest.main()
