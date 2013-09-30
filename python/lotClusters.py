f = open("clustersFromMathematica.txt", "rt")
clusterStr = f.read()
f.close()

clusterStr = clusterStr.replace("\"", "") #remove quotes
clusterStr = clusterStr.replace(" ", "") #remove spaces
clusterStr = clusterStr.replace("\n", "") #remove line breaks
clusterStr = clusterStr[1:-1] #remove brakets

clusters = clusterStr.split("},{")
clusters[0] = clusters[0].replace("{", "")
clusters[-1] = clusters[-1].replace("}", "")


f = open("clustersFromMathematica4Db.txt", "wt")

clusterNumber = 0
for cluster in clusters:
	clusterNumber += 1
	lots = cluster.split(",")
	for lot in lots:
		f.write(str(clusterNumber) + "\t" + lot + "\n")



f.close()