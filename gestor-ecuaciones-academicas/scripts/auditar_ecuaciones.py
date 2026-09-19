#!/usr/bin/env python3
"""Inventaría ecuaciones LaTeX/Markdown y revisa referencias mecánicas."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import tempfile


ENVIRONMENT_RE = re.compile(
    r"\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}"
    r"(.*?)\\end\{\1\}",
    re.DOTALL,
)
BRACKET_RE = re.compile(r"\\\[(.*?)\\\]", re.DOTALL)
DOLLAR_RE = re.compile(r"(?<!\\)\$\$(.*?)(?<!\\)\$\$", re.DOTALL)
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
EQREF_RE = re.compile(r"\\eqref\{([^{}]+)\}")
DISPLAY_MARKER_RE = re.compile(r"(?<!\\)\$\$")
BEGIN_ENV_RE = re.compile(r"\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}")
END_ENV_RE = re.compile(r"\\end\{(equation\*?|align\*?|gather\*?|multline\*?)\}")


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def braces_balanced(content: str) -> bool:
    depth = 0
    escaped = False
    for character in content:
        if escaped:
            escaped = False
            continue
        if character == "\\":
            escaped = True
        elif character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def equation_matches(text: str) -> list[tuple[int, int, str, str]]:
    matches: list[tuple[int, int, str, str]] = []
    for match in ENVIRONMENT_RE.finditer(text):
        matches.append((match.start(), match.end(), match.group(1), match.group(2)))
    for kind, pattern in (("bracket", BRACKET_RE), ("double_dollar", DOLLAR_RE)):
        for match in pattern.finditer(text):
            span = (match.start(), match.end())
            if any(span[0] < end and span[1] > start for start, end, _, _ in matches):
                continue
            matches.append((span[0], span[1], kind, match.group(1)))
    return sorted(matches, key=lambda item: item[0])


def issue(code: str, severity: str, message: str, **details: object) -> dict[str, object]:
    return {"code": code, "severity": severity, "message": message, **details}


def audit(text: str, source: Path) -> dict[str, object]:
    equations: list[dict[str, object]] = []
    issues: list[dict[str, object]] = []

    for index, (start, end, kind, content) in enumerate(equation_matches(text), 1):
        labels = LABEL_RE.findall(content)
        equations.append(
            {
                "id": index,
                "kind": kind,
                "line_start": line_number(text, start),
                "line_end": line_number(text, end),
                "labels": labels,
                "content": content.strip(),
            }
        )
        if not braces_balanced(content):
            issues.append(
                issue(
                    "unbalanced_braces",
                    "error",
                    "La ecuación contiene llaves desbalanceadas.",
                    equation=index,
                )
            )

    dollar_markers = list(DISPLAY_MARKER_RE.finditer(text))
    if len(dollar_markers) % 2:
        issues.append(
            issue(
                "unclosed_display_math",
                "error",
                "Existe un delimitador $$ sin cierre.",
                line=line_number(text, dollar_markers[-1].start()),
            )
        )

    if len(re.findall(r"\\\[", text)) != len(re.findall(r"\\\]", text)):
        issues.append(
            issue("unclosed_bracket_math", "error", "Existe un delimitador \\[ o \\] sin pareja.")
        )

    begin_counts = Counter(BEGIN_ENV_RE.findall(text))
    end_counts = Counter(END_ENV_RE.findall(text))
    for environment in sorted(set(begin_counts) | set(end_counts)):
        if begin_counts[environment] != end_counts[environment]:
            issues.append(
                issue(
                    "unclosed_equation_environment",
                    "error",
                    "El entorno de ecuación no tiene aperturas y cierres equivalentes.",
                    environment=environment,
                    begins=begin_counts[environment],
                    ends=end_counts[environment],
                )
            )

    labels = [label for equation in equations for label in equation["labels"]]
    references = EQREF_RE.findall(text)
    label_counts = Counter(labels)
    for label, count in sorted(label_counts.items()):
        if count > 1:
            issues.append(
                issue(
                    "duplicate_label",
                    "error",
                    "Una etiqueta identifica más de una ecuación.",
                    label=label,
                    count=count,
                )
            )
    for reference in sorted(set(references) - set(labels)):
        issues.append(
            issue(
                "missing_equation_reference",
                "error",
                "Una referencia apunta a una etiqueta de ecuación inexistente.",
                label=reference,
            )
        )
    for label in sorted(set(labels) - set(references)):
        issues.append(
            issue(
                "unreferenced_label",
                "warning",
                "La ecuación etiquetada no se referencia mediante \\eqref.",
                label=label,
            )
        )

    errors = sum(item["severity"] == "error" for item in issues)
    warnings = sum(item["severity"] == "warning" for item in issues)
    return {
        "source": str(source.resolve()),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {"equations": len(equations), "errors": errors, "warnings": warnings},
        "equations": equations,
        "labels": labels,
        "references": references,
        "issues": issues,
    }


def write_json(path: Path, report: dict[str, object], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"El informe ya existe: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inventaría ecuaciones LaTeX/Markdown y revisa etiquetas y referencias."
    )
    parser.add_argument("source", type=Path, help="Archivo UTF-8 .md, .tex o .txt")
    parser.add_argument("--out", required=True, type=Path, help="Informe JSON de salida")
    parser.add_argument("--overwrite", action="store_true", help="Reemplazar el informe existente")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        source = args.source.resolve(strict=True)
        output = args.out.resolve()
        if not source.is_file():
            raise ValueError(f"La entrada no es un archivo: {source}")
        if source == output:
            raise ValueError("La entrada y el informe no pueden ser el mismo archivo")
        if source.suffix.lower() not in {".md", ".tex", ".txt"}:
            raise ValueError("Formato no compatible; use .md, .tex o .txt")
        text = source.read_text(encoding="utf-8")
        report = audit(text, source)
        write_json(output, report, args.overwrite)
    except (FileNotFoundError, FileExistsError, OSError, UnicodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    return 1 if report["summary"]["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
