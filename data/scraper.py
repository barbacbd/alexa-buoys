#!/bin/python
# This script is used to find all cities and buoys and determine which buoys are
# within a distance of 50 miles of the city. If the city does not have any
# buoys in that range it is not added to the output. The intention is to use the
# script to shortcut the lookup time and keep a constant file in the repository
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from json import dumps, loads
from os import getcwd
from os.path  import join, realpath, dirname
from nautical.io import get_buoy_sources
from nautical.location import Point
from nautical.noaa import SourceType
from nautical.units import DistanceUnits

__location__ = realpath(join(getcwd(), dirname(__file__)))

class LocalPoint(Point):
    def __init__(self, json_dict):

        latitude = float( json_dict.get("latitude", json_dict.get("lat", 0.0)))
        longitude = float( json_dict.get("longitude", json_dict.get("lng", 0.0)))
        altitude = float( json_dict.get("altitude", json_dict.get("alt", 0.0)))

        super().__init__(lat=latitude, lon=longitude, alt=altitude)


def find_buoys_in_dist(city_loc, buoy, dist, units):
    '''Find the distance between the city location and buoy'''
    if city_loc.in_range(buoy.location, dist, units):
        return buoy.station
    return None


# Get all buoy information from the sources
def get_buoy_information():
    '''Get all buoy locations'''
    # only concerned with these types of buoys
    sources = get_buoy_sources([SourceType.NDBC_METEOROLOGICAL_OCEAN, SourceType.IOOS_PARTNERS])
    source_data = {}
    for source_type, source in sources.items():
        for buoy_id, buoy in source.buoys.items():
            source_data[buoy.station] = buoy

    return source_data

def save_buoy_information():
    '''Save the buoy locations and IDs to a file'''
    data = get_buoy_information()

    buoy_locations = {}
    for key, value in data.items():
        buoy_locations[key] = value.location.to_json()
    with open(join(__location__, "buoy_locations.json"), "w+") as jsonfile:
        jsonfile.write(dumps(buoy_locations, indent=2))


def create_city_buoy_lookup(dist, units):
    '''Create a json file that matches the buoys to the city if they are
    within the specified distance
    '''
    source_data = get_buoy_information()
    # Find the column number for this information
    required_rows = {
        "city": None,
        "state_name": None,
        "lat": None,
        "lng": None,
        "id": None
    }
    csvdata = None
    cities = {}
    with open(join(__location__, 'uscities.csv')) as csvfile:
        csvdata = list(csv.reader(csvfile))

    if csvdata is not None:

        for i, col in enumerate(csvdata[0]):
            if col in required_rows:
                required_rows[col] = i

        for row in csvdata[1:]:
            cities.update({row[required_rows["id"]]: {
                x: row[y] for x, y in required_rows.items()
            }})


    cities_with_buoys = {}
    # for each location find all buoys that are within 50 miles
    for city_id, city_data in cities.items():
        city_location = LocalPoint(city_data)
        buoy_ids_in_dist = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            tmp_buoys_fnd_in_dist = {executor.submit(find_buoys_in_dist, city_location, buoy, dist, units):
                                     buoy for _, buoy in source_data.items()}

            for futr in as_completed(tmp_buoys_fnd_in_dist):
                buoy_ids_in_dist.extend([futr.result()])

        buoy_ids_in_dist = [x for x in buoy_ids_in_dist if x is not None]
        if buoy_ids_in_dist:
            cities_with_buoys[city_id] = {"buoys": buoy_ids_in_dist}
            cities_with_buoys[city_id].update(cities[city_id])

    with open("cities_with_buoys.json", "w+") as jsonfile:
        jsonfile.write(dumps(cities_with_buoys, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='scraper',
        description='helper file for CI and base project purposes',
    )
    parser.add_argument('-f', '--function', type=str, choices=['buoy', 'match', 'diff'], default='match')
    parser.add_argument('-d', '--distance', type=float, default=50.0, help='max distance between city and buoy for validation')
    unit_names = [x.name for x in DistanceUnits]
    parser.add_argument('-u', '--units', type=str, default='MILES', help='distance unit', choices=unit_names)
    args = parser.parse_args()

    if args.function == 'match':
        dist = args.distance
        units = [x for x in DistanceUnits if x.name == args.units][0]
        create_city_buoy_lookup(dist, units)
    elif args.function == 'buoy':
        save_buoy_information()
    elif args.function == 'diff':
        with open(join(__location__, "buoy_locations.json"), "r") as jsonfile:
            original_buoy_data = loads(jsonfile.read())

        original_set = set(original_buoy_data)
        new_set = set(get_buoy_information())

        diff_set = new_set ^ original_set

        message = "No Updates" if len(diff_set) == 0 else "Changes Detected"
        print(dumps({"diff": len(diff_set), "message": message}))
