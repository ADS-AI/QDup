import re


def remove_punctuation(string):
    """
    Removes punctuation from a string.
    """
    string = re.sub(r"[^\w\s]", "", string)
    return string
