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
            if sameWords.count(word) == 0:
                sameWords.append(word)
    return sameWords

# return a list of words that only appear in one of the sentences
def lookForUniqueWords(sentence_1, sentence_2, sameWords):
    uniqueWords = []
    for word in sentence_1:
        if uniqueWords.count(word) == 0:
            uniqueWords.append(word)
    for word in sentence_2:
        if uniqueWords.count(word) == 0:
            uniqueWords.append(word)
    for word in sameWords:
        uniqueWords.remove(word)

    return uniqueWords

# A class that refers to the pre-processed raw data
class Data:
    def __init__(self, fileName):
        self.__readFile(fileName)
        self.__toLowerCase()
        self.__toLists()

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
            print "Repeat words"

    def __wordExist(self, word):
        for entry in self.__dictionary:
            if entry[0] == word:
                # increment the word count
                entry[2] = entry[2] + 1
                return True
        return False

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
            print sameWords
            # TODO: increase the significance of all the same words
            uniqueWords = lookForUniqueWords(row[3], row[4], sameWords)
            print uniqueWords
            # TODO: decrease the significance of all the different words
        else:   # the two questions are non-duplicate
            # look for words that are in both questions
            sameWords = lookForSameWords(row[3], row[4])
            print sameWords
            # TODO: decrease th significance of all the same words
            uniqueWords = lookForUniqueWords(row[3], row[4], sameWords)
            print uniqueWords
            # TODO: increase the significance of all the different words

if __name__ == "__main__":
    trainingSet = Data("train.csv")
    myDictionary = Dictionary()
    processedData = trainingSet.getRawData()
    for row in processedData:
        print row
    learn(myDictionary, processedData)

    # for row in myDictionary.getDictionary():
    #     print row
