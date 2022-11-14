from unittest import TestCase
import tokenizer
from tokenizer import GroupOneTokenizer


class GroupOneTokenizerTest(TestCase):

    def test_regex(self):
        test = GroupOneTokenizer.tokenize(GroupOneTokenizer(), 'He said \'Isn\'t O\'Brian the best?\'')
        self.assertEqual(['he', 'said', '\'', 'isn\'t', 'o\'brian', 'the', 'best', '?', '\''], test)

    def test_common_titles(self):
        test = GroupOneTokenizer.tokenize(GroupOneTokenizer(), 'Dr. Ross\'s dog jumped over the fence. Dr. Ross was amazed!')
        # print(test)
        self.assertEqual(['dr.', 'ross\'s', 'dog', 'jumped', 'over', 'the', 'fence', '.', 'dr.', 'ross', 'was', 'amazed', '!'], test)

        # class GroupOneTokenizerTest(TestCase):
        #
        #     def __init__(self):
        #         super().__init__()
        #         self.tokenizer = tokenizer.GroupOneTokenizer()
        #
        #     def test_tokenize_common_titles(self):
        #         self.assertEqual(self.tokenizer.tokenize('Dr. Ross'), ['Dr.', 'Ross'])
        #         # test = self.tokenizer.tokenize("Is Dr. Ross in today?")
        #         # print(test)
