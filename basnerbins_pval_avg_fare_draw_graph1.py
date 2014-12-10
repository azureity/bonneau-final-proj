import csv
import re

import networkx as nx
import matplotlib
import matplotlib.pyplot as plt


olist = list()
new_list_avg_price=[]
new_list_p_values=[]

def toTup(tupl):
	return tuple(int(s) for s in tupl[1:-1].split(','))

def reved(tupl):
	return (tupl[1], tupl[0])

def inHold(tupl):
	for item in olist:
		if(item[0] == tupl) or (item[0] == reved(tupl)):
			return True
	return False
print "begin"
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
		#print bin_perm

		if bin_perm[0]==bin_perm[1]:
			#print "BREAKING"
			continue;

		fares = list()
		for item in line[2:-2]:
			fares.append(nond.sub('', item))

		#print(bin_perm)
		#print(reved(bin_perm))

		if( not inHold(bin_perm)):
			L=[float(n) for n in fares if n]
			#print "L"
			#print L
			#print sum(L)
			#print len(L)
			#print sum(L)/len(L
			#	)
			ave = sum(L)/len(L) 

			#print "average"
			#print ave
			#print 
			olist.append([bin_perm, ave, [pval]])
		else:
			for item in olist:
				if(item[0] == bin_perm) or (item[0] == reved(bin_perm)):
					item[1] = ave
					item[2] += pval		

#round(float(el[2][0][1]),5)
	count=0;
	count2=0
	for item in olist:
		avg_price=round(item[1],3);
		p_value= round(float(item[2][0][1]),3);
		#print p_value
		if(avg_price>75 and item[0][0]!=35 and item[0][1]!=35 and count2 <20 ):
			count2+=1
			new_list_avg_price.append(item[0]+(round(item[1],3),))
		if (count<20 and item[0][0]!=35 and item[0][1]!=35 ):# and count<30):
			count+=1
			print p_value
			new_list_p_values.append(item[0]+(p_value,))

print olist[0]
print new_list_avg_price[0]
print len(new_list_avg_price)
print len(new_list_p_values)



#print olist[0][3]

#with open('basnerbins_avg_fare.csv', 'w') as fd:
#	fdwriter = csv.writer(fd)
#	fdwriter.writerows(olist)

