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

radius = 2000
token = None 

places = client.places_nearby(location=boston, radius=radius)

print(places)