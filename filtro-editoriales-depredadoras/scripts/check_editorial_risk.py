#!/usr/bin/env python3
"""Check journal/publisher names against the local editorial-risk watchlist."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def names_for(entry: dict) -> list[str]:
    return [entry["name"], *entry.get("aliases", [])]


def match_score(query: str, candidate: str) -> str | None:
    q = normalize(query)
    c = normalize(candidate)
    if not q or not c:
        return None
    if q == c:
        return "exact"
    generic = {'international', 'journal', 'of', 'the', 'and', 'for', 'in', 'research',
               'review', 'revista', 'de', 'la', 'el', 'y', 'editorial', 'publishing',
               'publisher', 'press', 'publications'}
    q_terms = set(q.split()) - generic
    c_terms = set(c.split()) - generic
    if not q_terms or not c_terms:
        return None
    if (f' {q} ' in f' {c} ' or f' {c} ' in f' {q} ') and q_terms & c_terms:
        return 'partial'
    shared = q_terms & c_terms
    if len(shared) >= 2 and len(shared) / len(q_terms | c_terms) >= .75:
        return "term-overlap"
    return None


def load_watchlist() -> dict:
    data_path = Path(__file__).resolve().parents[1] / "references" / "watchlist.json"
    return json.loads(data_path.read_text(encoding="utf-8"))


def check_query(query: str, data: dict) -> dict:
    matches = []
    for level in ("red", "yellow"):
        for entry in data[level]:
            for candidate in names_for(entry):
                score = match_score(query, candidate)
                if score:
                    matches.append(
                        {
                            "level": level,
                            "match": entry["name"],
                            "matched_as": candidate,
                            "score": score,
                            "reason": entry["reason"],
                        }
                    )
                    break
    return {
        "query": query,
        "decision": "review" if matches else "not-found-local-watchlist",
        "matches": matches,
        "note": "A local match is an alert. Confirm with DOI, ISSN, official URL, indexing, and editorial-policy evidence before final classification.",
    }


def read_queries(path: Path) -> list[str]:
    values: list[str] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        value = raw.strip().strip(",;")
        if not value or value.startswith("#"):
            continue
        if "," in value:
            value = value.split(",", 1)[0].strip()
        values.append(value)
    return values


def render_text(results: list[dict]) -> str:
    lines: list[str] = []
    for result in results:
        if not result["matches"]:
            lines.append(f"No local watchlist match for: {result['query']}")
            lines.append(result["note"])
        else:
            lines.append(f"Local watchlist match for: {result['query']}")
            for match in result["matches"]:
                lines.append(f"- {match['level'].upper()}: {match['match']} ({match['score']}; alias: {match['matched_as']})")
                lines.append(f"  Reason: {match['reason']}")
            lines.append(result["note"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check editorial risk by name or batch file.")
    parser.add_argument("query", nargs="*", help="Journal, publisher, conference, or platform name")
    parser.add_argument("--file", help="TXT/CSV file with one query per line")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    parser.add_argument("--out", help="Write text report to file")
    parser.add_argument("--json-out", help="Write JSON report to file")
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.file, Path(__file__).resolve().parents[1]/'references/watchlist.json'], [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))

    queries = read_queries(Path(args.file)) if args.file else [" ".join(args.query).strip()]
    queries = [query for query in queries if query]
    if not queries:
        raise SystemExit("Provide a query or --file.")

    data = load_watchlist()
    results = [check_query(query, data) for query in queries]
    payload = results[0] if len(results) == 1 else {"results": results}
    text_report = render_text(results)

    if args.out:
        atomic_write(args.out, text_report, overwrite=args.overwrite)
    if args.json_out:
        atomic_write(args.json_out, json.dumps(payload, ensure_ascii=False, indent=2), overwrite=args.overwrite)

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif not args.out:
        print(text_report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
