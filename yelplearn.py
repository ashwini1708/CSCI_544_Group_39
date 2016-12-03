import sys
import os
import json

from math import log10
def tokenize(input,dir_1,distinct_words):

    for i in input:
        distinct_words.add(i)
        if i not in dir_1:
            dir_1[i]=1
        else:
            dir_1[i]=dir_1[i]+1

    return dir_1


def read_recursive(src):

    file_counter_positive = 0
    file_counter_negative=0
    file_counter_neutral=0


    positive_dir={}
    negative_dir = {}
    neutral_dir={}
    total_words=[]
    doc_count=[]

    distinct_words=set([])
    total_file=0

    for root, directories, filenames in os.walk(src):

        for directory in directories:
            # if the directory is POSITIVE

            if (directory == "positive"):

                # look for files in directory Positive
                for root_1, directories_1, filenames_1 in os.walk(os.path.join(root, directory)):
                    # open files in positive folder

                    for filename_1 in filenames_1:

                        total_file=total_file +1
                        input = open(os.path.join(root_1, filename_1), "r", encoding="latin1").read()
                        input = input.split()

                        tokenize(input,positive_dir,distinct_words)
                        file_counter_positive=file_counter_positive+1;

            elif (directory == "negative"):
                # look for files in directory negative
                for root_1, directories_1, filenames_1 in os.walk(os.path.join(root, directory)):
                    # open files in negative folder

                    for filename_1 in filenames_1:
                        total_file = total_file + 1

                        input = open(os.path.join(root_1, filename_1), "r", encoding="latin1").read()
                        input = input.split()

                        tokenize(input,negative_dir,distinct_words)
                        file_counter_negative=file_counter_negative+1;

            elif (directory == "neutral"):
                # look for files in directory neutral
                for root_1, directories_1, filenames_1 in os.walk(os.path.join(root, directory)):
                    # open files in neutral folder

                    for filename_1 in filenames_1:
                        total_file = total_file + 1

                        input = open(os.path.join(root_1, filename_1), "r", encoding="latin1").read()
                        input = input.split()

                        tokenize(input,neutral_dir,distinct_words)
                        file_counter_neutral=file_counter_neutral+1;


    total_words_positive = sum(positive_dir.values())
    total_words_negative = sum(negative_dir.values())
    total_words_neutral = sum(neutral_dir.values())

    jenc=json.JSONEncoder();

    #DOC COUNT HAS probability OF positive AND negative and neutral
    doc_count.append(file_counter_positive/(file_counter_positive + file_counter_neutral+ file_counter_negative))
    doc_count.append(file_counter_negative/ (file_counter_positive + file_counter_neutral + file_counter_negative))
    doc_count.append(file_counter_neutral/ (file_counter_positive + file_counter_neutral + file_counter_negative))

#total_words has total word count in positive AND negative and neutral and  also the distinct words in both doc
    total_words.append(total_words_positive + len(distinct_words))
    total_words.append(total_words_negative + len(distinct_words))
    total_words.append(total_words_neutral+ len(distinct_words))


    total_words.append(len(distinct_words))

    #--- calculating the probability ----#

    for i in distinct_words:
        if i in positive_dir:
            positive_dir[i] = log10 (positive_dir[i] + 1) - log10 (total_words_positive + len(distinct_words))
        else:
            positive_dir[i] = log10(1) - log10(total_words_positive + len(distinct_words))

        if i in negative_dir:
            negative_dir[i] = log10(negative_dir[i] + 1) -  log10(total_words_negative + len(distinct_words))
        else:
            negative_dir[i] = log10(1) - log10(total_words_negative + len(distinct_words))

        if i in neutral_dir:
            neutral_dir[i] = log10(neutral_dir[i] + 1) -  log10(total_words_neutral + len(distinct_words))
        else:
            neutral_dir[i] = log10(1) - log10(total_words_neutral + len(distinct_words))

    #--- writing to an output file to evaluate results ---#
    try:
        os.remove('nbmodel.txt')
    except OSError:
        pass


    f=open('yelpmodel.txt', 'a')
    f.write(jenc.encode(doc_count)+ "\n")
    f.write(jenc.encode(total_words) + "\n")
    f.write(jenc.encode(positive_dir) + "\n")
    f.write(jenc.encode(negative_dir) + "\n")


    f.write(jenc.encode(neutral_dir) + "\n")


read_recursive(sys.argv[1])