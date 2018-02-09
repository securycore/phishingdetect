#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
from autocorrect import spell


def text_analysis(txt_str):
    texts = txt_str.split(' ')
    texts = [spell(w).lower() for w in texts]
    ct = collections.Counter(texts)
    ws = list()
    for i,j in ct.most_common(200):
        print (i,j)
        ws.append(i)

    print ("fk", ws)

"""
# Abandoned
email is not an english word        
from nltk.corpus import words
WORD_LIST = set(words.words())

def text_is_english_word(word):
    if word.lower() in WORD_LIST:
        return True
    else:
        return False
"""

if __name__ == "__main__":
    pass

