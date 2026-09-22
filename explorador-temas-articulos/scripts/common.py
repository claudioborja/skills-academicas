from __future__ import annotations

import csv
import io
import sys
import json
import re
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, atomic_output, validate_outputs


DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)


def norm_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def read_records(path: str) -> list[dict[str, Any]]:
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".json":
        data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        if isinstance(data, dict):
            for key in ("records", "items", "sources", "results"):
                if isinstance(data.get(key), list):
                    data = data[key]
                    break
        if not isinstance(data, list):
            raise SystemExit("JSON debe contener una lista de registros o una clave records/items/sources/results.")
        return [{norm_key(str(k)): v for k, v in item.items()} for item in data if isinstance(item, dict)]
    if suffix == ".csv":
        with p.open("r", encoding="utf-8-sig", errors="replace", newline="") as fh:
            rows = list(csv.DictReader(fh))
        return [{norm_key(str(k)): v for k, v in row.items()} for row in rows]
    return records_from_text(p.read_text(encoding="utf-8", errors="replace"))


def records_from_text(text: str) -> list[dict[str, Any]]:
    chunks = re.split(r"(?m)^#{1,3}\s+", text)
    records = []
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        lines = [line.strip() for line in chunk.splitlines() if line.strip()]
        title = lines[0] if lines else "Sin título"
        doi_match = DOI_RE.search(chunk)
        year_match = re.search(r"\b(19|20)\d{2}\b", chunk)
        records.append(
            {
                "title": title,
                "abstract": " ".join(lines[1:]),
                "doi": doi_match.group(0).rstrip(".,;)").lower() if doi_match else "",
                "year": year_match.group(0) if year_match else "",
                "source": "",
                "keywords": "",
            }
        )
    return records


def write_csv(path: str, rows: list[dict[str, Any]], fieldnames: list[str] | None = None, overwrite=False) -> None:
    if not rows:
        fieldnames = fieldnames or []
    else:
        fieldnames = fieldnames or sorted({key for row in rows for key in row})
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with io.StringIO(newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})
        atomic_write(out, fh.getvalue(), overwrite)


def write_json(path: str, payload: Any, overwrite=False) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(out, json.dumps(payload, ensure_ascii=False, indent=2), overwrite)


def tokens(text: str) -> list[str]:
    stop = {
        "para", "with", "from", "that", "this", "and", "the", "los", "las", "una", "uno", "del", "por",
        "con", "sobre", "entre", "como", "into", "using", "based", "study", "studies", "analysis",
        "educacion", "education", "higher", "superior", "articulo", "paper", "research",
    }
    words = [w.lower() for w in re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{4,}", text)]
    return [w for w in words if w not in stop]


def compact(text: str, limit: int = 180) -> str:
    text = re.sub(r"\s+", " ", str(text)).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "..."
