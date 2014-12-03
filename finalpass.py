# Opens rawoutput.csv and builds the reference list + bins/fare .csv table

# Imports
import csv
from itertools import izip

# Neighborhood list
nl = []

# Taken from stackoverflow thread: http://stackoverflow.com/questions/8115261/how-to-remove-all-the-escape-sequences-from-a-list-of-strings/8115378#8115378
# Removes escape sequences from a string
def stripEscape(string):
	""" Removes all escape sequences from the input string """
	delete = ""
	i = 1
	while (i < 0x20):
		delete += chr(i)
		i += 1
	t = string.translate(None, delete)
	return t

# Count lines - can be used to cross-reference line numbers from output csv to neighborhoods reference
linectr = 1 

# Open rawoutput.csv in read mode
with open('rawoutput.csv', 'r') as src:
	# Open new file that will be the output
	outputfile = open('binoutput.csv', 'wb')
        output = csv.writer(outputfile, delimiter=',', quoting=csv.QUOTE_ALL)	
	# Read line by line
	for line in src:
		# Get the neighborhoods
		pickup_neigh = line.split(',')[-2]
		dropoff_neigh = line.split(',')[-1]
		
		# Parse through pickup neighborhood and strip all misc characters from it (e.g. escape characters, quotes, whitespace
		pickup_neigh = stripEscape(pickup_neigh).strip('"').lstrip()
		# If the neighborhood doesn't exist in our list yet, add it
		if(pickup_neigh not in nl):
			nl.append(pickup_neigh)
		# Do the same with dropoff neighborhood: sanitize dropoff_neigh
		dropoff_neigh = stripEscape(dropoff_neigh).strip('"').lstrip()
		# Add to list if does not exist
		if(dropoff_neigh not in nl):
			nl.append(dropoff_neigh)


		# Build output for time (4 hour long intervals starting from 12am)
		

		# Build the output line which is int he form: number, number, number : index of pickup, index of dropoff, fare cost
		output_line = [nl.index(pickup_neigh), nl.index(dropoff_neigh), line.split(',')[19]]		

		# Print to makes sure script hasn't crashed and to reference if needed
		print('Line ' + str(linectr) + '\t' + pickup_neigh + '\t' + dropoff_neigh)
	
		# Write the output into the .csv
		output.writerow(output_line)
	
		# Keep track of the line counter
		linectr += 1

# Close output file
outputfile.close()

# Build the reference list using an enumerated list that starts from 0 which essentially gives the index of each neighborhood
nle = enumerate(nl)
with open('neighborhood_ref.txt', 'w') as ref:
	for item in nle:
		ref.write(str(item) + '\n')
