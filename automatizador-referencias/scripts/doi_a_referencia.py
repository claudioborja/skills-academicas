#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs


DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)


@dataclass
class DoiRecord:
    doi: str
    status: str
    title: str = ""
    authors: str = ""
    year: str = ""
    container: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""
    publisher: str = ""
    url: str = ""
    apa: str = ""
    ieee: str = ""
    error: str = ""
    source_type: str = ""
    warnings: list[str] = field(default_factory=list)


def clean_doi(value: str) -> str:
    match = DOI_RE.search(value)
    if not match:
        return value.strip().rstrip(".,;)")
    return match.group(0).rstrip(".,;)").lower()


def author_names(message: dict) -> tuple[str, str]:
    authors = message.get("author") or []
    if not authors:
        return "", ""
    apa_parts = []
    ieee_parts = []
    for item in authors:
        family = item.get("family", "").strip()
        given = item.get("given", "").strip()
        initials = " ".join(f"{part[0]}." for part in given.replace("-", " ").split() if part)
        if family:
            apa_parts.append(f"{family}, {initials}".strip().rstrip(","))
            ieee_parts.append(f"{initials} {family}".strip())
        elif item.get('name'):
            apa_parts.append(item['name'].strip())
            ieee_parts.append(item['name'].strip())
    if len(ieee_parts) > 6:
        ieee = ieee_parts[0] + ' et al.'
    elif len(ieee_parts) == 2:
        ieee = ' and '.join(ieee_parts)
    elif len(ieee_parts) > 2:
        ieee = ', '.join(ieee_parts[:-1]) + ', and ' + ieee_parts[-1]
    else:
        ieee = ''.join(ieee_parts)
    return ", ".join(apa_parts), ieee


def get_year(message: dict) -> str:
    for key in ("published-print", "published-online", "published", "issued"):
        parts = message.get(key, {}).get("date-parts", [])
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def crossref(doi: str, timeout: int = 12) -> DoiRecord:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": "SkillsReferencias/1.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return DoiRecord(doi=doi, status="pendiente", url=f"https://doi.org/{doi}", error=str(exc))

    message = data.get("message", {})
    title = (message.get("title") or [""])[0]
    container = (message.get("container-title") or [""])[0]
    apa_authors, ieee_authors = author_names(message)
    year = get_year(message)
    volume = message.get("volume", "")
    issue = message.get("issue", "")
    pages = message.get("page", "")
    publisher = message.get("publisher", "")
    resolved = message.get("URL", f"https://doi.org/{doi}")

    apa = f"{apa_authors} ({year}). {title}. {container}. https://doi.org/{doi}".strip()
    source_type = message.get('type', '')
    short_container = (message.get('short-container-title') or [container])[0]
    warnings = ['Borrador de metadatos: verificar autoría, fecha, abreviatura oficial, tipo documental y formato. APA también requiere revisión.']
    ieee_bits = [f'*{short_container}*' if short_container else '']
    if volume:
        ieee_bits.append(f"vol. {volume}")
    if issue:
        ieee_bits.append(f"no. {issue}")
    article_number = message.get('article-number', '')
    if pages:
        pages = re.sub(r'(?<=\d)-(?=\d)', '–', pages)
        ieee_bits.append(f"{'pp.' if re.search(r'[-–,]', pages) else 'p.'} {pages}")
    if year:
        ieee_bits.append(year)
    if article_number:
        ieee_bits.append(f'Art. no. {article_number}')
    ieee_bits.append(f"doi: {doi}")
    ieee = f'{ieee_authors}, "{title.rstrip(".,")}," ' + ", ".join(bit for bit in ieee_bits if bit) + '.'
    status = 'borrador'
    if source_type != 'journal-article' or not all((ieee_authors, title, container, year)):
        ieee = ''
        status = 'pendiente'
        warnings.append('No se genera IEEE: tipo no soportado automáticamente o datos esenciales incompletos. Aplicar su modelo manualmente.')

    return DoiRecord(
        doi=doi,
        status=status,
        title=title,
        authors=apa_authors,
        year=year,
        container=container,
        volume=volume,
        issue=issue,
        pages=pages,
        publisher=publisher,
        url=resolved,
        apa=apa,
        ieee=ieee,
        source_type=source_type,
        warnings=warnings,
    )


def render(records: list[DoiRecord], style: str) -> str:
    lines = ["# DOI a referencia", "", "Borradores, no referencias certificadas. Verificar metadatos y modelo documental antes de usar.", "", "| DOI | Estado | Año | Título | Referencia |", "| --- | --- | --- | --- | --- |"]
    for record in records:
        reference = record.apa if style == "apa" else record.ieee
        if not reference:
            reference = f"Pendiente de completar. DOI: https://doi.org/{record.doi}"
        lines.append(
            f"| {record.doi} | {record.status} | {record.year or 'pendiente'} | "
            f"{record.title.replace('|', '\\|') or 'pendiente'} | {reference.replace('|', '\\|')} |"
        )
    lines.append('')
    for record in records:
        lines.extend(f"- {record.doi}: {warning}" for warning in record.warnings)
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Consulta DOI en Crossref y genera referencias base.")
    parser.add_argument("doi", nargs="+", help="DOI, URL DOI o archivo de texto con DOI si usa --from-file")
    parser.add_argument("--from-file", action="store_true", help="Leer DOI desde archivos indicados")
    parser.add_argument("--style", choices=["apa", "ieee"], default="apa")
    parser.add_argument("--out")
    parser.add_argument("--json-out")
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs(args.doi if args.from_file else [], [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))

    values: list[str] = []
    if args.from_file:
        for item in args.doi:
            values.extend(DOI_RE.findall(Path(item).read_text(encoding="utf-8", errors="replace")))
    else:
        values = args.doi
    dois = sorted({clean_doi(value) for value in values if clean_doi(value)})
    records = [crossref(doi) for doi in dois]
    report = render(records, args.style)
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        atomic_write(args.json_out, json.dumps([asdict(r) for r in records], ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
