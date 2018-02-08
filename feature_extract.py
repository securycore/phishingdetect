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

# import nltk - a library for NLP analysis
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import tag
from autocorrect import spell
import re
import os
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
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
    words = [w for w in words if w not in stop_words]
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
        return None, None, None

    heads = '.'.join(t.text for t in soup.find_all(re.compile(r'h\d+')))
    things = '.'.join(p.text for p in soup.find_all('p'))
    tags = '.'.join(a.text for a in soup.find_all('a'))
    titles = '.'.join(t.text for t in soup.find_all('title'))

    raw = heads + ' ' + things + ' ' + tags + ' ' + titles
    sent = word_tokenize(raw)
    #tokenize html

    tokens = tag.pos_tag(sent)
    #_map = {i.lower():j for i,j in tokens}
    #remove no-alpha words

    words = [word.lower() for word, _ in tokens if word.isalpha()]
    #words = list(set(words))

    #remove stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if w not in stop_words]

    text_word_str = ' '.join(words)

    #form analysis
    forms = soup.find_all('form')
    num_of_forms = len(forms)
    candidate_attributes = ['type', 'name', 'submit', 'placeholder']
    attr_word_list = list()

    for idx, form in enumerate(forms):
        inputs = form.find_all('input')
        for i in inputs:
            for j in candidate_attributes:
                if i.has_attr(j):
                    attr_word_list.append(i[j])

    attr_word_str = ' '.join(attr_word_list)

    words = word_tokenize(attr_word_str)
    words = [word.lower() for word in words if word.isalpha()]
    # words = list(set(words))

    # remove stop words
    words = [w for w in words if w not in stop_words]
    attr_word_str = ' '.join(words)

    return text_word_str, num_of_forms, attr_word_str


WORD_TERM =[u'hidden', u'password', u'email', u'text', u'account', u'found', u'website', u'sign', u'paypal', u'page', u'facebook',
            u'web', u'security', u'error', u'access', u'hosting', u'new', u'online', u'directory', u'warning', u'open', u'copy',
            u'stream', u'failed', u'free', u'server', u'use', u'signed', u'address', u'requested', u'help', u'log', u'please',
            u'url', u'number', u'computer', u'mum', u'you', u'hostinger', u'checkbox', u'name', u'forbidden', u'submit', u'yahoo',
            u'service', u'information', u'many', u'request', u'site', u'phone', u'search', u'small', u'world', u'login', u'create',
            u'contact', u'domain', u'need', u'terms', u'card', u'using', u'home', u'wordpress', u'securely', u'one', u'trying',
            u'secure', u'ema', u'check', u'update', u'confirm', u'file', u'features', u'may', u'upgrade', u'share', u'support',
            u'get', u'your', u'encountered', u'unlimited', u'handle', u'credit', u'work', u'aoouunl', u'answer', u'today',
            u'policy', u'joola', u'production', u'indexiphp', u'passed', u'mobile', u'keep', u'privacy', u'safe', u'asked',
            u'time', u'mail', u'business', u'plan', u'yeux', u'yam', u'center', u'like', u'stay', u'remember', u'weeks', u'dropbox',
            u'services', u'shared', u'banking', u'bank', u'people', u'legal', u'try', u'para', u'united', u'forgot', u'top', u'connect', u'java',
            u'question', u'sleep', u'protect', u'looking', u'firstname', u'google', u'back', u'user', u'opens', u'code', u'others', u'owner',
            u'must', u'rights', u'window', u'suspended', u'wake', u'pass', u'soon', u'download', u'heliohost', u'cheap', u'think', u'find', u'close',
            u'conditions', u'link', u'friends', u'nei', u'therefore', u'best', u'automatically', u'hesse', u'caused', u'uncheck', u'ask',
            u'inconvenience', u'questions', u'verification', u'private', u'logging', u'possible',
            u'trouble', u'require', u'pages', u'websites', u'tel', u'usually', u'enter', u'sale', u'permanently', u'box']


def text_embedding_into_vector(txt_str):
    """
    :param text_str:
    :return:
    We split text into a list of features for training
    """
    texts = txt_str.split(' ')
    texts = [spell(w).lower() for w in texts]

    embedding_vector = [0]*(len(WORD_TERM)+1)
    for elem in texts:
        # if it exist, we set the index plus one
        # else the last position plus one
        index = WORD_TERM.index(elem) if elem in WORD_TERM else -1
        embedding_vector[index] += 1

    return embedding_vector


def feature_vector_extraction(c):
    """
    :param c: a candidate object
    :return: the feature vector
    it consists of three components: img-text, html-text, form-text
    """
    if os.path.exists(c.web_source) and os.path.exists(c.web_img):
        try:
            img_text = get_img_text_ocr(c.web_img)
            text_word_str, num_of_forms, attr_word_str = get_structure_html_text(c.web_source)
            img_v = text_embedding_into_vector(img_text)
            txt_v = text_embedding_into_vector(text_word_str)
            form_v = text_embedding_into_vector(attr_word_str)
            final_v = img_v + txt_v + form_v + [num_of_forms]
            return final_v

        except:

            return None

if __name__ == "__main__":
    img = "/mnt/sdb1/browser_phishingTank/Crawl/1/5457958.mobile.screen.png"
    wells_fargo_img = "/mnt/sdb1/browser_phishingTank/Crawl/7/5450291.mobile.screen.png"
    wells_fargo_html = "/mnt/sdb1/browser_phishingTank/Crawl/7/5450291.mobile.source.html"
    print (get_structure_html_text(wells_fargo_html))
    print (get_img_text_ocr(wells_fargo_img))

