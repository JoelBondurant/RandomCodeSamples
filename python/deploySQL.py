# A script to execute all the SQL DDL scripts which are needed in addition to what JPA does.
import pyodbc, os, sys, time


if (len(sys.argv) <= 1):
	databaseServer = 'SASERVER1\SQL2008R2'
	databaseName = 'imDev'
	userName = 'REMOVED'
	password = 'REMOVED'
	scriptPath = '.'
else:
	[scriptPath,databaseServer,databaseName,userName,password] = sys.argv[1:]

os.chdir(scriptPath)

dbConnectionString = "DRIVER={SQL Server};"
dbConnectionString += "SERVER=" + databaseServer + ";"
dbConnectionString += "DATABASE=" + databaseName + ";"
dbConnectionString += "UID=" + userName + ";"
dbConnectionString += "PWD=" + password
#print(dbConnectionString)
cnxn = pyodbc.connect(dbConnectionString)

printSQL = False
printNothing = True
printAllExceptions = False
tablePath = "../SQL/Tables/"
viewPath = "../SQL/Views/"
procPath = "../SQL/StoredProcs/"
functionPath = "../SQL/Functions/"

def executeSQL(fileName, sql):
	try:
		cursor = cnxn.cursor()
		cursor.execute(sql)
		cursor.close()
		cnxn.commit()
	except:
		err = sys.exc_info()
		if ((not printNothing) and printAllExceptions):
			print(err)
		elif ((not printNothing) and (-1 == str(err[1]).find("already"))):
			print(err)

def executePath(path):
	fileNames = os.listdir(path)
	for fileName in fileNames:
		if (not fileName.endswith(".sql")):
			continue
		f = open(path + fileName, "r")
		sql = f.read()
		f.close()
		msg = "Executing " + fileName
		if (printSQL):
			 msg += ":\n" + sql
		if (not printNothing):
			print(msg)
		executeSQL(fileName, sql)


executePath(tablePath)
executePath(viewPath)
executePath(procPath)
executePath(functionPath)
cnxn.close()
