import unittest
from highlighter import Highlighter


class HighlighterTest(unittest.TestCase):


    def setUp(self):
        doc = "This is my review on Panchos Mexican Restaurant. This is only a "
        doc = doc + "test of the emergency broadcasting system. The best "
        doc = doc + "tacos I've ever had were from Panchos. This sentence is "
        doc = doc + "about nothing. Great tacos, burritos, and enchaladas. "
        doc = doc + "Bean burritos are also good. Lots more filler text here. "
        doc = doc + "The filler text in this sentence is muy bueno. Remember to "
        doc = doc + "eat lots of tacos."
        self.doc = doc
        self.query = "tacos burritos enchaladas"
        self.hi = Highlighter(self.doc, self.query)


    def test_tokenize_query_terms(self):
        tokens_result = self.hi.tokenize_query_terms()
        expected_result = ["tacos", "burritos", "enchaladas"]
        #print(tokens_result)
        self.assertEqual(expected_result, tokens_result, tokens_result)


    def test_query_term_density(self):
        query_terms = self.hi.tokenize_query_terms()
        query_term_partial_density = self.hi.query_term_partial_density()
        total_query_term_density = self.hi.query_term_density(query_term_partial_density)
        expected_result = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0.2, 0.2, 0.2, 0.2, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.2,
            0, 0, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0, 0, 0, 0, 0, 0, 0.1, 0.1,
            0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0, 0, 0, 0, 0, 0, 0, 0.125, 0.125, 0.125, 0.125,
            0.125, 0.125, 0.125, 0.125, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.2, 0
            ]
        #print(total_query_term_density)
        self.assertEqual(total_query_term_density, expected_result, total_query_term_density)


    def test_max_term_density_window(self):
        query_terms = self.hi.tokenize_query_terms()
        query_term_partial_density = self.hi.query_term_partial_density()
        total_query_term_density = self.hi.query_term_density(query_term_partial_density)
        result_window = self.hi.max_term_density_window(total_query_term_density)
        self.assertTrue(0 <= result_window[0] < result_window[1], "Failed basic windowing.")
        self.assertTrue(self.hi.maximum_snippit_length >= result_window[1] - result_window[0], "Window width too large.")


    def test_highlight_document(self):
        highlighted_result = self.hi.highlight_document()
        #print(highlighted_result)
        self.assertTrue(highlighted_result, highlighted_result)


    def test_highlight_doc(self):
        highlighted_result = Highlighter.highlight_doc(self.doc, self.query)
        msg = "\nhighlighted_result =\n" + highlighted_result
        expected_result = " [[HIGHLIGHT]]tacos[[HIGHLIGHT]] I've ever had were from Panchos. "
        expected_result = expected_result + "This sentence is about nothing. Great [[HIGHLIGHT]]"
        expected_result = expected_result + "tacos burritos[[HIGHLIGHT]], and [[HIGHLIGHT]]"
        expected_result = expected_result + "enchaladas[[HIGHLIGHT]]. Bean [[HIGHLIGHT]]burritos[[HIGHLIGHT]]"
        msg = msg + "\nexpected_result = \n" + expected_result
        self.assertEquals(expected_result, highlighted_result, msg)

