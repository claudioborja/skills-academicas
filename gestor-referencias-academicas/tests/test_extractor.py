"""El extractor común conserva el contenido sin imponer un estilo de cita."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class ExtractorTests(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec('fitz'), 'Requiere PyMuPDF')
    def test_shared_extractor_preserves_evidence_and_is_style_neutral(self):
        import pymupdf as fitz
        script = Path(__file__).resolve().parents[1] / 'scripts/pdf_a_contexto.py'
        with tempfile.TemporaryDirectory(prefix='fuentes á ') as tmp:
            pdf = Path(tmp) / 'fuente con espacios.pdf'
            with fitz.open() as doc:
                page = doc.new_page()
                page.insert_text((72, 72), 'Resultados: educación y análisis de evidencia.')
                doc.save(pdf)
            result = subprocess.run([sys.executable, '-X', 'utf8', str(script), str(pdf)],
                                    capture_output=True, encoding='utf-8', timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('educación', result.stdout)
            self.assertNotIn('Referencia IEEE', result.stdout)


if __name__ == '__main__':
    unittest.main()
