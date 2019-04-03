# Import required modules.
from azure.cognitiveservices.search.websearch import WebSearchAPI
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials
import time, os, json

# Replace with your subscription key.
queriesFile = "/home/anamikas/work/Hyperpartisan-News-Detection/Queries.txt"
outputDir = "/scratch/anamikas/hyp/postVac/midterm-elections/dataset/bingWebSearch/"
subscription_key = "7b7e1e1efaa54695a1d2ea66b00d0585"


start = time.time()
# Instantiate the client.
client = WebSearchAPI(CognitiveServicesCredentials(subscription_key))

# Make a request. Replace Yosemite if you'd like.
with open(queriesFile, 'r', encoding='utf-8-sig') as f:
    for i, lines in enumerate(f):
        search_term = lines.strip()
        web_data = client.web.search(query=search_term, count=200)
        result = {}
        result['query'] = search_term
        result['count'] = len(web_data.web_pages.value)
        result['articles'] = {}
        if web_data.web_pages.value:
            for i, each in enumerate(web_data.web_pages.value):
                result['articles'][i] = {}
                result['articles'][i]['name'] = web_data.web_pages.value[i].name
                result['articles'][i]['url'] = web_data.web_pages.value[i].url

        else:
            print("No web search ", )

        with open(os.path.join(outputDir, search_term + ".json"), 'w') as fp:
            json.dump(result, fp)

        print("Done", search_term)
end = time.time()
totaltime=end-start

statsFile = open(os.path.join(outputDir, "bingWebsearchapitime.txt"), "w")
statsFile.write("The time taken to run the script bing web search on the queries is " + str(totaltime))
statsFile.close()

