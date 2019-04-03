from azure.cognitiveservices.search.newssearch import NewsSearchAPI
from msrest.authentication import CognitiveServicesCredentials

import pickle
import time
import json
import os

queriesFile = "/home/anamikas/work/Hyperpartisan-News-Detection/Queries.txt"
outputDir = "/scratch/anamikas/hyp/postVac/midterm-elections/dataset"
subscription_key = "c445e7f0ba1d4939b4a9aed60a0881f4"

start = time.time()

client = NewsSearchAPI(CognitiveServicesCredentials(subscription_key))

with open(queriesFile, 'r', encoding='utf-8-sig') as f:
    for lines in f:
        search_term = lines.strip()
        news_result = client.news.search(query=search_term, market="en-us", count=100)

        result = {}
        result['query'] = search_term
        result['count'] = len(news_result.value)
        result['estimated_matches'] = news_result.total_estimated_matches
        result['articles'] = {}
        import pdb; pdb.set_trace()
        if news_result.value:
            for i, each in enumerate(news_result.value):
                result['articles'][i] = {}
                result['articles'][i]['name'] = each.name
                result['articles'][i]['url'] = each.url
                result['articles'][i]['description'] = each.description
                result['articles'][i]['date_published'] = each.date_published
                result['articles'][i]['provider'] = each.provider[0].name
        else:
            print("Didn't see any news result data..")

        with open(os.path.join(outputDir, search_term + ".json"), 'w') as fp:
            json.dump(result, fp)

        print("Done", search_term)

end = time.time()
totaltime=end-start

statsFile = open(os.path.join(outputDir, "bingnewssearchapitime.txt"), "w")
statsFile.write("The time taken to run the script bing news search on the queries is " + str(totaltime))
statsFile.close()

