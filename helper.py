from __future__ import division
# CS434
# Final Project
# Tao Chen

# this is a file that contains helper functions
import string
import math
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
    print 1 - (2/math.pi)*math.atan(x/K)
    return 1 - (2/math.pi)*math.atan(x/K)

# return all pairs of different words in two questions
def createWordPairs(sentence_1, sentence_2):
    pairs = []
    for word_1 in sentence_1:
        for word_2 in sentence_2:
            if word_1 != word_2:
                # To make sure the no such pair or the reverse of the pair has been created
                if pairs.count((word_1, word_2)) == 0 and pairs.count((word_2, word_1)) == 0:
                    pairs.append((word_1, word_2))

    return pairs

# Analyze neighboring words
