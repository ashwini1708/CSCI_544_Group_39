import sys
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer

def main():

    # Read the data
    train_data = []
    train_labels = []
    test_data = []
    test_labels = []
    actualPos = 0
    actualNeg = 0
    actualNeu = 0

    #--- recursively walk through "DATA directories which has data ---#
    for root, directories, filenames in os.walk(sys.argv[1]):


        for each_filename in filenames:
            if each_filename.endswith(".txt"):

                path = root + '/' + each_filename


                with open(os.path.join(root, each_filename), 'r') as f:
                    tokens = f.read()

                    #---- if the folder is training set ----#
                    if "Train" in path:
                        train_data.append(tokens)
                        # test["word"]=tokens
                        if "positive" in path:
                            train_labels.append("positive")
                        elif "negative" in path:
                            train_labels.append("negative")
                        elif "neutral" in path:
                            train_labels.append("neutral")

                    # ---- if the folder is development set ----#
                    elif "Dev" in path:
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

    #-----calculate tf-idf for the train data set with eliminating words if frequency < 5 and frequency > 80%----#
    vectorizer = TfidfVectorizer(min_df=5,
                                 max_df = 0.8,
                                 sublinear_tf=True,
                                 use_idf=True)
    train_vectors = vectorizer.fit_transform(train_data)
    test_vectors = vectorizer.transform(test_data)



    # ------- Perform classification with SVM, kernel=linear-------#
    classifier = svm.LinearSVC()
    classifier.fit(train_vectors, train_labels)
    results = classifier.predict(test_vectors)

    print("Evaluation results of Linear SVC")
    print(classification_report(test_labels, results))

if __name__ == '__main__':

    main()
