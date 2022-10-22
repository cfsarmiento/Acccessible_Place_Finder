# Import Libraries
import googlemaps  # Google Places API For Location Details
import pprint
import requests
import json
import time
import csv
from geopy.geocoders import GoogleV3 as gm  # for address to coordinate conversion

# API Key
api_key = 'AIzaSyCsXFGypNDCNXMtHqplZrcEcoOhEMHrtz8'  # FIXME: remember to hide this

# Class for our Search
class GooglePlaces(object):
    def __init__(self, api_key):
        super(GooglePlaces, self).__init__()
        self.api_key = api_key  # api key within class

    def search_by_coord(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.api_key
        }

        temp = requests.get(endpoint_url, params = params)  # searching by coord
        results = json.loads(temp.content)  # saves results as json
        places.extend(results['results'])  # places gets results
        time.sleep(2)  # stops execution for 2 seconds

        while 'next_page_token' in results:
            # Reads data while there is still more data to be read
            params['pagetoken'] = results['next_page_token'],
            temp = requests.get(endpoint_url, params=params)
            results = json.loads(temp.content)
            places.extend(results['results'])
            time.sleep(2)
        return places

    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.api_key
        }
        temp = requests.get(endpoint_url, params=params)
        place_details = json.loads(temp.content)
        return place_details

if __name__ == '__main__':
    # Initilize API
    api = GooglePlaces(api_key)

    # Address to Coordinate Conversion
    geolocator = gm(api_key = api_key)
    location = geolocator.geocode('100 W 14th Ave Pkwy, Denver, CO 80204')  # Gets Coordinates from Address
    coordinates = f'{location.latitude},{location.longitude}'  # Saves coords as string for function

    places = api.search_by_coord(coordinates, 40000, 'resturant')  # location, radius, type of place
    fields = ['name', 'type', 'formatted_address', 'price_level',
              'rating', 'review', 'user_ratings_total', 'url']
    data = []  # empty list for csv later
    for place in places:
        details = api.get_place_details(place['place_id'], fields)

        try:
            name = details['result']['name']
            data.append(name)
        except KeyError:
            name = ""

        try:
            type = details['result']['type']
            data.append(type)
        except KeyError:
            type = ""

        try:
            address = details['result']['formatted_address']
            data.append(address)
        except KeyError:
            address = ""

        try:
            price_level = details['result']['price_level']
            data.append(price_level)
        except KeyError:
            price_level = ""

        try:
            rating = details['result']['rating']
            data.append(rating)
        except KeyError:
            rating = []

        try:
            reviews = details['result']['review']
            data.append(review)
        except KeyError:
            reviews = []

        try:
            user_ratings_total = details['result']['user_ratings_total']
            data.append(user_ratings_total)
        except KeyError:
            user_ratings_total = []

        try:
            url = details['result']['url']
            data.append(url)
        except KeyError:
            url = []

# Write data to csv
    with open('places.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow(fields)

        # Data
        writer.writerow(data)
