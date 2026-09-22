#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import html
import json
import re
import statistics
import sys
import zipfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs
from typing import Any
from xml.etree import ElementTree as ET


CONNECTORS = [
    "ademas", "además", "asimismo", "tambien", "también", "sin embargo", "no obstante",
    "por tanto", "por lo tanto", "por ello", "en consecuencia", "de este modo",
    "en este sentido", "ahora bien", "por otra parte", "en cambio", "a su vez",
    "conviene", "cabe destacar", "en terminos", "en términos", "dicho de otro modo",
    "en la practica", "en la práctica", "desde esta perspectiva",
]

HEDGES = [
    "puede", "podria", "podría", "suele", "tiende", "parece", "conviene",
    "en cierta medida", "en algunos casos", "segun", "según", "probablemente",
    "no siempre", "depende", "cuando", "siempre que",
]

STOPWORDS = {
    "para", "como", "pero", "esta", "este", "estos", "estas", "desde", "sobre", "entre",
    "tambien", "también", "ademas", "además", "porque", "cuando", "donde", "hacia",
    "tiene", "tienen", "puede", "pueden", "debe", "deben", "sido", "cada", "todo",
    "toda", "todos", "todas", "que", "los", "las", "una", "uno", "del", "por", "con",
}


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_docx(path: Path) -> str:
    paragraphs: list[str] = []
    with zipfile.ZipFile(path) as zf:
        names = [name for name in zf.namelist() if name.startswith("word/") and name.endswith(".xml")]
        targets = [name for name in names if name == "word/document.xml"]
        targets += [name for name in names if name.startswith("word/header") or name.startswith("word/footer")]
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        for name in targets:
            root = ET.fromstring(zf.read(name))
            for para in root.findall(".//w:p", ns):
                parts = [node.text or "" for node in para.findall(".//w:t", ns)]
                text = "".join(parts).strip()
                if text:
                    paragraphs.append(text)
    return "\n\n".join(paragraphs)


def read_pdf(path: Path) -> str:
    try:
        import pymupdf as fitz  # type: ignore
    except Exception:
        fitz = None
    if fitz is not None:
        parts = []
        with fitz.open(path) as doc:
            for page in doc:
                parts.append(page.get_text("text"))
        return "\n\n".join(parts)
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception as exc:
        raise SystemExit("Para leer PDF instala PyMuPDF o pypdf.") from exc
    reader = PdfReader(str(path))
    return "\n\n".join(page.extract_text() or "" for page in reader.pages)


def strip_html(text: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", text)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</p>", "\n\n", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)


