#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "ririhedou@gmail.com"


class Candidate(object):
    def __init__(self, idx, web_img, web_source, mobile_img, mobile_source):
        self.idx = idx
        self.web_img = web_img
        self.web_source = web_source
        self.mobile_img = mobile_img
        self.mobile_source = mobile_source



class Feature(object):
    def __init__(self):
        self.nlp_text = list()
        self.img_text = list()
        self.form_text = list()
        self.form_num = 0

    def update_nlp_text(self, text):
        self.nlp_text.extend(text)

    def update_img_text(self, text):
        self.img_text.extend(text)

    def update_structure(self):
        pass
