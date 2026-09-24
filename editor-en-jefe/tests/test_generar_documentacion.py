"""Pruebas funcionales del generador de documentación de skills."""

import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generar_documentacion_skills.py"


class GenerarDocumentacionSkillsTests(unittest.TestCase):
    def create_skill(
        self,
        root: Path,
        name: str,
        description: str,
        title: str | None = None,
        body: str = "",
        default_prompt: str | None = None,
    ) -> None:
        skill = root / name
        (skill / "scripts").mkdir(parents=True)
        (skill / "references").mkdir()
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n\n# {title or name}\n\n{body}",
            encoding="utf-8",
        )
        (skill / "scripts" / "accion.py").write_text(
            '"""Ejecuta la acción demostrativa."""\n\nprint("ok")\n', encoding="utf-8"
        )
        (skill / "references" / "criterios.md").write_text("# Criterios\n", encoding="utf-8")
        if default_prompt is not None:
            agents = skill / "agents"
            agents.mkdir()
            (agents / "openai.yaml").write_text(
                f'interface:\n  default_prompt: "{default_prompt}"\n', encoding="utf-8"
            )

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

    def test_does_not_link_historical_zip_backups_as_distributed_resources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "coleccion"
            output = Path(tmp) / "docs" / "skills"
            root.mkdir()
            self.create_skill(root, "editor-en-jefe", "Coordina la colección.")
            backups = root / "editor-en-jefe" / "assets" / "migraciones"
            backups.mkdir(parents=True)
            (backups / "antes-fusion.zip").write_bytes(b"respaldo local")

            result = self.run_generator(root, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            page = (output / "editor-en-jefe.md").read_text(encoding="utf-8")
            self.assertNotIn("antes-fusion.zip", page)

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

    def test_preserves_operational_guidance_and_uses_the_real_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "coleccion"
            output = Path(tmp) / "docs" / "skills"
            root.mkdir()
            self.create_skill(
                root,
                "alfa-skill",
                "Procesa entradas alfa de forma controlada.",
                title="Alfa Skill",
                body=(
                    "## Flujo\n\n"
                    "1. Conserva el archivo original.\n"
                    "2. Ejecuta el control reproducible.\n\n"
                    "```text\npython alfa-skill/scripts/accion.py entrada.txt\n```\n\n"
                    "## Límites\n\nNo reemplaza la revisión humana.\n"
                ),
                default_prompt="Usa $alfa-skill para comprobar este archivo sin alterar el original.",
            )

            result = self.run_generator(root, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            page = (output / "alfa-skill.md").read_text(encoding="utf-8")
            self.assertIn("Usa $alfa-skill para comprobar este archivo", page)
            self.assertIn("### Flujo", page)
            self.assertIn("Conserva el archivo original", page)
            self.assertIn("python alfa-skill/scripts/accion.py entrada.txt", page)
            self.assertIn("### Límites", page)
            self.assertIn("No reemplaza la revisión humana", page)
            self.assertNotIn("[describe aquí", page)

    def test_rewrites_local_links_from_the_skill_to_the_generated_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "coleccion"
            output = Path(tmp) / "docs" / "skills"
            root.mkdir()
            self.create_skill(
                root,
                "alfa-skill",
                "Procesa entradas alfa.",
                body=(
                    "## Referencias\n\n"
                    "Leer [criterios](references/criterios.md) y "
                    "[guía común](../editor-en-jefe/references/ruta.md).\n"
                ),
            )
            editor_reference = root / "editor-en-jefe" / "references"
            editor_reference.mkdir(parents=True)
            (editor_reference / "ruta.md").write_text("# Ruta\n", encoding="utf-8")

            result = self.run_generator(root, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            page = (output / "alfa-skill.md").read_text(encoding="utf-8")
            self.assertIn("(../../alfa-skill/references/criterios.md)", page)
            self.assertIn("(../../editor-en-jefe/references/ruta.md)", page)

    def test_describes_resources_instead_of_only_listing_filenames(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "coleccion"
            output = Path(tmp) / "docs" / "skills"
            root.mkdir()
            self.create_skill(root, "alfa-skill", "Procesa entradas alfa.")

            result = self.run_generator(root, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            page = (output / "alfa-skill.md").read_text(encoding="utf-8")
            self.assertIn("| Recurso | Función |", page)
            self.assertIn("Ejecuta la acción demostrativa.", page)
            self.assertIn("Criterios", page)

    def test_uses_the_first_docx_paragraph_as_the_asset_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "coleccion"
            output = Path(tmp) / "docs" / "skills"
            root.mkdir()
            self.create_skill(root, "alfa-skill", "Procesa entradas alfa.")
            assets = root / "alfa-skill" / "assets"
            assets.mkdir()
            document = assets / "formulario.docx"
            with ZipFile(document, "w") as archive:
                archive.writestr(
                    "word/document.xml",
                    (
                        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                        '<w:document xmlns:w="http://schemas.openxmlformats.org/'
                        'wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>'
                        "Ficha de control editorial de libros"
                        "</w:t></w:r></w:p></w:body></w:document>"
                    ),
                )

            result = self.run_generator(root, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            page = (output / "alfa-skill.md").read_text(encoding="utf-8")
            self.assertIn("Ficha de control editorial de libros", page)
            self.assertNotIn("Recurso auxiliar: Formulario", page)

    def test_groups_known_skills_by_workflow_in_the_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "coleccion"
            output = Path(tmp) / "docs" / "skills"
            root.mkdir()
            self.create_skill(root, "editor-en-jefe", "Coordina la colección.")
            self.create_skill(root, "constructor-tesis-academica", "Construye tesis.")
            self.create_skill(root, "gestor-ecuaciones-academicas", "Gestiona ecuaciones.")

            result = self.run_generator(root, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            index = (output / "README.md").read_text(encoding="utf-8")
            self.assertIn("## Orquestación y preparación", index)
            self.assertIn("## Tesis y libros", index)
            self.assertIn("## Recursos técnicos y visuales", index)

    def test_does_not_rewrite_headings_or_links_inside_code_fences(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "coleccion"
            output = Path(tmp) / "docs" / "skills"
            root.mkdir()
            self.create_skill(
                root,
                "alfa-skill",
                "Procesa entradas alfa.",
                body=(
                    "## Formato\n\n"
                    "```markdown\n"
                    "## Título del ejemplo\n"
                    "[enlace de muestra](references/no-real.md)\n"
                    "```\n\n"
                    "La sintaxis `![pie](archivo.png)` es solo un ejemplo.\n\n"
                    "Leer [criterios reales](references/criterios.md).\n"
                ),
            )

            result = self.run_generator(root, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            page = (output / "alfa-skill.md").read_text(encoding="utf-8")
            self.assertIn("### Formato", page)
            self.assertIn("## Título del ejemplo", page)
            self.assertIn("[enlace de muestra](references/no-real.md)", page)
            self.assertIn("`![pie](archivo.png)`", page)
            self.assertIn("[criterios reales](../../alfa-skill/references/criterios.md)", page)


if __name__ == "__main__":
    unittest.main()
