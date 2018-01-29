#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob

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

import collections
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
LOGGING = False

# Include the above line, if you don't have tesseract executable in your PATH
# Example tesseract_cmd: 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

def get_img_text_ocr(img_path):
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img, lang='eng')
    sent = word_tokenize(text.lower())
    words = [word.lower() for word in sent if word.isalpha()]
    words = list(set(words))

    # remove stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]

    tmp = ' '.join(words)
    print (tmp)
    return tmp


def get_structure_info(url):
    with open(url, 'r') as myfile:
        data = myfile.read()
    try:
        soup = BeautifulSoup(data, "lxml")
    except Exception as inst:
        f = open('log-error.log', 'a')
        f.write("SoupParse Exception: " + str(type(inst)) + " " + str(url) + '\n')
        f.close()
        return (None)

    forms = soup.find_all('form')
    candidate_attributes = ['type','name','submit','placeholder']
    attr = collections.defaultdict(list)
    for idx,form in enumerate(forms):
        print ("{}-ith form".format(idx))
        inputs = form.find_all('input')
        for i in inputs:
            for j in candidate_attributes:
                if i.has_attr(j):
                    attr[j].append(i[j])
    print (attr)


def get_html_text(url):
    with open(url, 'r') as myfile:
        data = myfile.read()
    try:
        soup = BeautifulSoup(data, "lxml")
    except Exception as inst:
        f = open('log-error.log', 'a')
        f.write("SoupParse Exception: " + str(type(inst)) + " " + str(url) + '\n')
        f.close()
        return (None)

    things = '.'.join(p.text for p in soup.find_all('p'))
    tags = '.'.join(a.text for a in soup.find_all('a'))
    titles =  '.'.join(t.text for t in soup.find_all('title'))

    raw = things + ' ' + tags + ' ' + titles

    sent = word_tokenize(raw) #tokenize html
    tokens = tag.pos_tag(sent)

    _map = {i.lower():j for i,j in tokens}
    #remove no-alpha words
    words = [word.lower() for word,_ in tokens if word.isalpha()]
    words = list(set(words))

    #remove stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]

    my_map = {i:_map[i] for i in words}
    tmp = ' '.join(words)

    print (tmp)
    print (my_map)
    return tmp

def get_html_page_text__and_imgs(img, html, keyword):

    text_img = get_img_text_ocr(img)
    text_html =  get_html_text(html)

    print ('-----------------TEXT-HTML-----------------')
    print (text_html)

    print ('-----------------TEXT-IMAG-----------------')
    print (text_img)

    f1,f2 = False,False

    if keyword in text_html:
        f1 = True
        print ("detect a keyword in HTML")

    if keyword in text_img:
        f2 = True
        print ("detect a keyword in IMG")

    return f1 or f2

def test(img_dir, html_dir):

    imgs = img_dir+'*.screen.png'
    pngs = glob.glob(imgs)
    #print (imgs, pngs)

    screen = 'screen.png'
    source = 'source.html'
    keyword = 'paypal'

    for png in pngs:
        html = png.split('/')[-1][:-len(screen)] + source
        html = html_dir + html
        if get_html_page_text__and_imgs(png,html, keyword):
            print (png)
            f = open('found.log', 'a')
            f.write(png + '\n')
            f.write(html + '\n')
            f.write('===================\n')
            f.flush()
            f.close()




if __name__ == "__main__":
    #img_dir =  '/Users/ketian/Desktop/browser_data_phishingTank/screenshots/'
    #source_dir ='/Users/ketian/Desktop/browser_data_phishingTank/sources/'

    #img_dir = '/Users/ketian/Desktop/browser_data/screenshots/'
    #source_dir = '/Users/ketian/Desktop/browser_data/sources/'

    #test(img_dir,source_dir)
    #test = '/Users/ketian/Desktop/browser_data_phishingTank/sources' \
    #       '/account-verifty.com03_54PM_on_October_07_2017.source.html'
    test = './test/sewauk.org'
    print get_html_text(test)
    print get_img_text_ocr('./test/sewauk.org.png')