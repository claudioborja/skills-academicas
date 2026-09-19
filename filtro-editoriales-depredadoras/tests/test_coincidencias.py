import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from check_editorial_risk import match_score

class MatchTests(unittest.TestCase):
    def test_generic_journal_words_do_not_match(self):
        self.assertIsNone(match_score('International Journal of Medicine','International Journal of Chemistry'))

    def test_short_generic_query_does_not_match(self):
        self.assertIsNone(match_score('Journal','International Journal of Medicine'))

    def test_exact_and_distinctive_containment_still_match(self):
        self.assertEqual(match_score('Editorial Álamo','Editorial Alamo'),'exact')
        self.assertEqual(match_score('Editorial Alamo','Editorial Alamo Publishing'),'partial')
