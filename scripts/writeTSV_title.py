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

########## OPTIONS HANDLING ##########
def parse_options():
    """Parses the command line options."""
    try:
        long_options = ["inputDataset=", "outputFile"]
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
        else:
            assert False, "Unknown option."

    if inputDataset == "undefined":
        sys.exit("Input dataset, the directory that contains the articles XML file, is undefined. Use option -d or --inputDataset.")
    elif not os.path.exists(inputDataset):
        sys.exit("The input dataset folder does not exist (%s)." % inputDataset)

    if outputFile == "undefined":
        sys.exit("Output file, the file to which the vectors should be written, is undefined. Use option -o or --outputFile.")

    return (inputDataset, outputFile)


########## ARTICLE HANDLING ##########
def handleArticle(article, tsvFile):

    # get text from article
    text = lxml.etree.tostring(article, method="text", encoding="unicode")
    textcleaned = re.sub('[^a-z ]', '', text.lower())
    # counting tokens

    tsvFile.write(article.get("id") + "\t" + \
                article.get("title") + "\n")

########## SAX FOR STREAM PARSING ##########
class HyperpartisanNewsTFExtractor(xml.sax.ContentHandler):
    def __init__(self, tsvFile):
        xml.sax.ContentHandler.__init__(self)
        self.tsvFile = tsvFile
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
                handleArticle(self.lxmlhandler.etree.getroot(), self.tsvFile)
                self.lxmlhandler = "undefined"


########## MAIN ##########
def main(inputDataset, outputFile):
    """Main method of this module."""
    start = time.time()
    groundTruthDict = {}
    groundTruthDict[0] = "false"
    groundTruthDict[1] = "true"
    currDir = os.getcwd()
    tsvFile = os.path.join(currDir, "tsvFile.tsv")
    with open(tsvFile, 'w') as tsvfile:
        for file in os.listdir(inputDataset):
            if file.endswith(".xml"):
                with open(inputDataset + "/" + file) as inputRunFile:
                    xml.sax.parse(inputRunFile, HyperpartisanNewsTFExtractor(tsvfile))



    print("Written to TSV format")

    with open(tsvFile, 'r') as tsvfile:

        titleFileDF = pd.read_csv(tsvFile, sep="\t", names=['id', 'title'], converters={'id': lambda x: str(x)})
        titleFileDF['title_new'] = titleFileDF['title'].fillna("")
        titleFileDF['lower_title'] = titleFileDF['title'].str.replace('[^\w\s]','')
        titleFileDF['lower_title'] = titleFileDF['lower_title'].fillna("")
        titleFileDF['withoutNumbers'] = titleFileDF['lower_title'].str.replace('\d+', '')
        titleFileDF['lowerprep'] = titleFileDF['withoutNumbers'].apply(lambda x: " ".join(x.lower() for x in x.split()))
        lemma = WordNetLemmatizer()
        titleFileDF['lemma'] = titleFileDF['lowerprep'].apply(lambda x: " ".join([lemma.lemmatize(word) for word in x.split()]))

        tfv = pickle.load(open(vectorizer, 'rb'))

        loaded_model = pickle.load(open(modelname, 'rb'))

        train_tfv = tfv.transform(titleFileDF.lemma)

        predictions = loaded_model.predict(train_tfv)

        with open(os.path.join(outputFile, "result.txt"), "w") as outFile:
            for i, items in enumerate(titleFileDF["id"]):
                outFile.write(str(items) + " " + \
                            str(groundTruthDict[predictions[i]]) + "\n")

        end = time.time()
        totaltime = end-start

        print(totaltime)

if __name__ == '__main__':

    modelname = "/scratch/anamikas/hyp/postVac/finalized_model.sav"
    vectorizer = "/scratch/anamikas/hyp/postVac/results/vectorizer.pk"

    #filename = "/home/murphy-brown/work/finalized_model.sav"
    main(*parse_options())
