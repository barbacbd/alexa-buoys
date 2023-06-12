#!/bin/python
# This script is used create a csv file with the ids of the buoys. This is simply
# to be used for importing data into the amazon web console for the BUOY_ID slot.
from json import loads
import csv

data = None
with open("buoy_locations.json") as jsonfile:
    data = loads(jsonfile.read())

with open('buoy_slot.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile)
    for k, _ in data.items():
        writer.writerow([k])

cities = []
states = []
data = None
with open("cities_with_buoys.json") as jsonfile:
    data = loads(jsonfile.read())
    
for _, v in data.items():
    cities.append(v["city"])
    states.append(v["state_name"])

cities = list(set(cities))
states = list(set(states))

with open('city_slot.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile)
    for city in cities:
        writer.writerow([city])


with open('state_slot.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile)
    for state in states:
        writer.writerow([state])