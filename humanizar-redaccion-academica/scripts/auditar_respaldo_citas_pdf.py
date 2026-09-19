#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_write, validate_outputs


STOPWORDS = {
    "a", "al", "algo", "ante", "antes", "asi", "aunque", "bajo", "cada", "como", "con",
    "contra", "cuando", "de", "del", "desde", "donde", "dos", "e", "el", "ella", "ellas",
    "ellos", "en", "entre", "esa", "esas", "ese", "eso", "esos", "esta", "estas", "este",
    "esto", "estos", "ha", "hay", "la", "las", "le", "les", "lo", "los", "mas", "mi",
    "mientras", "muy", "no", "o", "para", "pero", "por", "porque", "que", "se", "segun",
    "si", "sin", "sobre", "son", "su", "sus", "tambien", "tanto", "un", "una", "unas",
    "uno", "unos", "y", "ya", "the", "and", "with", "from", "this", "that",
}
SPANISH_ENGLISH_HINTS: dict[str, list[str]] = {}


def load_vocabulary(path: Path | None) -> None:
    """Cargar equivalencias opcionales del proyecto, sin un dominio implícito."""
    values = json.loads(path.read_text(encoding="utf-8")) if path else {}
    if not isinstance(values, dict) or any(
        not isinstance(key, str) or not isinstance(items, list)
        or not all(isinstance(item, str) for item in items)
        for key, items in values.items()
    ):
        raise ValueError("El vocabulario debe ser un objeto JSON de término a lista de equivalentes.")
    SPANISH_ENGLISH_HINTS.clear()
    SPANISH_ENGLISH_HINTS.update({normalize(key): [normalize(item) for item in items] for key, items in values.items()})


@dataclass
class PdfParagraph:
    ref_id: int
    page: int
    paragraph: int
    text: str


def repair_mojibake(text: str) -> str:
    if not isinstance(text, str):
        return text
    if not any(mark in text for mark in ("Ã", "Â", "Å", "Ä")):
        return text
    for encoding in ("cp1252", "latin1"):
        try:
            repaired = text.encode(encoding).decode("utf-8")
            if repaired.count("Ã") + repaired.count("Â") < text.count("Ã") + text.count("Â"):
                return repaired
        except UnicodeError:
            continue
    return text


def normalize(text: str) -> str:
    text = repair_mojibake(text).lower()
    text = text.translate(str.maketrans("áéíóúüñ", "aeiouun"))
    return text


def tokens(text: str) -> list[str]:
    normalized = normalize(text)
    raw = re.findall(r"[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]{4,}", normalized)
    result: list[str] = []
    for token in raw:
        if token in STOPWORDS:
            continue
        result.append(token)
        for hint in SPANISH_ENGLISH_HINTS.get(token, []):
            result.append(hint)
    return result


def load_references(manifest: Path, project_dir: Path) -> dict[int, dict]:
    rows = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("El manifiesto debe contener una lista de referencias.")
    refs = {}
    for row in rows:
        if not isinstance(row, dict) or type(row.get("id")) is not int or row["id"] < 1:
            raise ValueError("Cada referencia necesita un id entero positivo.")
        rid = row["id"]
        if rid in refs or not isinstance(row.get("pdf"), str) or not row["pdf"]:
            raise ValueError("Los identificadores deben ser únicos y cada referencia necesita una ruta pdf.")
        path = Path(row["pdf"])
        start = row.get("references_start_page")
        if start is not None and (type(start) is not int or start < 1):
            raise ValueError("references_start_page debe ser un entero positivo.")
        refs[rid] = {
            "label": repair_mojibake(str(row.get("label", f"Referencia {rid}"))),
            "ieee": repair_mojibake(str(row.get("reference", row.get("ieee", "")))),
            "pdf": path if path.is_absolute() else project_dir / path,
            "references_start_page": start,
        }
    return refs


def pdf_path_for_ref(refs: dict[int, dict], ref_id: int) -> Path | None:
    path = refs.get(ref_id, {}).get("pdf")
    return path if path is not None and path.is_file() else None


