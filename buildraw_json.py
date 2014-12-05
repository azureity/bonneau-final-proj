import argparse
from itertools import izip
import csv
from shapely.geometry import Polygon
from shapely.geometry import MultiPoint
from shapely.geometry import Point
import json
import time

start_time = time.time()

# Add arguments for cli use
parser = argparse.ArgumentParser(description='Sift through data')
parser.add_argument('-t', dest="tripdat", help="input a .csv tripdata file to sift through")
parser.add_argument('-f', dest="faredat", help="input a .csv faredata file to sift through")
args = parser.parse_args()

# Line counter to keep track of line number in csv's
ctr = 0
errfile = open('rawoutput_err.txt' ,'w')

# Open JSON data to read
json_data = open('neighborhoods-shapedata.geojson')
data = json.load(json_data)

# Give this function a list of lists and it will generate a list of tuples
def toTuple(listoflists):
	return [tuple(x) for x in listoflists]	

# Make a dictionary of {neighborhood shape : neighborhood }
neighborhoods = dict()

# Populate the dictionary once
def buildN():
	jdat = data['features']
	for i in jdat:
		neighborhoods[Polygon(toTuple(i['geometry']['coordinates'][0]))] = i['properties']['neighborhood']

buildN()

# Gets the neighborhood based on lat/long comparing to polygons from the JSON data
def getN(lat, lgt, line_num):
	point = Point(lat, lgt)
	for key in neighborhoods:
		if point.within(key):
			return neighborhoods[key]
	print("Failed to find the neighborhood of this lat/long: " + str(lat) + "," + str(lgt) + "\tLine:" + str(line_num) + "\n")
        errfile.write("Failed to find the neighborhood of this lat/long: " + str(lat) + "," + str(lgt) + "\tLine:" + str(line_num) + "\n")

nl = []

def stripEscape(string):
        """ Removes all escape sequences from the input string """
        delete = ""
        i = 1
        while (i < 0x20):
                delete += chr(i)
                i += 1
        t = string.translate(None, delete)
        return t


# Open the tripdata and faredata files at the same time
with open(args.tripdat) as tripdat, open(args.faredat) as faredat:
	# Skip header lines
	next(faredat)
	next(tripdat)
	# Open new csv which will hold the raw output
	outputfile = open('rawoutput.csv', 'wb')
	output = csv.writer(outputfile, delimiter=',', quoting=csv.QUOTE_ALL)

	binoutputfile = open('binoutput.csv', 'wb')
	binoutput = csv.writer(binoutputfile, delimiter=',', quoting=csv.QUOTE_ALL)
	# Go through each line in the fare and trip data
	for x, y in izip(tripdat, faredat):
		x_ori = x.strip()
		x = x_ori.split(',')
		y_ori = y.strip()
		y = y_ori.split(',')

		# To show that the program has not crashed and is working
		print('line ' + str(ctr) + '\tworking...')
		
		# Launch function to get the neighborhood based on lat/long
		location_pickup = getN(float(x[-4]),float(x[-3]), ctr)
		location_dropoff = getN(float(x[-2]), float(x[-1]), ctr)

		# Logging
		print(location_pickup)
		print(location_dropoff)

		# To show that the program has not crashed
		ctr += 1

		# Build output line for .csv
		output_line = x + y
		
		location_line = [location_pickup, location_dropoff]

		# Build full output here
		output_line += location_line

		#print(output_line)

		# Write ROW, not write ROWS
		output.writerow(output_line)


		if(location_pickup not in nl):
                        nl.append(location_pickup)
                if(location_dropoff not in nl):
                        nl.append(location_dropoff)

		binoutputline = [nl.index(location_pickup), nl.index(location_dropoff), output_line[19]]

		binoutput.writerow(binoutputline)
		print("Bin output writing line: " + str(ctr))


		# Test with 15 lines - COMMENT OUT OR DELETE IN PRODUCTION
		if(ctr == 1000):
			break


# Close opened files
outputfile.close()
json_data.close()
binoutputfile.close()

nle = enumerate(nl)
with open('neighborhood_ref.txt', 'w') as ref:
        for item in nle:
                ref.write(str(item[0]) + '\t' +  str(item[1]) + '\n')


print("Time it took to run (in seconds): " + str(time.time() - start_time))
