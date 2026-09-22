#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs


CONNECTORS = [
    "además",
    "asimismo",
    "en este sentido",
    "cabe destacar",
    "por otro lado",
    "de esta manera",
    "es importante mencionar",
    "en conclusión",
]
START_RE = re.compile(r"(?m)^\s*([A-ZÁÉÍÓÚÑ][^.\n]{8,90})")
SENTENCE_RE = re.compile(r"[^.!?]+[.!?]", re.M)


@dataclass
class RepetitionReport:
    repeated_starts: list[tuple[str, int]]
    connector_counts: dict[str, int]
    repeated_sentences: list[tuple[str, int]]
    average_sentence_words: float
    warnings: list[str]


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def analyze(text: str) -> RepetitionReport:
    starts = collections.Counter(norm(m.group(1)) for m in START_RE.finditer(text))
    sentences = [norm(m.group(0)) for m in SENTENCE_RE.finditer(text)]
    sent_counts = collections.Counter(s for s in sentences if len(s) > 40)
    connector_counts = {c: len(re.findall(rf"(?i)\b{re.escape(c)}\b", text)) for c in CONNECTORS}
    words_per_sentence = [len(re.findall(r"\b\w+\b", s, re.UNICODE)) for s in sentences]
    avg = sum(words_per_sentence) / len(words_per_sentence) if words_per_sentence else 0.0
    warnings = []
    if any(count >= 3 for count in connector_counts.values()):
        warnings.append("Hay conectores comodín repetidos tres o más veces.")
    if any(count >= 2 for _, count in sent_counts.items()):
        warnings.append("Hay oraciones largas repetidas.")
    if any(count >= 2 for _, count in starts.items()):
        warnings.append("Hay inicios de párrafo repetidos.")
    return RepetitionReport(
        repeated_starts=[item for item in starts.most_common() if item[1] > 1][:20],
        connector_counts={k: v for k, v in connector_counts.items() if v > 0},
        repeated_sentences=[item for item in sent_counts.most_common() if item[1] > 1][:20],
        average_sentence_words=round(avg, 2),
        warnings=warnings,
    )


def render(report: RepetitionReport, source: str) -> str:
    lines = ["# Análisis de repeticiones y muletillas", "", f"- Fuente: `{source}`", f"- Promedio palabras/oración: {report.average_sentence_words}"]
    if report.warnings:
        lines.append("- Advertencias:")
        lines.extend(f"  - {w}" for w in report.warnings)
    lines.extend(["", "## Conectores", ""])
    if report.connector_counts:
        lines.extend(f"- `{k}`: {v}" for k, v in sorted(report.connector_counts.items()))
    else:
        lines.append("- Sin conectores sobreobservados.")
    lines.extend(["", "## Inicios repetidos", ""])
    lines.extend(f"- {count}x: {text}" for text, count in report.repeated_starts) if report.repeated_starts else lines.append("- No detectados.")
    lines.extend(["", "## Oraciones repetidas", ""])
    lines.extend(f"- {count}x: {text}" for text, count in report.repeated_sentences) if report.repeated_sentences else lines.append("- No detectadas.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Analiza repeticiones, conectores y muletillas en manuscritos.")
    parser.add_argument("input")
    parser.add_argument("--out")
    parser.add_argument("--json-out")
    parser.add_argument('--overwrite', action='store_true', help='Autorizar reemplazo de informes, nunca de entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.input], [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    path = Path(args.input)
    report = analyze(path.read_text(encoding="utf-8", errors="replace"))
    text_report = render(report, str(path))
    if args.out:
        atomic_write(args.out, text_report, overwrite=args.overwrite)
    else:
        sys.stdout.write(text_report)
    if args.json_out:
        atomic_write(args.json_out, json.dumps(asdict(report), ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
