import unittest
from automatosfinitos import FiniteAutomata, NFA

class TestFiniteAutomata(unittest.TestCase):
    def setUp(self):
        self.fa = FiniteAutomata()
        self.fa.compute_transition_func("abc")

    def test_search_single_pattern(self):
        txt = "abcdeabc"
        patterns = ["abc"]
        expected = {"abc": [0, 5]}
        self.assertEqual(self.fa.search(patterns, txt), expected)

    def test_search_multiple_patterns(self):
        txt = "abcdeabcefghijkabclmnop"
        patterns = ["abc", "lmnop"]
        expected = {"abc": [0, 5, 15], "lmnop": [18]}
        self.assertEqual(self.fa.search(patterns, txt), expected)

    def test_search_empty_text(self):
        txt = ""
        patterns = ["abc"]
        with self.assertRaises(ValueError):
            self.fa.search(patterns, txt)

    def test_search_empty_patterns(self):
        txt = "abcdeabc"
        patterns = []
        with self.assertRaises(ValueError):
            self.fa.search(patterns, txt)

    def test_search_preprocessing(self):
        # search() function but when manually defining parameter 'preprocessing' as True (preprocessing=True)
        txt = "aBcDeAbC"
        patterns = ["aBc"]
        expected = {"abc": [0, 5]}
        self.assertEqual(self.fa.search(patterns, txt, preprocessing=True), expected)

    def test_search_no_preprocessing(self):
        # search() function but when manually defining parameter 'preprocessing' as False (preprocessing=False)
        txt = "aBcDeAbC"
        patterns = ["aBc"]
        expected = {"aBc": [0]}
        self.assertEqual(self.fa.search(patterns, txt, preprocessing=False), expected)

    def test_search_case_insensitivity(self):
        # search() function but when parameter 'preprocessing' is NOT manually defined and left in its default setting (preprocessing=True)
        txt = "aBcDeAbC"
        patterns = ["aBc"]
        expected = {"abc": [0, 5]}
        self.assertEqual(self.fa.search(patterns, txt), expected)

    def test_epsilon_closure(self):
        nfa = NFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transition={
                "q0": {"": {"q1"}},
                "q1": {"a": {"q2"}},
                "q2": {"b": {"q0"}}
            },
            initial_state="q0",
            accepting_states={"q2"}
        )
        self.assertEqual(nfa.epsilon_closure({"q0"}), {"q0", "q1"})

    def test_reset(self):
        self.fa.reset()
        self.assertEqual(self.fa.TF, [])
        self.assertEqual(self.fa.Q, set())
        self.assertEqual(self.fa.sigma, set())
        self.assertEqual(self.fa.q_0, 0)
        self.assertEqual(self.fa.F, set())
        self.assertEqual(self.fa.delta, {})

    def test_preprocess_text(self):
        txt = "aBcDeAbC"
        expected = "abcdeabc"  # After lowercasing
        self.assertEqual(self.fa.preprocess_text(txt), expected)

if __name__ == '__main__':
    unittest.main()