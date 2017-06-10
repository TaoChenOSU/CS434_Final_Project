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
            self.__dictionary[word] = [0, 1, dict()]    # positive connectivity, negative connectivity

    # after the entire dictionary has been generated,
    # reduce the significance of all the words according to
    # the # of appearance and total words ratio
    def reduceSignificanceByRatio(self):
        for key, value in self.__dictionary.iteritems():
            ratio = self.__dictionary[key][1]/self.__numOfAllWords
            self.__dictionary[key][0] *= helper.myArcTan(ratio, 0.1)


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

    # analyze connectivity and generates poistive/negative connectivity accordingly
    def analyzeConnectivity(self, pairs):
        for item in pairs:
            if item[2] != [] and item[3] != []:
                if item[2][0][0] == item[2][0][1] and item[3][0][0] == item[3][0][1]:
                    # this pair might be related to each other either positively or negatively
                    self._addConnection(item[0], item[1])

    # create connection/increase similarity between words
    def _addConnection(self, entry, word):
        # if the connection doesn't exist, create the connection
        if not self.__dictionary[entry][2].has_key(word):
            self.__dictionary[entry][2][word] = 1
            self.__dictionary[word][2][entry] = 1
        else:
            self.__dictionary[entry][2][word] += 1
            self.__dictionary[word][2][entry] += 1

    def getDictionary(self):
        return self.__dictionary

    def sort(self):
        for key, value in sorted(self.__dictionary.iteritems(), key=lambda (k, v): (v[0], k)):
            print key, value
