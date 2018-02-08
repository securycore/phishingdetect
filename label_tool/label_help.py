#!/usr/bin/env python
# -*- coding: utf-8 -*-


import subprocess
import os
import sys


DEFAULT_FILE = "LABEL.label"

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

import util_ke
#Three labels; y-yes, n-no, u-unknown

def label_image(img_path):
    p = subprocess.Popen(["display", img_path])
    label = raw_input("Give a label for image: ")
    p.kill()
    print ("We label {} as {}".format(img_path, label))
    write_label_into_file(img_path, label)


def write_label_into_file(img_path, label):
    idx = img_path.split('/')[-1].split('.')[0]
    s = str(idx) + "," + str(img_path) + "," + str(label) + "\n"
    with open(DEFAULT_FILE,'a') as f:
        f.write(s)
    pass


if __name__ == "__main__":
    d1 = "/mnt/sdb1/browser_phishingTank/Crawl/74"
    d2 = "/mnt/sdb1/browser_phishingTank/Crawl/1"
    d3 = "/mnt/sdb1/browser_phishingTank/Crawl/8"
    microsoft = "/mnt/sdb1/browser_phishingTank/Crawl/177"
    google = "/mnt/sdb1/browser_phishingTank/Crawl/76"
    already_labled = [d1, d2, d3, microsoft, google]

    parentDir = "/mnt/sdb1/browser_phishingTank/Crawl/"
    dires = [parentDir+i for i in os.listdir(parentDir)]
    dires.sort()

    t = 0
    for cur_folder in dires:
        if cur_folder in already_labled:
            continue
        cans = util_ke.read_pngs_sources_from_directory(cur_folder)
        if len(cans) <= 20 and len(cans) > 0:
            t += len(cans)
            print (cur_folder, len(cans))
            cans.sort(key=lambda x: x.web_img)

            for c in cans:
                if os.path.exists(c.web_img):
                    try:
                        print ("Current label {}".format(c.web_img))
                        label_image(c.web_img)
                        print ("\n")
                    except:
                        print ("error happened")

    print (t)
