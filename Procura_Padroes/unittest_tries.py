import unittest
from unittest.mock import patch
from tries import Tries

class TestTriesMethods(unittest.TestCase):

    def setUp(self):
        self.tries = Tries()

    def test_insert(self):
        self.tries.insert('apple')
        self.assertTrue(self.tries.search('apple'))

    def test_insert_fromList(self):
        word_list = ['apple', 'banana', 'orange']
        self.tries.insert_fromList(word_list)
        for word in word_list:
            self.assertTrue(self.tries.search(word))

    def test_insert_fromInput(self):
        input_values = ['3', 'apple', 'orange', 'banana']
        
        with patch('builtins.input', side_effect=input_values):
            self.tries.insert_fromInput()
            
        self.assertTrue(self.tries.search('apple'))
        self.assertTrue(self.tries.search('orange'))
        self.assertTrue(self.tries.search('banana'))

    def test_delete(self):
        self.tries.insert('apple')
        self.tries.delete('apple')
        self.assertFalse(self.tries.search('apple'))

    def test_delete_fromList(self):
        word_list = ['apple', 'banana', 'orange']
        self.tries.insert_fromList(word_list)
        self.tries.delete_fromList(['apple', 'banana'])
        self.assertFalse(self.tries.search('apple'))
        self.assertFalse(self.tries.search('banana'))
        self.assertTrue(self.tries.search('orange'))

    def test_search(self):
        self.tries.insert('apple')
        self.assertTrue(self.tries.search('apple'))
        self.assertFalse(self.tries.search('banana'))

    def test_search_fromList(self):
        words_to_insert = ['apple', 'pineapple', 'clementine', 'watermelon']
        self.tries.insert_fromList(words_to_insert)
        words_to_search = ['apple', 'banana', 'orange', 'pineapple', 'strawberry', 'clementine']
        search_result = self.tries.search_fromList(words_to_search)

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
        self.tries.insert_fromList(words_to_insert)

        input_values = ['apple', 'banana', 'orange', 'pineapple', 'strawberry', 'clementine', '']
        input_iter = iter(input_values)

        def mock_input(prompt):
            return next(input_iter)

        with patch('builtins.input', side_effect=mock_input):
            found_words, not_found_words = self.tries.search_fromInput()

        self.assertEqual(found_words, ['apple', 'pineapple', 'clementine'])
        self.assertEqual(not_found_words, ['banana', 'orange', 'strawberry'])

    def test_startsWith(self):
        self.tries.insert('apple')
        self.tries.insert('banana')
        self.assertTrue(self.tries.startsWith('app'))
        self.assertFalse(self.tries.startsWith('orn'))

    def test_getAllWords(self):
        word_list = ['apple', 'banana', 'orange']
        self.tries.insert_fromList(word_list)
        retrieved_words = self.tries.getAllWords()
        for word in word_list:
            self.assertIn(word, retrieved_words)

if __name__ == '__main__':
    unittest.main()