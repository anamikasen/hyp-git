import pickle
import time
import os

start = time.time()

writePath = '/scratch/anamikas/hyp/results/'
urlFile = open('/scratch/anamikas/hyp/preprocessing/urlTypeWithoutEmptyStringstrain.p', 'rb')
train = pickle.load(urlFile)
urlFile.close()

truthFile = open('/scratch/anamikas/hyp/results/groundTruth_training.p', 'rb')
truth = pickle.load(truthFile)
truthFile.close()

urlCount = dict()
urlCount['hyperpartisan-true'] = []
urlCount['hyperpartisan-false'] = []
writeFile = open(os.path.join(writePath, "urlCountstats.txt"), "w")

for k, v in truth.items():
    try:
        if truth[k]['hyperpartisan'] == 'true':
            urlCount['hyperpartisan-true'].append(len(train[k].values()))
        if truth[k]['hyperpartisan'] == 'false':
            urlCount['hyperpartisan-false'].append(len(train[k].values()))
        if truth[k]['bias'] not in urlCount:
            urlCount[truth[k]['bias']] = []
        urlCount[truth[k]['bias']].append(len(train[k].values()))
    except KeyError:
        writeFile.write(str(k) + str(truth[k]) + "\n")

pickle.dump( urlCount, open( str(writePath)+"urlCount.pickle", "wb" ) )

end = time.time()
totaltime = end-start

writeFile.write("The time taken to find url counts " + str(totaltime))
writeFile.close()
