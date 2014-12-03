import argparse
from geopy.geocoders import Nominatim
from itertools import izip
import csv
import re
import simplejson as json
import urllib2

# Add arguments for cli use
parser = argparse.ArgumentParser(description='Sift through data')
parser.add_argument('-t', dest="tripdat", help="input a .csv tripdata file to sift through")
parser.add_argument('-f', dest="faredat", help="input a .csv faredata file to sift through")
args = parser.parse_args()

# Line counter to keep track of line number in csv's
ctr = 0

_digits = re.compile('\d')
def contains_digits(d):
	return bool(_digits.search(d))

geolocator = Nominatim()

def getN(lat, lgt): #, errfile):
	url="http://api.geonames.org/neighbourhoodJSON?lat={0}&lng={1}&username=dbasner".format(lat,lgt)
	try:
		json_data = json.loads(urllib2.urlopen(url).readlines()[0])
		neighbourhood = json_data['neighbourhood']['name']
		print neighbourhood
		return neighbourhood
	except:
		try:
			location = geolocator.reverse(lat + ',' + lgt)
			location = location.address.split(',')
			if(contains_digits(location[2])):
				print location[3]
				return location[3]
			else:
				print location[2]
				return location[2]
		except:
			print json_data
			if(json_data['status']['value'] != 15):
				errWriter('Could not georesolve this lat/long: ' + str(lat) + ',' + str(lgt) + '\n')
				raise

def errWriter(string):
	with open('rawoutput_failures.txt' ,'w') as fd:
		fd.write(string)

# Open the tripdata and faredata files at the same time
with open(args.tripdat) as tripdat, open(args.faredat) as faredat:
	# Skip header lines
	next(faredat)
	next(tripdat)
	# Open new csv which will hold the raw output
	outputfile = open('rawoutput.csv', 'wb')
	output = csv.writer(outputfile, delimiter=',', quoting=csv.QUOTE_ALL)
	errfile = open('rawoutput_err.txt', 'w')
	# Initialize geo resolver
	# Go through each line in the fare and trip data
	for x, y in izip(tripdat, faredat):
		x_ori = x.strip()
		x = x_ori.split(',')
		y_ori = y.strip()
		y = y_ori.split(',')

		# To show that the program has not crashed and is working
		print('line ' + str(ctr) + '\tworking...')
		
		# If error occurs with geolocator, it will try again up to 10 times
		attempts = 0

		# Try 10 times to geolocate, else throw error and give up
		while (attempts < 10):
			try:
				# Gets the geolocation based on LAT/LONG
				location_dropoff = getN(x[-1], x[-2])
				location_pickup = getN(x[-3], x[-4])
				# Success cass, exit loop
				break
			# If the geo resolution times out
			except KeyboardInterrupt:
				exit()
			except:
				# Log a failed resolution
				print('failed to geo resolve line: ' + str(ctr) + '\t trying again until != 10 : #' + str(attempts))
				# Incrememt attempts
				attempts += 1
		if(attempts == 10):
			errfile.write("Failed to geo resolve line: " + str(ctr) + "\t containing this: " + x[-3] + ',' + x[-4] + '\t' + x[-1] + ',' + x[2] + '\n')
		
		# To show that the program has not crashed
		ctr += 1

		# Build output line for .csv
		output_line = x + y
		
		location_line = [location_pickup, location_dropoff]

		# Build full output here
		output_line += location_line

		print(output_line)

		# Write ROW, not write ROWS
		output.writerow(output_line)

		# Test with 15 lines - COMMENT OUT OR DELETE IN PRODUCTION
		if(ctr == 15):
			break


# Close line save file
outputfile.close()
errfile.close()
