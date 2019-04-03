# import requests
# import json
#
# subscription_key = "3c18edd9b04c4f39b2c36d7729951f48"
#
# def bing_search(query):
#     url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
#     payload = {'q': query}
#     headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
#     r = requests.get(url, params=payload, headers=headers)
#     return r.json()
#
# ans = bing_search('good news')
# print(ans.get('webPages', {}).get('value', {}))
# import pdb; pdb.set_trace()

import http.client, urllib.parse, json
import pickle

# **********************************************
# *** Update or verify the following values. ***
# **********************************************

# Replace the subscriptionKey string value with your valid subscription key.
subscriptionKey = "c445e7f0ba1d4939b4a9aed60a0881f4"

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing Web search instance in your Azure dashboard.
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/search"

term = "midterm elections 2018"

def BingWebSearch(search):
    "Performs a Bing Web search and returns the results."

    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(search)
    conn.request("GET", path + "?q=" + query, headers=headers)
    response = conn.getresponse()
    headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
    return headers, response.read().decode("utf8")

if len(subscriptionKey) == 32:

    print('Searching the Web for: ', term)

    headers, result = BingWebSearch(term)
    print("\nRelevant HTTP Headers:\n")
    print("\n".join(headers))
    print("\nJSON Response:\n")
    print(json.dumps(json.loads(result), indent=4))
    x = json.loads(result)
    with open('data.json', 'w') as outfile:
        json.dump(x, outfile)
    pickle.dump( x, open("data.pickle", "wb" ) )
else:

    print("Invalid Bing Search API subscription key!")
    print("Please paste yours into the source code.")

