/**
Spark solution to problem #4.
**/

import org.apache.spark.sql.SQLContext

val sqlc = new org.apache.spark.sql.SQLContext(sc)

// Load data:
val cols = Seq("ts","path","ref","cid")
val fn = "page-views.csv"
val pvs = sqlc.read.option("header","false").option("inferschema","true").csv(fn).toDF(cols: _*)

// Search counts:
val searchCounts = pvs.filter("ref is null").groupBy("path").count()

// Cheat with SparkSQL:
searchCounts.registerTempTable("SearchCounts")
val sqltxt = "select * from SearchCounts order by 2 desc, 1 asc limit 5"
val topSearches = sqlc.sql(sqltxt).coalesce(1).collect()

// Print results:
topSearches.foreach(println(_))

System.exit(0)

