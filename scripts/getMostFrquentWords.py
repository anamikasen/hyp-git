import pickle
import time
import os

start = time.time()

trainPickledFiles = ['/scratch/anamikas/hyp/v2/outputs/train/byArticle/article_preprocessed_trainbyArticle.p', \
                    '/scratch/anamikas/hyp/v2/outputs/train/byPublisher/article_preprocessed_trainbyPublisher.p']

groundTruthPickledFiles = ['/scratch/anamikas/hyp/v2/dataset/groundTruth/train/byArticle/groundTruthbyArticle.p', \
                        '/scratch/anamikas/hyp/v2/dataset/groundTruth/train/byPublisher/groundTruthbyPublisher.p']

totalCorpusCount = dict()
totalCorpusCount['true'] = {}
totalCorpusCount['false'] = {}


for i, files in enumerate(trainPickledFiles):
    file = pickle.load(open(files, 'rb'))
    groundTruth = pickle.load(open(groundTruthPickledFiles[i], 'rb'))
    for id, words in file.items():
        for word, count in words.items():
            if word not in totalCorpusCount[groundTruth[id]['hyperpartisan']]:
                totalCorpusCount[groundTruth[id]['hyperpartisan']][word] = count
            totalCorpusCount[groundTruth[id]['hyperpartisan']][word] += count


pickle.dump(totalCorpusCount, open(os.path.join('/scratch/anamikas/hyp/v2/outputs/train/totalCorpusCount' +'.p'), 'wb'))

end = time.time()
totaltime = end-start

writeFile = open("/scratch/anamikas/hyp/v2/outputs/train/mostFrequentWordsstats.txt", "w")
writeFile.write("The time taken to get most frequent words in the whole corpus is " + str(totaltime))
writeFile.close()
