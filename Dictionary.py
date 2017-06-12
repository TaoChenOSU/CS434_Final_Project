from __future__ import division
# CS434
# Final Project
# Tao Chen
import math
import random
import numpy as np
import helper
from helper import lookForSameWords
from helper import lookForUniqueWords
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
                    self.__addConnection(item[0], item[1])

    # create connection/increase similarity between words
    def __addConnection(self, entry, word):
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
        self.__sortedDictionary = sorted(self.__dictionary.iteritems(), key=lambda (k, v): (v[0], k))

    def getSortedDictionary(self):
        return self.__sortedDictionary
    # normalize the siginifance such that the the ranking of the words
    # in the dictionary is maintained while adjusting the significance
    # to maximize the significance difference for unique words and same words
    def normailizeSignificance(self, data):
        for pair in data:
            sameWords = lookForSameWords(pair[3], pair[4])
            uniqueWords = lookForUniqueWords(pair[3], pair[4], sameWords)

            sumOfSameWords = helper.sumOfSignificance(sameWords, self.getDictionary())
            sumOfUniqueWords = helper.sumOfSignificance(uniqueWords, self.getDictionary())

            if pair[5] == 1:
                if sumOfUniqueWords > sumOfSameWords:
                    # wrong because if the pair is duplicate, same words should
                    # have a greater sum of significance that unique words
                    # TODO: try to make sumOfSameWords > sumOfUniqueWords
                    # print pair[3]
                    # print pair[4]
                    # print sameWords, sumOfSameWords, sumOfUniqueWords
                    self.__adjust(sameWords, uniqueWords)
            else:
                if sumOfUniqueWords < sumOfSameWords:
                    # wrong because if the pair is non-duplicate, same words should
                    # have a smaller sum of significance that unique words
                    # TODO: try to make sumOfUniqueWords > sumOfSameWords
                    # print pair[3]
                    # print pair[4]
                    # print uniqueWords, sumOfSameWords, sumOfUniqueWords
                    self.__adjust(uniqueWords, sameWords)

    # try to maximize (toBeIncreased - toBeDecreased)
    def __adjust(self, toBeIncreased, toBeDecreased):
        itemizeDictionary = self.getSortedDictionary()
        # find the lower bound and upper bound
        # these two dictionaries are useless
        # declare them just in case I need them in the future
        rangeOfAllowanceForToBeIncreased = dict()
        rangeOfAllowanceForToBeDecreased = dict()

        # find the range between which the significance of the word is in
        for word in toBeIncreased:
            entry = self.__dictionary[word[0]]
            # index is the ranking of the word in the dictionary
            index = itemizeDictionary.index((word[0], entry))
            if index > 0 and index < len(itemizeDictionary) - 1:
                rangeOfAllowanceForToBeIncreased[word[0]] = (itemizeDictionary[index-1][1][0], itemizeDictionary[index+1][1][0])
            elif index == 0:
                rangeOfAllowanceForToBeIncreased[word[0]] = (-float('inf'), itemizeDictionary[index+1][1][0])
            else:
                rangeOfAllowanceForToBeIncreased[word[0]] = (itemizeDictionary[index-1][1][0], float('inf'))

            # new significance
            if rangeOfAllowanceForToBeIncreased[word[0]][1] == float('inf'):
                # increase by 10%
                newSignificance = self.__dictionary[word[0]][0] * 1.1
            else:
                # half point between upper bound and itself
                newSignificance = (rangeOfAllowanceForToBeIncreased[word[0]][1] + self.__dictionary[word[0]][0])/2
            self.__dictionary[word[0]][0] = newSignificance

        for word in toBeDecreased:
            entry = self.__dictionary[word[0]]
            # index is the ranking of the word in the dictionary
            index = itemizeDictionary.index((word[0], entry))
            if index > 0 and index < len(itemizeDictionary) - 1:
                rangeOfAllowanceForToBeDecreased[word[0]] = (itemizeDictionary[index-1][1][0], itemizeDictionary[index+1][1][0])
            elif index == 0:
                rangeOfAllowanceForToBeDecreased[word[0]] = (-float('inf'), itemizeDictionary[index+1][1][0])
            else:
                rangeOfAllowanceForToBeDecreased[word[0]] = (itemizeDictionary[index-1][1][0], float('inf'))

            # new significance
            if rangeOfAllowanceForToBeDecreased[word[0]][1] == -float('inf'):
                # decrease by 10%
                newSignificance = self.__dictionary[word[0]][0] * 0.9
            else:
                # half point between upper bound and itself
                newSignificance = (rangeOfAllowanceForToBeDecreased[word[0]][0] + self.__dictionary[word[0]][0])/2
            self.__dictionary[word[0]][0] = newSignificance


    # sum up the incoming words significance
    def sumOfSignificance(self, words):
        significance = 0
        for item in words:
            # signifiance times the # of appearance
            # words that're not in the dictionary have signifiance of 0
            if self.__dictionary.has_key(item[0]):
                significance += self.__dictionary[item[0]][0] * item[1]

        return significance
