#!/usr/bin/env python
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import *

from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm

from sklearn.metrics import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import linear_model


# this is to get score using cross_validation
def get_scroe_using_cv(clt, X, y):
    scores = cross_val_score(clt,X,y,cv=10)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# just want to draw a confusion matrix to make it look fantanstic
def draw_confusion_matrix(y_test, y_pred):
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, y_pred)
    print(cm)

    # Show confusion matrix in a separate window
    plt.matshow(cm)
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def get_fpr_tpr(clt, x, y):

    print ("\n")
    print (clt)

    random_state = np.random.RandomState(0)
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.35, random_state=random_state)

    clt = clt.fit(X_train, y_train)
    y_pred = clt.predict(X_test)

    #accuracy score
    _accuracy_score = accuracy_score(y_test, y_pred)
    print ("Accuracy score {}".format(_accuracy_score))

    pred = clt.predict(X_test)
    fp, fn = 0, 0
    for i,c in enumerate(pred):
        if c == 1 and y_test[i] == 0:
            fp += 1
        if c == 0 and y_test[i] == 1:
            fn += 1
    print ("False positive: %f" % (float(fp + 0.0)/len(y_test)))
    print ("False negative: %f" % (float(fn + 0.0) / len(y_test)))

    #roc curve
    probas_ = clt.predict_proba(X_test)
    #print (probas_)
    #draw_confusion_matrix(y_test,y_pred)

    #print probas_
    fpr, tpr, thresholds = roc_curve(y_test, probas_[:, 1])
    #print (fpr, tpr,thresholds)
    roc_auc = auc(fpr, tpr)
    print ("Area under the ROC curve : %f" % roc_auc)
    return fpr, tpr, roc_auc


def train_and_draw_roc(X_original, y):

    #KNN
    knn = KNeighborsClassifier(algorithm='auto', leaf_size=30,
                               metric='minkowski', n_neighbors=5, p=2, weights='uniform')

    #decision tree
    dtree = DecisionTreeClassifier( criterion='entropy', min_samples_leaf=4, min_samples_split=2,
                                    random_state=None, splitter='best')

    #random forest
    rforest = RandomForestClassifier(bootstrap=True, criterion='gini', max_depth=None, max_features='auto', class_weight='balanced',
                                     min_samples_leaf=1, min_samples_split=2, n_estimators=50, n_jobs=1, oob_score=False, random_state=3)

    #svm
    svmrbf= svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,  kernel='rbf',
                    max_iter=-1, probability=True, random_state=None,
                    shrinking=True, tol=0.001, verbose=False)


    logit = linear_model.LogisticRegression(C=1e5)

    X = np.asarray(X_original)
    print ("Train shape {}".format(X.shape))
    print ("1-label: {}".format(sum(1 for i in Y if i==1)))

    print ("KNN")
    get_scroe_using_cv(knn, X, y)
    print ("DT")
    get_scroe_using_cv(dtree, X, y)
    print ("RF")
    get_scroe_using_cv(rforest, X, y)
    print ("SVM")
    get_scroe_using_cv(svmrbf, X, y)
    print ("Logit")
    get_scroe_using_cv(logit, X, y)


    fpr_knn, tpr_knn, auc_knn = get_fpr_tpr(knn, X, y)
    fpr_dtree, tpr_dtree, auc_dtree = get_fpr_tpr(dtree, X, y)
    fpr_rforest, tpr_rforest, auc_rforest = get_fpr_tpr(rforest, X, y)
    fpr_svmrbf, tpr_svmrbf ,auc_svmrbf= get_fpr_tpr(svmrbf, X, y)
    fpr_log, tpr_log, auc_log = get_fpr_tpr(logit, X, y)

    plt.clf()
    plt.plot(fpr_svmrbf, tpr_svmrbf, 'y.--', label ='SVM AUC=%0.4f'% auc_svmrbf)
    plt.plot(fpr_knn, tpr_knn, 'r^--', label='KNN AUC=%0.4f' %auc_knn)
    plt.plot(fpr_dtree, tpr_dtree, 'b>--', label ='D.Tree AUC=%0.4f'% auc_dtree)
    plt.plot(fpr_rforest, tpr_rforest, 'go--', label ='R.Forest AUC=%0.4f'% auc_rforest)
    plt.plot(fpr_log, tpr_log, '^--', label='Logit AUC=%0.4f' % auc_log)

    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([-0.02, 1.02])
    plt.ylim([-0.02, 1.02])
    plt.xlabel('FPR(False Positive Rate)',fontsize=20)
    plt.ylabel('TPR(True Positive Rate)',fontsize=20)
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.grid()
    plt.show()

    del X
    del y


def tree_model_based_feature_importance(X,y):
    X = np.asarray(X)
    #random forest
    forest = RandomForestClassifier(bootstrap=True, criterion='gini', max_depth=None, max_features='auto', class_weight='balanced',
                                     min_samples_leaf=1, min_samples_split=2, n_estimators=50, n_jobs=1, oob_score=False, random_state=3)

    get_scroe_using_cv(forest, X, y)
    forest.fit(X, y)

    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")

    for f in range(X.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(X.shape[1]), importances[indices],
            color="r", yerr=std[indices], align="center")
    plt.xticks(range(X.shape[1]), indices)
    plt.xlim([-1, X.shape[1]])
    plt.show()


if __name__ =="__main__":
    X = np.loadtxt("X.txt")
    Y = np.loadtxt("Y.txt")
    train_and_draw_roc(X, Y)
