from unittest import TestCase
import tokenizer
from tokenizer import GroupOneTokenizer


class GroupOneTokenizerTest(TestCase):

    def setUp(self) -> None:
        self.tokenizer = GroupOneTokenizer()

    def test_tokenize__splits_words(self):
        self.assertEqual(['word1', 'word2'],
                         self.tokenizer.tokenize('word1 word2'))

    def test_tokenize__comma(self):
        self.assertEqual(['for', 'now', ',', 'we', 'are', 'here'],
                         self.tokenizer.tokenize('For now, we are here'))

    def test_tokenize__period(self):
        self.assertEqual(['for', 'now', ',', 'we', 'are', 'here', '.'],
                         self.tokenizer.tokenize('For now, we are here.'))

    def test_tokenize__other_non_word_chars(self):
        self.assertEqual(['10', '%', 'of', '$', '5', 'is', '50', 'c'],
                         self.tokenizer.tokenize('10% of $5 is 50 c'))

    def test_tokenize__apostrophe(self):
        self.assertEqual(['he', 'said', '\'', 'isn\'t', 'o\'brian', 'the', 'best', '?', '\''],
                         self.tokenizer.tokenize('He said \'Isn\'t O\'Brian the best?\''))

    def test_tokenize__ellipsis(self):
        self.assertEqual(['more', '...'], self.tokenizer.tokenize('More...'))

    def test_tokenize__common_titles(self):     # Iquoc T.
        self.assertEqual(['dr.', 'ross\'s', 'dog', 'jumped', 'over', 'the', 'fence', '.', 'dr.', 'ross', 'was', 'amazed', '!'],
                         self.tokenizer.tokenize('Dr. Ross\'s dog jumped over the fence. Dr. Ross was amazed!'))

    def test_tokenize__main(self):      # Imran A.
        self.assertEqual(["patients", "with", "positive", "m.", "pneumoniae", "cultures", "from", "respiratory",
                          "specimens", "from", "january", "1997", "through", "december", "1998"],
                         self.tokenizer.tokenize('Patients with positive M. pneumoniae cultures from respiratory specimens from January 1997 through December 1998'))

    def test_tokenize__parenthesis(self):       # Imran A.
        self.assertEqual(["pre-school", "children", "(", "22.5", "%", ")", ".", "it", "occurred", "year-round"],
                         self.tokenizer.tokenize("pre-school children (22.5%). It occurred year-round"))

    def test_tokenize_URL1(self):       # David A.
        c = self.tokenizer.url_tokenize('https://www.cnn.com/specials/mobile-apps hello hello')
        print(c)
        self.assertEqual(['https://www.cnn.com/specials/mobile-apps', 'hello', 'hello'], c)

    def test_tokenize_URL2(self):
        c = self.tokenizer.url_tokenize('my classes are: https://d2l.depaul.edu/d2l/home hello.com hello.')
        print(c)
        self.assertEqual(['my', 'classes', 'are:', 'https://d2l.depaul.edu/d2l/home', 'hello.com', 'hello.'], c)

    def test_tokenize_URL3(self):
        c = self.tokenizer.url_tokenize('http://info.cern.ch/ hello hello')
        print(c)
        self.assertEqual(['http://info.cern.ch/', 'hello', 'hello'], c)

    def test_tokenize_URL4(self):
        c = self.tokenizer.url_tokenize('videos here at www.youtube.com/ hello hello')
        print(c)
        self.assertEqual(['videos', 'here', 'at', 'www.youtube.com/', 'hello', 'hello'], c)

    # def test_tokenize__stemming(self):      # Carlos Q.
    #     tokens = ['Males', 'Modes', 'Playing', 'Cats', 'Several']
    #     self.assertEqual(self.tokenizer.stemm(tokens), ['male', 'mode', 'play', 'cat', 'sever'])
    #
    # def test_tokenize__lemmatization(self):     # Carlos Q.
    #     tokens = ['cities', 'Mice', 'Playing', 'Languages', 'Cities']
    #     self.assertEqual(self.tokenizer.lemm(tokens), ['city', 'mouse', 'play', 'language', 'city'])
