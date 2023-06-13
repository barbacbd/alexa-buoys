# Future Work

This docuement is intended to be a placeholder for work currently under development and all future work.

# Table of Contents

  * [Future Intents](./Intents.md#intents)
  * [Persistent Data Storage](#persistent-data-storage)
      * [Challenges](#challenges)
  * [Accurate Device Locations](#accurate-device-locations)
  * [Specific Variables](#specific-variables)
  * [Keep Running](#keep-running)

# Persistent Data Storage

The Alexa web console provides access to dynamo databases. I want to be able to use this for persistent data to avoid (re)loading large json files each time that a query is executed. The amount of memory will greatly increase as well as the time to execute each query. 

## Challenges 

- Permissions with the database and developer account in general do not allow the assumed role used for the dynamo database to access the full list of capabilities

- The dynamo db is not allowing batch imports. There are currently a couple hunder thousand lines that need to be imported.

- There is only a single table currently allowed with the developer settings that I have. The app requires 2 tables at a minimum to expand to the capabilities that I would like to add.


# Accurate Device Locations

The device location currently appears to use the region where the skill is hosted. In the event that I execute a "my data" query:

- List my buoys
- List my buoy data
<br>
I receive a latitude/longitude or city/state result in Northern Virginia. If the same code is executed locally, I receive a very accurate location. This is indicating that the AWS machines are where the response is coming from. 


# Specific Variables

The skill currently provides the user with common variables, but there are many more to select from. Allow the user to select specific data if it is available. 

# Keep Running

Keep the app open on alexa until it is closed by the user. 