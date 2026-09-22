import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from check_preentrega import render, run

class PreentregaTests(unittest.TestCase):
    def test_detects_working_markers_and_operational_headings_in_manuscript(self):
        text = """# Anatomía regional

## Desarrollo autorizado
Contenido del capítulo.

## Plantilla obligatoria de capítulo
- [ ] Verificar fuente.
```text
Pendiente de editar.
```
"""
        result = {item['check']: item for item in run(text)}
        self.assertFalse(result['rotulos_operativos']['ok'])
        self.assertIn('Plantilla obligatoria de capítulo', result['rotulos_operativos']['details']['headings'])
        self.assertFalse(result['marcas_de_trabajo']['ok'])
        self.assertEqual(result['marcas_de_trabajo']['details']['checkboxes'], 1)
        self.assertEqual(result['marcas_de_trabajo']['details']['code_fences'], 2)

    def test_compares_headings_against_authorized_structure(self):
        text = """# Libro
## Capítulo autorizado
## Roles de trabajo
"""
        result = {item['check']: item for item in run(text, expected_headings=['Libro', 'Capítulo autorizado'])}
        self.assertFalse(result['estructura_autorizada']['ok'])
        self.assertEqual(result['estructura_autorizada']['details']['unexpected'], ['Roles de trabajo'])

    def test_detects_skipped_levels_and_duplicate_headings(self):
        text = """# Libro
### Desarrollo
## Desarrollo
"""
        result = {item['check']: item for item in run(text)}
        self.assertFalse(result['jerarquia_titulos']['ok'])
        self.assertEqual(result['jerarquia_titulos']['details']['skipped_levels'], [{'line': 2, 'from': 1, 'to': 3}])
        self.assertEqual(result['jerarquia_titulos']['details']['duplicates'], ['Desarrollo'])

    def test_markdown_report_includes_actionable_details(self):
        results = run('## Roles de trabajo\n- [ ] Verificar fuente.')
        report = render(results, 'manuscrito.md')
        self.assertIn('Roles de trabajo', report)
        self.assertIn('Casillas: 1', report)

    def test_locator_is_detected(self):
        result={item['check']:item for item in run('Texto [1, p. 27].')}
        self.assertTrue(result['citas']['ok'])
        self.assertEqual(result['referencias']['severity'],'alta')

    def test_bibliography_alone_is_not_a_citation(self):
        result={item['check']:item for item in run('Sin citas.\n# Referencias\n[1] Obra.')}
        self.assertFalse(result['citas']['ok'])
