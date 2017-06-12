from __future__ import division

# this is the testing module.
# Read the data first, the same training dataset as
# the training module did because the testing data
# from Kaggle doesn't have labels
# Step 1: filter data
# Step 2:
# For each pair of questiions:
#   find duplicate words and unique words
# sum up the significance of those words
# if the sum of duplicate words is bigger than the
# sum of unique words, duplicate questions, otherwise
# non-duplicate

from Data import Data
from helper import lookForSameWords
from helper import lookForUniqueWords
from helper import wordConnection

class Test:
    def __init__(self, fileName, limit):
        self.__testingSet = Data(fileName, limit)
        self.__processedData = self.__testingSet.getRawData()

    def __test(self, dictionary):
        correct = 0
        incorrect = 0
        for pair in self.__processedData:
            sameWords = lookForSameWords(pair[3], pair[4])
            uniqueWords = lookForUniqueWords(pair[3], pair[4], sameWords)

            sumOfSameWords = self.__findSumOfSameWords(sameWords, dictionary)
            # sumOfUniqueWords = self.__findSumOfUniqueWords(uniqueWords, dictionary)
            # find out if some of the unique words are actually similar words
            if len(uniqueWords) >= 2:
                additionalSignificance, uniqueWords = self.__uniqueWordAnalizer(uniqueWords, dictionary)
                sumOfSameWords += additionalSignificance
            sumOfUniqueWords = self.__findSumOfUniqueWords(uniqueWords, dictionary)
        #
        #     if sumOfUniqueWords < sumOfSameWords:
        #         if pair[5] == 1:
        #             correct += 1
        #         else:
        #             incorrect += 1
        #     else:
        #         if pair[5] == 1:
        #             incorrect += 1
        #         else:
        #             correct += 1
        #
        # return correct, incorrect

    # sum up their significance
    def __findSumOfSameWords(self, sameWords, dictionary):
        significance = 0
        for item in sameWords:
            # signifiance times the # of appearance
            # words that're not in the dictionary have signifiance of 0
            if dictionary.has_key(item[0]):
                significance += dictionary[item[0]][0] * item[1]

        return significance

    # if two or multiple unique words are actually similar words
    # average their significance and add the result to the sumOfSameWords
    # I only look for one-level of similarity
    def __uniqueWordAnalizer(self, uniqueWords, dictionary):
        significance = 0
        entry = uniqueWords[0]
        quit = False
        while entry != uniqueWords[len(uniqueWords)-1]:
            length = len(uniqueWords)
            found = False
            index = uniqueWords.index(entry)
            for i in range(length-index-1):
                #  found one similar word
                # print len(uniqueWords), index, i
                if dictionary.has_key(entry[0]):
                    if dictionary[entry[0]][2].has_key(uniqueWords[index+i+1][0]):
                        word_1_significance = dictionary[entry[0]][0] * entry[1]
                        word_2_significance = dictionary[uniqueWords[index+i+1][0]][0] * uniqueWords[index+i+1][1]
                        totalAppearance = entry[1] + uniqueWords[index+i+1][1]
                        significance += 0.8 * (word_1_significance + word_1_significance)/totalAppearance
                        uniqueWords.pop(index)
                        uniqueWords.pop(index+i)
                        found = True
                        if len(uniqueWords) >= 2:
                            if index < len(uniqueWords):
                                entry = uniqueWords[index]
                            else:
                                entry = uniqueWords[len(uniqueWords)-1]
                            break
                        else:
                            quit = True
                            break
            # exit the for loop meaning no similar words are found
            if not found:
                entry = uniqueWords[index+1]
            if len(uniqueWords) < 2 or quit == True:
                break

        return significance, uniqueWords

    # sum up their significance
    def __findSumOfUniqueWords(self, uniqueWords, dictionary):
        significance = 0
        for item in uniqueWords:
            # signifiance times the # of appearance
            # words that're not in the dictionary have signifiance of 0
            if dictionary.has_key(item[0]):
                significance += dictionary[item[0]][0] * item[1]

        return significance

    def getResult(self, dictionary):
        correct, incorrect = self.__test(dictionary)
        print correct, incorrect
        return incorrect/(correct + incorrect)
