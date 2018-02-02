#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')


def load_label(filename):
    labels = dict()
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            x_label = line.split(",")[0]
            y_label = line.split(",")[1]
            labels[x_label] = y_label
    X = []
    Y = []
    for ele in labels:
        X.append(ele)
        Y.append(labels[ele])
    print (X, len(X))
    print (sum(1 for i in Y if i == "y"))

t = [u'hidden', u'password', u'email', u'text', u'a', u'account', u'found', u'website', u'de', u'mm', u'sign', u'paypal', u'page', u'facebook', u'us', u'web', u'security', u'error', u'access', u'w', u'hosting', u'le', u'new', u'e', u'online', u'directory', u'warning', u'open', u'he', u'copy', u'stream', u'failed', u'free', u'server', u'use', u'signed', u'address', u'wm', u'requested', u'help', u'log', u'please', u'url', u'number', u'computer', u'mum', u'you', u'hostinger', u'checkbox', u'name', u'forbidden', u'j', u'submit', u'yahoo', u'service', u'information', u'many', u'request', u'site', u'phone', u'search', u'small', u'world', u'login', u'create', u'contact', u'domain', u'need', u'terms', u'card', u'v', u'f', u'using', u'home', u'wordpress', u'securely', u'one', u'trying', u'secure', u'go', u'ema', u'check', u'update', u'confirm', u'file', u'n', u'features', u'may', u'upgrade', u'share', u'support', u'get', u'your', u'encountered', u'unlimited', u'handle', u'credit', u'work', u'la', u'aoouunl', u'answer', u'id', u'today', u'policy', u'joola', u'production', u'in', u'indexiphp', u'passed', u'mobile', u'keep', u'privacy', u'safe', u'asked', u'time', u'pm', u'mail', u'business', u'plan', u'yeux', u'yam', u'center', u'like', u'stay', u'mu', u'remember', u'weeks', u'dropbox', u'services', u'shared', u'banking', u'bank', u'people', u'legal', u'try', u'para', u'united', u'forgot', u'top', u'connect', u'java', u'question', u'sleep', u'protect', u'looking', u'firstname', u'google', u'back', u'q', u'user', u'opens', u'code', u'others', u'owner', u'r', u'must', u'rights', u'window', u'en', u'suspended', u'wake', u'pass', u'soon', u'download', u'heliohost', u'cheap', u'em', u'think', u'find', u'close', u'conditions', u'link', u'um', u'friends', u'nei', u'therefore', u'best', u'automatically', u'hesse', u'caused', u'uncheck', u'ask', u'inconvenience', u'questions', u'verification', u'private', u'mw', u'logging', u'possible', u'trouble', u'require', u'pages', u'websites', u'tel', u'usually', u'uk', u'enter', u'sale', u'permanently', u'box']

def remove_small(t):
    tt = []
    for i in t:
        if len(i) <= 2:
            pass
        else:
            tt.append(i)
    print (len(t))
    print (len(tt))
    print ("", tt)

#f = "LABELs"
#load_label(f)
remove_small(t)
