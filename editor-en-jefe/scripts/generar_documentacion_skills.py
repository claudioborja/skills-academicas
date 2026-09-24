#!/usr/bin/env python3
"""Genera fichas Markdown navegables para una colección de skills."""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import os
from pathlib import Path
import re
import sys
import tempfile


EXCLUDED_PARTS = {".runtime", "__pycache__", ".git", ".venv", "venv"}
RESOURCE_GROUPS = (
    ("scripts", "Herramientas automatizadas"),
    ("references", "Referencias"),
    ("assets", "Plantillas y recursos"),
    ("tests", "Pruebas"),
    ("agents", "Configuración de interfaz"),
)


@dataclass(frozen=True)
class ResourceInfo:
    path: Path
    purpose: str


@dataclass(frozen=True)
class SkillInfo:
    name: str
    title: str
    description: str
    path: Path
    guide: str
    default_prompt: str
    resources: dict[str, tuple[ResourceInfo, ...]]


CATEGORY_ORDER = (
    "Orquestación y preparación",
    "Tesis y libros",
    "Artículos y revisiones",
    "Evidencia, resultados y referencias",
    "Redacción y revisión",
    "Recursos técnicos y visuales",
    "Edición, autoría y entrega",
    "Otras especialidades",
)

SKILL_CATEGORIES = {
    "editor-en-jefe": "Orquestación y preparación",
    "planificador-obra-academica": "Orquestación y preparación",
    "preprocesador-documentos": "Orquestación y preparación",
    "auditor-documental-academico": "Orquestación y preparación",
    "constructor-tesis-academica": "Tesis y libros",
    "convertidor-tesis-a-libro": "Tesis y libros",
    "gestor-continuidad-libro": "Tesis y libros",
    "gestor-marco-teorico-estado-del-arte": "Tesis y libros",
    "explorador-temas-articulos": "Artículos y revisiones",
    "redaccion-articulo-cientifico-imryd": "Artículos y revisiones",
    "auditor-articulo-imryd": "Artículos y revisiones",
    "revision-sistematica-kitchenham": "Artículos y revisiones",
    "revision-sistematica-prisma": "Artículos y revisiones",
    "verificador-resultados-investigacion": "Evidencia, resultados y referencias",
    "gestor-referencias-academicas": "Evidencia, resultados y referencias",
    "automatizador-referencias": "Evidencia, resultados y referencias",
    "revisor-citas-consistencia-bibliografica": "Evidencia, resultados y referencias",
    "ajustes-editoriales-bibliograficos": "Evidencia, resultados y referencias",
    "filtro-editoriales-depredadoras": "Evidencia, resultados y referencias",
    "gestor-redaccion-latinoamerica": "Redacción y revisión",
    "humanizar-redaccion-academica": "Redacción y revisión",
    "correccion-estilo-ortotipografica": "Redacción y revisión",
    "auditor-coherencia-argumentativa": "Redacción y revisión",
    "normalizador-terminologia-glosario": "Redacción y revisión",
    "revisor-resumen-abstract-palabras-clave": "Redacción y revisión",
    "respondedor-observaciones-academicas": "Redacción y revisión",
    "gestor-tablas-figuras-pies": "Recursos técnicos y visuales",
    "gestor-imagenes-academicas-libros": "Recursos técnicos y visuales",
    "gestor-ecuaciones-academicas": "Recursos técnicos y visuales",
    "gestor-codigo-tecnico-editorial": "Recursos técnicos y visuales",
    "gestor-contribuciones-autoria": "Edición, autoría y entrega",
    "disenador-maquetador-word": "Edición, autoría y entrega",
    "maquetacion-academica-preentrega": "Edición, autoría y entrega",
}


def parse_frontmatter(text: str, source: Path) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError(f"Frontmatter ausente en {source}")
    try:
        block = text.split("---", 2)[1]
    except IndexError as error:
        raise ValueError(f"Frontmatter incompleto en {source}") from error
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.strip() in {"name", "description"}:
            fields[key.strip()] = value.strip().strip('"').strip("'")
    name = fields.get("name", "").strip()
    description = fields.get("description", "").strip()
    if not name or not description:
        raise ValueError(f"name o description ausente en {source}")
    return name, description


def parse_title(text: str, source: Path) -> str:
    match = re.search(r"^# (.+)$", text, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"Título principal ausente en {source}")
    return match.group(1).strip()


def validate_description(description: str, source: Path) -> None:
    if re.search(r"\bUse when(?: Codex needs to)?\b", description, flags=re.IGNORECASE):
        raise ValueError(f"La descripción contiene una mezcla de idiomas en {source}")


