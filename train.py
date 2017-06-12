from __future__ import division
# CS434
# Final Project
# Tao Chen

import math
import random
import numpy as np
import csv
import string
from Data import Data
from Dictionary import Dictionary
from helper import lookForSameWords
from helper import lookForUniqueWords
from helper import wordConnection
from Test import Test

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
            #print sameWords
            dictionary.increaseSignificanceWRTSameWords(sameWords)
            uniqueWords = lookForUniqueWords(row[3], row[4], sameWords)
            # print uniqueWords
            dictionary.reduceSignificanceWRTUniqueWords(uniqueWords)
            # Analyze neighboring words
            neighboringWords = wordConnection(row[3], row[4])
            dictionary.analyzeConnectivity(neighboringWords)
        else:   # the two questions are non-duplicate
            # look for words that are in both questions
            sameWords = lookForSameWords(row[3], row[4])
            # print sameWords
            dictionary.reduceSignificanceWRTSameWords(sameWords)
            uniqueWords = lookForUniqueWords(row[3], row[4], sameWords)
            # print uniqueWords
            dictionary.increaseSignificanceWRTUniqueWords(uniqueWords)
            # Analyze neighboring words
            neighboringWords = wordConnection(row[3], row[4])
            dictionary.analyzeConnectivity(neighboringWords)

if __name__ == "__main__":
    # create objects
    trainingSet = Data("train.csv", 20000)
    myDictionary = Dictionary()
    # filter data
    processedData = trainingSet.getRawData()
    # start learning using the processed data
    learn(myDictionary, processedData)
    # have to reduce the significance based on ratio
    # could potentially rearrange some of the words
    myDictionary.reduceSignificanceByRatio()
    # normalize the siginifance such that the the ranking of the words
    # in the dictionary is maintained while adjusting the significance
    # to maximize the significance difference
    myDictionary.sort()
    # adjust the significance multiple times
    for i in range(20):
        myDictionary.normailizeSignificance(processedData)
    # print myDictionary.getSortedDictionary()

    # start testing
    test = Test("train.csv", 1000)
    result = test.getResult(myDictionary.getDictionary())
    print "Error Rate: ", result
