import pickle
from urllib.parse import urlparse
import time

start = time.time()
# pickleFile_byArticle = pickle.load(open('/scratch/anamikas/hyp/v2/dataset/groundTruth/train/byArticle/groundTruthbyArticle.p', 'rb'))
# pickleFile_byPublisher = pickle.load(open('/scratch/anamikas/hyp/v2/dataset/groundTruth/train/byPublisher/groundTruthbyPublisher.p', 'rb'))

pickleFile = pickle.load(open('/scratch/anamikas/hyp/postVac/results/groundTruthParsing_ground-truth-validation-bypublisher-20181122.xml.p', 'rb'))

urlDict = dict()
urlDict['true'] = []
urlDict['false'] = []

def getUrl(pFile):
    for i in pFile:
        url = pFile[i]['url']
        parsed_url = urlparse(url)
        result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
        if pFile[i]['hyperpartisan'] == 'true':
            urlDict['true'].append(result)
        else:
            urlDict['false'].append(result)


getUrl(pickleFile)

pickle.dump(urlDict, open('/scratch/anamikas/hyp/postVac/jan30/url/urlDict_val.p', 'wb'))
end = time.time()

totaltime = end-start

f = open('/scratch/anamikas/hyp/postVac/jan30/url/urlDictValstats.txt', 'w+')
f.write("The ime taken to find url names for validation set is " +  str(totaltime))
f.close()
