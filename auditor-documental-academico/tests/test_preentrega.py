import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from check_preentrega import run

class PreentregaTests(unittest.TestCase):
    def test_locator_is_detected(self):
        result={item['check']:item for item in run('Texto [1, p. 27].')}
        self.assertTrue(result['citas']['ok'])
        self.assertEqual(result['referencias']['severity'],'alta')

    def test_bibliography_alone_is_not_a_citation(self):
        result={item['check']:item for item in run('Sin citas.\n# Referencias\n[1] Obra.')}
        self.assertFalse(result['citas']['ok'])
