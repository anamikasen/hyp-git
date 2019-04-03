'''
dataset division according to classes

'''
import json

with open('/scratch/anamikas/hyp/postVac/jan30/textOfArticles/fulldatasetText.json') as f:
    textDict = json.load(f)

with open('/scratch/anamikas/hyp/postVac/jan30/textOfArticles/fulldatasetTruth.json') as f:
    truthDict = json.load(f)

def concatWords(artFile, truthFile, label):
    catString = " "
    for k, v in artFile.items():
        if truthFile[k]['hyperpartisan']==label:
            catString += v
            import pdb; pdb.set_trace()
    return catString

classTrue = " "
classFalse = " "

classTrue += (concatWords(textDict[0], truthDict[0], 'true'))

