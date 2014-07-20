import simplejson
import urllib
import csv

# this is for lat-long translation
GEOCODE_BASE_URL = 'https://maps.google.com/maps/api/geocode/json'

# this for elevation, both use the same API key
ELEVATION_BASE_URL = 'https://maps.google.com/maps/api/elevation/json'

# convert raw address string to JSON string
# expects a string like "16th+and+Bryant,+san+francisco" and the API key
# generates a valid URL
# http://maps.googleapis.com/maps/api/geocode/json?address=16th+and+Bryant,+san+francisco&sensor=false
# return will be something like:
# {'status': 'OK', 'results': [{'geometry': {'location': {'lat': 37.765618, 'lng': -122.4105284},
def geocode(address,apiKey, sensor="false", **geo_args):
	geo_args.update({
				'address': address,
        'sensor': sensor,
				'key' : apiKey
    })

	url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
	# print url		-- uncomment to see the URLs
	result = simplejson.load(urllib.urlopen(url))
	return result

def getElevationJSON(lat,lng,apiKey):
	URL_PARAMS = "locations=" + str(lat) + "," + str(lng) + "&key=" + apiKey
	url = ELEVATION_BASE_URL + '?' + URL_PARAMS
	result = simplejson.load(urllib.urlopen(url))
	return result

# returns the lat from the jsonLine
def latFromGeocode(jsonLine):
	return jsonLine['results'][0]['geometry']['location']['lat']

# returns the lat from the jsonLine
def lngFromGeocode(jsonLine):
	return jsonLine['results'][0]['geometry']['location']['lng']

# from the elevtion API
def eleFromJSON(jsonLine):
	# these are our 4 values
	return  jsonLine['results'][0]['elevation']

# write the headers:
def writeHeader(headers, csvOutputFileObj):
	firstOne = True
	for h in headers:
		if firstOne == True:
			csvOutputFileObj.write(h + ",lat,lng,ele")
			firstOne = False
		else:
			csvOutputFileObj.write("," + h)

	csvOutputFileObj.write("\n")

# e.g. "York & 19th"
# e.g. "S Van Ness & 19th"
# at this point, we will have somthing like: ['York', '&', '19th']
# now add the correct format, like "York+and+19th,+san+francisco"
def makeSFGeocode(geoLine):
		lines =  geoLine.split(' ');

		firstHalf = True
		secondWord = False

		firstPart = ""
		secondPart = ""

		for l in lines:
				if l == "&":
					firstHalf = False
					secondWord = False
				elif firstHalf == True:
					if secondWord == True:
							firstPart = firstPart + " "
					else:
							secondWord = True
					firstPart = firstPart + l
				else:
					if secondWord == True:
						secondPart = secondPart + " "
					else:
						secondWord = True
						secondPart = secondPart + l

		if secondPart == "":
			return firstPart
		else:
			return firstPart + "+and+" + secondPart

		#print row[0]		-- row[0] = something like "York & 19th"
		##lines =  row[0].split(' ' );
		# at this point, we will have somthing like: ['York', '&', '19th']
		# now add the correct format, like "York+and+19th,+san+francisco"
		##sfAddress = lines[0] + "+and+" + lines[2] + ",+san+francisco"
		#csvOutputFileObj.write(row[0] + "\n")


# takes a filename, i.e. "data.csv"
# no header, 1st line is valid
def csvTranslate(csvInputFilename, csvOutputFileObj, apiKey):
	with open(csvInputFilename, "rb") as file_obj:
		reader = csv.reader(file_obj)
		firstLine = True
		headerLine = ""		# this will be our header line, which we parse and write out

		print "Geocoding:"
		for row in reader:

			# skip first line, which is the header
			if firstLine == True:
					writeHeader(row,csvOutputFileObj)
					firstLine = False
			else:
					print(row[0])		# user output

					outLine = ""
					firstOne = True
					for r in row:
						if firstOne == True:
							sfGeocode = makeSFGeocode(r)
							#print sfGeocode

							geo_jsonLine = geocode(sfGeocode,apiKey)
							#print jsonLine
							lat = latFromGeocode(geo_jsonLine)
							lng = latFromGeocode(geo_jsonLine)
							ele_jsonLine = getElevationJSON(lat,lng,apiKey)
							ele = eleFromJSON(ele_jsonLine)

							outLine = outLine + r  + "," + str(lat) + "," + str(lng) + "," + str(ele)
							firstOne = False
						else:

							outLine = outLine + "," + r
							print "outline = " + outLine + " row = " + r
					outLine = outLine + "\n"
					csvOutputFileObj.write(outLine)



			#outLine = str(loc) + "," + str(lat) + "," + str(lon) + "," + str(vol) + "\n"
			#csvOutputFileObj.write(outLine)
			#print "Parsing: " + outLine

			#results': [{'geometry': {'location': {'lat': 37.7532962, 'lng': -122.4275

			#jsonFileObj.write(jsonLine.dumps())
			#jsonFileObj.write("\n")
			#jsonFileObj.write(row[0])
			#jsonFileObj.write("\n")

# reads first line of the API key file
def getAPIKey():
	# grab the last quote
	f = open("google_api_key.txt", "r")
	k = f.read()
	f.close
	return k.rstrip('\n')

APIKEY = getAPIKey()
#jsonLine = geocode("16th+and+Mission,+san+francisco", APIKEY)
csvOutFileObj = open('out.csv', 'wb')
csvTranslate("in.csv", csvOutFileObj,APIKEY)
csvOutFileObj.close
print "Done!"
