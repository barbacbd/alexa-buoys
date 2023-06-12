# Repository Utilities

The script `scraper.py` contains utility functions for this repository. This document is a reference to the functions that the script provides.

# Match

The match function finds all buoys that are within a distance of each city in the file `uscities.csv`. If the city does not contain any buoys within a distance, then it is not added to the `cities_with_buoys.json` file. The user can input values for distance and units:

```bash
python3.x scraper.py -f match -d <distance> -u <units>
```

Where: 
- distance: any floating point value (default = 50.0)
- units: CENTIMETERS,FEET,YARDS,METERS,KILOMETERS,MILES,NAUTICAL_MILES (default = MILES)

# Locations

The locations function is used to save location data for quick lookups to json files. The files include a lookup from the id of the city/state and the city/state to the id:

- id_locations.json
- location_ids.json

# Buoy

The buoy function is used to create a json file that contains all buoy_ids linked to their geographical location (latitude/longitude/altitude).

- buoy_locations.json

# Diff

The diff tool is used in CI. The utility will determine what changes have been made to the list of buoys online vs the saved buoy information found in the `buoy` function above. 