#!/usr/bin/env python3
"""Normaliza espacios OMML y tablas de numeración de ecuaciones en un DOCX."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from xml.etree import ElementTree as ET
import zipfile


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
XML = "http://www.w3.org/XML/1998/namespace"
NS = {"w": W, "m": M}

ET.register_namespace("w", W)
ET.register_namespace("m", M)

EQUATION_NUMBER_RE = re.compile(r"^\([A-Za-z]?\d+(?:\.\d+)*(?:[A-Za-z])?\)$")
STORY_PART_RE = re.compile(
    r"^word/(?:document|header\d+|footer\d+|footnotes|endnotes)\.xml$"
)


def qn(namespace: str, local: str) -> str:
    return f"{{{namespace}}}{local}"


def direct_children(parent: ET.Element, tag: str) -> list[ET.Element]:
    return [child for child in parent if child.tag == tag]


def ensure_first(parent: ET.Element, tag: str) -> ET.Element:
    child = parent.find(f"./{tag}", NS)
    if child is None:
        child = ET.Element(qn(W, tag.split(":", 1)[1]))
        parent.insert(0, child)
    return child


def ensure_child(parent: ET.Element, local: str) -> ET.Element:
    tag = qn(W, local)
    child = parent.find(f"./w:{local}", NS)
    if child is None:
        child = ET.SubElement(parent, tag)
    return child


def clean_math_spacing(root: ET.Element) -> int:
    changes = 0
    parent_map = {child: parent for parent in root.iter() for child in parent}
    for run in list(root.findall(".//m:r", NS)):
        texts = run.findall(".//m:t", NS)
        if not texts:
            continue
        if all(not (node.text or "").strip() for node in texts):
            parent = parent_map.get(run)
            if parent is not None:
                parent.remove(run)
                changes += 1
            continue
        for node in texts:
            original = node.text or ""
            cleaned = original.strip(" \t\r\n")
            if cleaned != original:
                node.text = cleaned
                node.attrib.pop(qn(XML, "space"), None)
                changes += 1
    return changes


def cell_text(cell: ET.Element) -> str:
    values = []
    for path in (".//w:t", ".//m:t", ".//w:instrText"):
        values.extend((node.text or "") for node in cell.findall(path, NS))
    return "".join(values).strip()


def has_equation_number(cell: ET.Element) -> bool:
    text = cell_text(cell).replace(" ", "")
    if EQUATION_NUMBER_RE.fullmatch(text):
        return True
    instructions = " ".join(
        (node.text or "") for node in cell.findall(".//w:instrText", NS)
    )
    return bool(re.search(r"\bSEQ\b", instructions, flags=re.IGNORECASE))


def is_numbered_equation_table(table: ET.Element) -> bool:
    rows = direct_children(table, qn(W, "tr"))
    if not rows:
        return False
    for row in rows:
        cells = direct_children(row, qn(W, "tc"))
        if len(cells) != 3:
            return False
        left, equation, number = cells
        if cell_text(left) or equation.find(".//m:oMath", NS) is None or not has_equation_number(number):
            return False
    return True


def numeric_width(element: ET.Element | None) -> int | None:
    if element is None:
        return None
    raw = element.get(qn(W, "w"))
    if raw is None:
        return None
    try:
        value = int(raw)
    except ValueError:
        return None
    return value if value > 0 else None


def table_widths(table: ET.Element) -> tuple[int, int]:
    columns = table.findall("./w:tblGrid/w:gridCol", NS)
    widths = [numeric_width(column) for column in columns]
    if len(widths) == 3 and all(width is not None for width in widths):
        return int(widths[0]) + int(widths[1]), int(widths[2])
    total = numeric_width(table.find("./w:tblPr/w:tblW", NS)) or 9360
    number = min(max(round(total * 0.11), 720), 1100)
    return total - number, number


def set_cell_width(cell: ET.Element, width: int) -> ET.Element:
    properties = ensure_first(cell, "w:tcPr")
    cell_width = ensure_child(properties, "tcW")
    cell_width.set(qn(W, "w"), str(width))
    cell_width.set(qn(W, "type"), "dxa")
    return properties


def set_paragraph_alignment(cell: ET.Element, value: str) -> None:
    for paragraph in direct_children(cell, qn(W, "p")):
        properties = ensure_first(paragraph, "w:pPr")
        justification = ensure_child(properties, "jc")
        justification.set(qn(W, "val"), value)


def transform_equation_table(table: ET.Element) -> None:
    equation_width, number_width = table_widths(table)
    properties = ensure_first(table, "w:tblPr")
    layout = ensure_child(properties, "tblLayout")
    layout.set(qn(W, "type"), "fixed")

    grid = table.find("./w:tblGrid", NS)
    if grid is None:
        grid = ET.Element(qn(W, "tblGrid"))
        table.insert(1 if table.find("./w:tblPr", NS) is not None else 0, grid)
    for column in list(grid):
        grid.remove(column)
    for width in (equation_width, number_width):
        column = ET.SubElement(grid, qn(W, "gridCol"))
        column.set(qn(W, "w"), str(width))

    for row in direct_children(table, qn(W, "tr")):
        left, equation, number = direct_children(row, qn(W, "tc"))
        row.remove(left)
        equation_properties = set_cell_width(equation, equation_width)
        number_properties = set_cell_width(number, number_width)
        ensure_child(equation_properties, "vAlign").set(qn(W, "val"), "center")
        ensure_child(number_properties, "vAlign").set(qn(W, "val"), "center")
        ensure_child(number_properties, "noWrap")
        set_paragraph_alignment(equation, "center")
        set_paragraph_alignment(number, "right")


def normalize_part(data: bytes) -> tuple[bytes, int, int]:
    root = ET.fromstring(data)
    spaces = clean_math_spacing(root)
    tables = 0
    for table in root.findall(".//w:tbl", NS):
        if is_numbered_equation_table(table):
            transform_equation_table(table)
            tables += 1
    if not spaces and not tables:
        return data, 0, 0
    return ET.tostring(root, encoding="utf-8", xml_declaration=True), spaces, tables


def normalize_docx(source: Path, output: Path) -> dict[str, int]:
    if output.exists():
        raise FileExistsError(f"El archivo de salida ya existe: {output}")
    if source == output:
        raise ValueError("La salida no puede reemplazar la entrada")
    if source.suffix.lower() != ".docx" or output.suffix.lower() != ".docx":
        raise ValueError("La entrada y la salida deben usar la extensión .docx")
    if not zipfile.is_zipfile(source):
        raise ValueError(f"La entrada no es un DOCX válido: {source}")

    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output.stem}.", suffix=".docx", dir=output.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    totals = {"separadores_omml_limpiados": 0, "tablas_convertidas": 0}
    try:
        with zipfile.ZipFile(source, "r") as incoming, zipfile.ZipFile(
            temporary, "w"
        ) as outgoing:
            for info in incoming.infolist():
                data = incoming.read(info.filename)
                if STORY_PART_RE.fullmatch(info.filename):
                    data, spaces, tables = normalize_part(data)
                    totals["separadores_omml_limpiados"] += spaces
                    totals["tablas_convertidas"] += tables
                outgoing.writestr(info, data)
        os.replace(temporary, output)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return totals


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="DOCX de origen")
    parser.add_argument("--out", required=True, type=Path, help="DOCX nuevo de salida")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        source = args.input.resolve(strict=True)
        if not source.is_file():
            raise ValueError(f"La entrada no es un archivo: {source}")
        output = args.out.resolve()
        totals = normalize_docx(source, output)
        print(json.dumps({"status": "ok", "out": str(output), **totals}, ensure_ascii=False))
        return 0
    except (ET.ParseError, FileExistsError, OSError, ValueError, zipfile.BadZipFile) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
