f = open("flowsFromMathematica.txt", "rt")
flowStr = f.read()
f.close()

flowStr = flowStr.replace("\"", "") #remove quotes
flowStr = flowStr.replace(" ", "") #remove spaces
flowStr = flowStr.replace("\n", "") #remove line breaks
flowStr = flowStr[1:-1] #remove brakets

flows = flowStr.split("},{")
flows[0] = flows[0].replace("{", "")
flows[-1] = flows[-1].replace("}", "")


f = open("flowsFromMathematica4Db.txt", "wt")

clusterNumber = 0
for flow in flows:
	clusterNumber += 1
	ops = flow.split(",")
	stepNumber = 0
	for op in ops:
		stepNumber += 1
		f.write(str(clusterNumber) + "\t" + op + "\t" + str(stepNumber) +"\n")



f.close()