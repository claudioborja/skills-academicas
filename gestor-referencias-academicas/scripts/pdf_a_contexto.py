#!/usr/bin/env python3
"""
Convierte PDFs academicos en un paquete de lectura compacto para el skill
gestor-referencias-academicas, independiente del estilo de citación.

Ejemplos:
  python pdf_a_contexto.py articulo.pdf --out lectura.md
  python pdf_a_contexto.py https://sitio/articulo.pdf --download-dir refs/pdfs --out refs/metadata/articulo.md
  python pdf_a_contexto.py refs/pdfs --recursive --json-out refs/metadata/lecturas.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import textwrap
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs


DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
SPACE_RE = re.compile(r"[ \t]+")
LINEBREAK_RE = re.compile(r"\n{3,}")

PROFILE_KEYWORDS = {
    "fuente": ["resumen", "abstract", "objetivo", "resultados", "conclusiones", "doi"],
    "imryd": ["introducción", "objetivo", "método", "metodología", "resultados", "discusión", "limitaciones", "conclusiones"],
    "tesis": ["objetivo general", "objetivos específicos", "metodología", "resultados", "conclusiones", "recomendaciones", "marco teórico"],
}

SECTION_PATTERNS = {
    "resumen": re.compile(r"(?im)^\s*(resumen|abstract)\s*$"),
    "introduccion": re.compile(r"(?im)^\s*(introducci[oó]n|introduction)\s*$"),
    "metodologia": re.compile(r"(?im)^\s*(metodolog[ií]a|m[eé]todo|methodology|methods?)\s*$"),
    "resultados": re.compile(r"(?im)^\s*(resultados|results?|hallazgos|findings)\s*$"),
    "discusion": re.compile(r"(?im)^\s*(discusi[oó]n|discussion)\s*$"),
    "conclusiones": re.compile(r"(?im)^\s*(conclusiones?|conclusions?)\s*$"),
    "referencias": re.compile(r"(?im)^\s*(referencias|bibliograf[ií]a|references)\s*$"),
}


@dataclass
class PageText:
    page: int
    text: str


@dataclass
class PdfContext:
    source: str
    local_path: str
    sha256: str
    bytes: int
    extracted_at: str
    extractor: str
    page_count: int
    dois: list[str]
    title_guess: str
    section_hits: dict[str, list[int]]
    pages: list[dict[str, object]]
    relevant_snippets: list[dict[str, object]]


def normalize_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = SPACE_RE.sub(" ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = LINEBREAK_RE.sub("\n\n", text)
    return text.strip()


def compact_text(text: str, max_chars: int) -> str:
    text = normalize_text(text)
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars]
    last_space = cut.rfind(" ")
    if last_space > max_chars * 0.75:
        cut = cut[:last_space]
    return cut.rstrip() + " [...]"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_filename_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    name = Path(urllib.parse.unquote(parsed.path)).name or "documento.pdf"
    if not name.lower().endswith(".pdf"):
        name += ".pdf"
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
    return name or "documento.pdf"


def download_pdf(url: str, download_dir: Path, max_bytes: int = 50 * 1024 * 1024) -> Path:
    if urllib.parse.urlparse(url).scheme not in {'https', 'http'}:
        raise ValueError('Solo se admiten descargas HTTP(S).')
    if max_bytes < 1:
        raise ValueError('El límite de descarga debe ser positivo.')
    download_dir.mkdir(parents=True, exist_ok=True)
    name = Path(safe_filename_from_url(url))
    suffix = hashlib.sha256(url.encode('utf-8')).hexdigest()[:12] + '-' + uuid.uuid4().hex[:12]
    target = download_dir / (name.stem[:80] + '-' + suffix + '.pdf')
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 pdf-a-contexto-ieee/1.0",
            "Accept": "application/pdf,*/*",
        },
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        content_type = response.headers.get("Content-Type", "")
        data = response.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise RuntimeError(f'PDF supera el límite de {max_bytes} bytes.')
    if not data.lstrip().startswith(b"%PDF-"):
        raise RuntimeError(f"La URL no parece entregar un PDF: {content_type or 'sin Content-Type'}")
    atomic_write(target, data)
    return target


def extract_with_pymupdf(path: Path) -> tuple[str, list[PageText]]:
    import pymupdf as fitz  # type: ignore

    pages: list[PageText] = []
    with fitz.open(path) as document:
        for index, page in enumerate(document, start=1):
            pages.append(PageText(index, normalize_text(page.get_text("text"))))
    return "PyMuPDF", pages


def extract_with_pypdf(path: Path) -> tuple[str, list[PageText]]:
    from pypdf import PdfReader  # type: ignore

    reader = PdfReader(str(path))
    pages = [
        PageText(index, normalize_text(page.extract_text() or ""))
        for index, page in enumerate(reader.pages, start=1)
    ]
    return "pypdf", pages


def extract_pdf(path: Path) -> tuple[str, list[PageText]]:
    errors: list[str] = []
    for extractor in (extract_with_pymupdf, extract_with_pypdf):
        try:
            name, pages = extractor(path)
            if any(page.text for page in pages):
                return name, pages
            errors.append(f"{name}: no extrajo texto")
        except ImportError as exc:
            errors.append(str(exc))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{extractor.__name__}: {exc}")
    detail = "\n".join(f"- {error}" for error in errors)
    raise RuntimeError(
        "No se pudo extraer texto del PDF. Instala una dependencia y reintenta:\n"
        "  pip install pymupdf\n"
        "o:\n"
        "  pip install pypdf\n\n"
        f"Detalle:\n{detail}"
    )


def guess_title(pages: list[PageText]) -> str:
    first_page = pages[0].text if pages else ""
    candidates = []
    for line in first_page.splitlines()[:30]:
        clean = line.strip()
        if 12 <= len(clean) <= 180 and not DOI_RE.search(clean):
            if not re.search(r"^(issn|doi|vol\.|núm\.|num\.|www\.|http)", clean, re.I):
                candidates.append(clean)
    return candidates[0] if candidates else "Título no detectado"


def detect_section_hits(pages: list[PageText]) -> dict[str, list[int]]:
    hits: dict[str, list[int]] = {name: [] for name in SECTION_PATTERNS}
    for page in pages:
        for name, pattern in SECTION_PATTERNS.items():
            if pattern.search(page.text):
                hits[name].append(page.page)
    return {name: nums for name, nums in hits.items() if nums}


def keyword_score(text: str, keywords: list[str]) -> int:
    lower = text.lower()
    return sum(lower.count(keyword.lower()) for keyword in keywords if keyword.strip())


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    return re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ0-9])", text)


def build_snippets(pages: list[PageText], keywords: list[str], limit: int) -> list[dict[str, object]]:
    snippets: list[dict[str, object]] = []
    if not keywords:
        return snippets
    for page in pages:
        sentences = split_sentences(page.text)
        scored = [(keyword_score(sentence, keywords), sentence) for sentence in sentences]
        for score, sentence in sorted(scored, reverse=True)[:2]:
            if score > 0:
                snippets.append(
                    {
                        "page": page.page,
                        "score": score,
                        "text": compact_text(sentence, 650),
                    }
                )
    snippets.sort(key=lambda item: (-int(item["score"]), int(item["page"])))
    return snippets[:limit]


def build_context(path: Path, source: str, args: argparse.Namespace) -> PdfContext:
    extractor, pages = extract_pdf(path)
    full_text = "\n\n".join(page.text for page in pages)
    dois = sorted({match.group(0).rstrip(".,;:)").lower() for match in DOI_RE.finditer(full_text)})
    profile_keywords = PROFILE_KEYWORDS.get(args.profile, [])
    effective_keywords = [*profile_keywords, *args.keywords]
    page_summaries = []
    for page in pages:
        page_summaries.append(
            {
                "page": page.page,
                "chars": len(page.text),
                "preview": compact_text(page.text, args.page_chars),
            }
        )
    return PdfContext(
        source=source,
        local_path=str(path),
        sha256=sha256_file(path),
        bytes=path.stat().st_size,
        extracted_at=datetime.now().isoformat(timespec="seconds"),
        extractor=extractor,
        page_count=len(pages),
        dois=dois,
        title_guess=guess_title(pages),
        section_hits=detect_section_hits(pages),
        pages=page_summaries,
        relevant_snippets=build_snippets(pages, effective_keywords, args.snippet_limit),
    )


def render_markdown(contexts: list[PdfContext]) -> str:
    blocks = ["# Contexto simplificado de PDFs para referencias IEEE\n"]
    for idx, ctx in enumerate(contexts, start=1):
        blocks.append(f"## Documento {idx}: {ctx.title_guess}\n")
        blocks.append(f"- Fuente original: `{ctx.source}`")
        blocks.append(f"- Ruta local: `{ctx.local_path}`")
        blocks.append(f"- Extractor: {ctx.extractor}")
        blocks.append(f"- Páginas: {ctx.page_count}")
        blocks.append(f"- Tamaño: {ctx.bytes} bytes")
        blocks.append(f"- SHA-256: `{ctx.sha256}`")
        blocks.append(f"- Fecha de extracción: {ctx.extracted_at}")
        blocks.append("- DOI detectados: " + (", ".join(f"`{doi}`" for doi in ctx.dois) if ctx.dois else "No detectado"))
        if ctx.section_hits:
            hits = "; ".join(f"{name}: pp. {', '.join(map(str, pages))}" for name, pages in ctx.section_hits.items())
            blocks.append(f"- Secciones detectadas: {hits}")
        else:
            blocks.append("- Secciones detectadas: No detectadas por encabezado simple")

        if ctx.relevant_snippets:
            blocks.append("\n### Fragmentos relevantes por palabras clave\n")
            for snippet in ctx.relevant_snippets:
                blocks.append(f"**p. {snippet['page']} | score {snippet['score']}**")
                blocks.append("")
                blocks.append(f"> {snippet['text']}")
                blocks.append("")

        blocks.append("\n### Vista rápida por página\n")
        for page in ctx.pages:
            blocks.append(f"#### Página {page['page']} ({page['chars']} caracteres)\n")
            preview = str(page["preview"]).replace("\n", "\n\n")
            blocks.append(preview or "_Sin texto extraíble en esta página._")
            blocks.append("")

        blocks.append("### Ficha de decisión para el skill\n")
        blocks.append("- Pertinencia para la afirmación: Pendiente de evaluar.")
        blocks.append("- Secciones leídas: Pendiente de completar.")
        blocks.append("- Decisión: pendiente.")
        blocks.append("- Afirmaciones que podría respaldar: Pendiente de completar.")
        blocks.append("- Referencia preliminar (aplicar la norma del proyecto): Pendiente de completar.\n")
    return "\n".join(blocks).rstrip() + "\n"


def iter_inputs(input_path: str, recursive: bool) -> Iterable[str]:
    parsed = urllib.parse.urlparse(input_path)
    if parsed.scheme in {"http", "https"}:
        yield input_path
        return
    path = Path(input_path)
    if path.is_dir():
        pattern = "**/*.pdf" if recursive else "*.pdf"
        for pdf in sorted(path.glob(pattern)):
            yield str(pdf)
    else:
        yield input_path


def resolve_input(item: str, download_dir: Path) -> tuple[str, Path]:
    parsed = urllib.parse.urlparse(item)
    if parsed.scheme in {"http", "https"}:
        return item, download_pdf(item, download_dir)
    path = Path(item)
    if not path.exists():
        raise FileNotFoundError(f"No existe: {item}")
    return item, path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extrae texto de PDFs y genera un contexto simple para revisar fuentes académicas.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="PDF local, carpeta con PDFs o URL directa a PDF")
    parser.add_argument("--recursive", action="store_true", help="Procesa subcarpetas cuando input es una carpeta")
    parser.add_argument("--download-dir", default="referencias-descargadas/pdfs", help="Carpeta para PDFs descargados desde URL; indicar la del proyecto cuando exista")
    parser.add_argument("--out", help="Archivo Markdown de salida. Si se omite, imprime en pantalla")
    parser.add_argument("--json-out", help="Archivo JSON de salida con los mismos datos estructurados")
    parser.add_argument("--overwrite", action="store_true", help="Reemplazar reportes existentes, nunca PDFs de entrada.")
    parser.add_argument("--page-chars", type=int, default=1800, help="Caracteres máximos por página en Markdown")
    parser.add_argument("--snippet-limit", type=int, default=12, help="Cantidad máxima de fragmentos relevantes")
    parser.add_argument("--profile", choices=["ninguno", "fuente", "imryd", "tesis"], default="ninguno", help="Perfil de palabras clave para lectura compacta")
    parser.add_argument(
        "--keywords",
        nargs="*",
        default=[],
        help="Palabras clave para extraer fragmentos relevantes; ejemplo: --keywords privacidad datos consentimiento",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    contexts: list[PdfContext] = []
    errors: list[str] = []
    download_dir = Path(args.download_dir)
    items = list(iter_inputs(args.input, args.recursive))
    validate_outputs([item for item in items if urllib.parse.urlparse(item).scheme not in {'http', 'https'}],
                     [args.out, args.json_out], args.overwrite)

    for item in items:
        try:
            source, path = resolve_input(item, download_dir)
            contexts.append(build_context(path, source, args))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{item}: {exc}")

    if not contexts:
        print("No se generó contexto para ningún PDF.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    markdown = render_markdown(contexts)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(out_path, markdown, args.overwrite)
    else:
        print(markdown)

    if args.json_out:
        json_path = Path(args.json_out)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(json_path,
            json.dumps([asdict(context) for context in contexts], ensure_ascii=False, indent=2),
            args.overwrite,
        )

    if errors:
        print("Algunos archivos no pudieron procesarse:", file=sys.stderr)
        for error in errors:
            wrapped = textwrap.fill(error, width=100, subsequent_indent="  ")
            print(f"- {wrapped}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
