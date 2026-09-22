"""Pruebas funcionales de la auditoría mecánica PRISMA."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "auditar_prisma.py"
ITEMS = (
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10a", "10b", "11", "12",
    "13a", "13b", "13c", "13d", "13e", "13f", "14", "15", "16a", "16b", "17",
    "18", "19", "20a", "20b", "20c", "20d", "21", "22", "23a", "23b", "23c",
    "23d", "24a", "24b", "24c", "25", "26", "27",
)


class AuditarPrismaTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=20,
        )

    def write_flow(self, path: Path, *, screened: int = 80) -> None:
        path.write_text(
            json.dumps(
                {
                    "review_type": "new",
                    "identification": {"records_databases_registers": 100},
                    "removed_before_screening": {"duplicates": 15, "automation": 3, "other": 2},
                    "screening": {"records_screened": screened, "records_excluded": 50},
                    "database_path": {
                        "reports_sought": 30,
                        "reports_not_retrieved": 5,
                        "reports_assessed": 25,
                        "reports_excluded_by_reason": {
                            "wrong_population": 5,
                            "wrong_design": 3
                        }
                    },
                    "other_methods_path": {
                        "reports_identified": 10,
                        "reports_sought": 10,
                        "reports_not_retrieved": 1,
                        "reports_assessed": 9,
                        "reports_excluded_by_reason": {
                            "wrong_population": 3,
                            "insufficient_data": 1
                        }
                    },
                    "included": {"reports": 22, "studies": 20},
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def write_checklist(self, path: Path, *, missing_item: str | None = None) -> None:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle, fieldnames=("item", "status", "location", "evidence", "notes")
            )
            writer.writeheader()
            for item in ITEMS:
                if item == missing_item:
                    continue
                writer.writerow(
                    {
                        "item": item,
                        "status": "complete",
                        "location": f"sección-{item}",
                        "evidence": f"evidencia verificable del ítem {item}",
                        "notes": "",
                    }
                )

    def test_flow_check_accepts_consistent_counts_and_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "conteos.json"
            report = root / "informe.json"
            self.write_flow(source)

            result = self.run_cli("flow-check", "--input", str(source), "--out", str(report))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("PASS", result.stdout)
            data = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(data["derived"]["identified_records"], 100)
            self.assertEqual(data["derived"]["reports_identified_other_methods"], 10)
            self.assertEqual(data["derived"]["reports_included"], 22)

    def test_flow_check_rejects_an_inconsistent_transition(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "conteos.json"
            self.write_flow(source, screened=79)

            result = self.run_cli("flow-check", "--input", str(source))

            self.assertEqual(result.returncode, 1)
            self.assertIn("records_screened", result.stdout)
            self.assertIn("100 - 20 = 80", result.stdout)

    def test_flow_check_rejects_negative_counts_as_invalid_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "conteos.json"
            self.write_flow(source)
            data = json.loads(source.read_text(encoding="utf-8"))
            data["removed_before_screening"]["duplicates"] = -1
            source.write_text(json.dumps(data), encoding="utf-8")

            result = self.run_cli("flow-check", "--input", str(source))

            self.assertEqual(result.returncode, 2)
            self.assertIn("entero no negativo", result.stderr)

    def test_checklist_audit_accepts_every_required_subitem_with_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "checklist.csv"
            self.write_checklist(source)

            result = self.run_cli("checklist-audit", "--input", str(source))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("complete=42", result.stdout)
            self.assertIn("PASS", result.stdout)

    def test_checklist_audit_reports_absent_subitems_as_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "checklist.csv"
            self.write_checklist(source, missing_item="16b")

            result = self.run_cli("checklist-audit", "--input", str(source))

            self.assertEqual(result.returncode, 1)
            self.assertIn("16b", result.stdout)
            self.assertIn("INCOMPLETE", result.stdout)

    def test_checklist_audit_rejects_duplicate_items(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "checklist.csv"
            self.write_checklist(source)
            with source.open("a", encoding="utf-8", newline="") as handle:
                csv.writer(handle).writerow(("1", "complete", "otra", "duplicada", ""))

            result = self.run_cli("checklist-audit", "--input", str(source))

            self.assertEqual(result.returncode, 2)
            self.assertIn("duplicado", result.stderr)


if __name__ == "__main__":
    unittest.main()
