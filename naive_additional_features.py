import os
import sys
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier

#---append each token as a feature to the training set along with the respective label ----#
def word2features(tokens,all_words,root):

    if "positive" in root:
        return (dict([(word, True) for word in tokens]),"positive")
    elif "negative" in root:
        return (dict([(word, True) for word in tokens]), "negative")
    elif "neutral" in root:
        return (dict([(word, True) for word in tokens]), "neutral")
    else:
        return dict([(word, True) for word in tokens])

#----append each token as a feature of the test set
def word2features_test(tokens, all_words):


    return dict([(word, True) for word in tokens])



def main():

    all_words = []

    list_of_tokens_of_each_file=[]
    #---read all files to extract all word lists---#
    for root, directories, filenames in os.walk(sys.argv[1]):

        for each_filename in filenames:
            if each_filename.endswith(".txt"):
                input = open(os.path.join(root, each_filename), "r", encoding="latin1").read()
                tokens = input.split()
                list_of_tokens_of_each_file.append(tokens)
                for each_token in tokens:
                    if each_token not in all_words:
                        all_words.append(each_token)


    test_set_list=[]
    #---- fetch all dev data set ---#
    for root, directories, filenames in os.walk(sys.argv[2]):

        for each_filename in filenames:
            if each_filename.endswith(".txt"):
                test_input = open(os.path.join(root, each_filename), "r", encoding="latin1").read()
                test_tokens = test_input.split()
                test_set_list.append(test_tokens)



    total_list=[]
    X_list=[]

    #--- extract the features for each of the training file ----#
    for root, directories, filenames in os.walk(sys.argv[1]):

        if "positive" in root or "negative" in root or "neutral" in root:
            for i in range(len(filenames)):

                X_list .append(word2features(list_of_tokens_of_each_file[i],all_words,root))


    result_list=[]

    #-- applying naive bayes NLTK classification ---#
    classifier = NaiveBayesClassifier.train(X_list)
    f = open('nboutput.txt', 'w')

    actual_positive=0
    actual_negative=0
    actual_neutral=0
    positive_counter=0
    negative_counter=0
    neutral_counter=0
    classified_positive=0
    classified_negative=0
    classified_neutral=0
    for root, directories, filenames in os.walk(sys.argv[2]):

        print("root  is ", root)
        for i in range(len(filenames)):
            path=root + '/' + filenames[i]
            if "positive" in path:
                actual_positive=actual_positive+1
            elif "negative" in path:
                actual_negative=actual_negative+1
            elif "neutral" in path:
                actual_neutral = actual_neutral + 1


            if "positive" in root or "negative" in root or "neutral" in root:
                result_list.append(word2features_test(test_set_list[i], all_words))

                #--- classify each of the test file to respective category---#
                output=classifier.classify(word2features_test(test_set_list[i], all_words))

                if output=="positive":
                    classified_positive=classified_positive+1
                elif output=="negative":
                    classified_negative=classified_negative+1
                elif output=="neutral":
                    classified_neutral=classified_neutral+1
                f.write(output + " " + root + '/' + filenames[i] + "\n")


    print('accuracy:', nltk.classify.util.accuracy(classifier, X_list))
    # print(sorted(classifier.labels()))
    # classifier.show_most_informative_features()


#--------------------self evaluation --------------------------------#
   #  output = open("nboutput.txt", "r", encoding="latin1").readlines()
   #  for line in output:
   #      line = line.split()
   #
   #      if line[0].lower() in line[1]:
   #          # print("line value is ", line[0].lower())
   #          if line[0].lower() == "positive":
   #              positive_counter = positive_counter + 1
   #          elif line[0].lower() == "negative":
   #              negative_counter = negative_counter + 1
   #          elif line[0].lower() == "neutral":
   #              neutral_counter = neutral_counter + 1
   #
   #
   #  precision_positive= positive_counter/classified_positive
   #  precision_negative =  negative_counter/classified_negative
   #  precision_neutral=neutral_counter/classified_neutral
   #
   #  # REcall = (correctly classified as ck) / (belongs to ck)
   #
   #  recall_positive=positive_counter / actual_positive
   #  recall_negative = negative_counter / actual_negative
   #  recall_neutral=neutral_counter/actual_neutral
   #
   #
   # # F-score calculation
   #
   #  f_score_positive =(2* precision_positive * recall_positive )/ (precision_positive + recall_positive)
   #  f_score_negative = (2 * precision_negative * recall_negative) / (precision_negative + recall_negative)
   #  f_score_neutral = (2 * precision_neutral * recall_neutral) / (precision_neutral + recall_neutral)
   #
   #  print ("precison positive is " ,precision_positive )
   #  print("precison negative is ", precision_negative)
   #  print("precison neutral is ", precision_neutral)
   #  print("recall positive is ", recall_positive)
   #  print("recall negative is ", recall_negative)
   #  print("recall neutral is ", recall_neutral)
   #
   #  print("F score positive is" ,f_score_positive )
   #  print("F score negative is", f_score_negative)
   #  print("F score neutral is", f_score_neutral)
   #
   #  avg_weight = ((f_score_positive + f_score_negative + f_score_neutral) / 3)
   #
   #  print("weighted Avg : ", avg_weight)
   #
#--------------------self evaluation --------------------------------#

if __name__ == "__main__":
    main()