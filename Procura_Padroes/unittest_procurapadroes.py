import unittest
import procurapadroes as ps

class PatternSearchTests:
    def test_single_match(self):
        seq = "ATAGCAGTACGTACGATACG"
        pattern = "TACGT"
        expected = [7]
        self.assertEqual(self.func(seq, pattern), expected)

    def test_multiple_matches(self):
        seq = "ATAGCAGTACGTACGATACG"
        pattern = "ACG"
        expected = [8, 12, 17]
        self.assertEqual(self.func(seq, pattern), expected)

    def test_no_match(self):
        seq = "ATAGCAGTACGTACGATACG"
        pattern = "GCT"
        expected = []
        self.assertEqual(self.func(seq, pattern), expected)

    def test_empty_sequence(self):
        seq = ""
        pattern = "ACGT"
        expected = []
        self.assertEqual(self.func(seq, pattern), expected)

    def test_empty_pattern(self):
        seq = "ATAGCAGTACGTACGATACG"
        pattern = ""
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.assertEqual(self.func(seq, pattern), expected)

    def test_lowercase_match(self):
        seq = "acgtacgtACGT"
        pattern = "acgt"
        expected = [0, 4]
        self.assertEqual(self.func(seq, pattern), expected)
        
    def test_uppercase_match(self):
        seq = "acgtacgtACGT"
        pattern = "ACGT"
        expected = [8]
        self.assertEqual(self.func(seq, pattern), expected)

class TestNaive(PatternSearchTests, unittest.TestCase):
    def setUp(self):
        self.func = ps.naive

class TestKMP(PatternSearchTests, unittest.TestCase):
    def setUp(self):
        self.func = ps.KMP

    # KMP is supposed to return an empty list in this test, this overrides the common test during KMP testing
    def test_empty_pattern(self):
        seq = "ATAGCAGTACGTACGATACG"
        pattern = ""
        expected = []
        self.assertEqual(self.func(seq, pattern), expected)

class TestRabinKarp(PatternSearchTests, unittest.TestCase):
    def setUp(self):
        self.func = ps.rabin_karp

class TestBoyerMoore(PatternSearchTests, unittest.TestCase):
    def setUp(self):
        self.func = ps.boyer_moore

if __name__ == '__main__':
    unittest.main()