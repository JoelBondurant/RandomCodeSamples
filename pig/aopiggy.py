# AnalyticObjects Pig User Defined Jython Functions
#https://pig.apache.org/docs/r0.11.0/udf.html

@outputSchema("word:chararray")
def TEST(arg):
	return 'Test %s!' % arg

@outputSchema("schema")
def COALESCE(*arg):
	for el in arg:
		if el is not None:
			return el
	return None

