import sys
import os
import argparse
from geopy.geocoders import Nominatim


parser = argparse.ArgumentParser(description='Sift through data')
parser.add_argument('-t', dest="tripdat", required=True, help="input a .csv tripdata file to sift through")
parser.add_argument('-f', dest="faredat", required=True, help="input a .csv faredata file to sift through")
args = parser.parse_args()

with open(args.tripdat) as tripdat:
	with open(args.faredat) as faredat:
		geolocator = Nominatim()
					
	

