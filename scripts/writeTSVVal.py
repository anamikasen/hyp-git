#!/usr/bin/env python

"""Term frequency extractor for the PAN19 hyperpartisan news detection task"""
# Version: 2018-10-09

# Parameters:
# --inputDataset=<directory>
#   Directory that contains the articles XML file with the articles for which a prediction should be made.
# --outputFile=<file>
#   File to which the term frequency vectors will be written. Will be overwritten if it exists.

# Output is one article per line:
# <article id> <token>:<count> <token>:<count> ...


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

########## OPTIONS HANDLING ##########
def parse_options():
    """Parses the command line options."""
    try:
        long_options = ["inputDataset=", "outputFile=", "typ="]
        opts, _ = getopt.getopt(sys.argv[1:], "d:o:", long_options)
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    inputDataset = "undefined"
    outputFile = "undefined"

    for opt, arg in opts:
        if opt in ("-d", "--inputDataset"):
            inputDataset = arg
        elif opt in ("-o", "--outputFile"):
            outputFile = arg
        elif opt in ("-t", "--typ"):
            typ = arg
        else:
            assert False, "Unknown option."
    if inputDataset == "undefined":
        sys.exit("Input dataset, the directory that contains the articles XML file, is undefined. Use option -d or --inputDataset.")
    elif not os.path.exists(inputDataset):
        sys.exit("The input dataset folder does not exist (%s)." % inputDataset)

    if outputFile == "undefined":
        sys.exit("Output file, the file to which the vectors should be written, is undefined. Use option -o or --outputFile.")

    return (inputDataset, outputFile, typ)

########## ARTICLE HANDLING ##########
def handleArticle(article, outFile):
    termfrequencies = {}

    # get text from article
    text = lxml.etree.tostring(article, method="text", encoding="unicode")
    textcleaned = re.sub('[^a-z ]', '', text.lower())
    # counting tokens
    import pdb; pdb.set_trace()

    tsvFile.write(article.get("id") + "\t" + \
                truthFile[article.get("id")]['labeled-by'] + "\t" + \
                textcleaned + "\t" + \
                truthFile[article.get("id")]['hyperpartisan'] + "\t" + \
                truthFile[article.get("id")]['url'] + "\t" + \
                str(trainFile[article.get("id")]['lengthwords']) + "\n" )

########## SAX FOR STREAM PARSING ##########
class HyperpartisanNewsTFExtractor(xml.sax.ContentHandler):
    def __init__(self, outFile):
        xml.sax.ContentHandler.__init__(self)
        self.outFile = outFile
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
                handleArticle(self.lxmlhandler.etree.getroot(), self.outFile)
                self.lxmlhandler = "undefined"

########## MAIN ##########
def main(inputDataset, outputFile, typ):
    """Main method of this module."""
    start = time.time()

    with open(outputFile, 'w') as outFile:
        for file in os.listdir(inputDataset):
            if file.endswith(".xml"):
                with open(inputDataset + "/" + file) as inputRunFile:
                    xml.sax.parse(inputRunFile, HyperpartisanNewsTFExtractor(outFile))


    print("The vectors have been written to the output file.")

    end = time.time()
    totaltime = end-start

    writeFile = open("/scratch/anamikas/hyp/v2/tsvFileValStats.txt", "w")
    writeFile.write("The time taken to run the script for article words counting and tf-extractor validation dataset " + str(totaltime))
    writeFile.close()

if __name__ == '__main__':
    tsvFile = open('/scratch/anamikas/hyp/v2/tsvFileVal.tab', 'w')
    trainFile = pickle.load(open('/scratch/anamikas/hyp/v2/outputs/validation/byArticle/articletrainbyArticle.p', 'rb'))
    truthFile = pickle.load(open('/scratch/anamikas/hyp/v2/dataset/groundTruth/train/byArticle/groundTruthbyArticle.p', 'rb'))

    main(*parse_options())
