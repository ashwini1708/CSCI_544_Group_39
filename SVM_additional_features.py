import sys
import os
import time
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from sklearn.feature_extraction import FeatureHasher

#---feature extraction
def feature_extraction(token_split,dir_1,distinct_words):
    feature=[]

    for each_word in token_split:
        #--add each token as a feature---#
        feature.extend([
            'token=' + each_word

        ])
        feature.append(each_word)

        #-- check if token has punctuation and make it as a feature ---#
        if each_word in string.punctuation:
            punct="true"


        else:
            punct="false"

        feature.extend([
            'token.isPunctuation=%s'  %punct

        ])

    return feature

def main():

    # Read the data
    train_data = []
    train_labels = []
    test_data = []
    test_labels = []
    actualPos = 0
    actualNeg = 0
    actualNeu = 0

    distinct_words = set([])
    train_dir={}
    train=[]
    test=[]
    test_dir={}


    distinct_words_list=[]

    train_pos=0
    train_neg=0
    train_neu=0
    for root, directories, filenames in os.walk(sys.argv[1]):


        for each_filename in filenames:
            if each_filename.endswith(".txt"):

                path = root + '/' + each_filename


                with open(os.path.join(root, each_filename), 'r') as f:
                    tokens = f.read()

                    token_split=tokens.split()

                    # ---- if the folder is training set ----#
                    if "Train" in path:
                        feature=feature_extraction(token_split, train_dir, distinct_words_list)

                        train.append(feature)
                        train_data.append(tokens)
                        if "positive" in path:
                            train_pos=train_pos+1
                            train_labels.append("positive")
                        elif "negative" in path:
                            train_neg=train_neg+1
                            train_labels.append("negative")
                        elif "neutral" in path:
                            train_neu=train_neu+1
                            train_labels.append("neutral")
                    # ---- if the folder is development set ----#
                    elif "Dev" in path:
                        feature=feature_extraction(tokens, test_dir, distinct_words_list)
                        test.append(feature)
                        test_data.append(tokens)

                        if "positive" in path:
                            actualPos = actualPos + 1
                            test_labels.append("positive")
                        elif "negative" in path:
                            actualNeg = actualNeg + 1
                            test_labels.append("negative")
                        elif "neutral" in path:
                            actualNeu = actualNeu + 1
                            test_labels.append("neutral")

    # print("actual pos",actualPos)
    # print("actual neg", actualNeg)
    # print("actual neutral", actualNeu)
    #
    #--applying featurehasher to input ---#
    hasher = FeatureHasher(input_type='string')
    X = hasher.transform(train)
    Y = hasher.transform(test)

    #---perform classification on linear svc()---#
    classifier = svm.LinearSVC()
    clf = classifier.fit(X, train_labels)
    results = clf.predict(Y)


    pos=0
    neg=0
    neu=0
    print("Results for LinearSVC()")
    for each in results:
        if "positive" in each:
            pos=pos+1
        elif "negative" in each:
            neg=neg+1
        elif "neutral" in each:
            neu=neu+1

    # print("pred pos is ",pos)
    # print("pred neg is ", neg)
    # print("pred neu is ", neu)
    #
    # print("train pos is ", train_pos)
    # print("train neg is ", train_neg)
    # print("train neu is ", train_neu)

    print(classification_report(test_labels, results))



if __name__ == '__main__':

    main()