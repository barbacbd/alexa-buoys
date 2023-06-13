# -*- coding: utf-8 -*-

# The file provides utility functions that will be used as the main source of 
# information from the nautical package. The functions below can be linked to
# the intents created for this alexa skill.
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from email.policy import default
from json import loads
from statistics import mean
from os import getcwd
from os.path  import join, realpath, dirname
import requests
from nautical.io import create_buoy
from nautical.location import Point
from nautical.noaa import Buoy
from nautical.units import DistanceUnits


__location__ = realpath(join(getcwd(), dirname(__file__)))

__search_data = {
    "wvht": ["average wave height", "feet"],
    "apd": ["average period", "seconds"],
    "wtmp": ["average water temperature", "degrees"]
}


def describe_buoy(buoy_id):
    '''Provide the buoy information for a single buoy.
    
    :param buoy_id: Id of the buoy to find information about
    :return: String containing the buoy information. This will be used
    to state information via the interface.
    '''
    buoy = create_buoy(buoy_id)
    if buoy is None:
        return {}
 
    return {key: getattr(buoy.data, key) for key in __search_data}


def _find_buoys_in_dist(loc, buoy, dist, units):
    '''Find the distance between the location and buoy'''
    if loc.in_range(buoy.location, dist, units):
        return buoy.station
    return None


def get_buoys_near_coordinates(lat, lng):
	'''Get the list of buoys near the latitude and longitude coordinates.

	:param lat: Latitude float value
	:param lng: Longitude float value
	:return: list of buoy Ids near the provided location
	'''
	location_point = Point(lat, lng)
	buoy_ids_in_dist = []
	dist = 50.0
	units = DistanceUnits.MILES

	buoy_locations = {}
	with open(join(__location__, "../data/buoy_locations.json")) as jsonfile:
		data = loads(jsonfile.read())

		for buoy_station, buoy_json_data in data.items():
			buoy_locations[buoy_station] = Buoy(buoy_station, location=Point.from_json(buoy_json_data))

	with ThreadPoolExecutor(max_workers=10) as executor:
		tmp_buoys_fnd_in_dist = {executor.submit(_find_buoys_in_dist, location_point, buoy, dist, units):
									buoy for _, buoy in buoy_locations.items()}

		for futr in as_completed(tmp_buoys_fnd_in_dist):
			buoy_ids_in_dist.extend([futr.result()])

	buoy_ids_in_dist = [x for x in buoy_ids_in_dist if x is not None]
	return buoy_ids_in_dist


def get_buoys_near_location(city, state):
	'''Get the list of buoys near the city, state location.

	:param city: Name of the city to search for.
	:param state: Name of the state to search for.
	:return: list of buoy Ids near the provided location
	'''
	search_name = f"{city.lower()}, {state.lower()}"

	location_to_id = {}
	with open(join(__location__, "../data/location_ids.json")) as jsonfile:
		location_to_id = loads(jsonfile.read())

	if search_name not in location_to_id:
		return []

	location_buoys = {}
	with open(join(__location__, "../data/cities_with_buoys.json")) as jsonfile:
		location_buoys = loads(jsonfile.read())

	if location_to_id[search_name] not in location_buoys:
		return []

	return location_buoys[location_to_id[search_name]]['buoys']


def _parse_described(buoy_ids):
    '''Parse the buoy ids by pulling the buoy information online
    and putting the data into a dictionary of lists.
    
    :param buoy_ids: ids of the buoys to describe.
    :return: dictionary of lists for each value
    '''
    if not buoy_ids:
        return None

    described = [describe_buoy(x) for x in buoy_ids]

    buoy_data = defaultdict(list)
    for desc in described:
        if desc is not None:
            for k, v in desc.items():
                if v is not None:
                    buoy_data[k].append(v)

    return buoy_data


def _find_me():
    response = requests.get('https://api64.ipify.org?format=json').json()
    ipaddr = response["ip"]
    response = requests.get(f'https://ipapi.co/{ipaddr}/json/').json()
    return response
    

def describe_buoys_near_city(city, state):
    '''Describe the buoy information for a city,state. This can include
    multiple buoys.
    
    :param city: name of the city
    :param state: name of the state
    :return: A dictionary of listed values converted from the descibe_buoy function.
    The data should be used to find the max, min, average of the list
    '''
    buoys = get_buoys_near_location(city, state)
    return _parse_described(buoys)


def get_buoys_near_me():
    '''Get the buoy(s) that are closest to me
    
    :return: List of buoys that were found
    '''
    response = _find_me()
    
    buoys = []
    if 'latitude' in response and 'longitude' in response:
        buoys = get_buoys_near_coordinates(response['latitude'], response['longitude'])
    elif 'city' in response and 'region' in response:
        buoys = get_buoys_near_location(response['city'], response['region'])
        
    return buoys

def describe_my_buoy_data():
    '''Describe the buoy(s) that are closest to me
    
    :return: A dictionary of listed values converted from the descibe_buoy function.
    The data should be used to find the max, min, average of the list
    '''
    buoys = get_buoys_near_me()
    return _parse_described(buoys)


def create_buoy_list_output(buoys, location_str):
    output_location = "you" if location_str == "me" else location_str
    if not buoys:
        return f"no buoys found near {output_location}"
    return f"The following buoys were found near {output_location}, {', '.join(buoys)}"


def create_long_output(buoy_var_data):
    output = []
    for key, value in __search_data.items():
        if key in buoy_var_data:
            average_data =  round(mean([float(x) for x in buoy_var_data[key]]), 2)
            output.append(f"the {value[0]} is {average_data} {value[1]}")

    if not output:
        return "not valid buoy data found"
    return ", ".join(output)



#print(get_buoys_near_location("virginia beach", "virginia"))
#print(get_buoys_near_coordinates(36.7335, -76.0435))
#print(get_buoys_near_coordinates(36.8581681,-76.0901321))
