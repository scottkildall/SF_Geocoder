import simplejson
import urllib
import csv


GEOCODE_BASE_URL = 'http://maps.google.com/maps/api/geocode/json'

# convert raw address string to JSON string
# Format is like this
# http://maps.googleapis.com/maps/api/geocode/json?address=16th+and+Bryant,+san+francisco&sensor=false
# expects a string like "16th+and+Bryant,+san+francisco"
# &key=" + API_KEY
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
def csvTranslate(csvInputFilename, csvOutputFileObj):
	with open(csvInputFilename, "rb") as file_obj:
		reader = csv.reader(file_obj)
		for row in reader:
			#print row[0]		-- row[0] = something like "York & 19th"
			lines =  row[0].split(' ' );
			# at this point, we will have somthing like: ['York', '&', '19th']
			# now add the correct format, like "York+and+19th,+san+francisco"
			sfAddress = lines[0] + "+and+" + lines[2] + ",+san+francisco"
			jsonLine = geocode(sfAddress,APIKEY)

			# these are our 4 values
			loc = row[0]
			lat = jsonLine['results'][0]['geometry']['location']['lat']
			lon = jsonLine['results'][0]['geometry']['location']['lng']
			vol = row[1]

			#print loc
			#print lat
			#print lon
			#print vol
			outLine = str(loc) + "," + str(lat) + "," + str(lon) + "," + str(vol) + "\n"
			csvOutputFileObj.write(outLine)
			print "Parsing: " + outLine

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
#geocode("16th+and+Bryant,+san+francisco")
#csvOutFileObj = open('cisterns_out.csv', 'wb')
#csvTranslate("cisterns_in.csv", csvOutFileObj)
#csvOutFileObj.close
print "Done!"
