import xml.etree.ElementTree as ET
import pickle
import time

tree = ET.parse('/scratch/anamikas/hyp/v2/dataset/groundTruth/validation/ground-truth-validation-bypublisher-20181122.xml')
root = tree.getroot()
start = time.time()

article = dict()
lst = []
for child in root:
    article[child.attrib['id']] = {}
    for keys, vals in child.attrib.items():
        article[child.attrib['id']][keys]=vals

end = time.time()
totaltime=end-start

writeFile = open("/scratch/anamikas/hyp/postVac/results/ground-truth-validation-bypublisher-20181122.xml.txt", "w")
writeFile.write("The time taken to run the script for ground Truth XML parsing " + str(totaltime))
writeFile.close()

pickle.dump( article, open( "/scratch/anamikas/hyp/postVac/results/groundTruthParsing_ground-truth-validation-bypublisher-20181122.xml.p", "wb" ))
