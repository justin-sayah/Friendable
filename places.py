import googlemaps
import yaml


creds = yaml.safe_load(open("creds.yaml", "r"))
api_key = creds['api_key']


client = googlemaps.Client(key = api_key)

# 42.3601° N, 71.0589° W

lat =  42.3601, 
lon = 71.0589

boston = {
        "lat" : 42.3601,
        "lng" : -71.038887
    }

loc = str(lat) + ',' + str(lon)

radius = 800
token = None 
price = 2

places = client.places_nearby(location=boston, radius=radius, type='restaurant')

print(places['results'][0]['name'])
print(places['results'][0]['vicinity'])
print(places['results'][0]['rating'])
print(places['results'][0]['photos'])