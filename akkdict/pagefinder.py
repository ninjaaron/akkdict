#!/usr/bin/env python3

import sys
import pkg_resources
import unicodedata as ud

DICT_NAMES = 'cad', 'ahw', 'cda'
INDICIES = {}
RM = pkg_resources.ResourceManager()
for dict_ in DICT_NAMES:
    with RM.resource_stream('akkdict', 'indicies/' +dict_ + '.csv') as f:
        INDICIES[dict_] = [l.decode().rstrip().split(',') for l in f]

del dict_
CHARS = {c: i for i, c in enumerate('abdeghijklmnpqrsṣštṭuwyz')}
_sortkey = lambda word: [CHARS[c] for c in word[0]]


def fix_query(query: str) -> str:
    """removes diacritic irrelevant for alphabetization"""
    for c, r in map(tuple, ('yj', 'Sṣ', '$š', 'Tṭ')):
        query = query.replace(c, r)
    query = query.replace(' ', '').lower()

    fixed = ''
    for c in ud.normalize('NFC', query):
        if c not in CHARS:
            c = ud.normalize('NFD', c)[0]

        if c in CHARS:
            fixed += c
        else:
            raise ValueError \
                    ("'%s' is not an Akkadian transliteration character." % c)
    return fixed


def lookup(dictionary: str, query: str) -> str:
    """get near the page number of the query in given Akkadian dictionary"""
    query = fix_query(query)
    if  dictionary == 'cda':
        query = query.replace('j', 'y')
    index = INDICIES[dictionary].copy()
    index.append([query])
    index = sorted(index, key=_sortkey)
    guide_word = index[index.index([query]) - 1]
    return guide_word[1]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Akkadian headword")
    parser.add_argument("-d", help="Dictionary: {CDA,AWh,CAD}")
    args=parser.parse_args()
    if args.d:
        print(lookup(args.d.lower(), query))
    else:
        for dict_ in DICT_NAMES:
            print(dict_.upper() + ':', lookup(dict_ , query))
