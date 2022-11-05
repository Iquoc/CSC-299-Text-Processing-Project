import json
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple
from counters import tokenize, count_total_words, CounterBasedTextCounter


# 1
def compute_document_counts(texts: List[str]) -> Counter:
    counts = Counter()
    for text in texts:
        # unique_tokens = set(tokenize(text))
        # for token in unique_tokens:
        #     counts[token] += 1
        counts.update(set(tokenize(text)))
    return counts


# 2
def compute_stopwords(texts: List[str]) -> Set[str]:
    doc_counts = compute_document_counts(texts)
    total_counts = count_total_words(texts)
    stopwords = set()
    for w, _ in total_counts.most_common(20):
        if doc_counts[w] >= 9:
            stopwords.add(w)
    return stopwords


# 3
def get_best_terms_for_doc(text: str, stopwords: Set[str]) -> List[Tuple[str, int]]:
    word_counts = Counter(CounterBasedTextCounter().count_words(text))
    for w in stopwords:
        del word_counts[w]
    return word_counts.most_common(10)


def get_best_terms(texts: List[str], stopwords: Set[str]) -> List[List[Tuple[str, int]]]:
    return [get_best_terms_for_doc(text, stopwords) for text in texts]


# 4
def create_inverted_index(texts: List[str]) -> Dict[str, Set[int]]:
    output_dict = dict()
    # for i, text in enumerate(texts):
    for i in range(len(texts)):
        text = texts[i]
        for w in tokenize(text):
            if w in output_dict:
                output_dict[w].add(i)
            else:
                output_dict[w] = {i}
    return output_dict


# 5
def search_2_words(w1: str, w2: str, index: Dict[str, Set[int]]) -> Set[int]:
    return index[w1] & index[w2]


class JsonEncoderWithIterablesDefault(json.JSONEncoder):
    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o)
