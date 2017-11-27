import unittest
from ex5 import *


class MyTestCase(unittest.TestCase):
    def test_MatrixWithOneRow_IfStringIsFoundOnce(self):
        self.assertEqual(get_word_to_count(['apple'], ['apple']), {'apple': 1})

    def test_MatrixWithOneRow_IfSubstringIsFoundOnce(self):
        self.assertEqual(get_word_to_count(['apple'], ['app']), {'app': 1})

    def test_MatrixWithTwoRows_IfSubstringIsFoundOnce(self):
        self.assertEqual(get_word_to_count(['apple', 'bagel'], ['gel']), {'gel': 1})

    def test_MatrixWithTwoRows_IfFoundTwice(self):
        self.assertEqual(get_word_to_count(['apple', 'table'], ['le']), {'le': 2})

    def test_LiveTest(self):
        self.assertEqual(get_word_to_count(['apple',
                                            'agodo',
                                            'nnert',
                                            'gatac',
                                            'micsr',
                                            'popop'], ['apple', 'pop']),
                         {'apple': 1, 'pop': 2})


if __name__ == '__main__':
    unittest.main()
