'''
script to get type token ratio - feb 6
'''

dataPath = "/scratch/anamikas/hyp/postVac/jan30/textOfArticles/validation/articletext.p"
import nltk
import pickle
import string
import time
import os


start = time.time()
articleText = pickle.load(open(dataPath, "rb"))

exclude = set(string.punctuation)

result = {}
for id, text in articleText.items():
    result[id] = {}
    result[id]['length'] = []
    result[id]['avg'] = 0
    sents = nltk.sent_tokenize(text)
    for sent in sents:
        sent = " ".join(word.lower() for word in sent.split())
        sent = ''.join(ch for ch in sent if ch not in exclude)
        tokenised_text = nltk.word_tokenize(sent)
        if len(tokenised_text)==0:
            continue
        uniqueWords = {}
        for words in tokenised_text:
            if words not in uniqueWords:
                uniqueWords[words] = 1
        result[id]['length'].append(len(uniqueWords)/len(tokenised_text))
    result[id]['avg'] = (sum(result[id]['length'])/len(result[id]['length']))


pickle.dump(result, open(os.path.join('/scratch/anamikas/hyp/postVac/jan30/textOfArticles/validation/typeTokenRatio' +'.p'), 'wb'))
end = time.time()
totaltime = end-start

writeFile = open("/scratch/anamikas/hyp/postVac/jan30/textOfArticles/validation/TTR.txt", "w")
writeFile.write("The time taken to run the script for finding Type token ratio is  " + str(totaltime))
writeFile.close()

