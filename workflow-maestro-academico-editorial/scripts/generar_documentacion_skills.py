#!/usr/bin/env python3
"""Genera fichas Markdown navegables para una colección de skills."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import re
import sys
import tempfile


EXCLUDED_PARTS = {".runtime", "__pycache__", ".git", ".venv", "venv"}
RESOURCE_GROUPS = (
    ("scripts", "Scripts"),
    ("references", "Referencias"),
    ("assets", "Plantillas y recursos"),
    ("tests", "Pruebas"),
    ("agents", "Configuración de interfaz"),
)


@dataclass(frozen=True)
class SkillInfo:
    name: str
    description: str
    path: Path
    sections: tuple[str, ...]
    resources: dict[str, tuple[Path, ...]]


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


def discover_resources(skill: Path, directory: str) -> tuple[Path, ...]:
    root = skill / directory
    if not root.is_dir():
        return ()
    files = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        files.append(path.relative_to(skill))
    return tuple(sorted(files, key=lambda item: item.as_posix().casefold()))


def discover_skills(root: Path) -> list[SkillInfo]:
    skills: list[SkillInfo] = []
    for path in sorted(root.iterdir(), key=lambda item: item.name.casefold()):
        source = path / "SKILL.md"
        if path.name.startswith(".") or not path.is_dir() or not source.is_file():
            continue
        text = source.read_text(encoding="utf-8")
        name, description = parse_frontmatter(text, source)
        if name != path.name:
            raise ValueError(f"El nombre {name} no coincide con el directorio {path.name}")
        sections = tuple(
            heading.strip()
            for heading in re.findall(r"^## (.+)$", text, flags=re.MULTILINE)
            if heading.strip()
        )
        resources = {directory: discover_resources(path, directory) for directory, _ in RESOURCE_GROUPS}
        skills.append(SkillInfo(name, description, path, sections, resources))
    if not skills:
        raise ValueError(f"No se encontraron skills en {root}")
    return skills


def display_name(name: str) -> str:
    return " ".join(word.capitalize() for word in name.split("-"))


def render_skill(skill: SkillInfo) -> str:
    lines = [
        f"# {display_name(skill.name)}",
        "",
        skill.description,
        "",
        "## Uso",
        "",
        f"Invócala directamente con `${skill.name}` o permite que el orquestador la seleccione según el encargo.",
        "",
        "Ejemplo:",
        "",
        "```text",
        f"Usa ${skill.name} para [describe aquí la tarea y los archivos de entrada].",
        "```",
        "",
    ]
    if skill.sections:
        lines.extend(["## Cobertura", ""])
        lines.extend(f"- {section}" for section in skill.sections)
        lines.append("")
    lines.extend(["## Recursos incluidos", ""])
    has_resources = False
    for directory, title in RESOURCE_GROUPS:
        resources = skill.resources[directory]
        if not resources:
            continue
        has_resources = True
        lines.extend([f"### {title}", ""])
        for resource in resources:
            relative = resource.as_posix()
            lines.append(f"- [`{relative}`](../../{skill.name}/{relative})")
        lines.append("")
    if not has_resources:
        lines.extend(["La skill no necesita recursos auxiliares; sus reglas están en el archivo principal.", ""])
    lines.extend(
        [
            "## Integración",
            "",
            "Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.",
            "",
            f"Consulta las instrucciones normativas en [`{skill.name}/SKILL.md`](../../{skill.name}/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.",
            "",
        ]
    )
    return "\n".join(lines)


def render_index(skills: list[SkillInfo]) -> str:
    lines = [
        "# Catálogo de skills",
        "",
        "Cada ficha resume el propósito, la cobertura y los recursos de una skill. Las instrucciones ejecutables y normativas permanecen en el `SKILL.md` de cada directorio.",
        "",
        "| Skill | Uso principal |",
        "| --- | --- |",
    ]
    for skill in skills:
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
