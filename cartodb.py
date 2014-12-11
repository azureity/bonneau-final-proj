import csv
import re

olist = list()

def toTup(tupl):
	return tuple(int(s) for s in tupl[1:-1].split(','))

def reved(tupl):
	return (tupl[1], tupl[0])

def inHold(num):
	for item in olist:
		if item[0] == num:
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

		if(not inHold(bin_perm[0])):
			olist.append([bin_perm[0], fares])
		else:
			for item in olist:
				if(bin_perm[0] == item[0]):
					item[1] += fares

for item in olist:
	item[1] = map(float, item[1])
	item[1] = round(sum(item[1]) / len(item[1]), 2)


def getNeighs():
	tmp = list()
	nl = dict()
	
	with open('neighborhood_ref.txt', 'r') as fd:
		fr = fd.read()
		tmp = fr.split('\n')
	del tmp[-1]
	for item in tmp:
		tmpitem = item.split('\t')
		nl[tmpitem[0]] = tmpitem[1]
	return nl	

nlist = getNeighs()
for item in olist:
	item[0] = nlist[str(item[0])]

with open('cartodboutput.csv', 'w') as fd:
	fdwriter = csv.writer(fd)
	fdwriter.writerow(['neighborhood', 'average_fare'])
	fdwriter.writerows(olist)

