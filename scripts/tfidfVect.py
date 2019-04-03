import os
import pickle
import time
import numpy as np
import pandas as pd
from sklearn import preprocessing, model_selection
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression

dataFile = '/scratch/anamikas/hyp/v2/tsvFile.tab'

dataFileDF = pd.read_csv(dataFile, sep="\t", names=['id', 'labeled-by', 'text', 'hyperpartisan', 'url', 'length', 'numURL'])

lbl_enc = preprocessing.LabelEncoder()
y = lbl_enc.fit_transform(dataFileDF.hyperpartisan.values)

xtrain, xvalid, ytrain, yvalid = train_test_split(dataFileDF.text.values, y,
                                                 stratify=y,
                                                 random_state=42,
                                                 test_size=0.1, shuffle=True)


tfv = TfidfVectorizer(min_df=3, max_features=None,
                     strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                     ngram_range=(1, 3), use_idf=1, smooth_idf=1, sublinear_tf=1,
                     stop_words='english')

print("Fitting")
start=time.time()
tfv.fit(list(xtrain) + list(xvalid))
end=time.time()

print("Done fitting")

print("Time taken to fit", end-start)

print("Transforming")
start = time.time()
xtrain_tfv =  tfv.transform(xtrain)
xvalid_tfv = tfv.transform(xvalid)
end = time.time()
print("Done transforming")
print("Time taken to transform", end-start)

# Fitting a simple Logistic Regression on TFIDF
clf = LogisticRegression(C=1.0)
clf.fit(xtrain_tfv, ytrain)
predictionsprob = clf.predict_proba(xvalid_tfv)
predictions = clf.predict(xvalid_tfv)

import pdb; pdb.set_trace()
