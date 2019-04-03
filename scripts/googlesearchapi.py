from googleapiclient.discovery import build
import pprint

my_api_key = "AIzaSyDkW2kV7FsXdDm6y-bsC51K9zrAg4gBAUA"
my_cse_id = "006122868189276343896:fmngp_2vfle"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    import pdb; pdb.set_trace()
    return res['items']

results = google_search('University To Award Trayvon Martin With Posthumous Degree In Aviation', my_api_key, my_cse_id, num=10)

for result in results:
    pprint.pprint(result)
