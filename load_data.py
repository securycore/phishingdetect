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
            if len(line) < 1 or line.startswith("#"):
                continue
            x_label = line.split(",")[0]
            y_label = line.split(",")[-1]
            if len(y_label) <1:
                print (x_label)
                raw_input()
            labels[x_label] = y_label
    X = []
    Y = []
    for ele in labels:
        X.append(ele)
        Y.append(labels[ele])

    print ("LOAD total {} labels".format(len(labels)))
    print ("LOAD total y {} labels".format(sum(1 for i in labels if labels[i] == 'y')))
    print ("LOAD total n {} labels".format(sum(1 for i in labels if labels[i] == 'n')))
    return labels


#print load_label("./label_tool/LABEL.label")
