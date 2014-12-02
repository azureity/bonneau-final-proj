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
	output = csv.writer(outputfile)
	geolocator = Nominatim()
	for x, y in izip(tripdat, faredat):
		x = x.strip()
		x = x.split(',')
		y = y.strip()
		y = y.split(',')
		
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
			except:
				print('failed to geo resolve line: ' + ctr)
				attempts += 1
		
		# To show that the program has not crashed
		print('line ' + ctr + '\tworking...')
		ctr += 1

		# Build output line for .csv
		output_line = x + y
		output_line.append([str(location_pickup.address)])
		output_line.append([str(location_dropoff.address)])
	
		pickup_neigh = location_pickup.address.split(',')[2]
		dropoff_neigh = location_dropoff.address.split(',')[2]

		# These are the bins (neighborhoods)
		output_line.append([pickup_neigh])
		output_line.append([dropoff_neigh])

		output.writerows(output_line)

		# Test with 15 lines
		if(ctr == 15):
			break

# Close line save file
line_save.close()
