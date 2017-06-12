from __future__ import division
# CS434
# Final Project
# Tao Chen
# this is the file that contains the Data class and all its methods
import csv
from helper import wordsToLists
from features_generator import differenceInNumOfWord
from features_generator import wordRatio
from features_generator import sameOverUnique
from features_generator import calSignificance
from features_generator import significanceRatio
from helper import lookForSameWords
from helper import lookForUniqueWords

# A class that refers to the pre-processed raw data
class Data:
    def __init__(self, fileName, limit):
        self.__readFile(fileName, limit)
        self.__toLowerCase()
        self.__toLists()

    def __readFile(self, fileName, limit):
        openFile = open(fileName, 'r')
        readCSV = csv.reader(openFile, delimiter=',')
        self.__rawData = []

        currentAmount = 0
        for row in readCSV:
            if currentAmount > limit:
                break
            self.__rawData.append(row)
            currentAmount = currentAmount + 1

        # remove the headings
        self.__rawData.pop(0)
        # convert ids and labels to numbers instead of strings
        for row in self.__rawData:
            row[0] = int(row[0])
            row[1] = int(row[1])
            row[2] = int(row[2])
            row[5] = int(row[5])

    # convert all letters to lower case
    def __toLowerCase(self):
        for row in self.__rawData:
            row[3] = row[3].lower()
            row[4] = row[4].lower()

    # make the questions into lists of words while
    # removing punctuations
    def __toLists(self):
        for row in self.__rawData:
            row[3] = wordsToLists(row[3])
            row[4] = wordsToLists(row[4])

    def getRawData(self):
        return self.__rawData

    def generateFeatures(self, dictionary):
        featureTable = []
        index = 0
        for row in self.__rawData:
            featureTable.append([])
            # label
            featureTable[index].append(row[5])
            # first feature: difference in number of words
            featureTable[index].append(differenceInNumOfWord(row[3], row[4]))

            sameWords = lookForSameWords(row[3], row[4])
            uniqueWords = lookForUniqueWords(row[3], row[4], sameWords)
            totalWords = len(row[3]) + len(row[4])
            # second feature: ratio between number of same words and
            # total number of words in the two sentences
            featureTable[index].append(wordRatio(sameWords, totalWords))
            # third feature: ratio between number of unique words and
            # total number of words in the two sentences
            featureTable[index].append(wordRatio(uniqueWords, totalWords))
            # forth feature: ratio between # of same word and # of unique words
            featureTable[index].append(sameOverUnique(sameWords, uniqueWords))
            # fith feature: sum of the significance of all the same words over
            # total significance of the pair
            # sixth feature: sum of the significance of all the unique words over
            # total significance of the pair
            fifthFeature, sixthFeature = calSignificance(sameWords, uniqueWords, dictionary)
            featureTable[index].append(fifthFeature)
            featureTable[index].append(sixthFeature)
            # seventh feature: ration in same-word and unique-word significance
            featureTable[index].append(significanceRatio(fifthFeature, sixthFeature))
            # increment index
            index += 1
        return featureTable
