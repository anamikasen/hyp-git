import sys
import json
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from Bio import SeqIO
import json
from sklearn.feature_extraction.text import CountVectorizer
from toolz import partition_all
from joblib import Parallel, delayed
from nltk.corpus import stopwords
import pickle
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
from collections import Counter
import glob
from sklearn.utils import shuffle
import sys
from sklearn.decomposition import NMF, PCA
from sklearn.preprocessing import StandardScaler
import nltk
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib
import glob
import time
import string
from nltk.corpus import stopwords
stoplist = set(stopwords.words("english"))
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
from nltk import ngrams
from nltk.classify import NaiveBayesClassifier
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


lmtzr = WordNetLemmatizer()

trueFile = pickle.load(open("/scratch/anamikas/hyp/postVac/jan30/textOfArticles/trueText.pickle", "rb"))
falseFile = pickle.load(open("/scratch/anamikas/hyp/postVac/jan30/textOfArticles/falseText.pickle", "rb"))

stoplist = set(stopwords.words("english"))

def create_ngram_features_processed(words, mutuallist, rare10, n=2):
    #strip useless end punctuations
    useful_words = [word[:-1] for word in words.split(" ") if word.endswith(".") or word.endswith(";") or word.endswith(":") or word.endswith(",")]
    #string punctuations
    useful_words = [word for word in useful_words if word not in string.punctuation]
    #strip useless charaters
    useful_words = [word.strip('\n') for word in useful_words]
    #remove stop words
    useful_words = [word.lower() for word in useful_words if word not in stoplist]
    #lemmatize
    useful_words = [lmtzr.lemmatize(word) for word in useful_words]
    #remove most occurring mutual words from 50 most common
    useful_words = [word for word in useful_words if word not in mutuallist]
    #remove rare 10% words
    useful_words = [word for word in useful_words if word not in rare10]
    concatstring = " "
    concatstring = " ".join(word for word in useful_words)
    ngram_vocab = ngrams(useful_words, n)
    my_dict = dict([(ng, True) for ng in ngram_vocab])
    return my_dict

def create_word_features(words):
    #strip useless end punctuations
    useful_words = [word[:-1] for word in words if word.endswith(".") or word.endswith(";") or word.endswith(":") or word.endswith(",")]
    #string punctuations
    useful_words = [word for word in useful_words if word not in string.punctuation]
    #strip useless charaters
    useful_words = [word.strip('\n') for word in useful_words]
    #remove stop words
    useful_words = [word.lower() for word in useful_words if word not in stoplist]
    #lemmatize
    useful_words = [lmtzr.lemmatize(word) for word in useful_words]
    #make features
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict

