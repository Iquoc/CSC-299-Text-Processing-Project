from unittest import TestCase

from tokenizer import NaiveTokenizer


class TokenizerTest(TestCase):
    def __init__(self):
        super().__init__()
        self.tokenizer = NaiveTokenizer()

    def test_tokenize__splits_words(self):
        self.assertEqual(self.tokenizer.tokenize('word1 word2'), ['word1', 'word2'])

    def test_tokenize__comma(self):
        self.assertEqual(self.tokenizer.tokenize('For now, we are here'), ['for', 'now', ',', 'we', 'are', 'here'])

    def test_tokenize__period(self):
        self.assertEqual(self.tokenizer.tokenize('For now, we are here.'), ['for', 'now', ',', 'we', 'are', 'here', '.'])

    def test_tokenize__other_non_word_chars(self):
        self.assertEqual(self.tokenizer.tokenize('10% of $5 is 50 c'), ['10', '%', 'of', '$', '5', 'is', '50', 'c'])

    def test_tokenize__apostrophe(self):
        self.assertEqual(self.tokenizer.tokenize('He said \'Isn\'t O\'Brian the best?\''),
                         ['he', 'said', '\'', 'isn\'t', 'o\'brian', 'the', 'best', '?', '\''])

    def test_tokenize__ellipsis(self):
        self.assertEqual(self.tokenizer.tokenize('More...'), ['more', '...'])
