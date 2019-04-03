import json
import pickle
import time
import os
"""
Script to get number of sentences in each document, and words per sentence
"""
start = time.time()
articles = pickle.load(open("/scratch/anamikas/hyp/postVac/jan30/textOfArticles/validation/articletext.p", "rb"))
article = {}

for key, text in articles.items():
    article[key] = {}
    sent = text.split(". ")
    addLen = 0
    for items in sent:
        addLen += len(items.split(" "))
    article[key]['sentenceLen'] = len(sent)
    article[key]['wordsPerSent'] = addLen/len(sent)
    print(article[key])

with open('/scratch/anamikas/hyp/postVac/jan30/textOfArticles/validation/wordSentLen.json', 'w') as fp:
    json.dump(article, fp)
pickle.dump(article, open(os.path.join('/scratch/anamikas/hyp/postVac/jan30/textOfArticles/validation/wordSentLen' +'.p'), 'wb'))
end = time.time()
totaltime = end-start

writeFile = open("/scratch/anamikas/hyp/postVac/jan30/textOfArticles/validation/wordAndSent.txt", "w")
writeFile.write("The time taken to run the script for extracting number of sentences and words per sentence is  " + str(totaltime))
writeFile.close()
