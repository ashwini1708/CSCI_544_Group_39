import sys
import os
import json
import math
from math import log10

record=[]
def classify(src):
    intermediate_output= open("yelpmodel.txt", "r", encoding="latin1")
    for line in intermediate_output:
        record.append(json.loads(line))


    probability=record[0]
    words=record[1]
    positive_dic=record[2]
    negative_dic=record[3]
    neutral_dic=record[4]

    # FETCHING ACTUAL FILE COUNT
    file_counter_positive=0
    file_counter_negative=0
    file_counter_neutral = 0

    positive_counter=0
    negative_counter=0
    neutral_counter=0

    correct_positive=0
    correct_negative=0
    correct_neutral = 0

    #---- finding actual counters of files ---#
    for root, dirs, files in os.walk(src):

        for fname in files:
            path = root + '/' + fname
            if "positive" in path:
                file_counter_positive=file_counter_positive +1
            elif "negative" in path:
                file_counter_negative=file_counter_negative +1
            elif "neutral" in path:
                file_counter_neutral=file_counter_neutral +1

    #----writing to an output file ---#
    try:
        os.remove('yelpoutput.txt')
    except OSError:
        pass

    f = open('yelpoutput.txt', 'w')
    for root, dirs, files in os.walk(src):
        for file in files:
            if file.endswith(".txt"):
                file_open=open(root + "/" + file, "r", encoding="latin1").read()
                tokens=file_open.split()
                prob_positive_words = 0.0
                prob_negative_words = 0.0
                prob_neutral_words = 0.0

                for i in tokens:
                    if i in positive_dic:
                        prob_positive_words = (prob_positive_words) + positive_dic[i]


                    if i in negative_dic:
                        prob_negative_words = (prob_negative_words) + (negative_dic[i])


                    if i in neutral_dic:
                        prob_neutral_words = (prob_neutral_words) + (neutral_dic[i])


                prob_positive_words=log10(probability[0]) + (prob_positive_words)
                prob_negative_words = log10(probability[1]) +(prob_negative_words)
                prob_neutral_words = log10(probability[2]) + (prob_neutral_words)

                if(prob_positive_words > prob_negative_words and prob_positive_words > prob_neutral_words):
                    f.write("positive" +" " + root + '/' +file + "\n")
                    positive_counter=positive_counter+1
                elif(prob_negative_words > prob_positive_words and prob_negative_words > prob_neutral_words):
                    f.write("negative" +" " + root + '/'+ file + "\n")
                    negative_counter=negative_counter+1
                elif (prob_neutral_words > prob_positive_words and prob_neutral_words > prob_negative_words):
                    f.write("neutral" + " " + root + '/' + file + "\n")
                    neutral_counter = neutral_counter + 1


    f.close()

    output = open("yelpoutput.txt", "r", encoding="latin1").readlines()

    #--- comparing for evaluation ----#
    for line in output:
        line=line.split()

        if line[0].lower() in line[1]:

            if line[0].lower() == "positive":
                correct_positive=correct_positive + 1
            elif line[0].lower() == "negative":
                correct_negative = correct_negative + 1
            elif line[0].lower() == "neutral":
                correct_neutral = correct_neutral + 1


    #calculating precision
    #precision = (correctly classified as ck) / (classified as ck)

    precision_positive=correct_positive / positive_counter
    precision_negative = correct_negative / negative_counter
    precision_neutral = correct_neutral / neutral_counter

    # REcall = (correctly classified as ck) / (belongs to ck)

    recall_positive=correct_positive / file_counter_positive
    recall_negative = correct_negative / file_counter_negative
    recall_neutral = correct_neutral / file_counter_neutral

    # F-score calculation

    f_score_positive =(2* precision_positive * recall_positive )/ (precision_positive + recall_positive)
    f_score_negative = (2 * precision_negative * recall_negative) / (precision_negative + recall_negative)
    f_score_neutral = (2 * precision_neutral * recall_neutral) / (precision_neutral + recall_neutral)

    print ("precison positive is " ,precision_positive )
    print("precison negative is ", precision_negative)
    print("precison neutral is ", precision_neutral)

    print("recall positive is ", recall_positive)
    print("recall negative is ", recall_negative)
    print("recall neutral is ", recall_neutral)

    print("F score positive is" ,f_score_positive )
    print("F score negative is", f_score_negative)
    print("F score negative is", f_score_neutral)

    avg_weight = ((f_score_positive + f_score_negative+f_score_neutral) / 3)

    print("weighted Avg : ", avg_weight)

classify(sys.argv[1])