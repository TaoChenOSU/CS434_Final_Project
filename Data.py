from __future__ import division
# CS434
# Final Project
# Tao Chen
# this is the file that contains the Data class and all its methods
import csv
from helper import wordsToLists
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

        limit = 10000
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
