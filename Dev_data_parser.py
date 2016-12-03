import json
from itertools import islice
import io
import os
import nltk

record=[]

jenc = json.JSONEncoder();

#--read the yelp reviews---#
with open("yelp_academic_dataset_review.json", "r", encoding="latin1") as inputFile:
    slicedFile = islice(inputFile,  100000,125000)



    for line in slicedFile:
        record.append(json.loads(line))

    positive_counter = 0
    negative_counter = 0
    neutral_counter = 0
    file_counter = 0

    #--- clear the directories ---#
    dirPath = "Data/Dev/positive"
    fileList = os.listdir(dirPath)
    for fileName in fileList:
        os.remove(dirPath + "/" + fileName)

    dirPath = "Data/Dev/negative"
    fileList = os.listdir(dirPath)
    for fileName in fileList:
        os.remove(dirPath + "/" + fileName)

    dirPath = "Data/Dev/neutral"
    fileList = os.listdir(dirPath)
    for fileName in fileList:
        os.remove(dirPath + "/" + fileName)

    #---clearing ends ---#

    for each_review in record:


        stars = each_review['stars']
        tokens = nltk.wordpunct_tokenize(each_review['text'])

        # -- categorise file as positive, negative,neutral if stars >3, stars <3 and stars=3 respectively----#

        if (stars > 3):
            with io.open("Data/Dev/positive/file_" + str(file_counter) + ".txt", 'w',
                         encoding='utf-8') as positive_file:
                for each_token in tokens:
                    positive_file.write((each_token + " "))
                positive_counter = positive_counter + 1

        elif (stars < 3):
            with io.open("Data/Dev/negative/file_" + str(file_counter) + ".txt", 'w',
                         encoding='utf-8') as negative_file:
                for each_token in tokens:
                    negative_file.write((each_token + " "))
                negative_counter = negative_counter + 1

        else:
            with io.open("Data/Dev/neutral/file_" + str(file_counter) + ".txt", 'w',
                         encoding='utf-8') as neutral_file:
                for each_token in tokens:
                    neutral_file.write((each_token + " "))
                neutral_counter = neutral_counter + 1

        file_counter = file_counter + 1