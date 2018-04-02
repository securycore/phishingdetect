#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import util_ke
import argparse
import model
import numpy as np
import feature_extract


def parse_options():
    parser = argparse.ArgumentParser(description="running analysis...", prefix_chars='-+/')

    parser.add_argument('-t', '--html', type=str,
                        help='A html source data to extract features')
    parser.add_argument('-i', '--img', type=str,
                        help='A image data to extract features')
    args = parser.parse_args()

    return args


def predict_folder():
    X = np.loadtxt("./data/X.txt")
    Y = np.loadtxt("./data/Y.txt")

    forest = model.tree_model_based_feature_importance(X,Y)

    facebook_dir = "/home/ketian/tmp/509"
    #"/home/ketian/tmp/243"
    #uber_dir = "/mnt/sdb1/browser_data/uber_com-688"

    cans = util_ke.read_candidates_from_crawl_data(facebook_dir)

    DEFAULT_FILE = "Predict.txt"
    for c in cans:
        if os.path.exists(c.web_source) and os.path.exists(c.web_img):
            print (c.idx, c.web_img, c.web_source)
            v = feature_extract.feature_vector_extraction(c)
            if v is None:
                continue
            p = forest.predict(np.asarray(v).reshape(1, -1))
            print (c.idx, p)
            s = str(c.idx) + "," + str(p) + "\n"
            with open(DEFAULT_FILE, 'a') as f:
                f.write(s)
            pass


def predict(img, html):

    forest = None

    try:
        from sklearn.externals import joblib
        forest = joblib.load('saved_models/forest.pkl')
        print ("Use existing model")

    except:
        print ("No existing model? create a new one")
        X = np.loadtxt("./data/X.txt")
        Y = np.loadtxt("./data/Y.txt")
        forest = model.tree_model_based_feature_importance(X, Y)

    v = feature_extract.feature_vector_extraction_from_img_html(img, html)

    if v is None:
        return

    p = forest.predict(np.asarray(v).reshape(1, -1))

    print ("1-malicious 0-benign")
    print ("Prediction is that {}".format(p))


if __name__ == "__main__":
    args = parse_options()
    #predict_folder()
    #sys.exit(0)

    if args.html is None or args.img is None:
        print ("No input, system exit")
        sys.exit(1)
    else:
        predict(args.img, args.html)

    sys.exit(0)