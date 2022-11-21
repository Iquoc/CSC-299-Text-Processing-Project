import abc
import re
import nltk
from abc import ABC
from typing import List
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


class Tokenizer(ABC):
    """
    Tokenizer interface.

    Implemented as a part of HW2 exercise 3.
    """

    @abc.abstractmethod
    def tokenize(self, text: str) -> List[str]:
        pass


class NaiveTokenizer(Tokenizer):
    """
    Tokenizer implementation from HW1.
    """

    def tokenize(self, text: str) -> List[str]:
        initial = re.sub(r'(\W)', r' \1 ', text.lower())
        adjusted = re.sub(r'(\w) \' (\w)', r"\1'\2", initial)
        with_ellipses = re.sub(r'\.\s+\.\s+\.', '...', adjusted)
        return with_ellipses.split()


class GroupOneTokenizer(Tokenizer):     # Iquoc T.

    def __init__(self):
        # self.titles = {'dr', 'prof', 'mr', 'mrs', 'ms'}
        self.titles = {'Dr', 'Prof', 'Mr', 'Mrs', 'Ms'}
        self.abbreviations = {'etc', 'm'}
        self.urls = {'http', 'https', 'www', 'd2l'}
        self.domain = {'com', 'net', 'org', 'edu'}
        self.list = []

    # "abbr. word1 . Word2
    # (). 123,456
    # (). Word1
    # Quotations, mis-capitalized words?, pre-school?,...

    def tokenize(self, text: str) -> List[str]:
        adjusted = text     # default variable to be modified, for organization
        common_titles = self.tokenize_common_titles(adjusted)       # removes . whenever preceded by title
        remove_non_word = self.tokenize_non_word(common_titles)         # takes any non character and adds whitespace before and after
        end_of_sentence = self.sentence_boundary(remove_non_word)       # adds whitespace before and after . whenever proceeded by a word that is CAPITALIZED
        for title in self.titles:   # iterates through a list of titles
            end_of_sentence = re.sub(rf'{title}', rf'{title}.', end_of_sentence)        # adds back the . to the titles without interruption from sentence boundary
        apostrophe = re.sub(r'(\w) \' (\w)', r"\1'\2", end_of_sentence)     # adds whitespace before and after '
        print("apostrophe: " + apostrophe)
        with_ellipses = re.sub(r'\.(\s+)?\.(\s+?)\.', ' ... ', apostrophe)      # re-combines consecutive (.)
        lower_case = with_ellipses.lower()      # takes all the characters and makes them lowercase
        result = lower_case
        print(result)
        return result.split()

    def tokenize_non_word(self, text: str) -> str:
        adjusted = text
        adjusted = re.sub(r'(\W)', r' \1 ', adjusted)
        adjusted = re.sub(r'(\s)([\.\-])(\s)', r'\2', adjusted)
        print("non word: " + adjusted)
        return adjusted

    def tokenize_correct_errors(self):      # possibly for correcting spelling errors and the sort...
        pass

    def tokenize_common_titles(self, text: str) -> str:     # Iquoc T.
        adjusted = text
        for title in self.titles:
            self.list += re.findall(rf'{title}\.', adjusted)
            # if re.search(fr'{title}\.', adjusted):
            #     print("match found")
            #     print(self.list)
            #     print(adjusted)
            adjusted = re.sub(rf'{title}\.', rf'{title}', adjusted)
            # print("common titles: " + adjusted)
        return adjusted

    def tokenize_lower_case(self, text: str) -> str:        # dead function
        adjusted = text
        adjusted = re.sub(r'([A-Z])\1', self.toLowercase, adjusted)
        print(adjusted)
        return adjusted

    def toLowercase(self, match):       # dead function
        return match.group(1).lower()

    def sentence_boundary(self, text: str) -> str:    # David A.
        adjusted = text
        # Split sentences
        #       Look for a period, space, and capital letter
        #       Split after
        # adjusted = re.split(r'(?<=\.)\s+(?=[A-Z"\'])', adjusted)    # This keeps the period and whitespace
        adjusted = re.sub(r'([.?!])\s+([A-Z?]\w+)', r' \1 \2', adjusted)
        adjusted = re.sub(r'(\.)$', r' \1 ', adjusted)
        # ^^^ Does not split, adds space before and after period
        # adjusted = re.split(r'\.\s+(?=[A-Z"\'])', adjusted) -- This removes the period and whitespace
        return adjusted

    # def tokenize_other(self, nom: List[str]):   # Azaan A.
    #     for n in nom:
    #         if n == '.':
    #             n == ','
    #         return n.join()

    def url_tokenize(self, text: str) -> List[str]:   # Nicholas Y.
        url_tokenized = re.sub(r'(https:\/\/www\.|http:\/\/www\.|www\.)[a-zA-Z0-9\-_$]+\.[a-zA-Z]{2,5}$', r'', text)
        return url_tokenized.split()

    def stemm(self, tokenized: List[str]) -> List[str]:
        stem = PorterStemmer()
        stemmed = []
        for word in tokenized:
            stemmed.append(stem.stem(word))
        return stemmed

    def lemm(self, tokenized: List[str]) -> List[str]:
        lem = WordNetLemmatizer()
        lemmed = []
        for word in tokenized:
            lemmed.append(lem.lemmatize(word.lower()))
        print(lemmed)
        return lemmed
