#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import csv
import sys
from pathlib import Path

from common import read_records, write_csv, write_json, atomic_write, atomic_output, validate_outputs


def count_by(rows: list[dict], key: str) -> list[dict]:
    counter = collections.Counter(str(row.get(key, "") or "sin_dato") for row in rows)
    return [{key: name, "count": count} for name, count in counter.most_common()]


def year_type_table(rows: list[dict]) -> list[dict]:
    counter = collections.Counter((str(row.get("year", "") or "sin_año"), str(row.get("article_type", "") or "sin_tipo")) for row in rows)
    return [{"year": year, "article_type": kind, "count": count} for (year, kind), count in sorted(counter.items())]


def write_markdown(path: Path, tables: dict[str, list[dict]], charts: list[str], warnings: list[str], overwrite=False) -> None:
    lines = ["# Tabulación y visualización", ""]
    if warnings:
        lines.append("## Advertencias")
        lines.extend(f"- {w}" for w in warnings)
        lines.append("")
    for name, rows in tables.items():
        lines.append(f"## {name}")
        if not rows:
            lines.append("- Sin datos.")
            continue
        fields = list(rows[0].keys())
        lines.append("| " + " | ".join(fields) + " |")
        lines.append("| " + " | ".join(["---"] * len(fields)) + " |")
        for row in rows:
            lines.append("| " + " | ".join(str(row.get(field, "")).replace("|", "\\|") for field in fields) + " |")
        lines.append("")
    if charts:
        lines.append("## Gráficos")
        lines.extend(f"- `{chart}`" for chart in charts)
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(path, "\n".join(lines).rstrip() + "\n", overwrite)


def try_charts(tables: dict[str, list[dict]], out_dir: Path, prefix: str, overwrite=False) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    charts: list[str] = []
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except Exception:
        return [], ["matplotlib no está instalado; se generaron solo tablas CSV/JSON/Markdown."]

    for name, rows in tables.items():
        if name == "year_type" or not rows:
            continue
        label_key = next((key for key in rows[0].keys() if key != "count"), None)
        if not label_key:
            continue
        labels = [str(row[label_key]) for row in rows[:12]]
        values = [int(row["count"]) for row in rows[:12]]
        plt.figure(figsize=(9, 5))
        plt.barh(list(reversed(labels)), list(reversed(values)), color="#3B82F6")
        plt.xlabel("Cantidad")
        plt.title(name.replace("_", " ").title())
        plt.tight_layout()
        chart_path = out_dir / f"{prefix}_{name}.png"
        try:
            with atomic_output(chart_path, overwrite) as output:
                plt.savefig(output, format='png', dpi=160)
        finally:
            plt.close()
        charts.append(str(chart_path))
    return charts, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera tablas CSV y gráficos PNG desde clasificación/matriz bibliográfica.")
    parser.add_argument("input")
    parser.add_argument("--out-dir", default="exploracion-temas")
    parser.add_argument("--prefix", default="exploracion")
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    if not args.prefix or any(char in args.prefix for char in '/\\:') or args.prefix in ('.', '..'):
        parser.error('--prefix debe ser un nombre simple, no una ruta')

    rows = read_records(args.input)
    out_dir = Path(args.out_dir)
    names = [f'{args.prefix}_{name}.csv' for name in ('article_type', 'topic', 'year', 'year_type')]
    names += [f'{args.prefix}_{name}.png' for name in ('article_type', 'topic', 'year')]
    names += [f'{args.prefix}_tablas.json', f'{args.prefix}_reporte.md']
    try:
        validate_outputs([args.input], [out_dir/name for name in names], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    out_dir.mkdir(parents=True, exist_ok=True)
    tables = {
        "article_type": count_by(rows, "article_type"),
        "topic": count_by(rows, "topic"),
        "year": count_by(rows, "year"),
        "year_type": year_type_table(rows),
    }
    for name, table in tables.items():
        write_csv(str(out_dir / f"{args.prefix}_{name}.csv"), table, overwrite=args.overwrite)
    charts, warnings = try_charts(tables, out_dir, args.prefix, args.overwrite)
    write_json(str(out_dir / f"{args.prefix}_tablas.json"), tables, overwrite=args.overwrite)
    write_markdown(out_dir / f"{args.prefix}_reporte.md", tables, charts, warnings, args.overwrite)
    print(f"Reporte: {out_dir / f'{args.prefix}_reporte.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
