import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from auditar_citas_bibliografia import audit
from doi_a_referencia import author_names, crossref, get_year


class CitationTests(unittest.TestCase):
    def test_locators_do_not_become_reference_numbers(self):
        result = audit('Texto [1, p. 27], [2, Ch. 3, pp. 5–10].\n# Referencias\n[1] Uno.\n[2] Dos.')
        self.assertEqual(result.numeric_citations, [1, 2])
        self.assertEqual(result.uncited_numeric_references, [])

    def test_first_appearance_order_is_checked(self):
        result = audit('Texto [2], [1].\n# Referencias\n[1] Uno.\n[2] Dos.')
        self.assertTrue(any('orden' in w.lower() for w in result.warnings))

    def test_duplicate_labels_are_reported(self):
        result = audit('Texto [1].\n# Referencias\n[1] Uno.\n[1] Otro.')
        self.assertTrue(any('duplicad' in w.lower() for w in result.warnings))

    def test_legacy_ranges_are_expanded_and_flagged(self):
        result = audit('Texto [1]–[3].\nReferences\n[1] Uno.\n[2] Dos.\n[3] Tres.')
        self.assertEqual(result.numeric_citations, [1, 2, 3])
        self.assertTrue(any('rango' in w.lower() for w in result.warnings))

    def test_code_and_appendix_are_not_bibliography(self):
        result = audit('Texto [1]. `vector[8]`\n```python\nx[9]\n```\n# Referencias\n[1] Uno.\n# Apéndice\n[2] Dato.')
        self.assertEqual(result.numeric_citations, [1, 2])  # el apéndice sigue siendo texto citable
        self.assertEqual(result.numeric_references, [1])

    def test_absent_heading_does_not_treat_citation_as_reference(self):
        result = audit('[1] afirma esto.')
        self.assertEqual(result.numeric_references, [])
        self.assertTrue(any('sección' in w.lower() for w in result.warnings))

    def test_strict_cli_returns_nonzero_for_missing_reference(self):
        with tempfile.TemporaryDirectory(prefix='ieee prueba ') as tmp:
            source = Path(tmp) / 'citación.md'
            source.write_text('Texto [1].\n# Referencias\n', encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPTS / 'auditar_citas_bibliografia.py'),
                                     str(source), '--style', 'ieee', '--strict'],
                                    capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn('sin referencia: 1', result.stdout)

    def test_valid_ieee_reuse_has_no_errors(self):
        result = audit('Texto [1], [2]; repetición [1, eq. (2)].\n# References\n[1] Uno.\n[2] Dos.', 'ieee')
        self.assertEqual(result.errors, [])
        self.assertEqual(result.first_appearance, [1, 2])

    def test_bad_ranges_do_not_expand_unboundedly(self):
        for citation in ('[9–2]', '[1–999999999]'):
            with self.subTest(citation=citation):
                self.assertTrue(audit(citation, 'ieee').errors)

    def test_six_authors_are_not_abbreviated(self):
        names = [{'given': 'Ana', 'family': f'Autor{i}'} for i in range(1, 7)]
        result = author_names({'author': names})[1]
        self.assertNotIn('et al.', result)
        self.assertTrue(result.endswith(', and A. Autor6'))


class MetadataTests(unittest.TestCase):
    def test_seven_authors_are_abbreviated(self):
        authors = [{'given': 'Ana', 'family': f'Autor{i}'} for i in range(1, 8)]
        self.assertEqual(author_names({'author': authors})[1], 'A. Autor1 et al.')

    def test_two_authors_use_and(self):
        self.assertEqual(author_names({'author': [{'given': 'Ana', 'family': 'Uno'},
                                                {'given': 'Luis', 'family': 'Dos'}]})[1],
                         'A. Uno and L. Dos')

    def test_corporate_author_is_preserved(self):
        self.assertEqual(author_names({'author': [{'name': 'Instituto X'}]})[1], 'Instituto X')

    def test_deposit_date_is_not_publication_date(self):
        self.assertEqual(get_year({'created': {'date-parts': [[2025]]}}), '')

    def record(self, **extra):
        message = {'type': 'journal-article', 'title': ['Study'], 'container-title': ['Journal'],
                   'short-container-title': ['J. Test'], 'author': [{'given': 'Ana', 'family': 'Uno'}],
                   'issued': {'date-parts': [[2023]]}, 'volume': '2', 'issue': '1', 'page': '10-15'}
        message.update(extra)
        # Solo se sustituye el transporte externo; transformación y salida son reales.
        with patch('urllib.request.urlopen', return_value=io.BytesIO(json.dumps({'message': message}).encode())):
            return crossref('10.1234/example')

    def test_journal_punctuation_and_abbreviation(self):
        record = self.record()
        self.assertEqual(record.ieee, 'A. Uno, "Study," *J. Test*, vol. 2, no. 1, pp. 10–15, 2023, doi: 10.1234/example.')
        self.assertNotEqual(record.status, 'ok')

    def test_article_number_is_not_page_range(self):
        record = self.record(page='', **{'article-number': 'e123'})
        self.assertIn('Art. no. e123', record.ieee)
        self.assertNotIn('pp. e123', record.ieee)

    def test_book_is_not_formatted_as_journal(self):
        record = self.record(type='book')
        self.assertEqual(record.ieee, '')
        self.assertEqual(record.status, 'pendiente')

    def test_report_keeps_multiple_rows_in_one_markdown_table(self):
        from doi_a_referencia import render
        first, second = self.record(), self.record()
        second.doi = '10.1234/second'
        text = render([first, second], 'ieee')
        between = text.split('| 10.1234/example |', 1)[1].split('| 10.1234/second |', 1)[0]
        self.assertNotIn('\n- ', between)


if __name__ == '__main__':
    unittest.main()
