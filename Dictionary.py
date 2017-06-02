from __future__ import division
# CS434
# Final Project
# Tao Chen
import math
import random
import numpy as np
import helper
# this file contains the Dictionary class and all its methods

# A class that refers to the dictionary
class Dictionary:
    def __init__(self):
        self.__dictionary = dict()
        self.__numOfAllWords = 0

    # the addWords function will convert all words
    # from plural to singlular form if they are plural
    def addWords(self, word):
        self.__numOfAllWords += 1
        if self.__wordExist(word) == False:
            self.__dictionary[word] = [0, 1, []]
        else:
            # reduce the significance of the word based on
            # # of appearances / total # of words in all sentences
            ratio = self.__dictionary[word][1]/self.__numOfAllWords
            self.__dictionary[word][0] *= helper.myArcTan(ratio, 0.1)

    def __wordExist(self, word):
        if self.__dictionary.has_key(word) == True:
            # increment the word count
            self.__dictionary[word][1] += 1
            return True
        return False

    def increaseSignificanceWRTSameWords(self, words):
        totalWords = len(words)
        for word in words:
            ratio = word[1]/totalWords
            self.__dictionary[word[0]][0] += helper.myTan(ratio, 2.3)

    def reduceSignificanceWRTUniqueWords(self, words):
        totalWords = len(words)
        for word in words:
            ratio = word[1]/totalWords
            self.__dictionary[word[0]][0] -= helper.myTan(ratio, 2.3)

    def increaseSignificanceWRTUniqueWords(self, words):
        totalWords = len(words)
        for word in words:
            ratio = word[1]/totalWords
            self.__dictionary[word[0]][0] += helper.myTan(ratio, 2.3)

    def reduceSignificanceWRTSameWords(self, words):
        totalWords = len(words)
        for word in words:
            ratio = word[1]/totalWords
            self.__dictionary[word[0]][0] -= helper.myTan(ratio, 2.3)

    def getDictionary(self):
        return self.__dictionary

    def sort(self):
        for key, value in sorted(self.__dictionary.iteritems(), key=lambda (k, v): (v[0], k)):
            print key, value
