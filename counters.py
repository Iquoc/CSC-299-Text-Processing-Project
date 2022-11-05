import abc
from abc import ABC
from typing import Dict, List
from collections import defaultdict, Counter
import json
import re


class TextCounter(ABC):
    @staticmethod
    @abc.abstractmethod
    def count_characters(text: str) -> Dict[str, int]:
        pass


class DictBasedTextCounter(TextCounter):
    @staticmethod
    def count_characters(text: str) -> Dict[str, int]:
        counts = dict()
        for char in text:
            if char in counts:
                counts[char] += 1
            else:
                counts[char] = 1
        return counts


class DefaultDictBasedTextCounter(TextCounter):
    @staticmethod
    def count_characters(text: str) -> Dict[str, int]:
        counts = defaultdict(int)
        for char in text:
            counts[char] += 1
        return counts


def tokenize(text: str) -> List[str]:
    initial = re.sub(r'(\W)', r' \1 ', text.lower())
    adjusted = re.sub(r'(\w) \' (\w)', r"\1'\2", initial)
    with_elipses = re.sub(r'\.\s+\.\s+\.', '...', adjusted)
    return with_elipses.split()


class CounterBasedTextCounter(TextCounter):
    @classmethod
    def count_characters(cls, text: str) -> Dict[str, int]:
        counts = Counter()
        counts.update(text)
        return counts

    def count_words(self, text: str) -> Dict[str, int]:
        counts = Counter()
        counts.update(tokenize(text))
        return counts


def get_small_wiki():
    with open(r'C:\Users\Alex\Documents\DePaul\lectures\wiki_small.json') as fp:
        return json.load(fp)


def count_total_words(texts_list: List[str]) -> Counter:
    counts = Counter()
    counter = CounterBasedTextCounter()
    for text in texts_list:
        counts.update(counter.count_words(text))
    return counts


# [d['init_text'] for d in data if d['init_text']]
def get_texts_from_data(data):
    output = []
    for d in data:
        if d['init_text']:
            text = d['init_text']
            output.append(text)
    return output
