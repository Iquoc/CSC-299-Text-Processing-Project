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


class StemAndLem(Tokenizer):
    def tokenize(self, text: str) -> List[str]:
        initial = re.sub(r'(\W)', r' \1 ', text.lower())
        adjusted = re.sub(r'(\w) \' (\w)', r"\1'\2", initial)
        with_ellipses = re.sub(r'\.\s+\.\s+\.', '...', adjusted)
        return with_ellipses.split()

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
