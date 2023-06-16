"""alexa-buoys License

Copyright (c) 2023 Brent Barbachem

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from sys import version_info


# The base variable is a map of the expected nautical.Buoy object
# variable to the actual name and the
BaseVariables = {
    "wvht": ["wave height", "feet"],
    "apd": ["period", "seconds"],
    "wtmp": ["water temperature", "degrees"]
}

OtherVariables = {
    "depth": ["depth", "feet"],
    "wwp": ["wind wave period", "seconds"],
    "swp": ["swell period", "seconds"],
    "wwh": ["wind wave height", "feet"],
    "swh": ["swell height", "feet"],
    "tide": ["tide", "feet"],
    "vis": ["visibility", "nautical miles"],
    "sal": ["salinity", "psu"],
    "dewp": ["dew point", "degrees"],
    "atmp": ["air temperature", "degrees"],
    "pres": ["pressure", "psi"],
    "dpd": ["dominant period", "seconds"],
    "wspd": ["wind speed", "knots"],
    "gst": ["gust", "knots"]
}


if version_info[0] == 3 and version_info[1] >= 9:
    TotalBuoyVariables = BaseVariables | OtherVariables
elif version_info[0] == 3 and version_info[1] >= 5:
    TotalBuoyVariables = {**BaseVariables, **OtherVariables}
else:
    TotalBuoyVariables = OtherVariables.copy()
    TotalBuoyVariables.update(BaseVariables)

ReverseVarsLookup = {value[0]: key for key, value in TotalBuoyVariables.items()}


def find_buoy_variable(spoken_buoy_var):
    """Find the variable in the buoy from spoken words.

    :param spoken_buoy_var: phrase entered by the user representing a buoy variable
    :return: The shortened name of the buoy variable or None when nothing was foudn
    """
    if spoken_buoy_var.lower() in ReverseVarsLookup:
        return ReverseVarsLookup[spoken_buoy_var.lower()]

    return None
