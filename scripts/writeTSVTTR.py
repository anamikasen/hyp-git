import pickle
import os

# ttrfile = pickle.load(open("/scratch/anamikas/hyp/postVac/jan30/textOfArticles/train/byPublisher/typeTokenRatio.p", "rb"))
#
# f = open("/scratch/anamikas/hyp/postVac/jan30/textOfArticles/train/byArticle/ttr.tsv", "a")
#
# for k, v in ttrfile.items():
#     f.write(str(k) + "\t" + str(v['length']) + "\t" + str(v['avg']) + "\n")
#
# f.close()

truthfile = pickle.load(open("/scratch/anamikas/hyp/v2/dataset/groundTruth/train/byPublisher/groundTruthbyPublisher.p", "rb"))

f = open("/scratch/anamikas/hyp/v2/dataset/groundTruth/train/byArticle/groundtruth.tsv", "a")

for k, v in truthfile.items():
    f.write(str(k) + "\t" + str(v['hyperpartisan']) + "\n")

f.close()

