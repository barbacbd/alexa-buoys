from concurrent.futures import ThreadPoolExecutor, as_completed
from json import loads
from os import getcwd
from os.path  import join, realpath, dirname
from nautical.location import Point
from nautical.noaa import Buoy
from nautical.units import DistanceUnits


__location__ = realpath(join(getcwd(), dirname(__file__)))


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


#print(get_buoys_near_location("virginia beach", "virginia"))
#print(get_buoys_near_coordinates(36.7335, -76.0435))
#print(get_buoys_near_coordinates(36.8581681,-76.0901321))