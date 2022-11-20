# Will take a string
from typing import List
import re

text = "Hello, my name is David. I like to have fun. Okay bye!"
text2 = "The decimal 0.61 stands for 61 hundredths. The recurring decimal 3.999... is also described as 3.9 recurring."


def sentence_boundary(tokens: str) -> List[str]:    # David A.
    """
    :param tokens: a string of tokens
    :return: returns a list of tokens that have been split by new sentence
    """
    # token = re.findall(r".*?\.(?=\ [A-Z]|$)", tokens)
    token = re.split(r'(?<=[?.!])\s+', tokens)
    # token = re.split(r'(?<=[?.!])\s+', tokens)
    # token = re.split(r'/(?<=[.?!]\s)(?=[A-Z])/', tokens)
    return token


print(sentence_boundary(text))