def extract_pdf_paragraphs(refs: dict[int, dict], ref_id: int) -> list[PdfParagraph]:
    path = pdf_path_for_ref(refs, ref_id)
    if path is None:
        return []
    try:
        import pymupdf as fitz  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PyMuPDF no esta instalado; no puedo auditar PDFs.") from exc

    paragraphs: list[PdfParagraph] = []
    refs_start = refs.get(ref_id, {}).get('references_start_page')
    with fitz.open(path) as doc:
        for page_index, page in enumerate(doc, 1):
            if refs_start is not None and page_index >= refs_start:
                continue
            text = page.get_text("text")
            text = repair_mojibake(text)
            pieces = re.split(r"\n\s*\n|(?<=\.)\s*\n(?=[A-Z0-9])", text)
            para_no = 0
            for piece in pieces:
                cleaned = re.sub(r"\s+", " ", piece).strip()
                if len(cleaned) < 120:
                    continue
                lowered = cleaned.lower()
                if any(marker in lowered for marker in (
                    "e-mail", "email", "@", "corresponding author", "copyright",
                    "creative commons", "all rights reserved", "doi.org", "references",
                    "bibliography", "available online", "received:", "accepted:",
                )):
                    continue
                if re.match(r"^\[?\d+\]?\s+[A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñ\-]+,", cleaned):
                    continue
                if len(re.findall(r"\bdoi\b|10\.\d{4,9}/", lowered)) >= 1:
                    continue
                if len(tokens(cleaned)) < 8:
                    continue
                para_no += 1
                paragraphs.append(PdfParagraph(ref_id, page_index, para_no, cleaned))
    return paragraphs


def split_book_paragraphs(book_text: str) -> list[tuple[str, str, list[int]]]:
    current_section = "Preliminares"
    items: list[tuple[str, str, list[int]]] = []
    in_bibliography = False
    for raw in re.split(r"\n\s*\n", book_text):
        paragraph = raw.strip()
        if not paragraph:
            continue
        if normalize(paragraph) == "bibliografia":
            in_bibliography = True
            continue
        if in_bibliography:
            continue
        if re.match(r"^\d+\.\d+\.\s+", paragraph):
            current_section = paragraph
            continue
        ids = sorted({int(match) for match in re.findall(r"\[(\d+)\]", paragraph)})
        if ids:
            items.append((current_section, paragraph, ids))
    return items


def score(query: Counter[str], paragraph: PdfParagraph) -> float:
    paragraph_tokens = Counter(tokens(paragraph.text))
    if not paragraph_tokens:
        return 0.0
    shared = set(query) & set(paragraph_tokens)
    if not shared:
        return 0.0
    weighted = sum(min(query[t], paragraph_tokens[t]) * (1.0 + math.log1p(len(t))) for t in shared)
    density = weighted / math.sqrt(sum(query.values()) * sum(paragraph_tokens.values()))
    return density


def clean_query_text(book_paragraph: str, refs: dict[int, dict]) -> str:
    cleaned = re.sub(r"\[\d+\]", " ", book_paragraph)
    for ref in refs.values():
        label = ref.get("label", "")
        if label:
            cleaned = cleaned.replace(label, " ")
            for piece in re.split(r",| y | and | et al\.?", label):
                piece = piece.strip()
                if len(piece) > 2:
                    cleaned = re.sub(re.escape(piece), " ", cleaned, flags=re.I)
    return cleaned


def best_support(
    book_paragraph: str,
    pdf_paragraphs: list[PdfParagraph],
    refs: dict[int, dict],
) -> tuple[PdfParagraph | None, float]:
    query = Counter(tokens(clean_query_text(book_paragraph, refs)))
    best: PdfParagraph | None = None
    best_score = 0.0
    for paragraph in pdf_paragraphs:
        current = score(query, paragraph)
        if current > best_score:
            best = paragraph
            best_score = current
    return best, best_score


def trim(text: str, limit: int = 420) -> str:
    cleaned = re.sub(r"\s+", " ", repair_mojibake(text)).strip()
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 1].rsplit(" ", 1)[0] + "..."


def reason(book_paragraph: str, support: PdfParagraph | None) -> str:
    if support is None:
        return "No se encontro un parrafo de soporte en el PDF local."
    book_terms = set(tokens(book_paragraph))
    support_terms = set(tokens(support.text))
    shared = sorted(book_terms & support_terms, key=lambda t: (-len(t), t))[:10]
    if not shared:
        return "La relacion es debil: requiere revision manual antes de conservar la cita."
    return "Coincidencias lexicas que requieren comprobar el sentido y el contexto: " + ", ".join(shared) + ". No demuestran respaldo."


