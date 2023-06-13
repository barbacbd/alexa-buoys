# Intents

The docuement is intended to track intents and the requirements for each if they are to be added to the skill. 

# Table of Contents

  * [List of My Buoys](#list-of-my-buoys)
  * [List My Buoy Data](#list-my-buoy-data)
  * [Buoys Near Location](#buoys-near-location)
  * [Data Near Location](#data-near-location)
  * [Slots](#slot-types)
  * [Common Functions](#utility-functions)

# List of My Buoys

The intent will provide users with the ability to list a maximum of the five closest buoys (within 50 miles) of the users current location.

- Name: MyBuoys

## Invocations

- my buoys
- what buoys are close to me
- list my buoys
- list the buoys close to me
- can you list the buoys close to me
- can you list my buoys

## Handler

```python

class MyBuoysIntentHandler(AbstractRequestHandler):
    """Handler for my buoy list intent. The buoy ids will be read back to 
    the user if the are found. 
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("MyBuoys")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        geo_response = None
        
        # find my ip address, and from that pull the geographical location
        response = requests.get('https://api64.ipify.org?format=json')
        if response.status_code == 200:
            # successful, pull the ip address
            ipaddr = response.json()["ip"]
            
            # find the geo location
            response = requests.get(f'https://ipapi.co/{ipaddr}/json/')
            if response.status_code == 200:
                geo_response = response.json()


        if not geo_response:
            speak_output = MY_LOC_ERROR
        else:
            buoys = []
            # Find the list of the buoys near the location of the device
            if 'latitude' in geo_response and 'longitude' in geo_response:
                buoys = get_buoys_near_coordinates(
                    geo_response['latitude'],
                    geo_response['longitude']
                )
            elif 'city' in geo_response and 'region' in geo_response:
                buoys = get_buoys_near_location(
                    geo_response['city'],
                    geo_response['region']
                )
            
            if buoys:
                speak_output = ", ".join(buoys)
            else:
                speak_output = "I was not able to find any buoys near you."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

```

**Note**: _Don't forget to add the new handler to the Skill Builder object._


# List My Buoy Data

The intent will provide users with the average values from all buoys found near the user's location. 

- Name: MyBuoyData

## Invocations

- report my buoy information
- report my buoy data
- describe my buoys
- provide my buoy information
- provide my buoy data
- give me my buoy information
- give me my buoy data
- can you give me my buoy information
- can ou give me my buoy data
- can you provide my buoy information
- can you provide my buoy data
- can you report my buoy informaiton
- can you report my buoy data

## Handler

```python
class MyBuoyDataIntentHandler(AbstractRequestHandler):
    """Handler that is triggered when the user asks for buoy data about the buoys
    that are close to their location. This will include variables such as:
    - wave height
    - period
    - water temperature
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("MyBuoyData")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
    
        geo_response = None
        
        # find my ip address, and from that pull the geographical location
        response = requests.get('https://api64.ipify.org?format=json')
        if response.status_code == 200:
            # successful, pull the ip address
            ipaddr = response.json()["ip"]
            
            # find the geo location
            response = requests.get(f'https://ipapi.co/{ipaddr}/json/')
            if response.status_code == 200:
                geo_response = response.json()

        
        if not geo_response:
            speak_output = MY_LOC_ERROR
        else:
            buoys = []
            # Find the list of the buoys near the location of the device
            if 'latitude' in geo_response and 'longitude' in geo_response:
                buoys = get_buoys_near_coordinates(
                    geo_response['latitude'],
                    geo_response['longitude']
                )
            elif 'city' in geo_response and 'region' in geo_response:
                buoys = get_buoys_near_location(
                    geo_response['city'],
                    geo_response['region']
                )
                
            
            if buoys:
                some_other_data = describe_buoys(buoys)
                # turn the data into a nice string

                speak_output = string_created_above
            else:
                speak_output = "I was not able to find any buoys near you."
        
        logger.info("Handling My Buoy Information")

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
```

**Note**: _Don't forget to add the new handler to the Skill Builder object._


# Buoys Near Location

The intent is intended to provide users with buoy ids near a city/state combination. 

## Invocations

- buoys close to {near_city} {near_state}
- buoys near {near_city} {near_state}
- what buoys are near {near_city} {near_state}
- what buoys are close to {near_city} {near_state}
- can you list the buoys near {near_city} {near_state}
- list the buoys near {near_city} {near_state}

## Handler

```python
class BuoysNearLocationIntentHandler(AbstractRequestHandler):
    """Handler to provide buoys that can be found close to a
    specific city/state location.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("BuoysNearLocation")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        city = handler_input.request_envelope.request.intent.slots["near_city"].value
        state = handler_input.request_envelope.request.intent.slots["near_state"].value
        
        # Use the same logic to get buoys from a specific location as above
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
```

**Note**: _Don't forget to add the new handler to the Skill Builder object._


# Data Near Location

The intent is intended to provide users with buoy data near a city/state combination. 

## Invocations

- report for {near_city} {near_state}
- can you provide a report for {near_city} {near_state}
- what is the report near {near_city} {near_state}
- what is the report for {near_city} {near_state}
- can you provide a report near {near_city} {near_state}
- report near {near_city} {near_state}

## Handler

```python
class DataNearLocationIntentHandler(AbstractRequestHandler):
    """Handler to provide information about buoys that can be found close to a
    specific city/state location.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DataNearLocation")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        city = handler_input.request_envelope.request.intent.slots["near_city"].value
        state = handler_input.request_envelope.request.intent.slots["near_state"].value
        
        # Use the same logic to describe buoys from a specific location as above

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
```

**Note**: _Don't forget to add the new handler to the Skill Builder object._


# Slot Types

The following slot types will be used for two of the intents above. 

## AMAZON.City

This is technically a built in type but the data should include all cities from the scripts in the [data directory](https://github.com/barbacbd/alexa-buoys/tree/main/data). 

- name: near_city

## AMAZON.US_STATE

This is technically a built in type but the data should include all states from the scripts in the [data directory](https://github.com/barbacbd/alexa-buoys/tree/main/data). 

- name: near_state


# Utility Functions

```python
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
```