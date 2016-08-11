#!/usr/bin/env python3

import sys
import os
import pkg_resources
from unicodedata import normalize as un

DICT_NAMES = 'ahw', 'cda'
INDICIES = {}
RM = pkg_resources.ResourceManager()
for dict_ in DICT_NAMES:
    with RM.resource_stream('akkdict', 'indicies/' +dict_ + '.csv') as f:
        INDICIES[dict_] = [l.decode().rstrip().split(',') for l in f]

with os.environ['HOME']+'/.cache/akkdict/cat.csv' as f:
    INDICIES['cad'] = [l.decode().rstrip().split(',') for l in f]

del dict_
CHARS = {c: i for i, c in enumerate('abdeghijklmnpqrsṣštṭuwyz')}


def _sortkey(word):
    return [CHARS[c] for c in word[0].lower()]


def fix_query(query: str) -> str:
    """removes diacritic irrelevant for alphabetization"""
    fixed = ''
    for c in un('NFC', query.lower().replace('y', 'j').replace('ʾ', '')):
        if c not in CHARS:
            c = un('NFD', c)[0]
        if c in CHARS:
            fixed += c
        else:
            print(c.upper(), 'is not an Akkadian transliteration character.')
            exit()
    return fixed


def lookup(dictionary: str, query: str) -> str:
    """get near the page number of the query in given Akkadian dictionary"""
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
    query = fix_query(args.query)
    if args.d:
        print(lookup(args.d.lower(), query))
    else:
        for dict_ in DICT_NAMES:
            print(dict_.upper() + ':', lookup(dict_ , query))
