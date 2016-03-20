-- Daily Rates Pig Calculation --
-- Analytic Objects 2014-09-23 --
-- ====================================================SETUP===================================================
set default_parallel <<CLUSTER_SIZE>>;
register file:/home/hadoop/pig/lib/piggybank.jar;
define CSVStorage org.apache.pig.piggybank.storage.CSVExcelStorage();
define UnixToISO org.apache.pig.piggybank.evaluation.datetime.convert.UnixToISO();
define ISOToUnix org.apache.pig.piggybank.evaluation.datetime.convert.ISOToUnix();
register s3://ao-code/aopiggy.py using jython as aoiggy;

-- I was joining in the Advertiser_UID from the dim_advertiser files, but will do so in a relational database.
-- =================================================IMPRESSIONS=================================================
-- Load raw DataXu impression data:
dx_imps_raw_wheader = load 's3n://ao-data/dataxu/*/fact_impressions/<<FILE_GLOB>>'
	using CSVStorage(',', 'YES_MULTILINE', 'NOCHANGE');

-- Filter out the header rows:
dx_imps_raw_woheader = filter dx_imps_raw_wheader by $0 != 'event_id';

-- Apply schema:
dx_imps_raw = foreach dx_imps_raw_woheader generate (chararray) $0 as event_id, (long) $1 as source_timestamp,
	(chararray) $2 as user_id, (chararray) $3 as created_dt, (int) $4 as hour, (chararray) $5 as campaign_uid,
	(chararray) $6 as flight_uid, (chararray) $7 as creative_uid, (chararray) $8 as site_name,
    (chararray) $9 as exchange_uid, (chararray) $10 as placement_uid, (chararray) $11 as winning_audience_uid,
    (int) $12 as metrocode_code, (chararray) $13 as country_code, (chararray) $14 as region_code,
    (chararray) $15 as postal_code, (double) $16 as micro_raw_spend, (chararray) $17 as ip_address,
    (chararray) $18 as page_url, (chararray) $19 as top_category, (chararray) $20 as dx_category_list,
    (chararray) $19 as exchange_publisher, (chararray) $20 as cookies, (chararray) $21 as user_agent_dim_uid;

-- Project DataXu impression data fields common to other sources for later combination:
dx_imps = foreach dx_imps_raw generate 'DATAXU' as source, source_timestamp, user_id, campaign_uid,
    flight_uid, creative_uid, 1L as impressions, micro_raw_spend;

-- Load Facebook impression data:
fb_imps_raw_wheader = load 's3n://ao-data/dataxu/*/fact_impressions_facebook/<<FILE_GLOB>>'
	using CSVStorage(',', 'YES_MULTILINE', 'NOCHANGE');

-- Filter out the header rows:
fb_imps_raw_woheader = filter fb_imps_raw_wheader by $0 != 'event_id';

-- Apply schema:
fb_imps_raw = foreach fb_imps_raw_woheader generate (chararray) $0 as event_id, (long) $1 as source_timestamp,
	(chararray) $2 as user_id, (chararray) $3 as created_dt, (int) $4 as hour, (chararray) $5 as campaign_uid,
	(chararray) $6 as flight_uid, $7 as creative_uid, (double) $8 as micro_raw_spend, (long) $9 as impressions;

-- Project Facebook impression data fields common to other sources for later combination:
fb_imps = foreach fb_imps_raw generate 'FACEBOOK' as source, source_timestamp, user_id, campaign_uid,
    flight_uid, creative_uid, impressions, micro_raw_spend;

-- Union DataXu and Facebook impressions to have everything in one place:
imps_prefilter = union dx_imps, fb_imps;

-- Parse dates:
imps_dated = foreach imps_prefilter generate source.., ToString(ToDate(REPLACE(UnixToISO(source_timestamp), 'T', ' '), 'yyyy-MM-dd HH:mm:ss.SSSZ', 'America/Los_Angeles'), 'yyyy-MM-dd') as datebin;

-- Date filter:
imps = filter imps_dated by (datebin >= '<<ISO_START_DATE>>') and (datebin < '<<ISO_END_DATE>>');

-- Group and aggregate results:
imps_grp = group imps by (datebin, campaign_uid, flight_uid, creative_uid);
imps_agg = foreach imps_grp generate FLATTEN(group) as (datebin, campaign_uid, flight_uid, creative_uid),
	SUM(imps.impressions) as impressions, (1e-6 * SUM(imps.micro_raw_spend)) as raw_spend;


-- ===================================================CLICKS===================================================
-- Load raw DataXu click data:
dx_clks_raw_wheader = load 's3n://ao-data/dataxu/*/fact_clicks/<<FILE_GLOB>>'
	using CSVStorage(',', 'YES_MULTILINE', 'NOCHANGE');

-- Filter out the header rows:
dx_clks_raw_woheader = filter dx_clks_raw_wheader by $0 != 'begin_event_id';

