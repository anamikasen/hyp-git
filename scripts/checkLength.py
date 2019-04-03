import pickle
import time
import os

start = time.time()

writePath = '/scratch/anamikas/hyp/results/'
trainFile = open('/scratch/anamikas/hyp/results/articleTraining.pickle', 'rb')
train = pickle.load(trainFile)
trainFile.close()

truthFile = open('/scratch/anamikas/hyp/results/groundTruth_training.p', 'rb')
truth = pickle.load(truthFile)
truthFile.close()

length = dict()
length['hyperpartisan-true'] = []
length['hyperpartisan-false'] = []
writeFile = open(os.path.join(writePath, "checkLengthstatsWithStopWords.txt"), "w")

for k, v in truth.items():
    try:
        if truth[k]['hyperpartisan'] == 'true':
            length['hyperpartisan-true'].append(train[k]['lengthwords'])
        if truth[k]['hyperpartisan'] == 'false':
            length['hyperpartisan-false'].append(train[k]['lengthwords'])
        if truth[k]['bias'] not in length:
            length[truth[k]['bias']] = []
        length[truth[k]['bias']].append(train[k]['lengthwords'])
    except KeyError:
        writeFile.write(str(k) + str(truth[k]) + "\n")

pickle.dump( length, open( str(writePath)+"lengthWithStopWords.pickle", "wb" ) )

end = time.time()
totaltime = end-start

writeFile.write("The time taken to find length according to bias is " + str(totaltime))
writeFile.close()
