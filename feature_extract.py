#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

from bs4 import BeautifulSoup

#import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import tag

#from autocorrect import spell

import re
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
# Include the above line, if you don't have tesseract executable in your PATH
# Example tesseract_cmd: 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'



def get_img_text_ocr(img_path):
    """
    :param img_path:
    :return:
    This part is to extract words from an image. We apply OCR technique to read texts from images.
    More info on OCR can be found:
    https://github.com/madmaze/pytesseract
    """
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img, lang='eng')
    sent = word_tokenize(text.lower())
    words = [word.lower() for word in sent if word.isalpha()]

    #words = list(set(words))
    # remove stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    ocr_text = ' '.join(words)
    return ocr_text


def get_structure_html_text(html_path):
    """
    :param html_path:
    :return:
    """
    with open(html_path, 'r') as myfile:
        data = myfile.read()
    try:
        soup = BeautifulSoup(data, "lxml")
    except Exception as inst:
        f = open('log-error.log', 'a')
        f.write("SoupParse Exception: " + str(type(inst)) + " " + str(html_path) + '\n')
        f.close()
        return (None,None,None)

    heads = '.'.join(t.text for t in soup.find_all(re.compile(r'h\d+')))
    things = '.'.join(p.text for p in soup.find_all('p'))
    tags = '.'.join(a.text for a in soup.find_all('a'))
    titles =  '.'.join(t.text for t in soup.find_all('title'))

    raw = heads + ' ' + things + ' ' + tags + ' ' + titles
    sent = word_tokenize(raw) #tokenize html
    tokens = tag.pos_tag(sent)

    #_map = {i.lower():j for i,j in tokens}
    #remove no-alpha words

    words = [word.lower() for word,_ in tokens if word.isalpha()]
    #words = list(set(words))

    #remove stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]

    text_word_str = ' '.join(words)

    #form analysis
    forms = soup.find_all('form')
    num_of_forms = len(forms)
    candidate_attributes = ['type', 'name', 'submit', 'placeholder']
    attr_word_list = list()

    for idx, form in enumerate(forms):
        print ("{}-ith form".format(idx))
        inputs = form.find_all('input')
        for i in inputs:
            for j in candidate_attributes:
                if i.has_attr(j):
                    attr_word_list.append(i[j])

    attr_word_str = ' '.join(attr_word_list)
    return text_word_str, num_of_forms, attr_word_str





