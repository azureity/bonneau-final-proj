import sys
import os
import argparse
from geopy.geocoders import Nominatim
from itertools import izip
import csv


parser = argparse.ArgumentParser(description='Sift through data')
parser.add_argument('-t', dest="tripdat", help="input a .csv tripdata file to sift through")
parser.add_argument('-f', dest="faredat", help="input a .csv faredata file to sift through")
args = parser.parse_args()

ctr = 0

neighlist_pickup = []
neighlist_dropoff = []
				
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
		location_pickup = geolocator.reverse(x[-3]+','+x[-4])
		location_dropoff = geolocator.reverse(x[-1]+','+x[-2])
		print("PICKUP:\t\t" + location_pickup.address)		
		print("DROPOFF:\t" + location_dropoff.address)
		ctr += 1
		output_line = [x, y]
		output_line.append([location_pickup.address])
		output_line.append([location_dropoff.address])
	
		pickup_neigh = location_pickup.address.split(',')[2]
		dropoff_neigh = location_dropoff.address.split(',')[2]

		output_line.append([pickup_neigh])
		output_line.append([dropoff_neigh])

		output.writerows(output_line)
		if(ctr == 15):
			break
'''
		if(pickup_neigh in neighlist_pickup):
			output_line.append(neighlist_pickup.index(pickup_neigh))
		else:
			neighlist_pickup.append(pickup_neigh)
			output_line.append(neighlist_pickup.index(pickup_neigh))

		if(dropoff_neigh in neighlist_dropoff):
			output_line.append(neighlist_dropoff.index(dropoff_neigh))
		else:
			neighlist_dropoff.append(dropoff_neigh)
			output_line.append(neighlist_dropoff.index(dropoff_neigh))

		output.writerows(output_line)


		if(ctr == 15):
			outputfile.close()
			break
'''

ref_file = open('neigh_ref.txt', 'wb')
ref_file.write(neighlist_pickup)
ref_file.write(neighlist_dropoff)
ref_file.close()
