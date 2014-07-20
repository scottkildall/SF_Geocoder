SF_Geocoder
========

Given CSV of street intersections **in San Francisco**, this will encode lat, long and elevation fields using Google Map API Keys

by Scott Kildall

**Input CSV** 
This should be called "input.csv"

It should have a header, which describes each column
Column 1: this should always be the intersection, using the format: "Bryant & 16th" or "S Van Ness & 15th". Always use an ampersand for the street names.

Column 2, 3, 4, etc can be any custom data. This will be saved to the output CSV

**What it does** 
(1) Google Maps will translate this intersection to a lat, long. We always add ", SF" to the end so that it knows this is San Francisco

(2) From the lat + long, we use the Google Elevate API to get an elevation, in feet.

(3) Creates a CSV with this new info in it and copies the old one.

**Output CSV** 
This should be called "output.csv"

Headers will be preserved, with "lat", "lng" and "ele" added for lat, long and elevation

Column 1 = Street intersection
Column 2 = Latitude, floating point number
Column 3 = Longitude, floating point number
Column 4 = Elevation, floating point number
Other columns, match the input CSV

**API Keys**
I have garbage keys, in the file: "google_api_key.txt". You'll want to request your own from the Google Maps API.
