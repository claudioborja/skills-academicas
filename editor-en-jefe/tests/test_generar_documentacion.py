"""Pruebas funcionales del generador de documentación de skills."""

import subprocess
import sys
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generar_documentacion_skills.py"


class GenerarDocumentacionSkillsTests(unittest.TestCase):
    def create_skill(
        self, root: Path, name: str, description: str, title: str | None = None
    ) -> None:
        skill = root / name
        (skill / "scripts").mkdir(parents=True)
        (skill / "references").mkdir()
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n\n# {title or name}\n",
            encoding="utf-8",
        )
        (skill / "scripts" / "accion.py").write_text("print('ok')\n", encoding="utf-8")
        (skill / "references" / "criterios.md").write_text("# Criterios\n", encoding="utf-8")

    def run_generator(self, root: Path, output: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), "--out", str(output), *extra],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=20,
        )

    def test_generates_index_and_one_page_per_visible_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "coleccion"
            output = Path(tmp) / "docs" / "skills"
            root.mkdir()
            self.create_skill(root, "zeta-skill", "Resuelve el caso zeta.")
            self.create_skill(root, "alfa-skill", "Resuelve el caso alfa.")
            hidden = root / ".oculta"
            hidden.mkdir()
            (hidden / "SKILL.md").write_text(
                "---\nname: oculta\ndescription: No publicar.\n---\n", encoding="utf-8"
            )

            result = self.run_generator(root, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                sorted(path.name for path in output.glob("*.md")),
                ["README.md", "alfa-skill.md", "zeta-skill.md"],
            )
            index = (output / "README.md").read_text(encoding="utf-8")
            self.assertLess(index.index("alfa-skill"), index.index("zeta-skill"))
            page = (output / "alfa-skill.md").read_text(encoding="utf-8")
            self.assertIn("Resuelve el caso alfa.", page)
            self.assertIn("../../alfa-skill/scripts/accion.py", page)
            self.assertIn("../../alfa-skill/references/criterios.md", page)

    def test_refuses_to_replace_documentation_without_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "coleccion"
            output = Path(tmp) / "docs" / "skills"
            root.mkdir()
            self.create_skill(root, "alfa-skill", "Resuelve el caso alfa.")
            output.mkdir(parents=True)
            existing = output / "README.md"
            existing.write_text("conservar\n", encoding="utf-8")

            result = self.run_generator(root, output)

            self.assertEqual(result.returncode, 2)
            self.assertIn("ya contiene", result.stderr)
            self.assertEqual(existing.read_text(encoding="utf-8"), "conservar\n")

    def test_overwrite_removes_pages_for_skills_that_no_longer_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "coleccion"
            output = Path(tmp) / "docs" / "skills"
            root.mkdir()
            self.create_skill(root, "vigente", "La skill que permanece activa.")
            output.mkdir(parents=True)
            (output / "obsoleta.md").write_text("# Ficha obsoleta\n", encoding="utf-8")

            result = self.run_generator(root, output, "--overwrite")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output / "vigente.md").is_file())
            self.assertFalse((output / "obsoleta.md").exists())

    def test_uses_the_skill_heading_as_the_documentation_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "coleccion"
            output = Path(tmp) / "docs" / "skills"
            root.mkdir()
            self.create_skill(
                root,
                "revision-sistematica-prisma",
                "Documenta revisiones sistemáticas.",
                title="Revisión Sistemática PRISMA",
            )

            result = self.run_generator(root, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            page = (output / "revision-sistematica-prisma.md").read_text(encoding="utf-8")
            self.assertTrue(page.startswith("# Revisión Sistemática PRISMA\n"))

    def test_rejects_the_english_activation_template_in_a_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "coleccion"
            output = Path(tmp) / "docs" / "skills"
            root.mkdir()
            self.create_skill(
                root,
                "descripcion-bilingue",
                "Resume documentos. Use when Codex needs to prepare reports.",
                title="Descripción Bilingüe",
            )

            result = self.run_generator(root, output)

            self.assertEqual(result.returncode, 2)
            self.assertIn("mezcla de idiomas", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
