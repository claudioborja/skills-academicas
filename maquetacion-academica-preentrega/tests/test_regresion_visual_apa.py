from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from regresion_visual_apa import check_pdf, run_suite


class RenderChecksTests(unittest.TestCase):
    def make_pdf(self, folder, *, number_x=534, missing_number=False,
                 border=None, body_page=3, extra_page=False):
        path = Path(folder) / 'prueba.pdf'
        with pymupdf.open() as pdf:
            for number in range(1, 5 if extra_page else 4):
                page = pdf.new_page(width=612, height=792)
                if not missing_number:
                    page.insert_text((number_x, 45), str(number), fontsize=12)
                page.insert_text((72, 45), 'APRENDIZAJE', fontsize=12)
                if number == 1:
                    page.insert_text((180, 155), 'Titulo de prueba', fontsize=12)
                    if border is not None:
                        page.draw_line((72, 170), (540, 170), color=border)
                if number == 2:
                    page.insert_text((72, 90), 'Resumen', fontsize=12)
                    page.insert_text((72, 125), 'Sintesis controlada.', fontsize=12)
                if number == body_page:
                    page.insert_text((72, 180), 'Titulo de prueba', fontsize=12)
                    page.insert_text((72, 215), 'Cuerpo controlado.', fontsize=12)
            pdf.save(path)
        return path

    def check(self, path):
        return check_pdf(path, title='Titulo de prueba', running_head='APRENDIZAJE',
                         abstract_marker='Sintesis controlada.', body_marker='Cuerpo controlado.')

    def test_accepts_expected_rendered_geometry(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self.check(self.make_pdf(tmp))['errors'], [])

    def test_detects_colored_and_black_decorative_borders(self):
        for color in ((0.31, 0.51, 0.74), (0, 0, 0)):
            with self.subTest(color=color), tempfile.TemporaryDirectory() as tmp:
                result = self.check(self.make_pdf(tmp, border=color))
                self.assertIn('cover_border', [e['code'] for e in result['errors']])

    def test_detects_centered_and_missing_page_numbers(self):
        for options in ({'number_x': 303}, {'missing_number': True}):
            with self.subTest(options=options), tempfile.TemporaryDirectory() as tmp:
                result = self.check(self.make_pdf(tmp, **options))
                self.assertIn('page_number', [e['code'] for e in result['errors']])

    def test_detects_body_on_abstract_page_and_extra_blank_page(self):
        for options, code in (({'body_page': 2}, 'body_page'), ({'extra_page': True}, 'page_count')):
            with self.subTest(options=options), tempfile.TemporaryDirectory() as tmp:
                result = self.check(self.make_pdf(tmp, **options))
                self.assertIn(code, [e['code'] for e in result['errors']])

    def test_cli_refuses_existing_output_before_rendering(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'existente'
            target.mkdir()
            sentinel = target / 'original.txt'
            sentinel.write_text('conservar', encoding='utf-8')
            script = Path(__file__).resolve().parents[1] / 'scripts/regresion_visual_apa.py'
            result = subprocess.run([sys.executable, str(script), '--out', str(target),
                                     '--renderer-python', sys.executable, '--renderer-script', str(script)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(list(target.iterdir()), [sentinel])
            self.assertEqual(sentinel.read_text(encoding='utf-8'), 'conservar')

    def test_renderer_failure_is_reported_as_error_not_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            renderer = Path(tmp) / 'renderizador fallido.py'
            renderer.write_text('raise SystemExit(9)\n', encoding='utf-8')
            output = Path(tmp) / 'resultado'
            report = run_suite(output, Path(sys.executable), renderer)
            self.assertEqual(report['status'], 'error')
            self.assertEqual(len(report['cases']), 4)
            self.assertTrue(all(any(e['code'] == 'execution' for e in c['errors']) for c in report['cases']))
            self.assertTrue((output / 'informe.json').is_file())

    def test_missing_dependency_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'resultado'
            with self.assertRaises(ValueError):
                run_suite(output, Path(sys.executable), Path(tmp) / 'no-existe.py')
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
