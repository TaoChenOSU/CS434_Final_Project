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
            #print uniqueWords
            dictionary.reduceSignificanceWRTUniqueWords(uniqueWords)
            # TODO: Analyze neighboring words
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
            # TODO: Analyze neighboring words
            neighboringWords = wordConnection(row[3], row[4])
            dictionary.analyzeConnectivity(neighboringWords)

if __name__ == "__main__":
    trainingSet = Data("train.csv")
    myDictionary = Dictionary()
    processedData = trainingSet.getRawData()
    # for row in processedData:
    #     print row
    learn(myDictionary, processedData)

    myDictionary.reduceSignificanceByRatio()
    myDictionary.sort()
    # for row in myDictionary.getDictionary():
    #     print row, myDictionary.getDictionary()[row]
