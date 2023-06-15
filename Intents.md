# Intents

The docuement provides a map of utterances to the intent.

# Table of Contents

  * [Buoy](#buoy)
  * [Buoys Near Location](#buoys-near-location)
  * [Data Near Location](#data-near-location)


# Buoy 

The intent will provide users with information about a specific buoy.

## Utterances

- buoy report for {buoy_id}
- what is the buoy report for {buoy_id}
- {buoy_id} report
- {buoy_id} buoy report
- can you provide the buoy report for {buoy_id}

## Input

- buoy_id - ID or name of the buoy 


# Buoys Near Location

The intent will provide users with the list of buoy IDs near a city/state combination.

## Utterances

- what buoys are near {near_city} {near_state}
- list buoys close to {near_city} {near_state}
- what buoys are close to {near_city} {near_state}
- list buoys near {near_city} {near_state}

## Input

- near_city - Name of the city
- near_state - Name of the state


# Data Near Location

The intent will:
- Find all buoys near the city/state combination
- For each buoy, get the data that the buoy provides
- Average the data into a single value for each variable.

## Utterances

- list buoy data near {near_city} {near_state}
- list data near {near_city} {near_state}

## Input

- near_city - Name of the city
- near_state - Name of the state
