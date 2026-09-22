#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs


WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ-]+\b", re.UNICODE)
NUMBERED_HEADING_RE = re.compile(r"^\d+(?:\.\d+)+\.?\s+\S")
LIST_RE = re.compile(r"^(?:[-*+]\s+|\d+[.)]\s+)")
PROTECTED_TAIL_RE = re.compile(r"^(?:Glosario|Bibliograf[ií]a|Referencias)\s*$", re.I)
STRUCTURAL_RE = re.compile(r"^(?:Tabla\.?|Figura\.?|Descripción:|Fuente:|Nota:)", re.I)


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def normalize_prose_block(block: str) -> str:
    return " ".join(line.strip() for line in block.splitlines() if line.strip())


def is_mergeable_prose(block: str) -> bool:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if not lines:
        return False
    first = lines[0]
    if PROTECTED_TAIL_RE.match(first):
        return False
    if NUMBERED_HEADING_RE.match(first) or LIST_RE.match(first) or STRUCTURAL_RE.match(first):
        return False
    if first.startswith(("#", ">", "|", "```")):
        return False
    if any(line.startswith("|") for line in lines):
        return False
    words = word_count(normalize_prose_block(block))
    if len(lines) == 1 and words <= 18 and not re.search(r"[.!?…:]$", first):
        return False
    return words >= 8


def connect_short_paragraphs(
    text: str,
    *,
    min_words: int = 80,
    max_words: int = 180,
) -> tuple[str, dict[str, int]]:
    blocks = re.split(r"(?:\r?\n){2,}", text.strip())
    output: list[str] = []
    pending = ""
    protected_tail = False
    stats = {
        "input_blocks": len(blocks),
        "short_paragraphs_absorbed": 0,
        "protected_blocks": 0,
    }

    def flush() -> None:
        nonlocal pending
        if pending:
            output.append(pending.strip())
            pending = ""

    for block in blocks:
        stripped = block.strip()
        first_line = next((line.strip() for line in stripped.splitlines() if line.strip()), "")
        if PROTECTED_TAIL_RE.match(first_line):
            protected_tail = True
        if protected_tail:
            flush()
            output.append(stripped)
            stats["protected_blocks"] += 1
            continue
        if not is_mergeable_prose(block):
            flush()
            output.append(stripped)
            continue

        prose = normalize_prose_block(block)
        if not pending:
            pending = prose
            continue
        if word_count(pending) < min_words and word_count(pending) + word_count(prose) <= max_words:
            pending = pending.rstrip() + " " + prose.lstrip()
            stats["short_paragraphs_absorbed"] += 1
        else:
            flush()
            pending = prose

    flush()
    connected = "\n\n".join(output).strip() + "\n"
    stats["output_blocks"] = len(output)
    stats["original_words"] = word_count(text)
    stats["final_words"] = word_count(connected)
    return connected, stats


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Fusiona párrafos narrativos breves adyacentes en archivos TXT sin "
            "reescribir contenido ni insertar transiciones."
        )
    )
    parser.add_argument("input", help="Archivo TXT fuente.")
    parser.add_argument("--out", required=True, help="Salida diferente de la entrada.")
    parser.add_argument("--overwrite", action="store_true", help="Reemplazar salidas existentes, nunca la entrada.")
    parser.add_argument("--report", help="Reporte JSON.")
    parser.add_argument("--min-paragraph-words", type=int, default=80)
    parser.add_argument("--max-paragraph-words", type=int, default=180)
    args = parser.parse_args()

    if args.min_paragraph_words < 20 or args.max_paragraph_words <= args.min_paragraph_words:
        raise SystemExit("Usa un mínimo >= 20 y un máximo mayor que el mínimo.")

    source = Path(args.input)
    try:
        validate_outputs([source], [args.out, args.report], args.overwrite)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    if not source.exists():
        raise SystemExit(f"No existe: {source}")
    original = source.read_text(encoding="utf-8")
    connected, stats = connect_short_paragraphs(
        original,
        min_words=args.min_paragraph_words,
        max_words=args.max_paragraph_words,
    )

    output = Path(args.out)
    atomic_write(output, connected, args.overwrite)
    stats.update(
        {
            "input": str(source),
            "output": str(output),
            "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
    )
    if args.report:
        report = Path(args.report)
        report.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(report, json.dumps(stats, ensure_ascii=False, indent=2), args.overwrite)
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
