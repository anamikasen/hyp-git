import pickle
import pandas as pd
from nltk.corpus import stopwords
stop = stopwords.words('english')
import re
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import time
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np

import os
import getopt
import sys
import xml.sax
import lxml.sax
import lxml.etree
import re
import json
import pickle
import time
import csv
import xml.etree.ElementTree as ET

def parse_options():
    """Parses the command line options."""
    try:
        long_options = ["inputDataset=", "outputFile=", "groundTruth="]
        opts, _ = getopt.getopt(sys.argv[1:], "d:o:", long_options)
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    inputDataset = "undefined"
    outputFile = "undefined"
    groundTruth = "undefined"

    for opt, arg in opts:
        if opt in ("-d", "--inputDataset"):
            inputDataset = arg
        elif opt in ("-o", "--outputFile"):
            outputFile = arg
        elif opt in ("-g", "--groundTruth"):
            groundTruth = arg

        else:
            assert False, "Unknown option."

    if inputDataset == "undefined":
        sys.exit("Input dataset, the directory that contains the articles XML file, is undefined. Use option -d or --inputDataset.")
    elif not os.path.exists(inputDataset):
        sys.exit("The input dataset folder does not exist (%s)." % inputDataset)

    if outputFile == "undefined":
        sys.exit("Output file, the file to which the vectors should be written, is undefined. Use option -o or --outputFile.")

    if groundTruth == "undefined":
        sys.exit("Ground Truth file, the directory that contains the ground Truth XML file, is undefined. Use option -g or --groundTruth.")
    elif not os.path.exists(groundTruth):
        sys.exit("The groundTruthFile does not exist (%s)." % groundTruth)


    return (inputDataset, outputFile, groundTruth)

########## ARTICLE HANDLING ##########
def handleArticle(article, outFile, groundTruth):
    #print(article.get("title"), groundTruth[article.get("id")])

    #print(article.get("id"), article.get("title"), groundTruth[article.get("id")]["hyperpartisan"])
    print(article.get("id"))
    outFile.write(article.get("id") + "\t" +\
                article.get("title") + "\t" + \
                groundTruth[article.get("id")]["hyperpartisan"] + "\n")

########## SAX FOR STREAM PARSING ##########
class HyperpartisanNewsTFExtractor(xml.sax.ContentHandler):
    def __init__(self, outFile, groundTruthFile):
        xml.sax.ContentHandler.__init__(self)
        self.outFile = outFile
        self.groundTruthFile = groundTruthFile
        self.lxmlhandler = "undefined"

    def startElement(self, name, attrs):
        if name != "articles":
            if name == "article":
                self.lxmlhandler = lxml.sax.ElementTreeContentHandler()

            self.lxmlhandler.startElement(name, attrs)

    def characters(self, data):
        if self.lxmlhandler != "undefined":
            self.lxmlhandler.characters(data)

    def endElement(self, name):
        if self.lxmlhandler != "undefined":
            self.lxmlhandler.endElement(name)
            if name == "article":
                # pass to handleArticle function
                handleArticle(self.lxmlhandler.etree.getroot(), self.outFile, self.groundTruthFile)
                self.lxmlhandler = "undefined"



########## MAIN ##########
def main(inputDataset, outputFile, groundTruth):
    """Main method of this module."""
    groundTruthFile = pickle.load(open(groundTruth, "rb"))
    with open(outputFile, 'w') as outFile:
        for file in os.listdir(inputDataset):
            if file.endswith(".xml"):
                with open(inputDataset + "/" + file) as inputRunFile:
                    xml.sax.parse(inputRunFile, HyperpartisanNewsTFExtractor(outFile, groundTruthFile))

    outFile.close()

if __name__ == '__main__':
    main(*parse_options())
