import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from normalizar_referencias import process

class DuplicateTests(unittest.TestCase):
    def test_same_doi_with_different_labels_is_duplicate(self):
        refs=process('[1] Uno, Obra, doi: 10.1234/ABC.\n[2] Otro formato. https://doi.org/10.1234/abc')
        self.assertEqual([r.duplicate for r in refs],[False,True])

    def test_same_text_without_doi_ignores_label(self):
        refs=process('[1] A. Autor, Obra, 2023.\n[2] A. Autor, Obra, 2023.')
        self.assertEqual([r.duplicate for r in refs],[False,True])
