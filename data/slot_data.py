#!/bin/python
# This script is used create a csv file with the ids of the buoys. This is simply
# to be used for importing data into the amazon web console for the BUOY_ID slot.
from json import loads
import csv

data = None
with open("buoy_locations.json") as jsonfile:
    data = loads(jsonfile.read())

with open('slot.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile)
    for k, _ in data.items():
        writer.writerow([k])
