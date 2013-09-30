f = open("rawFlowData.txt","rt")
lotFile = open("lots4Mathematica.txt","wt")
opFile = open("operations4Mathematica.txt","wt")
devFile = open("devices4Mathematica.txt","wt")

minOpChainSize = 4
lotSet = set()
ops = {}
devs = {}

for x in f:
	xs = x.split("\t")
	lot = xs[0]
	dev = xs[1]
	op = xs[2]
	prodUse = xs[3].replace("\n", "")
	if (lot in devs):
		if (not devs[lot] == dev):
			continue # skip reworks
	else:
		if (not prodUse == "PROD"):
			continue # skip non-PROD lots
		devs[lot] = dev
	lotSet.add(lot)
	if (lot not in ops):
		ops[lot] = []
	if (op not in ops[lot]):
		ops[lot].append(op)

f.close()

lots = []
lots.extend(lotSet)

for lot in lots:
	if (len(ops[lot]) < minOpChainSize):
		continue # filter out short chains
	devFile.write(devs[lot] + "\n")
	lotFile.write(lot + "\n")
	for op in ops[lot]:
		opFile.write(op + "\t")
	opFile.write("\n")

devFile.close()
lotFile.close()
opFile.close()
