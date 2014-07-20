import simplejson
import urllib
import csv
import json

ELEVATION_BASE_URL = 'https://maps.google.com/maps/api/elevation/json'
API_KEY = 'AIzaSyB3DZsChl-uBjZ5QRAjI2YhUbrxuY2Rt_Q'

# convert raw address string to JSON string
# Format is like this
# http://maps.googleapis.com/maps/api/geocode/json?address=16th+and+Bryant,+san+francisco&sensor=false
# expects a string like "16th+and+Bryant,+san+francisco"
def geocode(address,sensor="false", **geo_args):
	geo_args.update({
				'address': address,
        'sensor': sensor
    })

	url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
	result = simplejson.load(urllib.urlopen(url))
	return result

# takes a filename, i.e. "data.csv"
# no header, 1st line is valid

# csvInputFilename format is
# row[0] = intersection
# row[1] = lat
# row[2] = long
# row[3] = volume
# we care about row[1] and fow[2]
def csvElevationOut(csvInputFilename, csvOutputFileObj):
	with open(csvInputFilename, "rb") as file_obj:
		reader = csv.reader(file_obj)
		for row in reader:
			print row[0]		# something like "York & 19th"
			#lines =  row[0].split(' ' );
			# at this point, we will have somthing like: ['York', '&', '19th']
			# now add the correct format, like "York+and+19th,+san+francisco"
			lat = row[1]
			lng  = row[2]
			jsonLine = get_elevation(lat,lng)
			
			#print jsonLine
			# these are our 4 values
			elevation = jsonLine['results'][0]['elevation']
			
			print row[0] + ": " +  row[1] + ", " + row[2] + " ele = " + str(elevation)
			
			outLine = row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + str(elevation) + "\n" 
			csvOutputFileObj.write(outLine)
			#print "Parsing: " + outLine

			#results': [{'geometry': {'location': {'lat': 37.7532962, 'lng': -122.4275

			#jsonFileObj.write(jsonLine.dumps())
			#jsonFileObj.write("\n")
			#jsonFileObj.write(row[0])
			#jsonFileObj.write("\n")





#  sensor=False, this is always the default
def get_elevation(lat, lng,):
	"""
    Returns the elevation of a specific location on earth using the Google
    Maps API.

    @param lat (float): The latitude of the location in degrees. Latitudes can
    take any value between -90 and 90.
    @param lng (float): The longitude of the location in degrees. Longitudes
    can take any value between -180 and 180.
    
    @return: A tuple (elevation, lat, lng, status):
      * elevation (float): The requested elevation in meters. If the location is
        on the sea floor the returned elevation has a negative value.
      * lat, lng (float): The latitude and longitude of the location (for testing
        purposes: must be equal to the input values).
      * status (str): Error code:
        "OK": the API request was successful.
        "INVALID_REQUEST": the API request was malformed.
        "OVER_QUERY_LIMIT": the requester has exceeded quota.
        "REQUEST_DENIED": the API did not complete the request, likely because
        of an invalid 'sensor' parameter.
        "UNKNOWN_ERROR": other error
      * If the error code 'status' is not 'OK' then all other members of the
        returned tuple are set to 'None'.

    @note: More information about the Google elevation API and its usage limits
    can be found in https://developers.google.com/maps/documentation/elevation/.
    
    @example:
    >>> round(get_elevation(-38.407, -25.297)[0], 2) == -3843.86
    True
    >>> round(get_elevation(37.32522, -104.98470)[0], 2) == 2934.24    
    True
    """
	URL_PARAMS = "locations=" + str(lat) + "," + str(lng) + "&key=" + API_KEY
	url = ELEVATION_BASE_URL + '?' + URL_PARAMS
	#urllib.urlencode(geo_args)
	print url
	#http://maps.google.com/maps/api/elevation/json?locations=37.7983359,-122.4030815&sensor=False%22

	result = simplejson.load(urllib.urlopen(url))
	return result


#result = simplejson.load(urllib.urlopen(url))
#return 0	#result

    ## make the call (ie. read the contents of the generated url) and decode the
    ## result (note: the result is in json format).
    ##with urllib.urlopen(url) as f:
     ##   response = json.loads(f.read().decode())

    ##status = response["status"]
    ##if status == "OK":
    ##    result = response["results"][0]
    ##    elevation = float(result["elevation"])
     ##   lat = float(result["location"]["lat"])
      ##  lng = float(result["location"]["lng"])
    ##else:
     ##   elevation = lat = lng = None
    ##return (elevation, lat, lng, status)

csvOutFileObj = open('cisterns_out.csv', 'wb')
csvElevationOut("cisterns_in.csv", csvOutFileObj)
csvOutFileObj.close


