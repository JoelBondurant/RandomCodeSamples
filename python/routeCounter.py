f = open("routes.txt","rt")

maxLen = 0
for x in f:
	rtes = x.split("\t")[2]
	a = len(rtes)
	b = len(rtes.replace(",",""))
	c = a - b
	if (c > maxLen):
		maxLen = c

print(maxLen)
f.close()