-- Apply schema:
dx_clks_raw = foreach dx_clks_raw_woheader generate (chararray) $0 as event_id, (chararray) $1 as end_event_id,
	(long) $2 as begin_source_timestamp, (long) $3 as end_source_timestamp, (long) $4 as attribution_value,
	(chararray) $5 as created_dt, (int) $6 as hour, (chararray) $7 as campaign_uid, (chararray) $8 as user_id,
    (chararray) $9 as flight_uid, (chararray) $10 as creative_uid, (chararray) $11 as site_name,
	(chararray) $12 as exchange_uid, (chararray) $13 as winning_audience_uid, (chararray) $14 as metrocode_code,
	(chararray) $15 as country_code, (chararray) $16 as region_code, (chararray) $17 as postal_code,
	(double) $18 as micro_raw_spend, (chararray) $19 as ip_address, (chararray) $20 as top_category,
	(chararray) $21 as dx_category_list, (chararray) $22 as exchange_publisher, (chararray) $23 as cookies,
	(long) $24 as impression_dt, (int) $25 as impression_hour, (chararray) $26 as page_url,
	(chararray) $27 as attribution_scope;

-- Project DataXu click data fields common to other sources for later combination:
dx_clks = foreach dx_clks_raw generate 'DATAXU' as source, begin_source_timestamp as source_timestamp, user_id,
	campaign_uid, flight_uid, creative_uid, 1L as clicks, micro_raw_spend;

-- Load Facebook click data:
fb_clks_raw_wheader = load 's3n://ao-data/dataxu/*/fact_clicks_facebook/<<FILE_GLOB>>'
		using CSVStorage(',', 'YES_MULTILINE', 'NOCHANGE');

-- Filter out the header rows:
fb_clks_raw_woheader = filter fb_clks_raw_wheader by $0 != 'begin_event_id';

-- Apply schema:
fb_clks_raw = foreach fb_clks_raw_woheader generate (chararray) $0 as begin_event_id,
	(chararray) $1 as end_event_id, (long) $2 as begin_source_timestamp, (long) $3 as end_source_timestamp,
    (long) $4 as attribution_value, (long) $5 as created_dt, (int) $6 as hour, (chararray) $7 as campaign_uid,
	(chararray) $8 as user_id, (chararray) $9 as flight_uid, (chararray) $10 as creative_uid,
	(double) $11 as micro_raw_spend, (chararray) $12 as impression_dt, (int) $13 as impression_hour,
    (int) $14 as cnt;

-- Project Facebook click data fields common to other sources for later combination:
fb_clks = foreach fb_clks_raw generate 'FACEBOOK' as source, begin_source_timestamp as source_timestamp, user_id,
	campaign_uid, flight_uid, creative_uid, cnt as clicks, micro_raw_spend;

-- Union DataXu and Facebook clicks to have everything in one place:
clks_prefilter = union dx_clks, fb_clks;

-- Parse dates:
clks_dated = foreach clks_prefilter generate source.., ToString(ToDate(REPLACE(UnixToISO(source_timestamp), 'T', ' '), 'yyyy-MM-dd HH:mm:ss.SSSZ', 'America/Los_Angeles'), 'yyyy-MM-dd') as datebin;

-- Date filter:
clks = filter clks_dated by (datebin >= '<<ISO_START_DATE>>') and (datebin < '<<ISO_END_DATE>>');

-- Group and aggregate results:
clks_grp = group clks by (datebin, campaign_uid, flight_uid, creative_uid);
clks_agg = foreach clks_grp generate FLATTEN(group) as (datebin, campaign_uid, flight_uid, creative_uid),
	SUM(clks.clicks) as clicks, (1e-6 * SUM(clks.micro_raw_spend)) as raw_spend;

-- ===================================================COMBINED===================================================
daily_rates_raw = join imps_agg by (datebin, campaign_uid, flight_uid, creative_uid) full outer,
	clks_agg by (datebin, campaign_uid, flight_uid, creative_uid);

daily_rates_coalesced = foreach daily_rates_raw generate
	aoiggy.COALESCE(imps_agg::datebin, clks_agg::datebin) as datebin,
	aoiggy.COALESCE(imps_agg::campaign_uid, clks_agg::campaign_uid) as campaign_uid,
	aoiggy.COALESCE(imps_agg::flight_uid, clks_agg::flight_uid) as flight_uid,
	aoiggy.COALESCE(imps_agg::creative_uid, clks_agg::creative_uid) as creative_uid,
	aoiggy.COALESCE(imps_agg::raw_spend, 0.0) + aoiggy.COALESCE(clks_agg::raw_spend, 0.0) as raw_spend,
	aoiggy.COALESCE(imps_agg::impressions, 0) as impressions,
	aoiggy.COALESCE(clks_agg::clicks, 0) as clicks;

-- Parallel 1 makes sure one reducer is used to produce a single aggregated output file.
daily_rates = order daily_rates_coalesced by datebin, campaign_uid, flight_uid, creative_uid parallel 1;

store daily_rates into 'daily_rates' using CSVStorage(',', 'YES_MULTILINE', 'UNIX');

-- Doesn't work via AWS, executed via ssh on master node.
--copyToLocal daily_rates daily_rates;

