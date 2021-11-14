from serpapi import GoogleSearch
import yaml, random, googlemaps

creds = yaml.safe_load(open("creds.yaml", "r"))

def get_event():
    private_key = creds['private_key']
    if bool(random.getrandbits(1)):
        params = {
        "q": "events near Boston University",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
        "api_key": private_key
        }
    else:
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
    name = events_results[0]['title']
    date = events_results[0]['date']
    address = events_results[0]['address']
    thumbnail = events_results[0]['thumbnail']
    return [name, date, address, thumbnail]

def get_place():
    api_key = creds['api_key']
    client = googlemaps.Client(key = api_key)

    boston = {
            "lat" : 42.349634,
            "lng" : -71.099688
        }
    radius = random.randint(200,2000)

    places = client.places_nearby(location=boston, radius=radius, type='restaurant')
    name = places['results'][0]['name']
    vicinity = places['results'][0]['vicinity']
    rating = places['results'][0]['rating']
    photos = places['results'][0]['photos']
    return [name, vicinity, rating, photos]


def gen_result():
    if bool(random.getrandbits(1)):
        result = get_event()
    else:
        result = get_place()
    return result