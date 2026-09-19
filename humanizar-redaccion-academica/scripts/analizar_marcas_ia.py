#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import json
import re
import statistics
import sys
from pathlib import Path


CONNECTORS = [
    "además",
    "asimismo",
    "en este sentido",
    "cabe destacar",
    "por ello",
    "por lo tanto",
    "desde una perspectiva",
    "en la práctica",
    "también es importante",
]

FORMULAIC = [
    "este apartado tiene como propósito",
    "en una obra introductoria",
    "no son asuntos separados",
    "la siguiente tabla se integra",
    "la tabla muestra que",
    "el siguiente esquema queda embebido",
    "la figura resume",
    "la protección de la información no se logra",
    "requiere pasar de la idea general",
    "decisión responsable documentada",
]

WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ-]+\b", flags=re.UNICODE)


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def protected_counts(text: str) -> dict[str, int]:
    return {
        "fenced_blocks": len(re.findall(r"```.*?```", text, flags=re.S)),
        "markdown_tables": sum(1 for line in text.splitlines() if line.strip().startswith("|")),
        "blockquote_lines": sum(1 for line in text.splitlines() if line.strip().startswith(">")),
        "numeric_citations": len(re.findall(r"\[[0-9]+(?:\],?\s*\[[0-9]+|,\s*[0-9]+)*\]", text)),
        "doi_or_url": len(re.findall(r"(?:doi:\s*\S+|https?://\S+)", text, flags=re.I)),
    }


def sentences(text: str) -> list[str]:
    compact = re.sub(r"```.*?```", " ", text, flags=re.S)
    compact = re.sub(r"\n\|.*", " ", compact)
    parts = re.split(r"(?<=[.!?])\s+", compact)
    return [p.strip() for p in parts if len(p.strip()) > 20]


def prose_paragraphs(text: str) -> list[str]:
    compact = re.sub(r"```.*?```", "\n\n", text, flags=re.S)
    compact = re.split(
        r"(?im)^(?:#{1,6}\s*)?(?:glosario|bibliograf[ií]a|referencias)\s*$",
        compact,
        maxsplit=1,
    )[0]
    blocks = re.split(r"(?:\r?\n){2,}", compact)
    paragraphs = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        if any(line.startswith("|") for line in lines):
            continue
        if all(re.match(r"^(?:#{1,6}\s|>|[-*+]\s|\d+[.)]\s)", line) for line in lines):
            continue
        paragraph = " ".join(
            line for line in lines
            if not re.match(r"^(?:#{1,6}\s|>)", line)
        ).strip()
        if len(WORD_RE.findall(paragraph)) >= 8:
            paragraphs.append(paragraph)
    return paragraphs


def paragraph_profile(text: str, short_words: int = 60) -> dict[str, object]:
    paragraphs = prose_paragraphs(text)
    lengths = [len(WORD_RE.findall(paragraph)) for paragraph in paragraphs]
    short_flags = [length < short_words for length in lengths]
    runs = []
    start = None
    for index, is_short in enumerate(short_flags + [False]):
        if is_short and start is None:
            start = index
        elif not is_short and start is not None:
            run_length = index - start
            if run_length >= 2:
                runs.append({"start_paragraph": start + 1, "length": run_length})
            start = None
    return {
        "total_words": len(WORD_RE.findall(text)),
        "prose_words": sum(lengths),
        "paragraph_count": len(lengths),
        "avg_words": round(statistics.mean(lengths), 1) if lengths else None,
        "median_words": round(statistics.median(lengths), 1) if lengths else None,
        "stdev_words": round(statistics.pstdev(lengths), 1) if len(lengths) >= 2 else None,
        "under_60_words": sum(length < 60 for length in lengths),
        "short_words_threshold": short_words,
        "short_paragraph_count": sum(short_flags),
        "under_35_words": sum(length < 35 for length in lengths),
        "short_paragraph_ratio": round(sum(short_flags) / len(lengths), 3) if lengths else None,
        "fragmented_runs": runs,
        "max_fragmented_run": max((run["length"] for run in runs), default=0),
    }


def compare_profiles(current: dict[str, object], baseline: dict[str, object], min_ratio: float = 0.95, max_ratio: float = 1.10) -> dict[str, object]:
    current_words = int(current["prose_words"])
    baseline_words = int(baseline["prose_words"])
    ratio = current_words / baseline_words if baseline_words else None
    current_short = current["short_paragraph_ratio"]
    baseline_short = baseline["short_paragraph_ratio"]
    warnings = []
    if ratio is not None and ratio < min_ratio:
        warnings.append(f"La proporción de prosa editable es inferior a {min_ratio:g}; revisar compresión editorial.")
    if ratio is not None and ratio > max_ratio:
        warnings.append(f"La proporción de prosa editable supera {max_ratio:g}; revisar si la ampliación aporta contenido.")
    if current_short is not None and baseline_short is not None and current_short - baseline_short >= 0.10:
        warnings.append(f"Aumentó la proporción de párrafos menores de {current.get('short_words_threshold', 60)} palabras.")
    if int(current["max_fragmented_run"]) > int(baseline["max_fragmented_run"]):
        warnings.append("Aumentó la racha máxima de párrafos breves consecutivos.")
    return {
        "prose_word_ratio": round(ratio, 3) if ratio is not None else None,
        "prose_word_change_percent": round((ratio - 1) * 100, 1) if ratio is not None else None,
        "paragraph_count_change": int(current["paragraph_count"]) - int(baseline["paragraph_count"]),
        "median_words_change": (
            round(float(current["median_words"]) - float(baseline["median_words"]), 1)
            if current["median_words"] is not None and baseline["median_words"] is not None
            else None
        ),
        "warnings": warnings,
    }


