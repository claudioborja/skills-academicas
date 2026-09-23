"""Pruebas funcionales del selector de perfiles de contribución y autoría."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "seleccionar_perfil.py"


class SeleccionarPerfilTests(unittest.TestCase):
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

    def test_general_research_article_uses_credit_without_inventing_authorship_rule(self):
        report = self.parse_success(
            {
                "tipo_obra": "articulo",
                "disciplina": "general",
                "salida_investigacion": True,
                "decidir_autoria": True,
                "destinos": [],
            }
        )

        self.assertEqual(report["perfil_principal"], "CRediT")
        self.assertIn("CRediT", report["taxonomias"])
        self.assertNotIn("ICMJE", report["criterios_autoria"])
        self.assertTrue(report["requiere_politica_autoria"])
        self.assertIn("no decide autoría", " ".join(report["advertencias"]).lower())

    def test_biomedical_article_combines_icmje_credit_and_cope(self):
        report = self.parse_success(
            {
                "tipo_obra": "articulo",
                "disciplina": "biomedicina",
                "salida_investigacion": True,
                "decidir_autoria": True,
                "destinos": ["jats", "crossref", "orcid"],
            }
        )

        self.assertEqual(report["perfil_principal"], "CRediT")
        self.assertIn("ICMJE", report["criterios_autoria"])
        self.assertIn("COPE", report["integridad_y_disputas"])
        self.assertEqual(report["representacion"], ["JATS XML", "Crossref", "ORCID"])

    def test_dataset_adds_datacite_without_replacing_credit(self):
        report = self.parse_success(
            {
                "tipo_obra": "dataset",
                "disciplina": "general",
                "salida_investigacion": True,
                "decidir_autoria": False,
                "destinos": [],
            }
        )

        self.assertEqual(report["perfil_principal"], "CRediT")
        self.assertIn("DataCite Contributor Types", report["taxonomias"])
        self.assertEqual(report["representacion"], ["DataCite"])

    def test_software_adds_codemeta_and_cff(self):
        report = self.parse_success(
            {
                "tipo_obra": "software",
                "disciplina": "ingenieria",
                "salida_investigacion": True,
                "decidir_autoria": False,
                "destinos": [],
            }
        )

        self.assertEqual(report["perfil_principal"], "CRediT")
        self.assertEqual(report["representacion"], ["CodeMeta", "Citation File Format"])

    def test_nonresearch_translation_prefers_marc_relators(self):
        report = self.parse_success(
            {
                "tipo_obra": "traduccion",
                "disciplina": "humanidades",
                "salida_investigacion": False,
                "decidir_autoria": False,
                "destinos": [],
            }
        )

        self.assertEqual(report["perfil_principal"], "MARC Relator Terms")
        self.assertNotIn("CRediT", report["taxonomias"])
        self.assertEqual(report["representacion"], ["MARC 21"])

    def test_knowledge_graph_adds_cro_and_prov_o(self):
        report = self.parse_success(
            {
                "tipo_obra": "dataset",
                "disciplina": "general",
                "salida_investigacion": True,
                "decidir_autoria": False,
                "destinos": ["grafo"],
            }
        )

        self.assertIn("CRO", report["taxonomias"])
        self.assertEqual(report["representacion"], ["DataCite", "PROV-O"])

    def test_rejects_unknown_product_and_destination(self):
        result = self.run_selector(
            {
                "tipo_obra": "pelicula",
                "disciplina": "general",
                "salida_investigacion": False,
                "decidir_autoria": False,
                "destinos": ["desconocido"],
            }
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("tipo_obra", result.stderr)

    def test_refuses_to_overwrite_an_existing_report_without_permission(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "contexto.json"
            output = Path(tmp) / "reporte.json"
            source.write_text(
                json.dumps(
                    {
                        "tipo_obra": "articulo",
                        "disciplina": "general",
                        "salida_investigacion": True,
                        "decidir_autoria": False,
                        "destinos": [],
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
