import os,sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
import numpy as np
from nltk.stem.porter import PorterStemmer
import nltk

stemmer = PorterStemmer()

def stem_tokens(tokens, stemmer):
    stem=[]
    for token in tokens:
        stem.append(stemmer.stem(token))
    return stem

def tokenize(text):
    text_lower = text.lower()
    tokens = nltk.wordpunct_tokenize(text_lower)
    stem = stem_tokens(tokens, stemmer)
    return stem


train_data = []
train_labels = []
test_data = []
test_labels = []

'''1. sys.argv[1] specifies the path for training_data
   2. Read each file from the training data and add all the text to a list(train_data)
   3. create a list of training labels'''
for root, directories, filenames in os.walk(sys.argv[1]):

    for each_file in filenames:
        if each_file.endswith(".txt"):
            #print(type(each_file))
            fopen=open(os.path.join(root, each_file), 'r')
            content = fopen.read()
            train_data.append(content)
            if "positive" in each_file:
                train_labels.append("positive")
            elif "negative" in each_file:
                train_labels.append("negative")
            elif "neutral" in each_file:
                train_labels.append("neutral")


'''1. sys.argv[2] specifies the path for the test data
   2. Read each file from the test data and all the text to a list(test_data)
   3. Create a list of test labels which will be required for classification_report'''
for root, directories, filenames in os.walk(sys.argv[2]):

    for each_file in filenames:
        if each_file.endswith(".txt"):
            fopen = open(os.path.join(root, each_file), 'r')
            content = fopen.read()
            test_data.append(content)

            if "positive" in each_file:
                test_labels.append('positive')
            elif "negative" in each_file:
                test_labels.append('negative')
            elif "neutral" in each_file:
                test_labels.append('neutral')

# Create TF-IDF feature vectors
vectorizer = TfidfVectorizer(min_df=3,
                             max_df = 0.7,
                             sublinear_tf=True,
                             tokenizer=tokenize,
                             use_idf=True)
train_vectors = vectorizer.fit_transform(train_data)
test_vectors = vectorizer.transform(test_data)

'''create an object for the random forest classifier and then feed the training data to the
   classifier. And then predict the labels for test_data'''
classifier = RandomForestClassifier(n_estimators=20)

classifier.fit(train_vectors, train_labels)

prediction= classifier.predict(test_vectors)

print(np.mean(prediction== test_labels))
print(classification_report(test_labels, prediction))


