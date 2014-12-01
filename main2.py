import sys
import os
import argparse
from geopy.geocoders import Nominatim
from itertools import izip
import csv

# Arguments here
parser = argparse.ArgumentParser(description='Sift through data')
parser.add_argument('-t', dest="tripdat", help="input a .csv tripdata file to sift through")
parser.add_argument('-f', dest="faredat", help="input a .csv faredata file to sift through")
parser.add_argument('--firstpass', dest="firstpass", action='store_false', default=False, help="first pass will build an excluded lines file and the rest will exist in an output .csv")
parser.add_argument('--secondpass', dest='secondpass', action='store_false', default=False, help="second pass to pick up all excluded lines")
parser.add_argument('--finalpass', dest='finalpass', action='store_false', default=False, help="to build a table for bins")
args = parser.parse_args()

ctr = 0

# Create an external file that saves all the lines that cannot be resolved
line_save = open('excludedlines.txt', 'w')

# To resolve first pass
if(args.firstpass):
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
			
			#print("TRIP: {0}\n\tFARE: {1}". format(x, y))

			# If error occurs with geolocator, it will write the line into a separate file
			try:
				location_pickup = geolocator.reverse(x[-3]+','+x[-4], timeout=15)
				location_dropoff = geolocator.reverse(x[-1]+','+x[-2], timeout=15)
			except:
				line_save.write(ctr)
			#print("PICKUP:\t\t" + location_pickup.address)		
			#print("DROPOFF:\t" + location_dropoff.address)

			# To show that the program has not crashed
			print('working...')

			ctr += 1
	
			# Build output line for .csv
			output_line = x + y
			output_line.append([location_pickup.address])
			output_line.append([location_dropoff.address])
		
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

# To resolve excluded lines
if(args.secondpass):
	with open(args.tripdat) as tripdat, open(args.faredat) as faredat:
		next(faredat)
		next(tripdat)
	outputfile = open('rawoutput.csv', 'a')
		
	# Take excluded line file and read it all as an array
	with open('excludedlines.txt' ,'r') as excludedlinesfile:
		excludedlines = excludedlinesfile.read()
	excludedlines = excludedlines.split('\n')

	output = csv.writer(outputfile)
	geolocator = Nominatim()
	for x, y in izip(tripdat, faredat):
		# If this line number is an excluded line, resolve it
		if(ctr in excludedlines):
			x = x.strip()
			x = x.split(',')
			y = y.strip()
			y = y.split(',')
			try:
				location_pickup = geolocator.reverse(x[-3]+','+x[-4], timeout=15)
				location_dropoff = geolocator.reverse(x[-1]+','+x[-2], timeout=15)
			except:
				line_save.write(ctr)
			print("PICKUP:\t\t" + location_pickup.address)		
			print("DROPOFF:\t" + location_dropoff.address)
	
			# Each line should be in one record in the .csv
			output_line = x + y
			output_line.append([location_pickup.address])
			output_line.append([location_dropoff.address])
		
			pickup_neigh = location_pickup.address.split(',')[2]
			dropoff_neigh = location_dropoff.address.split(',')[2]
	
			output_line.append([pickup_neigh])
			output_line.append([dropoff_neigh])
	
			output.writerows(output_line)
		# Increment ctr as line number
		ctr += 1	

# Final pass will open output .csv and take it and build an external file table that shows which bin to which bin
if(args.finalpass):
	nl_pu = []
	nl_do = []
	binoutput = open('binoutput.csv', 'wb')
	binoutput2 = csv.writer(binoutput)
	with open('rawoutput.csv' ,'r') as truefile:
		for line in truefile:
			binlines = [line[-2], line[-2]]
			# If the neighborhood exists in the list, take the index. Else, append it beforehand
			try:
				nl_pu.index(line[-2])
			except:
				nl_pu.append(line[-2])
			try:
				nl_do.index(line[-1])
			except:
				nl_do.append(line[-1])

			# TRUEFILE[19] SHOULD BE THE FARE AMT
			# Writes the the csv: bin# to bin# and fare
			binoutput2.writerows(nl_pu.index(line[-2]), nl_do.index(line[-1]), truefile[19])
	
	# Write the index of each item in the neighborhoods list
	with open('neigh_ref.txt' ,'wb') as ref_file:
		nlpu_ctr = 0
		nldo_ctr = 0
		# Write all pickup neighborhoods line by line
		ref_file.write("PICKUPS\n")
		for item in nl_pu:
			ref_file.write(nlpu_ctr + ":\t" + item)
			nlpu_ctr += 1
		# Write all dropoff neighborhoods line by line
		ref_file.write("\n\nDROPOFFS\n")
		for item in nl_do:
			ref_file.write(nldo_ctr + '\t' + item)
			nldo_ctr += 1

'''
	After all passes, you should have the raw output csv file, a excluded lines file, a bin output file, and a neighborhoods reference list.

'''