def sentence_starts(items: list[str], words: int = 5) -> list[tuple[str, int]]:
    starts = []
    for s in items:
        clean = re.sub(r"^[#>*\-\d.\s]+", "", s.lower())
        tokens = re.findall(r"[a-záéíóúñü]+", clean)
        if len(tokens) >= words:
            starts.append(" ".join(tokens[:words]))
    return collections.Counter(starts).most_common(12)


def phrase_hits(text: str, phrases: list[str]) -> list[dict[str, object]]:
    low = text.lower()
    hits = []
    for phrase in phrases:
        count = low.count(phrase)
        if count:
            hits.append({"phrase": phrase, "count": count})
    return sorted(hits, key=lambda x: (-int(x["count"]), str(x["phrase"])))


def uniformity(items: list[str]) -> dict[str, object]:
    lengths = [len(re.findall(r"\w+", s)) for s in items]
    if len(lengths) < 3:
        return {"sentence_count": len(lengths), "avg_words": None, "stdev_words": None}
    return {
        "sentence_count": len(lengths),
        "avg_words": round(statistics.mean(lengths), 1),
        "stdev_words": round(statistics.pstdev(lengths), 1),
        "low_variation_warning": statistics.pstdev(lengths) < 8,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Señala patrones editoriales que pueden hacer sonar formulaico un texto académico."
    )
    parser.add_argument("input", help="Archivo UTF-8 o '-' para stdin")
    parser.add_argument("--baseline", help="Versión original para comparar extensión y fragmentación")
    parser.add_argument("--json", action="store_true", help="Imprime JSON")
    parser.add_argument("--min-ratio", type=float, default=0.95, help="Proporción mínima orientativa respecto al original")
    parser.add_argument("--max-ratio", type=float, default=1.10, help="Proporción máxima orientativa respecto al original")
    parser.add_argument("--short-words", type=int, default=60, help="Umbral orientativo de párrafo breve")
    args = parser.parse_args()
    if not 0 < args.min_ratio <= args.max_ratio < float('inf') or args.short_words < 1:
        parser.error('Los umbrales deben ser positivos y finitos, con min-ratio <= max-ratio.')

    text = read_text(args.input)
    items = sentences(text)
    result = {
        "protected_content": protected_counts(text),
        "formulaic_phrases": phrase_hits(text, FORMULAIC),
        "overused_connectors": [h for h in phrase_hits(text, CONNECTORS) if int(h["count"]) >= 3],
        "repeated_sentence_starts": [
            {"start": start, "count": count}
            for start, count in sentence_starts(items)
            if count >= 2
        ],
        "sentence_uniformity": uniformity(items),
        "paragraph_profile": paragraph_profile(text, args.short_words),
        "note": "Este análisis no detecta IA; solo prioriza aspectos de edición humana.",
    }
    if args.baseline:
        baseline_profile = paragraph_profile(read_text(args.baseline), args.short_words)
        result["baseline_paragraph_profile"] = baseline_profile
        result["editorial_comparison"] = compare_profiles(result["paragraph_profile"], baseline_profile, args.min_ratio, args.max_ratio)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print("Análisis de marcas editoriales")
    print("=============================")
    print(f"Oraciones analizadas: {result['sentence_uniformity']['sentence_count']}")
    print(f"Contenido protegido: {result['protected_content']}")
    print()
    print("Frases formulaicas:")
    for hit in result["formulaic_phrases"]:
        print(f"- {hit['count']}x {hit['phrase']}")
    if not result["formulaic_phrases"]:
        print("- Sin hallazgos relevantes")
    print()
    print("Conectores sobreusados:")
    for hit in result["overused_connectors"]:
        print(f"- {hit['count']}x {hit['phrase']}")
    if not result["overused_connectors"]:
        print("- Sin hallazgos relevantes")
    print()
    print("Inicios de oración repetidos:")
    for hit in result["repeated_sentence_starts"]:
        print(f"- {hit['count']}x {hit['start']}")
    if not result["repeated_sentence_starts"]:
        print("- Sin hallazgos relevantes")
    print()
    print(f"Uniformidad: {result['sentence_uniformity']}")
    print(f"Perfil de párrafos: {result['paragraph_profile']}")
    if "editorial_comparison" in result:
        print(f"Comparación editorial: {result['editorial_comparison']}")
    print("Nota: este análisis no detecta IA; solo prioriza aspectos de edición humana.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
