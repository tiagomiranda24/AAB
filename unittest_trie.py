import unittest
from unittest.mock import patch
from trie import Trie

class TestTrieMethods(unittest.TestCase):

    def setUp(self):
        self.trie = Trie()

    def test_insert(self):
        self.trie.insert('apple')
        self.assertTrue(self.trie.search('apple'))

    def test_insert_fromList(self):
        word_list = ['apple', 'banana', 'orange']
        self.trie.insert_fromList(word_list)
        for word in word_list:
            self.assertTrue(self.trie.search(word))

    def test_insert_fromInput(self):
        input_values = ['3', 'apple', 'orange', 'banana']
        
        with patch('builtins.input', side_effect=input_values):
            self.trie.insert_fromInput()
            
        self.assertTrue(self.trie.search('apple'))
        self.assertTrue(self.trie.search('orange'))
        self.assertTrue(self.trie.search('banana'))

    def test_delete(self):
        self.trie.insert('apple')
        self.trie.delete('apple')
        self.assertFalse(self.trie.search('apple'))

    def test_delete_fromList(self):
        word_list = ['apple', 'banana', 'orange']
        self.trie.insert_fromList(word_list)
        self.trie.delete_fromList(['apple', 'banana'])
        self.assertFalse(self.trie.search('apple'))
        self.assertFalse(self.trie.search('banana'))
        self.assertTrue(self.trie.search('orange'))

    def test_search(self):
        self.trie.insert('apple')
        self.assertTrue(self.trie.search('apple'))
        self.assertFalse(self.trie.search('banana'))

    def test_search_fromList(self):
        words_to_insert = ['apple', 'pineapple', 'clementine', 'watermelon']
        self.trie.insert_fromList(words_to_insert)
        words_to_search = ['apple', 'banana', 'orange', 'pineapple', 'strawberry', 'clementine']
        search_result = self.trie.search_fromList(words_to_search)

        expected_result = {
            'apple': True,
            'banana': False,
            'orange': False,
            'pineapple': True,
            'strawberry': False,
            'clementine': True
        }
        self.assertEqual(search_result, expected_result)

    def test_search_fromInput(self):
        words_to_insert = ['apple', 'pineapple', 'clementine', 'watermelon']
        self.trie.insert_fromList(words_to_insert)

        input_values = ['apple', 'banana', 'orange', 'pineapple', 'strawberry', 'clementine', '']
        input_iter = iter(input_values)

        def mock_input(prompt):
            return next(input_iter)

        with patch('builtins.input', side_effect=mock_input):
            found_words, not_found_words = self.trie.search_fromInput()

        self.assertEqual(found_words, ['apple', 'pineapple', 'clementine'])
        self.assertEqual(not_found_words, ['banana', 'orange', 'strawberry'])

    def test_startsWith(self):
        self.trie.insert('apple')
        self.trie.insert('banana')
        self.assertTrue(self.trie.startsWith('app'))
        self.assertFalse(self.trie.startsWith('orn'))

    def test_getAllWords(self):
        word_list = ['apple', 'banana', 'orange']
        self.trie.insert_fromList(word_list)
        retrieved_words = self.trie.getAllWords()
        for word in word_list:
            self.assertIn(word, retrieved_words)

if __name__ == '__main__':
    unittest.main()
