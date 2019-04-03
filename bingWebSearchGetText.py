from bs4 import BeautifulSoup
import os, json, urllib
import time

queriesDir = "/scratch/anamikas/hyp/postVac/midterm-elections/dataset/bingWebSearch"
articleDir = "/scratch/anamikas/hyp/postVac/midterm-elections/dataset/bingWebSearch/articleText/"

start = time.time()

for files in os.listdir(queriesDir):
    with open(os.path.join(queriesDir,files)) as data:
        data_dic = json.load(data)
        for i in range(len(data_dic['articles'])):
            url = data_dic['articles'][str(i)]['url']
            try:
                soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html')
                paragraphs = soup.find_all('p')
                with open(os.path.join(articleDir + str(files) + str(".") + str(i) + ".txt"), 'w') as fp:
                    for p in paragraphs:
                        fp.write(p.getText())
                    fp.close()
            except:
                continue

    print("Done" , files)

end = time.time()
totaltime=end-start

statsFile = open(os.path.join(articleDir, "articlTextStats"), "w")
statsFile.write("The time taken to get the text from the urls 01/04 is  " + str(totaltime))
statsFile.close()

