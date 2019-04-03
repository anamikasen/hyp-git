import pickle
import time

start = time.time()
urlFile = pickle.load(open('/scratch/anamikas/hyp/postVac/jan30/url/urlDict.p', 'rb'))

webUrls = dict()
webUrls['true'] = {}
webUrls['false'] = {}


for k, v in urlFile.items():
    for items in v:
        if items not in webUrls[k].keys():
            webUrls[k][items] = 0
        webUrls[k][items] += 1

pickle.dump(webUrls, open('/scratch/anamikas/hyp/postVac/jan30/url/webUrl.p', 'wb'))
end  = time.time()


totaltime = end - start
f = open('/scratch/anamikas/hyp/postVac/jan30/url/webUrlstats.txt', 'w+')
f.write("The time taken to find individual URL counts is " + str(totaltime))
f.close()
