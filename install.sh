#!/bin/bash

echo "check your python and pip version first"
echo "Passed version is Python 2.7.14 and pip 9.0.1 from /usr/local/lib/python2.7/dist-packages (python 2.7)"
python --version
pip --version

echo "Install dependences"

echo "Install tesseract OCR, package name:tesseract or tesseract-OCR"
#https://github.com/tesseract-ocr/tesseract/wiki
sudo apt-get update


sudo apt-get install tesseract-ocr

echo "Your installed tesseract is located at:"
which tesseract
echo "Please make sure it should be in /usr/bin/tesseract!"
echo "Did you check this?"

read -p "Continue (y/n)?" choice
case "$choice" in
  y|Y ) echo "yes";;
  n|N ) echo "no";;
  * ) echo "invalid";;
esac


sleep 5

sudo apt-get install python-tk

sudo apt-get clean

sleep 3

echo "Install your python dependences"

sudo pip install -U pytesseract==0.2.0

echo "Install libraries needed for feature extraction"
sudo pip install -U beautifulsoup4==4.6.0
sudo pip install -U autocorrect==0.3.0
sudo pip install -U nltk==3.2.1


echo "Let download nltk data"
sleep 5
python -m nltk.downloader all


echo "Install libraries needed for machine learning"
sleep 3
sudo pip install -U numpy==1.14.1
sudo pip install -U scipy==0.19.1
sudo pip install -U scikit-learn==0.18.2

sudo pip install -U matplotlib

echo "Done!"