def read_any(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return read_docx(path)
    if suffix == ".pdf":
        return read_pdf(path)
    if suffix in {".html", ".htm"}:
        return strip_html(read_text_file(path))
    return read_text_file(path)


def clean_for_analysis(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"(?m)^\s*\|.*$", " ", text)
    text = re.sub(r"https?://\S+|doi:\s*\S+|10\.\d{4,9}/[-._;()/:A-Z0-9]+", " ", text, flags=re.I)
    return re.sub(r"\s+", " ", text).strip()


def paragraphs(text: str) -> list[str]:
    chunks = re.split(r"\n\s*\n+", text)
    return [re.sub(r"\s+", " ", p).strip() for p in chunks if len(p.strip()) > 40]


def sentences(text: str) -> list[str]:
    text = clean_for_analysis(text)
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [part.strip() for part in parts if len(part.strip()) > 20]


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{3,}", text.lower())


def count_hits(text: str, phrases: list[str]) -> list[dict[str, Any]]:
    low = text.lower()
    hits = []
    for phrase in phrases:
        count = len(re.findall(rf"(?<!\w){re.escape(phrase.lower())}(?!\w)", low))
        if count:
            hits.append({"phrase": phrase, "count": count})
    return sorted(hits, key=lambda item: (-item["count"], item["phrase"]))[:20]


def ngrams(items: list[str], n: int) -> list[str]:
    grams = []
    for i in range(0, max(0, len(items) - n + 1)):
        chunk = items[i : i + n]
        if any(token in STOPWORDS for token in chunk):
            continue
        grams.append(" ".join(chunk))
    return grams


def top_terms(text: str) -> dict[str, list[dict[str, Any]]]:
    toks = [token for token in words(text) if token not in STOPWORDS]
    return {
        "keywords": [{"term": term, "count": count} for term, count in collections.Counter(toks).most_common(20)],
        "bigrams": [{"term": term, "count": count} for term, count in collections.Counter(ngrams(toks, 2)).most_common(12)],
        "trigrams": [{"term": term, "count": count} for term, count in collections.Counter(ngrams(toks, 3)).most_common(10)],
    }


def start_patterns(items: list[str]) -> list[dict[str, Any]]:
    starts = []
    for item in items:
        toks = words(item)
        if len(toks) >= 4:
            starts.append(" ".join(toks[:4]))
    return [{"start": start, "count": count} for start, count in collections.Counter(starts).most_common(15) if count > 1]


def stats(lengths: list[int]) -> dict[str, Any]:
    if not lengths:
        return {"count": 0, "avg": 0, "median": 0, "stdev": 0, "min": 0, "max": 0}
    return {
        "count": len(lengths),
        "avg": round(statistics.mean(lengths), 2),
        "median": round(statistics.median(lengths), 2),
        "stdev": round(statistics.pstdev(lengths), 2) if len(lengths) > 1 else 0,
        "min": min(lengths),
        "max": max(lengths),
    }


def punctuation_profile(items: list[str]) -> dict[str, float]:
    if not items:
        return {}
    marks = {",": 0, ";": 0, ":": 0, "(": 0, "?": 0, "!": 0}
    for item in items:
        for mark in marks:
            marks[mark] += item.count(mark)
    return {mark: round(count / len(items), 3) for mark, count in marks.items()}


def protected_counts(text: str) -> dict[str, int]:
    return {
        "fenced_blocks": len(re.findall(r"```.*?```", text, flags=re.S)),
        "markdown_tables": sum(1 for line in text.splitlines() if line.strip().startswith("|")),
        "blockquote_lines": sum(1 for line in text.splitlines() if line.strip().startswith(">")),
        "numeric_citations": len(re.findall(r"\[[0-9]+(?:\],?\s*\[[0-9]+|,\s*[0-9]+)*\]", text)),
        "doi_or_url": len(re.findall(r"(?:doi:\s*\S+|https?://\S+|10\.\d{4,9}/[-._;()/:A-Z0-9]+)", text, flags=re.I)),
    }


def classify_voice(sentence_lengths: list[int], connector_hits: list[dict[str, Any]], hedge_hits: list[dict[str, Any]]) -> list[str]:
    notes = []
    if sentence_lengths:
        avg = statistics.mean(sentence_lengths)
        stdev = statistics.pstdev(sentence_lengths) if len(sentence_lengths) > 1 else 0
        if avg > 32:
            notes.append("Predominan oraciones largas y explicativas.")
        elif avg < 18:
            notes.append("Predominan oraciones breves o de ritmo directo.")
        else:
            notes.append("Ritmo medio, con espacio para alternar explicacion y cierre.")
        if stdev < 7:
            notes.append("La longitud de las oraciones es bastante uniforme; conviene introducir mas variacion.")
        elif stdev > 15:
            notes.append("Hay variacion marcada de ritmo entre oraciones densas y frases mas cortas.")
    if connector_hits:
        notes.append("La cohesion depende de conectores explicitos; diversificar relaciones logicas al reescribir.")
    if hedge_hits:
        notes.append("El estilo usa matizadores; conservar prudencia argumentativa y evitar afirmaciones absolutas.")
    return notes


def build_profile(paths: list[Path]) -> dict[str, Any]:
    sources = []
    texts = []
    for path in paths:
        text = read_any(path)
        sources.append({"path": str(path), "characters": len(text), "words": len(words(text))})
        texts.append(text)
    raw = "\n\n".join(texts)
    pars = paragraphs(raw)
    sents = sentences(raw)
    sentence_lengths = [len(words(item)) for item in sents]
    paragraph_lengths = [len(words(item)) for item in pars]
    connectors = count_hits(raw, CONNECTORS)
    hedges = count_hits(raw, HEDGES)
    return {
        "sources": sources,
        "counts": {"characters": len(raw), "words": len(words(raw)), "paragraphs": len(pars), "sentences": len(sents)},
        "protected_content": protected_counts(raw),
        "sentence_stats": stats(sentence_lengths),
        "paragraph_stats": stats(paragraph_lengths),
        "punctuation_per_sentence": punctuation_profile(sents),
        "connectors": connectors,
        "hedges": hedges,
        "repeated_sentence_starts": start_patterns(sents),
        "repeated_paragraph_starts": start_patterns(pars),
        "terms": top_terms(clean_for_analysis(raw)),
        "voice_notes": classify_voice(sentence_lengths, connectors, hedges),
        "style_directives": [
            "Usar el perfil como guia de ritmo y decisiones, no como banco de frases copiables.",
            "Variar entradas de parrafo y cierres para evitar molde repetido.",
            "Conservar citas, DOI, URL, tablas, codigo, formulas y referencias.",
            "Mantener matices si el perfil los usa; no convertir el texto en afirmaciones absolutas.",
            "Agregar concrecion solo cuando el contenido la permita.",
        ],
    }


def render(profile: dict[str, Any]) -> str:
    lines = ["# Perfil de estilo", "", "## Fuentes"]
    for src in profile["sources"]:
        lines.append(f"- `{src['path']}`: {src['words']} palabras")
    lines.extend(["", "## Ritmo", ""])
    lines.append(f"- Oraciones: {profile['sentence_stats']}")
    lines.append(f"- Parrafos: {profile['paragraph_stats']}")
    lines.append(f"- Puntuacion por oracion: {profile['punctuation_per_sentence']}")
    lines.extend(["", "## Conectores frecuentes", ""])
    lines.extend(f"- {item['phrase']}: {item['count']}" for item in profile["connectors"]) if profile["connectors"] else lines.append("- Sin conectores destacados.")
    lines.extend(["", "## Matizadores", ""])
    lines.extend(f"- {item['phrase']}: {item['count']}" for item in profile["hedges"]) if profile["hedges"] else lines.append("- Sin matizadores destacados.")
    lines.extend(["", "## Inicios repetidos", ""])
    if profile["repeated_paragraph_starts"]:
        lines.extend(f"- Parrafo: {item['count']}x {item['start']}" for item in profile["repeated_paragraph_starts"])
    if profile["repeated_sentence_starts"]:
        lines.extend(f"- Oracion: {item['count']}x {item['start']}" for item in profile["repeated_sentence_starts"])
    if not profile["repeated_paragraph_starts"] and not profile["repeated_sentence_starts"]:
        lines.append("- No se detectaron repeticiones fuertes.")
    lines.extend(["", "## Terminos caracteristicos", ""])
    lines.extend(f"- {item['term']}: {item['count']}" for item in profile["terms"]["keywords"][:12])
    lines.extend(["", "## Notas de voz", ""])
    lines.extend(f"- {note}" for note in profile["voice_notes"])
    lines.extend(["", "## Directrices de reescritura", ""])
    lines.extend(f"- {item}" for item in profile["style_directives"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extrae un perfil de estilo desde PDF, DOCX, HTML, TXT o Markdown.")
    parser.add_argument("inputs", nargs="+", help="Documento(s) modelo.")
    parser.add_argument("--out", help="Salida Markdown.")
    parser.add_argument("--json-out", help="Salida JSON.")
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs(args.inputs, [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    paths = [Path(item) for item in args.inputs]
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise SystemExit("No existen: " + ", ".join(missing))
    profile = build_profile(paths)
    report = render(profile)
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        atomic_write(args.json_out, json.dumps(profile, ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
