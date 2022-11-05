import abc
import re
from abc import ABC
from typing import List


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
