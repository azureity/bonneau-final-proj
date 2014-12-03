import sys

i = 0

with open(sys.argv[1]) as filec:
	for line in filec:
		print(str(i))
		i+=1

