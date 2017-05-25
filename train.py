from __future__ import division
# CS434
# Final Project
# Tao Chen

import math
import random
import numpy as np
import csv
import string

# return a list of words with punctuations removed
def wordsToLists(sentence):
    return list(sentence.translate(None, string.punctuation).split())

# return a list of words that are in both sentences
def lookForSameWords(sentence_1, sentence_2):
    sameWords = []
    for word in sentence_1:
        appearance = sentence_2.count(word)
        if appearance != 0:
            # add the word if it hasn't been added

# A class that refers to the pre-processed raw data
class Data:
    def __init__(self, fileName):
        self.__readFile(fileName)
        self.__toLowerCase()
        self.__toLists()
        # initialize the dictionary
        self.__dictionary = []

    def __readFile(self, fileName):
        openFile = open(fileName, 'r')
        readCSV = csv.reader(openFile, delimiter=',')
        self.__rawData = []

        limit = 10
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

# A class that refers to the dictionary
class Dictionary:
    def __init__(self):
        self.__dictionary = []

    def addWords(self, word):
        if self.__wordExist(word) == False:
            self.__dictionary.append([word, 0.5, 1, ()])
        else:
            # reduce the significance of the word
            self.__incrementCount(word)
            print "Repeat words"

    def __wordExist(self, word):
        for entry in self.__dictionary:
            if entry[0] == word:
                return True
        return False

    def __incrementCount(self, word):


    def getDictionary(self):
        return self.__dictionary

# start analyzing the data and updating the dictionary
def learn(dictionary, data):
    # insert words to the dictionary
    for row in data:
        # Add words that are in the two questions to the dictionary
        for word in row[3]:
            dictionary.addWords(word)
        for word in row[4]:
            dictionary.addWords(word)

        # The two questions are duplicate
        if row[5] == 1:
            # look for words that are in both questions
            sameWords = lookForSameWords(row[3], row[4])


if __name__ == "__main__":
    trainingSet = Data("train.csv")
    myDictionary = Dictionary()
    processedData = trainingSet.getRawData()
    learn(myDictionary, processedData)

    for row in myDictionary.getDictionary():
        print row
