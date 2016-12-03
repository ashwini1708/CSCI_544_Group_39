import nltk
import string
import os
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import TweetTokenizer
import numpy as np
from sklearn.feature_extraction import FeatureHasher
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

path = 'train_data_knn'
token_dict = {}
token_dict_test = {}
stemmer = PorterStemmer()
tokener=TweetTokenizer(strip_handles=True, reduce_len=True)

'''This method reduces each word to its root word. Uses the Porter Stemmer method'''
def stem_tokens(tokens, stemmer):
    stem=[]
    for token in tokens:
        stem.append(stemmer.stem(token))
    return stem

def tokenize(text):
    tokens = tokener.tokenize(text)
    stem = stem_tokens(tokens,stemmer)
    return stem

def get_bigrams(text):
    bigram_tokens = [bigrams for bigrams in zip(text[:-1], text[1:])]
    return bigram_tokens

def POS_tagging(text):
    POS_tags = nltk.pos_tag(text)
    return POS_tags

Y_act_tag=[]
for dirName, subDir, files in os.walk(path):
    for file in files:
        fopen=open(os.path.join(dirName, file), 'r')
        review=fopen.read()
        text = review.lower()
        final_text = text.translate(None , string.punctuation)
        token_dict[file] = final_text

'''Extracting the features and adding it to a list'''
X_feature=[]
for file in token_dict:
      feature = []

      #response=tfidf.transform(token_dict[file])
      tokens=tokenize(token_dict[file])

      for token in tokens:
        feature.extend([
               'TOKEN_' + token
               ])
      pos = POS_tagging(tokens)

      for tag in pos:
          #print(tag[1])
          feature.extend([
              'POS_' + tag[1]
          ])
      #print(type(token_dict[file]))
      bigrams=get_bigrams(tokens)

      #for bigram in b
      for bigram in bigrams:
           feature.extend([
               'BIGRAM_' + ('_').join(bigram)
           ])

      X_feature.append(feature)

      if 'positive' in file:
          Y_act_tag.append('positive')
      elif 'negative' in file:
          Y_act_tag.append('negative')
      elif 'neutral' in file:
          Y_act_tag.append('neutral')


'''Converting the list into Feature_Hasher which is given as input to the classifier'''

hasher = FeatureHasher(input_type='string')
X = hasher.transform(X_feature)
print(type(X))
Y_act_tag_test=[]

for dirName, subDir, files in os.walk('test_data_knn'):
    for file in files:
        #print(file)
        fopen=open(os.path.join(dirName, file), 'r')
        review=fopen.read()
        #stem=stem_tokens(review, stemmer)
        text = review.lower()
        final_text = text.translate(None , string.punctuation)
        token_dict_test[file] = final_text


X_feature_test=[]
for file in token_dict_test:
    feature = []

    tokens = tokenize(token_dict_test[file])

    for token in tokens:
        feature.extend([
            'TOKEN_' + token
        ])
    pos = POS_tagging(tokens)

    for tag in pos:
        # print(tag[1])
        feature.extend([
            'POS_' + tag[1]
        ])

    bigrams = get_bigrams(tokens)

    # for bigram in b
    for bigram in bigrams:
        feature.extend([
            'BIGRAM_' + ('_').join(bigram)
        ])

    X_feature_test.append(feature)


    if 'positive' in file:
        Y_act_tag_test.append('positive')
    elif 'negative' in file:
        Y_act_tag_test.append('negative')
    elif 'neutral' in file:
        Y_act_tag_test.append('neutral')



Y = hasher.transform(X_feature_test)


dec_tree=DecisionTreeClassifier(n_estimators=20)
clf=dec_tree.fit(X,Y_act_tag)

predicted = clf.predict(Y)

print(np.mean(predicted == Y_act_tag_test))


print(classification_report(Y_act_tag_test, predicted))