if __name__ == "__main__":
    start = time.time()
    true_data = []
    print("load true class")
    for k, v in trueFile.items():
        words = v.split(" ")
        true_data.append((create_word_features(words), "positive"))

    print("Load false class")
    false_data = []
    for k, v in falseFile.items():
        words = v.split(" ")
        false_data.append((create_word_features(words), "negative"))

    classTrue = ""
    for key, text in trueFile.items():
        classTrue += text

    classFalse = ""
    for key, text in falseFile.items():
        classFalse += text

    print("freq distribution, class 0")
    #stopwords removal
    filtered_classTrue = [word.lower() for word in classTrue.split(" ") if word.lower() not in stopwords.words("english")]
    filtered_classTrue_stop = filtered_classTrue
    filtered_classTrue = []
    filtered_classTrue = [lmtzr.lemmatize(word) for word in filtered_classTrue_stop]
    fdist0 = nltk.FreqDist(filtered_classTrue)
    #Get 50 Most Common Words
    print (fdist0.most_common(500))

    # pickle.dumps(fdist0, open("/scratch/anamikas/hyp/results/fdist0.p", "wb"))

    print("frequency distribution, class 1")
    #stopwords removal
    filtered_classFalse = [word.lower() for word in classFalse.split(" ") if word.lower() not in stopwords.words("english")]
    filtered_classFalse_stop = filtered_classFalse
    filtered_classFalse = []
    filtered_classFalse = [lmtzr.lemmatize(word) for word in filtered_classFalse_stop]
    fdist1 = nltk.FreqDist(filtered_classFalse)
    #Get 50 Most Common Words
    print (fdist1.most_common(500))

    # pickle.dumps(fdist0, open("/scratch/anamikas/hyp/results/fdist1.p", "wb"))

    all_0 = set([])
    all_1 = set([])
    for items in fdist0.most_common(500):
        all_0.add(items[0])

    for items in fdist1.most_common(500):
        all_1.add(items[0])

    print("intersection of most common words")

    mutual_keys = all_0.intersection(all_1)
    print(len(mutual_keys))

    fdist_0 = []
    for item in fdist0.items():
        fdist_0.append(item)

    fdist_1 = []
    for item in fdist1.items():
        fdist_1.append(item)

    sorted_fdist_1 = sorted(fdist_1, key=lambda x: x[1], reverse=True)
    sorted_fdist_0 = sorted(fdist_0, key=lambda x: x[1], reverse=True)

    #get all the top 80% and least 10% words
    doc1_8010 = []
    for words in sorted_fdist_1[-(round(0.1*len(sorted_fdist_1))):]:
        doc1_8010.append(words[0])

    doc0_8010 = []
    for words in sorted_fdist_0[-(round(0.1*len(sorted_fdist_0))):]:
        doc0_8010.append(words[0])


    print("new freq dist, class 0")
    #stopwords removal
    filtered_doc0 = [word.lower() for word in classTrue.split(" ") if word.lower() not in stopwords.words("english")]
    filtered_doc0_stop = filtered_doc0
    filtered_doc0 = []
    filtered_doc0 = [lmtzr.lemmatize(word) for word in filtered_doc0_stop]
    #remove 80% most occurring and 10% rare
    filtered_doc0 = [word for word in filtered_doc0 if word not in doc0_8010]
    #remove mutual words
    filtered_doc0 = [word for word in filtered_doc0 if word not in mutual_keys]
    fdist0_rem = nltk.FreqDist(filtered_doc0)
    #Get 50 Most Common Words
    print (fdist0_rem.most_common(500))

    # pickle.dumps(fdist0_rem, open("/scratch/anamikas/hyp/results/fdist0_rem.p", "wb"))

    filtered_doc0_string = " ".join(word for word in filtered_doc0)
    # pickle.dump(filtered_doc0_string, open("/scratch/anamikas/hyp/results/filtered_doc0_string.p", "wb"))

    print("new freq dist, class1")
    #stopwords removal
    filtered_doc1 = [word.lower() for word in classFalse.split(" ") if word.lower() not in stopwords.words("english")]
    filtered_doc1_stop = filtered_doc1
    filtered_doc1 = []
    filtered_doc1 = [lmtzr.lemmatize(word) for word in filtered_doc1_stop]
    #remove 80% most occurring and 10% rare
    filtered_doc1 = [word for word in filtered_doc1 if word not in doc1_8010]
    #remove mutual words
    filtered_doc1 = [word for word in filtered_doc1 if word not in mutual_keys]
    fdist1_rem = nltk.FreqDist(filtered_doc1)
    #Get 50 Most Common Words
    print (fdist1_rem.most_common(500))

    # pickle.dumps(fdist1_rem, open("/scratch/anamikas/hyp/results/fdist1_rem.p", "wb"))

    filtered_doc1_string = " ".join(word for word in filtered_doc1)
    # pickle.dump(filtered_doc1_string, open("/scratch/anamikas/hyp/results/filtered_doc1_string.p", "wb"))

    print("starting n gram")
    start_0 = time.time()
    for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:

        print("Creating ", str(n), " grams")

        class0_data = []
        for key, text in trueFile.items():
            class0_data.append((create_ngram_features_processed(text, mutual_keys, doc0_8010, n), "class0"))

        class1_data = []
        for key, text in class_1_dict.items():
            class1_data.append((create_ngram_features_processed(text, mutual_keys, doc1_8010, n), "class1"))

        shuffle(class0_data)
        shuffle(class1_data)

        if len(class0_data)>len(class1_data):
            class0_data = callRemoveExtra(class0_data, class1_data)
        else:
            class1_data = callRemoveExtra(class1_data, class0_data)

        limit = round(0.8*len(class0_data))

        train_set = class0_data[:limit] + class1_data[:limit]
        test_set =  class0_data[limit:] + class1_data[limit:]

        print("Training")

        start = time.time()
        classifier = NaiveBayesClassifier.train(train_set)
        end = time.time()
        print("Time taken", end-start)

        print("Training done")

        print("Testing for test dataset")

        start = time.time()
        accuracy = nltk.classify.util.accuracy(classifier, test_set)
        end = time.time()
        print("Time taken", end-start)

        print(str(n)+'-gram accuracy for test:', accuracy)

        print(classifier.show_most_informative_features(10))

    end_0 = time.time()
    print(end_0-start_0)
    print("Total time taken")

    end = time.time()
    print(end-start)
