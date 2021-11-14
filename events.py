from serpapi import GoogleSearch
import yaml

def get_events():

    creds = yaml.safe_load(open("creds.yaml", "r"))
    private_key = creds['private_key']

    params = {
    "q": "events in Boston",
    "google_domain": "google.com",
    "gl": "us",
    "hl": "en",
    "api_key": private_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    events_results = results['events_results']
    print(events_results)
    return events_results

x = get_events()
print(x[0]['address'])