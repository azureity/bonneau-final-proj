import csv
import re

olist = list()

def toTup(tupl):
	return tuple(int(s) for s in tupl[1:-1].split(','))

def reved(tupl):
	return (tupl[1], tupl[0])

def inHold(tupl):
	for item in olist:
		if(item[0] == tupl) or (item[0] == reved(tupl)):
			return True
	return False

with open('finaloutput.csv', 'rb') as fd:
	fdreader = csv.reader(fd, delimiter=',', quotechar = "'")
	nond = re.compile(r'[^\d.]+')
	nond2 = re.compile(r'[^\d.,]+')
	ctr = 0

	for line in fdreader:
		bin_perm = ','.join([line[0], line[1]])
		bin_perm = bin_perm.replace('"', '')
		bin_perm = toTup(bin_perm)		

		pval = nond2.sub('', ','.join(line[-2:]))
		pval = pval.split(',')
		pval = (pval[0], pval[1])

		fares = list()
		for item in line[2:-2]:
			fares.append(nond.sub('', item))

		#print(bin_perm)
		#print(reved(bin_perm))

		if( not inHold(bin_perm)):
			olist.append([bin_perm, fares, [pval]])
		else:
			for item in olist:
				if(item[0] == bin_perm) or (item[0] == reved(bin_perm)):
					item[1] += fares
					item[2] += pval		

with open('basnerbins.csv', 'w') as fd:
	fdwriter = csv.writer(fd)
	fdwriter.writerows(olist)

