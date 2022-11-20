from unittest import TestCase

import tokenizer
from tokenizer import NaiveTokenizer, GroupOneTokenizer


class TokenizerTest(TestCase):

    def __init__(self):
        super().__init__()
        self.tokenizer = NaiveTokenizer()

    def test_tokenize__splits_words(self):
        self.assertEqual(self.tokenizer.tokenize('word1 word2'), ['word1', 'word2'])

    def test_tokenize__comma(self):
        self.assertEqual(self.tokenizer.tokenize('For now, we are here'), ['for', 'now', ',', 'we', 'are', 'here'])

    def test_tokenize__period(self):
        self.assertEqual(self.tokenizer.tokenize('For now, we are here.'),
                         ['for', 'now', ',', 'we', 'are', 'here', '.'])

    def test_tokenize__other_non_word_chars(self):
        self.assertEqual(self.tokenizer.tokenize('10% of $5 is 50 c'), ['10', '%', 'of', '$', '5', 'is', '50', 'c'])

    def test_tokenize__apostrophe(self):
        self.assertEqual(self.tokenizer.tokenize('He said \'Isn\'t O\'Brian the best?\''),
                         ['he', 'said', '\'', 'isn\'t', 'o\'brian', 'the', 'best', '?', '\''])

    def test_tokenize__ellipsis(self):
        self.assertEqual(self.tokenizer.tokenize('More...'), ['more', '...'])
    
    def test_tokenize__main(self):
        self.assertEqual(self.tokenizer.tokenize('Patients with positive M. pneumoniae cultures from respiratory specimens from January 1997 through December 1998',
                        ["patients", "with", "positive", "m.", "pneumoniae", "cultures", "from", "respiratory", "specimens", "from", "january", "1997", "through", "december", "1998"]))
    def test_tokenize__pun(self):
        self.assertEqual(self.tokenizer.tokenize("pre-school children (22.5%). It occurred year-round",
                        ["pre-school", "children", "(", "22.5", "%", ")", ".", "it", "occurred", "year-round"]))
        
    def test_tokenize__stemming(self):
        tokens = ['Males', 'Modes', 'Playing', 'Cats', 'Several']
        self.assertEqual(self.tokenizer.stemm(tokens), ['male', 'mode', 'play', 'cat', 'sever'])

    def test_tokenize__lemmatization(self):
        tokens = ['cities', 'Mice', 'Playing', 'Languages', 'Cities']
        self.assertEqual(self.tokenizer.lemm(tokens), ['city', 'mouse', 'play', 'language', 'city'])
