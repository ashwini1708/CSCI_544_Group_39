import json
from itertools import islice
import io
import os, glob, nltk

from nltk.stem.porter import PorterStemmer



reviewRecord = []

jenc = json.JSONEncoder();


#--- stemming using porter stemmer ----#
stemmer = PorterStemmer()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

# ------reading from yelp review file------- #
with open("yelp_academic_dataset_review.json", "r", encoding="latin1") as inputFile:
    slicedFile = islice(inputFile,1, 100000)

    for line in slicedFile:
        reviewRecord.append(json.loads(line))

    file_counter = 0

    positive_counter = 0
    negative_counter = 0
    neutral_counter = 0
    distinct_words = set([])

    #-----clearing out the directories ----#
    dirPath = "Data/Train/positive"
    fileList = os.listdir(dirPath)
    for fileName in fileList:
        os.remove(dirPath + "/" + fileName)

    dirPath = "Data/Train/negative"
    fileList = os.listdir(dirPath)
    for fileName in fileList:
        os.remove(dirPath + "/" + fileName)

    dirPath = "Data/Train/neutral"
    fileList = os.listdir(dirPath)
    for fileName in fileList:
        os.remove(dirPath + "/" + fileName)

    # -----clearing out the directories ends ----#



    max_file_length=0

    # ------creating files and placing file tokens in resp. folders------#
    for each_review in reviewRecord:

        stars = each_review['stars']

        tokens = nltk.wordpunct_tokenize(each_review['text'])
        stems = stem_tokens(tokens, stemmer)
        if(max_file_length < len(stems)):
            max_file_length=len(stems)

        #-- categorise file as positive, negative,neutral if stars >3, stars <3 and stars=3 respectively----#
        if (stars > 3):


            with io.open("Data/Train/positive/file_" + str(file_counter) + ".txt", 'w',
                         encoding='utf-8') as positive_file:
                for each_token in stems:
                    distinct_words.add(each_token)
                    positive_file.write((each_token+" "))
                positive_counter = positive_counter + 1

        elif (stars < 3):
            with io.open("Data/Train/negative/file_" + str(file_counter) + ".txt", 'w',
                         encoding='utf-8') as negative_file:
                for each_token in stems:
                    distinct_words.add(each_token)
                    negative_file.write((each_token + " "))
                negative_counter = negative_counter + 1

        else:
            with io.open("Data/Train/neutral/file_" + str(file_counter) + ".txt", 'w',
                         encoding='utf-8') as neutral_file:
                for each_token in stems:
                    distinct_words.add(each_token)
                    neutral_file.write((each_token+" "))
                neutral_counter = neutral_counter + 1

        file_counter = file_counter + 1

    print("positive counter is ", positive_counter)
    print("negative counter is ", negative_counter)
    print("neutral counter is ", neutral_counter)

