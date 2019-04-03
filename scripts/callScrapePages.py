import subprocess
import json
from pprint import pprint
import os
from newspaper import Article
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import argparse

def main(map_args):
    outputDir = "/scratch/anamikas/hyp/postVac/midterm-elections/dataset/dataText1"
    file = (" ").join(map_args.filename)
    currDir = os.path.join(outputDir, file.rsplit( ".", 1 )[ 0 ] )
    article = Article(map_args.url[0])
    try:
        article.download()
        article.html
        article.parse()
        with open(os.path.join(currDir, str(map_args.articles[0]) + "." +file.rsplit( ".", 1 )[ 0 ] + ".txt"), mode="w",encoding="utf-8") as f:
            f.write(article.title)
            f.write("\n")
            f.write(article.text)
        with open(os.path.join(currDir, str(map_args.articles[0]) + file.rsplit( ".", 1 )[ 0 ] + ".html"), mode="w",encoding="utf-8") as f:
            f.write(article.html)
    except:
        with open(os.path.join(currDir, file.rsplit( ".", 1 )[ 0 ] + ".exception"), mode="w",encoding="utf-8") as f:
            f.write(str(map_args.articles[0]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-articles', type=str, nargs='+',
                        help='article number')
    parser.add_argument('-url', type=str, nargs='+',
                        help='url of news article')
    parser.add_argument('-filename', type=str, nargs="+",
                        help='JSON filename')
    map_args = parser.parse_args()

    main(map_args)
