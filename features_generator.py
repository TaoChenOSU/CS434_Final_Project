from __future__ import division

import math

def differenceInNumOfWord(sentence_1, sentence_2):
    return math.fabs(len(sentence_1)-len(sentence_2))

# word ratio
def wordRatio(words, totalWords):
    wordCount = 0
    for word in words:
        wordCount += word[1]

    return wordCount/totalWords

# significance ratio
def significanceRatio(sameSignificance, uniqueSignificance):
    if uniqueSignificance == 0:
        return float('inf')
    else:
        return sameSignificance/uniqueSignificance

# ratio between unique words and same words
def sameOverUnique(same, unique):
    sameCount = 0
    uniqueCount = 0
    for word in same:
        sameCount += word[1]
    for word in unique:
        uniqueCount += word[1]

    if uniqueCount == 0:
        return float('inf')
    else:
        return sameCount/uniqueCount

# return the sum of significance of all the same words
# and the sum of significance of all the unique words
def calSignificance(sameWords, uniqueWords, dictionary):
    sumOfSameWords = dictionary.sumOfSignificance(sameWords)
    if len(uniqueWords) >= 2:
        additionalSignificance, uniqueWords = uniqueWordAnalizer(uniqueWords, dictionary.getDictionary())
        sumOfSameWords += additionalSignificance
    sumOfUniqueWords = dictionary.sumOfSignificance(uniqueWords)

    return sumOfSameWords, sumOfUniqueWords


# if two or multiple unique words are actually similar words
# average their significance and add the result to the sumOfSameWords
# I only look for one-level of similarity
def uniqueWordAnalizer(uniqueWords, dictionary):
    significance = 0
    entry = uniqueWords[0]
    quit = False
    while entry != uniqueWords[len(uniqueWords)-1]:
        length = len(uniqueWords)
        found = False
        index = uniqueWords.index(entry)
        for i in range(length-index-1):
            #  found one similar word
            # print len(uniqueWords), index, i
            if dictionary.has_key(entry[0]):
                if dictionary[entry[0]][2].has_key(uniqueWords[index+i+1][0]):
                    word_1_significance = dictionary[entry[0]][0] * entry[1]
                    word_2_significance = dictionary[uniqueWords[index+i+1][0]][0] * uniqueWords[index+i+1][1]
                    totalAppearance = entry[1] + uniqueWords[index+i+1][1]
                    significance += 0.8 * (word_1_significance + word_1_significance)/totalAppearance
                    uniqueWords.pop(index)
                    uniqueWords.pop(index+i)
                    found = True
                    if len(uniqueWords) >= 2:
                        if index < len(uniqueWords):
                            entry = uniqueWords[index]
                        else:
                            entry = uniqueWords[len(uniqueWords)-1]
                        break
                    else:
                        quit = True
                        break
        # exit the for loop meaning no similar words are found
        if not found:
            entry = uniqueWords[index+1]
        if len(uniqueWords) < 2 or quit == True:
            break

    return significance, uniqueWords
