import csv

olist = list()
hold_list = list()

def reved(tupl):
	return ((tupl[1], tupl[0]))

with open('finaloutput.csv', 'rb') as fd:
	fdreader = csv.reader(fd, delimiter=',', quotechar = "'")
	for line in fdreader:
		bin_perm = ','.join([line[0], line[1]])
		bin_perm = bin_perm.replace('"', '')
	
		
	
		fares = line[2:-2]

		



'''
		if(bin_perm not in hold_list) or (reved(bin_perm) not in hold_list):
			hold_list.append(bin_perm)
			olist.append([bin_perm, fares, pval])

		else:
			for item in olist:
				if (item[0] == bin_perm) or (item[0] == reved(bin_perm)):
					item[1] += fares
'''		
