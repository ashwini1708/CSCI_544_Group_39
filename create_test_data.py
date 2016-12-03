import json
from itertools import islice
import io
import os, glob

reviewRecord = []

jenc = json.JSONEncoder();


with open("yelp_academic_dataset_review.json", "r", encoding="latin1") as inputFile:
    slicedFile = islice(inputFile, 675000, 900000)

    for line in slicedFile:
        reviewRecord.append(json.loads(line))

    file_counter = 0

    positive_counter = 0
    negative_counter = 0
    neutral_counter = 0

    filelist = glob.glob("*.txt")
    for f in filelist:
        os.remove(f)


    for each_review in reviewRecord:

        stars = each_review['stars']

        if (stars > 3):
            with io.open("positive_test/file_positive_" + str(file_counter) + ".txt", 'w',
                         encoding='utf-8') as positive_file:
                positive_file.write(str(each_review['text']))
                positive_counter = positive_counter + 1

                file_counter = file_counter + 1


        elif (stars < 3):

            with io.open("negative_test/file_negative_" + str(file_counter) + ".txt", 'w',
                         encoding='utf-8') as negative_file:
                negative_file.write(str(each_review['text']))
                negative_counter = negative_counter + 1
                file_counter = file_counter + 1


        else:

            with io.open("neutral_test/file_neutral_" + str(file_counter) + ".txt", 'w',
                         encoding='utf-8') as neutral_file:
                neutral_file.write(str(each_review['text']))
                neutral_counter = neutral_counter + 1
                file_counter = file_counter + 1




    print("positive counter is ", positive_counter)
    print("negative counter is ", negative_counter)
    print("neutral counter is ", neutral_counter)
