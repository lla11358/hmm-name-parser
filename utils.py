"""
Text utilities.

Functions to normalize and tokenize words.

"""

import unicodedata


def save_dict_to_file(dictionary, filename):
    f = open(filename, 'w')
    f.write(str(dictionary))
    f.close()


def load_dict_from_file(filename):
    f = open(filename, 'r')
    data = f.read()
    f.close()
    return eval(data)


def normalize(text, case=None):
    """
    Normalize text string.

    Normalize unicode data to remove accents, etc. and change capitalization.

    Parameters:
        text (str): text to be normalized.
        case (str): 'upper' | 'lower' | None

    Returns:
        normalized (str): normalized text.

    """
    normalized = unicodedata.normalize(
        'NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    if case == 'lower':
        normalized = normalized.lower()
    if case == 'upper':
        normalized = normalized.upper()
    return normalized


def to_token(word, length):
    """
    Obtain the token corresponding to a given word.

    Takes the last 'lenght' characters of each word.

    Parameters:
        word (str): word compliant with config.word_pattern regular expression.
            Ex.: 'eva', 'julio-jose', 'rodriguez', 'lopez']
        length (int): length of token. Ex.: 3
            If len(word) <= length then token = word

    Returns:
        token (str): token with the specified length.
            Ex.: 'eva', 'ose', 'uez', 'pez'

    """
    return word[-length:]
