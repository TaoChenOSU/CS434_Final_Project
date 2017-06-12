from __future__ import division
# CS434
# Final Project
# Tao Chen

# this is a file that contains helper functions
import string
import math
import numpy as np
# return a list of words with punctuations removed
def wordsToLists(sentence):
    return list(sentence.translate(None, string.punctuation).split())

# return a list of words with # of appearance
# that are in both sentences
def lookForSameWords(sentence_1, sentence_2):
    sameWords = []
    sameWordsAssocArray = dict([])
    for word in sentence_1:
        appearance = sentence_2.count(word)
        if appearance != 0:
            # add the word if it hasn't been added
            if sameWords.count(word) == 0:
                sameWords.append(word)
                sameWordsAssocArray[word] = appearance + 1
            else:
                sameWordsAssocArray[word] += 1

    sameWords = []
    for item in sameWordsAssocArray:
        sameWords.append([item, sameWordsAssocArray[item]])

    return sameWords

# return a list of words that only appear in one of the sentences
# and # of times they appear
def lookForUniqueWords(sentence_1, sentence_2, sameWords):
    allWords = []
    uniqueWords = []
    uniqueWordsAssocArray = dict([])
    # add all words in sentence 1
    for word in sentence_1:
        if allWords.count(word) == 0:
            allWords.append(word)
            uniqueWordsAssocArray[word] = 1
        else:
            uniqueWordsAssocArray[word] += 1
    # add all words in sentence 2
    for word in sentence_2:
        if allWords.count(word) == 0:
            allWords.append(word)
            uniqueWordsAssocArray[word] = 1
        else:
            uniqueWordsAssocArray[word] += 1
    # remove all the same words
    for word in sameWords:
        allWords.remove(word[0])
    # add all unique words and their # of appearance to the array
    for word in allWords:
        uniqueWords.append([word, uniqueWordsAssocArray[word]])

    return uniqueWords

# return the amount of significance to be reduced or
# increased
# K must be bigger that 2
# when K is super close to 2, the amount of
# significance to be reduced/increased will be huge
def myTan(x, K):
    return math.tan((math.pi*x)/K)

# return the new significance of a word after it appears
# again.
# If a word reappears all the time, its siginifance should
# suffer.
# K is a parameter that control how must the significance should suffer
# when a word appears again
# The bigger k gets, the less it will suffer
# K > 0
def myArcTan(x, K):
    # print 1 - (2/math.pi)*math.atan(x/K)
    return 1 - (2/math.pi)*math.atan(x/K)

# return all pairs of different words in two questions
# also record the positions of both words in the sentences
def createWordPairs(sentence_1, sentence_2):
    pairs = []
    pairsWithPositions = []
    word_1_pos = 0
    for word_1 in sentence_1:
        word_2_pos = 0
        for word_2 in sentence_2:
            if word_1 != word_2:
                # To make sure the no such pair or the reverse of the pair has been created
                # if pairs.count([word_1, word_2]) == 0 and pairs.count([word_2, word_1]) == 0:
                # if pairs.count([word_1, word_2]) == 0:
                pairs.append([word_1, word_2])
                pairsWithPositions.append([word_1, word_2, [[word_1_pos, word_2_pos]]])
                # elif pairs.count([word_1, word_2]) == 0 and pairs.count([word_2, word_1]) != 0:
                #     index = pairs.index([word_2, word_1])
                #     pairsWithPositions[index][2].append([word_1_pos, word_2_pos])
                # else:
                #     index = pairs.index([word_1, word_2])
                #     pairsWithPositions[index][2].append([word_1_pos, word_2_pos])
            word_2_pos += 1
        word_1_pos += 1

    return pairsWithPositions

# find neighboring words
def wordConnection(sentence_1, sentence_2):
    # default k to be 1, meaning the function is going
    # to analyze the two neighboring words on each side
    # For now, k is fixed at 1 to avoid more complex programming
    # and k = 1 makes finding connectivity more easily
    # if you change k to any number other than 1, the program
    # will crash
    k = 1
    # the original pair plus the neighboring words
    connections = []
    wordPairs = createWordPairs(sentence_1, sentence_2)
    # find neighboring words
    # if there's less than 2 neighboring words, work with however
    # many there is.
    sentence_1_len = len(sentence_1)
    sentence_2_len = len(sentence_2)

    for pair in wordPairs:
        # [[words in sentence_1], [words in sentence_2]]
        left = []
        right = []
        for position in pair[2]:
            # left side, both words have at least k words on their left sides
            if position[0]-k >= 0 and position[1]-k >= 0:
                for i in range(k):
                    left.append([sentence_1[position[0]-1-i], sentence_2[position[1]-1-i]])
            # left side, one or both of the sides has less than k words
            elif position[0]-k < 0 or position[1]-k < 0:
                if position[0] <= position[1]:
                    for i in range(position[0]):
                        left.append([sentence_1[position[0]-1-i], sentence_2[position[1]-1-i]])
                else:
                    for i in range(position[1]):
                        left.append([sentence_1[position[0]-1-i], sentence_2[position[1]-1-i]])

            # right side, both words have at least k words on their right sides
            if position[0]+k < sentence_1_len and position[1]+k < sentence_2_len:
                for i in range(k):
                    right.append([sentence_1[position[0]+1+i], sentence_2[position[1]+1+i]])
            # right side, one of the sides has less than k words
            elif position[0]+k >= sentence_1_len or position[1]+k >= sentence_2_len:
                if sentence_1_len-position[0] >= sentence_2_len-position[1]:
                    for i in range(sentence_2_len-position[1]-1):
                        right.append([sentence_1[position[0]+1+i], sentence_2[position[1]+1+i]])
                else:
                    for i in range(sentence_1_len-position[0]-1):
                        right.append([sentence_1[position[0]+1+i], sentence_2[position[1]+1+i]])

        connections.append([pair[0], pair[1], list(left), list(right)])

    # for item in connections:
    #     print item
    return connections

# sum up their significance
def sumOfSignificance(words, dictionary):
    significance = 0
    for item in words:
        # signifiance times the # of appearance
        significance += dictionary[item[0]][0] * item[1]

    return significance
