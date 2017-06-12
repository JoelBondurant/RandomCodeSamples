/**
 GitHub Problem 4 in Spark.
**/

import org.apache.spark.sql.SparkSession


def main() {
	val ss = SparkSession.builder().getOrCreate()

	// Load data:
	val fileName = "page-views.csv"
	val header = Seq("ts","path","ref","cid")
	val pageViews = ss.read.option("header","false").option("inferschema","true").csv(fileName).toDF(header: _*)

	// Search counts:
	val searchCounts = pageViews.filter("ref is null").groupBy("path").count()

	// Cheat with SparkSQL:
	searchCounts.createOrReplaceTempView("SearchCounts")
	val sqlTxt = "select * from SearchCounts order by 2 desc, 1 asc limit 5"
	val topSearches = ss.sql(sqlTxt).coalesce(1).collect()
	// May need an additional layer of sum & merge sort for huge datasets...
	
	// Print results and exit:
	topSearches.foreach(println(_))
	System.exit(0)
}


main()
