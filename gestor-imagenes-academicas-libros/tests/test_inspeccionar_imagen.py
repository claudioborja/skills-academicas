"""Pruebas del inspector técnico de imágenes rasterizadas."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/inspeccionar_imagen.py'


class InspeccionarImagenTests(unittest.TestCase):
    def run_inspector(self, image, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(image), '--ancho-cm', '10.16',
             '--ppi-minimo', '300', *arguments],
            capture_output=True, text=True, encoding='utf-8', timeout=20,
        )

    def test_reports_dimensions_and_effective_resolution(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / 'opaca.png'
            Image.new('RGB', (1200, 600), 'white').save(image)
            result = self.run_inspector(image)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual((report['ancho_px'], report['alto_px']), (1200, 600))
            self.assertEqual(report['ppi_efectivo'], 300.0)
            self.assertTrue(report['cumple_ppi'])
            self.assertFalse(report['tiene_transparencia'])
            self.assertEqual(report['estado'], 'aprobada')

    def test_reports_real_transparency_and_low_resolution(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / 'transparente.png'
            resource = Image.new('RGBA', (300, 200), (255, 0, 0, 255))
            resource.putpixel((0, 0), (255, 0, 0, 0))
            resource.save(image)
            result = self.run_inspector(image)
            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(result.stdout)
            self.assertTrue(report['canal_alpha'])
            self.assertTrue(report['tiene_transparencia'])
            self.assertEqual(report['ppi_efectivo'], 75.0)
            self.assertFalse(report['cumple_ppi'])
            self.assertEqual(report['estado'], 'advertencia')

    def test_corrupt_image_is_reported_and_report_can_be_saved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image, output = root / 'dañada.png', root / 'informe.json'
            image.write_bytes(b'no es una imagen')
            result = self.run_inspector(image, '--out', str(output))
            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(output.read_text(encoding='utf-8'))
            self.assertFalse(report['integridad'])
            self.assertEqual(report['estado'], 'rechazada')
            self.assertIn('error', report)


if __name__ == '__main__':
    unittest.main()
