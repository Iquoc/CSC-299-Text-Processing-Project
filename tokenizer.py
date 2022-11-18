import abc
import re
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

class GroupOneTokenizer(Tokenizer):

    def __init__(self):
        self.titles = {'dr', 'prof', 'mr', 'mrs', 'ms'}
        self.abbreviations = {'etc'}
        self.urls = {'http', 'https', 'www', 'd2l'}
        self.domain = {'com', 'net', 'org', 'edu'}
        self.list = []

    def tokenize(self, text: str) -> List[str]:
        adjusted = text
        common_titles = self.tokenize_common_titles(adjusted)
        remove_non_word = re.sub(r'(\W)', r' \1 ', common_titles)
        end_of_sentence = re.sub(r'(w)\.\s([A-Z])', r'\1 \. \2', remove_non_word)
        apostrophe = re.sub(r'(\w) \' (\w)', r"\1'\2", end_of_sentence)
        with_ellipses = re.sub(r'\.\s+\.\s+\.', '...', apostrophe)
        result = with_ellipses
        for title in self.titles:
            result = re.sub(rf'{title}', rf'{title}.', result)
        print(result)
        return result.split()

    def tokenize_common_titles(self, text: str) -> str:
        adjusted = text.lower()
        for title in self.titles:
            self.list += re.findall(rf'{title}\.', adjusted)
            # if re.search(fr'{title}\.', adjusted):
            #     print("match found")
            #     print(self.list)
            #     print(adjusted)
            adjusted = re.sub(rf'{title}\.', rf'{title}', adjusted)
            print(adjusted)
        return adjusted

    def tokenize_end_of_sentence(self, text: str) -> List[str]:
        adjusted = text
        adjusted = re.sub(r'(w)\.\s([A-Z])', r'\1 \. \2', adjusted)
        return adjusted.split()
       

    def stemm(self, tokenized: List[str]) -> List[str]:
        stem = PorterStemmer()
        stemmed = list()
        for word, i in tokenized:
            stemmed[i] = stem.stem(word)
        return stemmed

    def lemm(self, tokenized: List[str]) -> List[str]:
        lem = WordNetLemmatizer()
        lemmed = list()
        for word, i in tokenized:
            lemmed[i] = lem.lemmatize(word)
        return lemmed
