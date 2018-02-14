# Phishing Page Detect

A simple machine learning model to identify phishing pages by looking at:

* HTML text
* HTML structure
* IMAGE text


## Model
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


KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
           metric_params=None, n_jobs=1, n_neighbors=5, p=2,
           weights='uniform')
Accuracy score 0.824347826087
False positive: 0.050435
False negative: 0.125217
Area under the ROC curve : 0.895357


DecisionTreeClassifier(class_weight=None, criterion='entropy', max_depth=None,
            max_features=None, max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=4,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            presort=False, random_state=None, splitter='best')
Accuracy score 0.886956521739
False positive: 0.040000
False negative: 0.073043
Area under the ROC curve : 0.900039


RandomForestClassifier(bootstrap=True, class_weight='balanced',
            criterion='gini', max_depth=None, max_features='auto',
            max_leaf_nodes=None, min_impurity_split=1e-07,
            min_samples_leaf=1, min_samples_split=2,
            min_weight_fraction_leaf=0.0, n_estimators=50, n_jobs=1,
            oob_score=False, random_state=3, verbose=0, warm_start=False)
Accuracy score 0.926956521739
False positive: 0.034783
False negative: 0.038261
Area under the ROC curve : 0.982916


SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
  decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
  max_iter=-1, probability=True, random_state=None, shrinking=True,
  tol=0.001, verbose=False)
Accuracy score 0.859130434783
False positive: 0.034783
False negative: 0.106087
Area under the ROC curve : 0.936241


LogisticRegression(C=100000.0, class_weight=None, dual=False,
          fit_intercept=True, intercept_scaling=1, max_iter=100,
          multi_class='ovr', n_jobs=1, penalty='l2', random_state=None,
          solver='liblinear', tol=0.0001, verbose=0, warm_start=False)
Accuracy score 0.893913043478
False positive: 0.038261
False negative: 0.067826
Area under the ROC curve : 0.947001

```

## Problem shooting

- export python when import does not work
```
export PYTHONPATH="${PYTHONPATH}/usr/local/lib/python2.7/site-packages:/usr/lib/python2.7/site-packages"
>>>>>>> 22449ef7a83f97d4f37d2561241e0d7fdbd6ddc9
```

## Disclaimer

research prototype

