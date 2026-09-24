"""Pruebas funcionales de normalización de ecuaciones OMML en DOCX."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import zipfile
from xml.etree import ElementTree as ET


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "normalizar_ecuaciones_word.py"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
NS = {"w": W, "m": M}


CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""

ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""


def document_xml(body: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{W}" xmlns:m="{M}"><w:body>{body}<w:sectPr/></w:body></w:document>"""


def equation_table(left: str = "", number: str = "(1)") -> str:
    return f"""
<w:tbl>
  <w:tblPr><w:tblW w:w="5800" w:type="dxa"/></w:tblPr>
  <w:tblGrid><w:gridCol w:w="1000"/><w:gridCol w:w="4000"/><w:gridCol w:w="800"/></w:tblGrid>
  <w:tr>
    <w:tc><w:tcPr><w:tcW w:w="1000" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>{left}</w:t></w:r></w:p></w:tc>
    <w:tc><w:tcPr><w:tcW w:w="4000" w:type="dxa"/></w:tcPr><w:p><m:oMath>
      <m:r><m:t>a</m:t></m:r><m:r><m:t xml:space="preserve"> </m:t></m:r>
      <m:r><m:t>+</m:t></m:r><m:r><m:t xml:space="preserve"> b </m:t></m:r>
    </m:oMath></w:p></w:tc>
    <w:tc><w:tcPr><w:tcW w:w="800" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>{number}</w:t></w:r></w:p></w:tc>
  </w:tr>
</w:tbl>"""


def ordinary_table() -> str:
    cells = "".join(f"<w:tc><w:p><w:r><w:t>{value}</w:t></w:r></w:p></w:tc>" for value in ("A", "B", "C"))
    return f"<w:tbl><w:tblGrid><w:gridCol/><w:gridCol/><w:gridCol/></w:tblGrid><w:tr>{cells}</w:tr></w:tbl>"


def write_docx(path: Path, body: str) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as package:
        package.writestr("[Content_Types].xml", CONTENT_TYPES)
        package.writestr("_rels/.rels", ROOT_RELS)
        package.writestr("word/document.xml", document_xml(body))


def read_document(path: Path) -> ET.Element:
    with zipfile.ZipFile(path) as package:
        return ET.fromstring(package.read("word/document.xml"))


class NormalizarEcuacionesWordTests(unittest.TestCase):
    def run_script(self, body: str, output_exists: bool = False):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        source = root / "entrada.docx"
        output = root / "salida.docx"
        write_docx(source, body)
        if output_exists:
            output.write_bytes(b"conservar")
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--input", str(source), "--out", str(output)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=20,
        )
        return completed, source, output

    def test_removes_empty_math_spacing_without_losing_symbols(self):
        completed, source, output = self.run_script(equation_table())

        self.assertEqual(completed.returncode, 0, completed.stderr)
        root = read_document(output)
        math_texts = [node.text or "" for node in root.findall(".//m:oMath//m:t", NS)]
        self.assertEqual(math_texts, ["a", "+", "b"])
        self.assertEqual("".join(math_texts), "a+b")
        original = read_document(source)
        self.assertEqual(len(original.findall(".//m:oMath//m:r", NS)), 4)

    def test_converts_only_numbered_equation_tables_to_two_columns(self):
        completed, _, output = self.run_script(equation_table() + ordinary_table())

        self.assertEqual(completed.returncode, 0, completed.stderr)
        root = read_document(output)
        tables = root.findall(".//w:tbl", NS)
        equation, ordinary = tables
        self.assertEqual(len(equation.findall("./w:tblGrid/w:gridCol", NS)), 2)
        cells = equation.findall("./w:tr/w:tc", NS)
        self.assertEqual(len(cells), 2)
        self.assertIsNotNone(cells[0].find(".//m:oMath", NS))
        self.assertEqual("".join(cells[1].itertext()).strip(), "(1)")
        self.assertEqual(cells[0].find("./w:tcPr/w:tcW", NS).get(f"{{{W}}}w"), "5000")
        self.assertEqual(cells[0].find("./w:p/w:pPr/w:jc", NS).get(f"{{{W}}}val"), "center")
        self.assertEqual(cells[1].find("./w:p/w:pPr/w:jc", NS).get(f"{{{W}}}val"), "right")
        self.assertIsNotNone(cells[1].find("./w:tcPr/w:noWrap", NS))
        self.assertEqual(len(ordinary.findall("./w:tr/w:tc", NS)), 3)

    def test_does_not_convert_ambiguous_three_column_table(self):
        completed, _, output = self.run_script(equation_table(left="nota"))

        self.assertEqual(completed.returncode, 0, completed.stderr)
        table = read_document(output).find(".//w:tbl", NS)
        self.assertEqual(len(table.findall("./w:tr/w:tc", NS)), 3)

    def test_existing_output_is_preserved(self):
        completed, _, output = self.run_script(equation_table(), output_exists=True)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("ya existe", completed.stderr.lower())
        self.assertEqual(output.read_bytes(), b"conservar")


if __name__ == "__main__":
    unittest.main()