def make_report(project_dir: Path, book_path: Path, out_path: Path, manifest: Path, overwrite=False) -> None:
    refs = load_references(manifest, project_dir)
    validate_outputs([book_path, manifest, *(ref['pdf'] for ref in refs.values())], [out_path], overwrite)

    book_text = book_path.read_text(encoding="utf-8")
    cited_paragraphs = split_book_paragraphs(book_text)
    used_ids = sorted({rid for _section, _paragraph, ids in cited_paragraphs for rid in ids})

    pdf_cache: dict[int, list[PdfParagraph]] = {}
    for rid in used_ids:
        pdf_cache[rid] = extract_pdf_paragraphs(refs, rid)

    lines: list[str] = [
        "Auditoria de respaldo de citas",
        "",
        f"Libro auditado: {book_path}",
        f"Parrafos del libro con citas: {len(cited_paragraphs)}",
        f"Referencias citadas auditadas: {len(used_ids)}",
        "",
        "Criterio de lectura",
        "",
        (
            "Cada entrada compara el parrafo citado del libro con el PDF local correspondiente. "
            "El campo 'parrafo fuente' identifica pagina y numero de parrafo extraido automaticamente del PDF. "
            "El fragmento es un candidato por similitud lexica. Revisar siempre el PDF y el contexto, cualquiera sea el puntaje; no certifica respaldo semantico."
        ),
        "",
    ]

    weak = 0
    total_checks = 0
    for item_no, (section, paragraph, ids) in enumerate(cited_paragraphs, 1):
        lines.extend([
            f"Entrada {item_no}",
            f"Ubicacion en el libro: {section}",
            f"Parrafo del libro: {trim(paragraph, 700)}",
            f"Citas en el parrafo: {', '.join(f'[{rid}]' for rid in ids)}",
            "",
        ])
        for rid in ids:
            total_checks += 1
            support, support_score = best_support(paragraph, pdf_cache.get(rid, []), refs)
            if support_score < 0.08:
                weak += 1
            pdf_path = pdf_path_for_ref(refs, rid)
            lines.append(f"Referencia [{rid}]: {refs.get(rid, {}).get('label', 'Referencia no registrada')}")
            lines.append(f"Archivo PDF: {pdf_path if pdf_path else 'No localizado'}")
            if support is None:
                lines.append("Parrafo fuente: NO LOCALIZADO")
                lines.append("Fragmento de soporte: NO LOCALIZADO")
            else:
                lines.append(
                    f"Parrafo fuente: pagina {support.page}, parrafo extraido {support.paragraph} del PDF"
                )
                lines.append(f"Puntaje de afinidad textual: {support_score:.3f}")
                lines.append(f"Que dice el documento fuente: {trim(support.text)}")
            lines.append(f"Por que respalda la cita: {reason(paragraph, support)}")
            if support_score < 0.08:
                lines.append("Alerta: respaldo debil; conviene revisar manualmente o reemplazar la cita.")
            lines.append("")
        lines.append("-" * 80)
        lines.append("")

    by_ref = defaultdict(int)
    for _section, _paragraph, ids in cited_paragraphs:
        for rid in ids:
            by_ref[rid] += 1

    summary = [
        "Resumen ejecutivo",
        "",
        f"Comprobaciones cita-documento realizadas: {total_checks}",
        f"Comprobaciones con respaldo debil: {weak}",
        "Uso de referencias en el libro:",
    ]
    for rid in used_ids:
        summary.append(f"- [{rid}] {refs.get(rid, {}).get('label', '')}: {by_ref[rid]} apariciones auditadas")
    summary.extend(["", "=" * 80, ""])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(out_path, "\n".join(summary + lines), overwrite)
    print(f"Informe creado: {out_path}")
    print(f"Parrafos citados: {len(cited_paragraphs)}")
    print(f"Comprobaciones: {total_checks}")
    print(f"Respaldos debiles: {weak}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--book", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True, help="JSON con id, label y ruta pdf relativa al proyecto")
    parser.add_argument("--vocabulary", type=Path, help="JSON opcional de término a lista de equivalentes")
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        validate_outputs([args.book, args.manifest, args.vocabulary], [args.out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    load_vocabulary(args.vocabulary)
    make_report(args.project_dir.resolve(), args.book.resolve(), args.out.absolute(), args.manifest.resolve(), args.overwrite)


if __name__ == "__main__":
    main()
