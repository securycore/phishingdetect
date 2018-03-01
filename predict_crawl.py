#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import util_ke
import model
import numpy as np
import feature_extract

#/mnt/sdb1/browser_data/facebook_com-247/screenshots


def predict():
    X = np.loadtxt("./data/X.txt")
    Y = np.loadtxt("./data/Y.txt")

    forest = model.tree_model_based_feature_importance(X,Y)

    facebook_dir = "/mnt/sdb1/browser_data/facebook_com-247"
    #uber_dir = "/mnt/sdb1/browser_data/uber_com-688"

    cans = util_ke.read_candidates_from_crawl_data(facebook_dir)

    DEFAULT_FILE = "Predict.txt"
    for c in cans:
        if os.path.exists(c.web_source) and os.path.exists(c.web_img):
            v = feature_extract.feature_vector_extraction(c)
            if v is None:
                continue
            p = forest.predict(np.asarray(v).reshape(1, -1))
            print (c.idx, p)
            s = str(c.idx) + "," + str(p) + "\n"
            with open(DEFAULT_FILE, 'a') as f:
                f.write(s)
            pass

predict()