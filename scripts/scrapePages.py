import json
from pprint import pprint
import os
from newspaper import Article
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import subprocess

start = time.time()
os.chdir("/scratch/anamikas/hyp/postVac/midterm-elections/dataset/bingResults")
outputDir = "/scratch/anamikas/hyp/postVac/midterm-elections/dataset/dataText1"

for filename in os.listdir("."):
    with open(filename) as f:
        currDir = os.path.join(outputDir, filename.rsplit( ".", 1 )[ 0 ] )
        os.mkdir(currDir)
        data = json.load(f)
        # pprint(data)
        for articles in data['articles']:
            url = data['articles'][articles]['url'].strip()
            cmd = "python /home/anamikas/work/Hyperpartisan-News-Detection/scripts/callScrapePages.py -articles " + str(articles) + " -url " +\
                    str(url) + " -filename " + str(filename)
            subprocess.call(cmd, shell=True)

end=time.time()
totaltime = end-start
print(totaltime)
statsFile = open(os.path.join(outputDir, "stats.txt"), "w")
statsFile.write("The time taken to get most html and text " + str(totaltime))
statsFile.close()
