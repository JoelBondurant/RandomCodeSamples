// DataXu daily rates v3, the Apache-Spark version.
//=========================================SETUP=================================================
import sys.process._
import org.apache.spark.sql.{Row, SQLContext}
import org.apache.spark.sql.types.{StructField, StructType, StringType, LongType, DoubleType}

val base_path = "s3n://aiobj-data/dataxu/*/"
val file_glob = "<<FILE_GLOB>>" // e.g. "*_{20160331,20160401,20160402,20160403}_*"
// Notice template sets <{ISO_START_DATE}> and <{ISO_END_DATE}> below.

//=====================================IMPRESSIONS===============================================

// Load DataXu impressions:
val dx_imps_arrs = try {
	val dx_imps_path = base_path + "fact_impressions/" + file_glob
	val dx_imps_raw = sc.textFile(dx_imps_path)
	val dx_imps_arrs_tmp = dx_imps_raw.map(_.split(',').slice(1, 17)
		).filter(_(0) != "source_timestamp").map(x => Array(x(0), x(4), x(5), x(6), x(15), "1"))
	val dx_imps_force_eval = dx_imps_arrs_tmp.take(1)
	dx_imps_arrs_tmp
} catch {
	case ex: Exception => sc.emptyRDD[Array[String]]
}

// Load Facebook impressions:
val fb_imps_arrs = try {
	val fb_imps_path = base_path + "fact_impressions_facebook/" + file_glob
	val fb_imps_raw = sc.textFile(fb_imps_path)
	val fb_imps_arrs_tmp = fb_imps_raw.map(_.split(',').slice(1, 10)
		).filter(_(0) != "source_timestamp").map(x => Array(x(0), x(4), x(5), x(6), x(7), x(8)))
	val fb_imps_force_eval = fb_imps_arrs_tmp.take(1)
	fb_imps_arrs_tmp
} catch {
	case ex: Exception => sc.emptyRDD[Array[String]]
}

// Merge impressions into a DataFrame:
val imps_schema = StructType(Seq(
	StructField("source_timestamp", LongType, false),
	StructField("campaign_uid", StringType, false),
	StructField("flight_uid", StringType, false),
	StructField("creative_uid", StringType, false),
	StructField("micro_raw_spend", DoubleType, false),
	StructField("impressions", LongType, false)))

val imps_arrs = dx_imps_arrs.union(fb_imps_arrs)
val imps_typed = imps_arrs.map(x => 
	Array(x(0).toString.toLong, x(1).toString, x(2).toString, x(3).toString, x(4).toString.toDouble, x(5).toString.toLong))
val imps_all = sqlContext.createDataFrame(imps_typed.map(Row.fromSeq(_)), imps_schema)

// Spark-SQL has better date functions than scala/java7:
imps_all.registerTempTable("imps_all")
val imps_sqltxt = """
select 
to_date(from_utc_timestamp(to_utc_timestamp(from_unixtime(source_timestamp/1000.0), 'UTC'), 'America/Los_Angeles')) as datebin,
campaign_uid, flight_uid, creative_uid, micro_raw_spend, impressions 
from imps_all"""
val imps_dated = sqlContext.sql(imps_sqltxt)

// Done with impression math:
val imps_agg = imps_dated.groupBy("datebin","campaign_uid","flight_uid","creative_uid").agg(
	sum("micro_raw_spend").alias("imps_micro_raw_spend"), sum("impressions").alias("impressions"))

//========================================CLICKS=================================================

// Load DataXu clicks:
val dx_clks_arrs = try {
	val dx_clks_path = base_path + "fact_clicks/" + file_glob
	val dx_clks_raw = sc.textFile(dx_clks_path)
	val dx_clks_arrs_tmp = dx_clks_raw.map(_.split(',').slice(2, 19)
		).filter(_(0) != "begin_source_timestamp").map(x => Array(x(0), x(5), x(7), x(8), x(16), "1"))
	val dx_clks_force_eval = dx_clks_arrs_tmp.take(1)
	dx_clks_arrs_tmp
} catch {
	case ex: Exception => sc.emptyRDD[Array[String]]
}

// Load Facebook clicks:
val fb_clks_arrs = try {
	val fb_clks_path = base_path + "fact_clicks_facebook/" + file_glob
	val fb_clks_raw = sc.textFile(fb_clks_path)
	val fb_clks_arrs_tmp = fb_clks_raw.map(_.split(',').drop(2)
		).filter(_(0) != "begin_source_timestamp").map(x => Array(x(0), x(5), x(7), x(8), x(9), x(12)))
	val fb_clks_force_eval = fb_clks_arrs_tmp.take(1)
	fb_clks_arrs_tmp
} catch {
	case ex: Exception => sc.emptyRDD[Array[String]]
}

// Merge clicks into a DataFrame:
val clks_schema = StructType(Seq(
	StructField("source_timestamp", LongType, false),
	StructField("campaign_uid", StringType, false),
	StructField("flight_uid", StringType, false),
	StructField("creative_uid", StringType, false),
	StructField("micro_raw_spend", DoubleType, false),
	StructField("clicks", LongType, false)))

val clks_arrs = dx_clks_arrs.union(fb_clks_arrs)
val clks_typed = clks_arrs.map(x => 
	Array(x(0).toString.toLong, x(1).toString, x(2).toString, x(3).toString, x(4).toString.toDouble, x(5).toString.toLong))
val clks_all = sqlContext.createDataFrame(clks_typed.map(Row.fromSeq(_)), clks_schema)

// Spark-SQL has better date functions than scala/java7:
clks_all.registerTempTable("clks_all")
val clks_sqltxt = """
select 
to_date(from_utc_timestamp(to_utc_timestamp(from_unixtime(source_timestamp/1000.0), 'UTC'), 'America/Los_Angeles')) as datebin,
campaign_uid, flight_uid, creative_uid, micro_raw_spend, clicks 
from clks_all"""
val clks_dated = sqlContext.sql(clks_sqltxt)

// Done with click math:
val clks_agg = clks_dated.groupBy("datebin","campaign_uid","flight_uid","creative_uid").agg(
	sum("micro_raw_spend").alias("clks_micro_raw_spend"), sum("clicks").alias("clicks"))

//=======================================MERGE&OUTPUT===============================================
val dailyrates_raw = imps_agg.join(clks_agg, Seq("datebin", "campaign_uid", "flight_uid", "creative_uid"), "outer") 
dailyrates_raw.registerTempTable("dailyrates_raw")
val dr_sqltxt = """
select datebin, campaign_uid, flight_uid, creative_uid,
coalesce(1e-6*(imps_micro_raw_spend + clks_micro_raw_spend), 0.0) as raw_spend,
coalesce(impressions, 0) as impressions,
coalesce(clicks, 0) as clicks 
from dailyrates_raw
where datebin between '<<ISO_START_DATE>>' and '<<ISO_END_DATE>>'"""
val dailyrates = sqlContext.sql(dr_sqltxt).coalesce(1).map(
	x => Array(x(0).toString, x(1).toString, x(2).toString, x(3).toString, x(4).toString, x(5).toString, x(6).toString)
	).collect().toList.map(_.toList.map("\"" + _ + "\"").mkString("\t")).mkString("\n")
scala.tools.nsc.io.File("daily_rates.tsv").writeAll(dailyrates)
"aws s3 cp daily_rates.tsv s3://aiobj-export/daily_rates.tsv"!
