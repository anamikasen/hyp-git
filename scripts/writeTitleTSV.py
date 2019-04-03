import pickle
import time


start = time.time()
truthFile = pickle.load(open('/scratch/anamikas/hyp/v2/dataset/groundTruth/train/byPublisher/groundTruthbyPublisher.p', 'rb'))
titleFile = pickle.load(open('/scratch/anamikas/hyp/v2/outputs/train/byPublisher/titletrainByPublisher.p', 'rb'))

tsvFile = open('/scratch/anamikas/hyp/v2/tsvFilewithtitle.tab', 'a')

for id, title in titleFile.items():
    tsvFile.write(str(id) + "\t" + str(title) + "\t" + str(truthFile[id]['hyperpartisan']) + "\n")


end = time.time()
totaltime = end-start

writeFile = open("/scratch/anamikas/hyp/v2/tsvFileTitleStats.txt", "a")
writeFile.write("The time taken to get ground truth for title is " + str(totaltime))
writeFile.close()
