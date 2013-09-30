fin = open("routesRaw.txt", "r")

routes = {}
for x in fin:
	xs = x.split("\t")
	routeId = xs[1]
	operationId = xs[2]
	stepNumber = int(xs[3].replace("\n", ""))
	if (routeId in routes):
		routes[routeId].append(operationId)
	else:
		routes[routeId] = []
		routes[routeId].append(operationId)
	if (len(routes[routeId]) != stepNumber):
		input("err!")

fin.close()


fout = open("routes.txt", "w")

for routeId in routes:
	rowStr = "RTE\t" + routeId + "\t"
	for op in routes[routeId]:
		rowStr += "," + op
	fout.write(rowStr + "\n")

fout.close()

