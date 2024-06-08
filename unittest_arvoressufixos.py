from arvoressufixos import SuffixTree
import unittest

class TestSuffixTree(unittest.TestCase):
    def setUp(self):
        # Initialize suffix tree with a test string
        self.suffix_tree = SuffixTree("banana")

    def test_construction(self):
        # Test construction of suffix tree
        # Verify the structure of the tree by checking nodes and edges
        root = self.suffix_tree.root
        self.assertEqual(root.start, -1)                # Root node should represent an empty string
        self.assertEqual(root.end, -1)                  # The end index of the root node should be -1
        self.assertEqual(len(root.children), 4)         # Root should have 4 children ('b', 'a', 'n', '$')

        # Check the children of the root node (checks if each element is a child of the root)
        self.assertIn('b', root.children)              
        self.assertIn('a', root.children)               
        self.assertIn('n', root.children)               
        self.assertIn('$', root.children)               

        # Check if the edges are set correctly (checks if each edge start at their correct indexes)
        self.assertEqual(root.children['b'].start, 0)
        self.assertEqual(root.children['a'].start, 1)
        self.assertEqual(root.children['n'].start, 2)
        self.assertEqual(root.children['$'].start, 6) 

    def test_search_substring(self):
        # Test substring search functionality
        input_str = "nan"
        expected_output = [2]
        actual_output = self.suffix_tree.substring_search(input_str)
        self.assertEqual(actual_output, expected_output, f"Substring search failed for input '{input_str}': Expected {expected_output}, but got {actual_output}")

    def test_pattern_matching(self):
        # Test pattern matching functionality
        input_pattern = "ana"
        expected_output = [1, 3]
        actual_output = self.suffix_tree.pattern_matching(input_pattern)
        self.assertEqual(actual_output, expected_output, f"Pattern matching failed for pattern '{input_pattern}': Expected {expected_output}, but got {actual_output}")

    def test_longest_common_substring(self):
        # Test longest common substring functionality
        string2 = "bandana"
        expected_output = "ban"
        actual_output = self.suffix_tree.longest_common_substring(string2)
        self.assertEqual(actual_output, expected_output, f"Longest common substring test failed: Expected {expected_output}, but got {actual_output}")

    def test_boundary_cases(self):
        # Test boundary cases
        # Verify the behavior of the suffix tree with edge cases
        # Test empty string
        empty_suffix_tree = SuffixTree("")
        expected_output = ""
        actual_output = empty_suffix_tree.longest_common_substring("")  # Pass empty string as the second argument
        self.assertEqual(actual_output, expected_output, f"Boundary case test failed for empty string: Expected {expected_output}, but got {actual_output}")

        # Test single character string
        single_char_suffix_tree = SuffixTree("a")
        expected_output = "a"
        actual_output = single_char_suffix_tree.longest_common_substring("a")  # Pass a string as the second argument
        self.assertEqual(actual_output, expected_output, f"Boundary case test failed for single character string: Expected {expected_output}, but got {actual_output}")

        # Test repeated character string
        repeated_char_suffix_tree = SuffixTree("aaaaa")
        expected_output = "aaaaa"
        actual_output = repeated_char_suffix_tree.longest_common_substring("aaaaa")  # Pass a string as the second argument
        self.assertEqual(actual_output, expected_output, f"Boundary case test failed for repeated character string: Expected {expected_output}, but got {actual_output}")


if __name__ == '__main__':
    unittest.main()


