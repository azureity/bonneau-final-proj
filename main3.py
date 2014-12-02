import sys
import os
import argparse
from geopy.geocoders import Nominatim
from itertools import izip
import csv
import time

# Arguments here
parser = argparse.ArgumentParser(description='Sift through data')
parser.add_argument('-t', dest="tripdat", help="input a .csv tripdata file to sift through")
parser.add_argument('-f', dest="faredat", help="input a .csv faredata file to sift through")
args = parser.parse_args()

ctr = 0

# Create an external file that saves all the lines that cannot be resolved
line_save = open('excludedlines.txt', 'w')

# To resolve first pass
with open(args.tripdat) as tripdat, open(args.faredat) as faredat:
	next(faredat)
	next(tripdat)
	outputfile = open('rawoutput.csv', 'wb')
	output = csv.writer(outputfile, delimiter=',', quoting=csv.QUOTE_ALL)
	geolocator = Nominatim()
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
				location_pickup = geolocator.reverse(x[-3] + ',' + x[-4])
				location_dropoff = geolocator.reverse(x[-1] + ',' + x[-2])
				
				print(location_pickup.address)
				print(location_dropoff.address)
				break
			except geopy.exc.GeocoderTimedOut:
				print('failed to geo resolve line: ' + str(ctr) + '\t trying again until != 10 : #' + str(attempts))
				attempts += 1
		
		# To show that the program has not crashed
		ctr += 1

		# Build output line for .csv
		output_line = x + y
		location_line = [location_pickup.address.split(',')[2], location_dropoff.address.split(',')[2], location_pickup.address, location_dropoff.address]

		output_line += location_line

		# Write ROW, not write ROWS
		output.writerow(output_line)

		# Test with 15 lines
		if(ctr == 15):
			break

L = []

binfile = open('binoutput.csv', 'wb')
bins = csv.writer(binfile, delimiter=',', quoting=csv.QUOTE_ALL)

with open('rawoutput.csv', 'rb') as rawdata:
	reader = csv.reader(rawdata, delimiter=',',quotechar='|')
	for row in reader:
		new_output_line = []

		if (row[25] in L):
			new_output_line.append(L.index(row[25]))
		else:
			L.append(row[25])
			new_output_line.append(L.index(row[25]))

		if (row[26] in L):
			new_output_line.append(L.index(row[26]))
		else:
			L.append(row[26])
			new_output_line.append(L.index(row[26]))

		new_output_line.append(row[19])

		bins.writerow(new_output_line)

		#print(L)



# Close line save file
line_save.close()
