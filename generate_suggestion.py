from flask.globals import request
from serpapi import GoogleSearch
import yaml, random, googlemaps
from firebase_admin import credentials, firestore, initialize_app
import uuid
import requests
from PIL import Image
from io import BytesIO

cred = credentials.Certificate("google_auth_creds.json")
initialize_app(cred)
db = firestore.client()


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
    return ['event', name, date, address, thumbnail]

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
    api_call = '''https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=''' + str(photos[0]['photo_reference']) + '''&key=''' + str(api_key)

    return ['place', name, vicinity, rating, photos, api_call]


def gen_result():
    dict = {}
    if bool(random.getrandbits(1)):
        result = get_event()
        dict['type'] = result[0]
        dict['name'] = result[1]
        dict['date'] = result[2]
        dict['address'] = result[3]
        dict['thumbnail'] = result[4]

        
    else:
        result = get_place()
        dict['type'] = result[0]
        dict['name'] = result[1]
        dict['vicinity'] = result[2]
        dict['rating'] = result[3]
        dict['photos'] = result[4]
        dict['api_call'] = result[5]

    activies = db.collection('activies')

    id = str(uuid.uuid4())

    dict['id'] = id

    activies.document(str(id)).set(dict)

    return id

# get_place()