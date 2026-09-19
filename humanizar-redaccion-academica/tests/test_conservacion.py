import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from limpiar_entrega_final_txt import clean_text


class ConservacionTests(unittest.TestCase):
    def test_explicit_line_selection_preserves_other_bytes(self):
        text='«Cita».\r\nAndamiaje aprobado.\r\n\r\nDato: 3.\r\n'
        self.assertEqual(clean_text(text,[2])[0],'«Cita».\r\n\r\nDato: 3.\r\n')
        with self.assertRaises(ValueError):
            clean_text(text,[20])

    def test_literal_and_domain_text_are_unchanged(self):
        text = ('«La figura sugerida es preliminar».\n\n'
                'Las figuras, en cambio, quedan como indicaciones para una etapa posterior de maquetación o diseño visual.\n')
        self.assertEqual(clean_text(text)[0], text)

    def test_labels_code_and_spacing_are_not_deleted_by_default(self):
        text = 'Pregunta guía: dato del instrumento.\n```\n\n\nResultado esperado: 2\n```\n'
        self.assertEqual(clean_text(text)[0], text)

    def test_cleaner_and_connector_do_not_overwrite_by_default(self):
        for script in ('limpiar_entrega_final_txt.py', 'conectar_prosa_final_txt.py'):
            with self.subTest(script=script), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / 'original.txt'
                source.write_text('Pregunta guía: conservar.\n', encoding='utf-8')
                result = subprocess.run([sys.executable, str(SCRIPTS/script), str(source)], capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(source.read_text(encoding='utf-8'), 'Pregunta guía: conservar.\n')
                self.assertEqual(len(list(Path(tmp).iterdir())), 1)

    def test_report_cannot_overwrite_input_or_output(self):
        for script in ('limpiar_entrega_final_txt.py', 'conectar_prosa_final_txt.py'):
            for report_on_input in (True, False):
                with self.subTest(script=script, report_on_input=report_on_input), tempfile.TemporaryDirectory() as tmp:
                    source, dest = Path(tmp)/'original.txt', Path(tmp)/'nuevo.txt'
                    source.write_text('Original.\n', encoding='utf-8')
                    result = subprocess.run([sys.executable,str(SCRIPTS/script),str(source),'--out',str(dest),
                                             '--report',str(source if report_on_input else dest)],capture_output=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(source.read_text(encoding='utf-8'),'Original.\n')
                    self.assertFalse(dest.exists())