def extract_guide(text: str, source: Path) -> str:
    title = re.search(r"^# .+$", text, flags=re.MULTILINE)
    if title is None:
        raise ValueError(f"Título principal ausente en {source}")
    return text[title.end() :].strip()


def parse_default_prompt(skill: Path, name: str) -> str:
    metadata = skill / "agents" / "openai.yaml"
    if metadata.is_file():
        text = metadata.read_text(encoding="utf-8")
        match = re.search(r"^\s*default_prompt:\s*(.+?)\s*$", text, flags=re.MULTILINE)
        if match:
            return match.group(1).strip().strip('"').strip("'")
    return f"Usa ${name} para aplicar esta especialidad al material indicado."


def first_heading(text: str) -> str | None:
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def humanize_stem(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").strip().capitalize()


def resource_purpose(path: Path) -> str:
    suffix = path.suffix.lower()
    try:
        if suffix == ".py":
            module = ast.parse(path.read_text(encoding="utf-8"))
            docstring = ast.get_docstring(module, clean=True)
            if docstring:
                return docstring.splitlines()[0].strip()
        if suffix == ".md":
            heading = first_heading(path.read_text(encoding="utf-8"))
            if heading:
                return heading
        if path.name == "openai.yaml":
            return "Metadatos de interfaz e invocación de la skill."
        if suffix == ".csv":
            return f"Plantilla o registro editable: {humanize_stem(path)}."
        if suffix == ".json":
            return f"Datos estructurados o ejemplo: {humanize_stem(path)}."
        if "requirements" in path.name:
            return "Dependencias Python fijadas para esta herramienta."
    except (OSError, SyntaxError, UnicodeError):
        pass
    return f"Recurso auxiliar: {humanize_stem(path)}."


def discover_resources(skill: Path, directory: str) -> tuple[ResourceInfo, ...]:
    root = skill / directory
    if not root.is_dir():
        return ()
    files = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in {".pyc", ".pyo", ".zip"}:
            continue
        files.append(ResourceInfo(path.relative_to(skill), resource_purpose(path)))
    return tuple(sorted(files, key=lambda item: item.path.as_posix().casefold()))


def discover_skills(root: Path) -> list[SkillInfo]:
    skills: list[SkillInfo] = []
    for path in sorted(root.iterdir(), key=lambda item: item.name.casefold()):
        source = path / "SKILL.md"
        if path.name.startswith(".") or not path.is_dir() or not source.is_file():
            continue
        text = source.read_text(encoding="utf-8")
        name, description = parse_frontmatter(text, source)
        title = parse_title(text, source)
        validate_description(description, source)
        if name != path.name:
            raise ValueError(f"El nombre {name} no coincide con el directorio {path.name}")
        guide = extract_guide(text, source)
        default_prompt = parse_default_prompt(path, name)
        resources = {directory: discover_resources(path, directory) for directory, _ in RESOURCE_GROUPS}
        skills.append(SkillInfo(name, title, description, path, guide, default_prompt, resources))
    if not skills:
        raise ValueError(f"No se encontraron skills en {root}")
    return skills


def transform_outside_inline_code(line: str, transform) -> str:
    pattern = re.compile(r"(?P<ticks>`+).*?(?P=ticks)")
    output: list[str] = []
    cursor = 0
    for match in pattern.finditer(line):
        output.append(transform(line[cursor : match.start()]))
        output.append(match.group(0))
        cursor = match.end()
    output.append(transform(line[cursor:]))
    return "".join(output)


def transform_outside_fences(markdown: str, transform) -> str:
    inside_fence = False
    output: list[str] = []
    for line in markdown.splitlines(keepends=True):
        if re.match(r"^\s*(?:```|~~~)", line):
            output.append(line)
            inside_fence = not inside_fence
            continue
        output.append(
            line if inside_fence else transform_outside_inline_code(line, transform)
        )
    return "".join(output)


def rewrite_local_links(markdown: str, skill: SkillInfo) -> str:
    root = skill.path.parent.resolve()

    def replace(match: re.Match[str]) -> str:
        prefix, target, suffix = match.group("prefix"), match.group("target"), match.group("suffix")
        if target.startswith(("#", "/", "mailto:")) or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", target):
            return match.group(0)
        path_text, separator, anchor = target.partition("#")
        candidate = (skill.path / path_text).resolve()
        try:
            relative = candidate.relative_to(root)
        except ValueError:
            return match.group(0)
        rewritten = f"../../{relative.as_posix()}"
        if separator:
            rewritten += f"#{anchor}"
        return f"{prefix}{rewritten}{suffix}"

    pattern = re.compile(
        r"(?P<prefix>!?\[[^\]]*\]\()(?P<target>[^)\s]+)(?P<suffix>[^)]*\))"
    )
    return transform_outside_fences(markdown, lambda line: pattern.sub(replace, line))


def demote_headings(markdown: str) -> str:
    pattern = re.compile(r"^(#{2,5})(\s+)")
    return transform_outside_fences(
        markdown,
        lambda line: pattern.sub(
            lambda match: f"#{match.group(1)}{match.group(2)}", line
        ),
    )


def table_cell(text: str) -> str:
    return " ".join(text.split()).replace("|", "\\|")


def render_skill(skill: SkillInfo) -> str:
    guide = demote_headings(rewrite_local_links(skill.guide, skill))
    lines = [
        f"# {skill.title}",
        "",
        skill.description,
        "",
        "## Ejemplo de uso",
        "",
        "```text",
        skill.default_prompt,
        "```",
        "",
        "## Guía operativa",
        "",
    ]
    if guide:
        lines.extend([guide, ""])
    else:
        lines.extend(["La skill concentra sus reglas en la descripción y los recursos enlazados.", ""])
    lines.extend(["## Recursos incluidos", ""])
    has_resources = False
    for directory, title in RESOURCE_GROUPS:
        resources = skill.resources[directory]
        if not resources:
            continue
        has_resources = True
        lines.extend([f"### {title}", ""])
        lines.extend(["| Recurso | Función |", "| --- | --- |"])
        for resource in resources:
            relative = resource.path.as_posix()
            lines.append(
                f"| [`{relative}`](../../{skill.name}/{relative}) | {table_cell(resource.purpose)} |"
            )
        lines.append("")
    if not has_resources:
        lines.extend(["La skill no necesita recursos auxiliares; sus reglas están en el archivo principal.", ""])
    lines.extend(
        [
            "## Fuente normativa",
            "",
            f"Esta ficha se genera desde [`{skill.name}/SKILL.md`](../../{skill.name}/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.",
            "",
        ]
    )
    return "\n".join(lines)


def render_index(skills: list[SkillInfo]) -> str:
    lines = [
        "# Catálogo de skills",
        "",
        "Las fichas reproducen de forma navegable la guía operativa, los ejemplos reales y los recursos de cada skill. El `SKILL.md` de cada directorio permanece como contrato normativo.",
        "",
        "Empieza por [`editor-en-jefe`](editor-en-jefe.md) cuando el encargo abarque varias etapas. Si la necesidad es aislada, entra directamente en la categoría correspondiente.",
        "",
    ]
    grouped: dict[str, list[SkillInfo]] = {category: [] for category in CATEGORY_ORDER}
    for skill in skills:
        category = SKILL_CATEGORIES.get(skill.name, "Otras especialidades")
        grouped[category].append(skill)
    for category in CATEGORY_ORDER:
        category_skills = grouped[category]
        if not category_skills:
            continue
        lines.extend([f"## {category}", "", "| Skill | Uso principal |", "| --- | --- |"])
        for skill in category_skills:
            lines.append(f"| [`{skill.name}`]({skill.name}.md) | {skill.description} |")
        lines.append("")
    return "\n".join(lines)


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def generate(root: Path, output: Path, overwrite: bool) -> int:
    root = root.resolve(strict=True)
    output = output.resolve()
    if not root.is_dir():
        raise ValueError(f"La raíz no es un directorio: {root}")
    existing = list(output.glob("*.md")) if output.is_dir() else []
    if existing and not overwrite:
        raise FileExistsError(f"El destino ya contiene documentación: {output}")
    skills = discover_skills(root)
    expected_pages = {"README.md", *(f"{skill.name}.md" for skill in skills)}
    if overwrite:
        for page in existing:
            if page.name not in expected_pages:
                page.unlink()
    atomic_write(output / "README.md", render_index(skills))
    for skill in skills:
        atomic_write(output / f"{skill.name}.md", render_skill(skill))
    print(f"Documentadas {len(skills)} skills en {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Genera documentación Markdown para cada skill.")
    parser.add_argument("--root", required=True, type=Path, help="Raíz de la colección")
    parser.add_argument("--out", required=True, type=Path, help="Directorio docs/skills")
    parser.add_argument("--overwrite", action="store_true", help="Actualizar archivos existentes")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return generate(args.root, args.out, args.overwrite)
    except (FileNotFoundError, FileExistsError, OSError, UnicodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
