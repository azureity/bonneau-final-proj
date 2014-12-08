import csv

olist = list()
hold_list = list()

def reved(tupl):
	return ((tupl[1], tupl[0]))

with open('finaloutput.csv', 'rb') as fd:
	for line in fd:
		data = line.split('"')

		bin_perm = data[1]

		pval = data[5]

		if(data[2] == "'"):
			fares = data[3]
		else:
			fares = data[2] + data[3]
