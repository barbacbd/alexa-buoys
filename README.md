# Alexa Buoy Skill

![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/barbacbd/13b743bab03c7a43a72994b1512a112e/raw/AvailableBuoys.json) ![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/barbacbd/09fbedcdba4bab564596abfdd22d35e2/raw/AvailableCities.json)
![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/barbacbd/7e85f87f1f599809fd45d9ef75e9ef42/raw/DynamicBuoyBadgeData.json) 

An Alexa Skill to retrieve buoy information. The skill is built around the base library [nautical](https://github.com/barbacbd/nautical). 

# Using the skill

The user will open the skill on the alexa by stating:

"nautical data"
<br>

After the skill has been opened the user can ask or state any of the uterrances found [here](./Intents.md). For example:

"{buoy_id} report" 
<br>

If the data is found, alexa will read the [returned data](#data-provided) back to the user.

<br>
<h1 align="center">
  <a>
    <img src="https://github.com/barbacbd/alexa-buoys/blob/53009b2a9cd8e0f6b0b635ed465452e6d90aadad/.images/model.jpeg" width="512" height="128" >
  </a>
</h1>

For more information about intents view the following [page](./Intents.md).

# Skill Uses

The following is a list of examples where the skill may be useful:

- Surfing
- Fishing
- Beach Days
- Research

# Data Provided

The current information that can be provided from a buoy is concise.

- Wave Height
- Period
- Water Temperature