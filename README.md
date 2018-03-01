# Phishing Page Detect

A simple machine learning model to identify phishing pages by looking at:

* HTML text
* HTML structure
* IMAGE text

## Install OCR, NLTK and ML dependences
```
bash install.sh
```

## Run the model

```
python predict_crawl.py -h
usage: predict_crawl.py [-h] [-t HTML] [-i IMG]

running analysis...

optional arguments:
  -h, --help            show this help message and exit
  -t HTML, --html HTML  A html source data to extract features
  -i IMG, --img IMG     A image data to extract features

```

### Demo

Malicious sample:
```
python predict_crawl.py --img=test/sewauk.org.png --html=test/sewauk.org

Use existing model
Img is test/sewauk.org.png
HTML is test/sewauk.org
1-malicious 0-benign
Prediction is that [1.]
```

Benign sample:
```
python predict_crawl.py --img=test/100022538-facebook.com.png --html=test/100022538-facebook.source.txt

Use existing model
Img is test/100022538-facebook.com.png
HTML is test/100022538-facebook.source.txt
1-malicious 0-benign
Prediction is that [0.]
```

## Model Evaluation
```
Train shape (1641, 526)
1-label: 643
KNN
Accuracy: 0.81 (+/- 0.15)
DT
Accuracy: 0.88 (+/- 0.13)
RF
Accuracy: 0.92 (+/- 0.06)
SVM
Accuracy: 0.85 (+/- 0.11)
Logit
Accuracy: 0.88 (+/- 0.13)

KNeighborsClassifier
False positive: 0.050435
False negative: 0.125217
Area under the ROC curve : 0.895357

DecisionTreeClassifier
Accuracy score 0.886956521739
False positive: 0.040000
False negative: 0.073043
Area under the ROC curve : 0.900039

RandomForestClassifier
Accuracy score 0.926956521739
False positive: 0.034783
False negative: 0.038261
Area under the ROC curve : 0.982916

SVC
Accuracy score 0.859130434783
False positive: 0.034783
False negative: 0.106087
Area under the ROC curve : 0.936241

LogisticRegression
Accuracy score 0.893913043478
False positive: 0.038261
False negative: 0.067826
Area under the ROC curve : 0.947001

```


## FAQ

- export python when import does not work
```
export PYTHONPATH="${PYTHONPATH}/usr/local/lib/python2.7/site-packages:/usr/lib/python2.7/site-packages"
>>>>>>> 22449ef7a83f97d4f37d2561241e0d7fdbd6ddc9
```

## Disclaimer

research prototype

