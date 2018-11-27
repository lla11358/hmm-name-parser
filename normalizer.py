"""
Text normalizer.

Common text normalization functions.

"""

import unicodedata


def unicode(str):
    """Normalize unicode data to remove umlauts, accents etc."""
    return unicodedata.normalize(
        'NFKD', str).encode('ASCII', 'ignore').decode('utf-8')
