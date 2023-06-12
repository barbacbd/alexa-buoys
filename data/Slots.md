# Amazon Alexa Skill Slots

This document is provided as a reference to update/upload slot information when/if data has changed. To determine if data has changed, view the [homepage](https://github.com/barbacbd/alexa-buoys/). The number of buoys that have been updated will be listed in a badge. 
<br>
Start by executing the `slot_data.py` file: 

```bash
python3.x slot_data.py
```

This will produce files:
- buoy_slot.csv
- city_slot.csv
- state_slot.csv

<br>

The outputs are csv files that can be uploaded to the amazon alexa web console. On the left side of the screen select the drop down and find Slot Types. When you are on the Slot Types page, edit each slot and you can import values from a csv file. 