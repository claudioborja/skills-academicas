"""Los umbrales del proyecto cambian las alertas, no el manuscrito."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'


class ConfiguracionTests(unittest.TestCase):
    def test_thresholds_are_configurable_and_preserve_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            current, baseline = Path(tmp) / 'actual.md', Path(tmp) / 'original.md'
            current.write_text(('evidencia ' * 50) + '\n\n' + ('contexto ' * 50), encoding='utf-8')
            baseline.write_text('evidencia ' * 200, encoding='utf-8')
            before = current.read_bytes()
            command = [sys.executable, str(SCRIPTS/'analizar_marcas_ia.py'), str(current),
                       '--baseline', str(baseline), '--json']
            default = subprocess.run(command, capture_output=True, encoding='utf-8')
            custom = subprocess.run(command + ['--min-ratio','0.4','--max-ratio','1.5','--short-words','40'],
                                    capture_output=True, encoding='utf-8')
            self.assertEqual(default.returncode, 0, default.stderr)
            self.assertEqual(custom.returncode, 0, custom.stderr)
            self.assertTrue(json.loads(default.stdout)['editorial_comparison']['warnings'])
            self.assertEqual(json.loads(custom.stdout)['editorial_comparison']['warnings'], [])
            self.assertEqual(json.loads(custom.stdout)['paragraph_profile']['max_fragmented_run'], 0)
            self.assertEqual(current.read_bytes(), before)

    def test_lexical_audit_does_not_assume_an_education_domain(self):
        spec = importlib.util.spec_from_file_location('citation_audit', SCRIPTS/'auditar_respaldo_citas_pdf.py')
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        self.assertNotIn('learning', module.tokens('aprendizaje'))
        self.assertIn('learning', module.tokens('learning'))
        with tempfile.TemporaryDirectory() as tmp:
            vocabulary = Path(tmp) / 'vocabulary.json'
            vocabulary.write_text(json.dumps({'aprendizaje':['learning']}),encoding='utf-8')
            module.load_vocabulary(vocabulary)
            self.assertIn('learning', module.tokens('aprendizaje'))

    @unittest.skipUnless(importlib.util.find_spec('fitz'), 'Requiere PyMuPDF')
    def test_citation_audit_uses_manifest_without_project_code(self):
        import pymupdf as fitz
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            passage = 'La evidencia documental exige revisar el contexto, los resultados y las limitaciones antes de utilizar una fuente para respaldar una afirmación científica.'
            with fitz.open() as doc:
                page = doc.new_page()
                page.insert_textbox((72,72,500,700), passage)
                doc.save(project/'fuente.pdf')
            (project/'referencias.json').write_text(json.dumps([{'id':1,'label':'Fuente verificada','pdf':'fuente.pdf'}]),encoding='utf-8')
            (project/'libro.md').write_text('# Evidencia\n\n'+passage+' [1].',encoding='utf-8')
            output = project/'auditoria.txt'
            result = subprocess.run([sys.executable,str(SCRIPTS/'auditar_respaldo_citas_pdf.py'),str(project),
                                     '--manifest',str(project/'referencias.json'),'--book',str(project/'libro.md'),
                                     '--out',str(output)],capture_output=True,encoding='utf-8')
            self.assertEqual(result.returncode,0,result.stderr)
            report=output.read_text(encoding='utf-8')
            self.assertIn('Fuente verificada',report)
            self.assertIn('pagina 1',report)


if __name__ == '__main__':
    unittest.main()
