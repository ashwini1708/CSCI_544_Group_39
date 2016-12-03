import sys
import os
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier



train_data = []
train_labels = []
test_data = []
test_labels = []
actualPos = 0
actualNeg = 0
actualNeu = 0

'''Reads the Training data samples and tokenizes the individual files.
   It takes the text and appends them to the train_Data. Each
   file name is checked for positive, negative and neutral categories
   and the corresponding label is appended to the train_labels list'''

for root, directories, filenames in os.walk(sys.argv[1]):


    for each_filename in filenames:
        if each_filename.endswith(".txt"):

            path = root + '/' + each_filename


            with open(os.path.join(root, each_filename), 'r') as f:
                tokens = f.read()
                train_data.append(tokens)
                if "positive" in path:
                    train_labels.append("positive")
                elif "negative" in path:
                    train_labels.append("negative")
                elif "neutral" in path:
                    train_labels.append("neutral")

'''Reads the Testing data samples and tokenizes the individual files.
   It takes the text and appends them to the train_Data.
   Each file name is checked for positive, negative and neutral
   categories and the corresponding label is appended to the test_labels list'''



for root, directories, filenames in os.walk(sys.argv[2]):

    for each_filename in filenames:
        if each_filename.endswith(".txt"):

            path = root + '/' + each_filename

            with open(os.path.join(root, each_filename), 'r') as f:
                # print("path is ",f)
                tokens = f.read()

                test_data.append(tokens)

                if "positive" in path:
                    actualPos = actualPos + 1
                    test_labels.append('positive')
                elif "negative" in path:
                    actualNeg = actualNeg + 1
                    test_labels.append('negative')
                elif "neutral" in path:
                    actualNeu = actualNeu + 1
                    test_labels.append('neutral')



'''TfidfVectorizer of Sklearn is used to convert collections
   of raw documents to matrix of TF-IDF features'''

vectorizer = TfidfVectorizer(min_df=5,
                             max_df = 0.8,
                             sublinear_tf=True,
                             use_idf=True)

'''Fit_Transform method of sklearn, learns vocabulary
   and idf from the training data and converts the data
   learnt from fit into document-term frequency '''

train_vectors = vectorizer.fit_transform(train_data)
test_vectors = vectorizer.transform(test_data)


classifier_linear = DecisionTreeClassifier(random_state=0)

classifier_linear.fit(train_vectors, train_labels)

prediction_linear = classifier_linear.predict(test_vectors)


print("Results for Decision Tree classifier are as follows - ")
print(classification_report(test_labels, prediction_linear))

