import nltk
import string
import os,sys
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import TweetTokenizer
import numpy as np
from sklearn.feature_extraction import FeatureHasher
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


token_dict = {}
token_dict_test = {}
stemmer = PorterStemmer()


def stem_tokens(tokens, stemmer):
    stem=[]
    for token in tokens:
        stem.append(stemmer.stem(token))
    return stem

def tokenize(text):
    tokens = nltk.wordpunct_tokenize(text)
    stem = stem_tokens(tokens,stemmer)
    return stem

def get_bigrams(text):
    bigram_tokens = [bigrams for bigrams in zip(text[:-1], text[1:])]
    return bigram_tokens

def POS_tagging(text):
    POS_tags = nltk.pos_tag(text)
    return POS_tags

Y_act_tag=[]
for dirName, subDir, files in os.walk(sys.argv[1]):
    for file in files:
        fopen=open(os.path.join(dirName, file), 'r')
        review=fopen.read()
        text = review.lower()
        final_text = text.translate(None , string.punctuation)
        token_dict[file] = final_text

'''extreact the feature from each file and append to a list'''
X_feature=[]
for file in token_dict:
      feature = []
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
      bigrams=get_bigrams(tokens)
      for bigram in bigrams:
           feature.extend([
               'BIGRAM_' + ('_').join(bigram)
           ])

      feature.extend([
          'TEXT :' + token_dict[file]
      ])

      X_feature.append(feature)

      if 'positive' in file:
          Y_act_tag.append('positive')
      elif 'negative' in file:
          Y_act_tag.append('negative')
      elif 'neutral' in file:
          Y_act_tag.append('neutral')


''' convert the feature list into featureHasher which will be fed to the classifier'''
hasher = FeatureHasher(input_type='string')
X = hasher.transform(X_feature)
print(type(X))
Y_act_tag_test=[]

for dirName, subDir, files in os.walk(sys.argv[2]):
    for file in files:
        fopen=open(os.path.join(dirName, file), 'r')
        review=fopen.read()
        text = review.lower()
        final_text = text.translate(None , string.punctuation)
        token_dict_test[file] = final_text


X_feature_test=[]
for file in token_dict_test:
    feature = []

    # response=tfidf.transform(token_dict[file])
    tokens = tokenize(token_dict_test[file])

    for token in tokens:
        feature.extend([
            'TOKEN_' + token
        ])
    pos = POS_tagging(tokens)

    for tag in pos:
        feature.extend([
            'POS_' + tag[1]
        ])
    bigrams = get_bigrams(tokens)

    for bigram in bigrams:
        feature.extend([
            'BIGRAM_' + ('_').join(bigram)
        ])
    feature.extend([
        'TEXT :' + token_dict_test[file]
    ])
    X_feature_test.append(feature)


    if 'positive' in file:
        Y_act_tag_test.append('positive')
    elif 'negative' in file:
        Y_act_tag_test.append('negative')
    elif 'neutral' in file:
        Y_act_tag_test.append('neutral')



Y = hasher.transform(X_feature_test)

random_forest=RandomForestClassifier(n_estimators=20)
clf=random_forest.fit(X,Y_act_tag)
predicted = clf.predict(Y)
print(np.mean(predicted == Y_act_tag_test))
print(classification_report(Y_act_tag_test, predicted))
