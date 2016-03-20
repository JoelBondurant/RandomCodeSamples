"""
CreativeMeasureHistoryWeekly wrapper.
"""
from analyticobjects.connectors.sql import SQL
from analyticobjects.util import logger

TABLE_NAME = 'CreativeMeasureHistoryWeekly'

FILL_SQL = """
# Denormalize Creative Measures:
INSERT INTO tgolap.CreativeMeasureHistoryWeekly (
	yearbin, weekbin, advertiser_id, campaign_id, site_id, placement_id, creative_id, activity_id,
	impressions, clicks, click_conversions, view_conversions, click_revenue, view_revenue, cost
)
SELECT iso_year(dt.date), iso_week(dt.date), gd.advertiser_id, gd.campaign_id, gd.site_id,
	pgpj.prisma_placement_id, gd.creative_id, gd.activity_id,
	SUM(gd.impressions), SUM(gd.clicks), SUM(gd.click_conversions), SUM(gd.view_conversions),
	SUM(gd.click_revenue), SUM(gd.view_revenue), COALESCE(SUM(gc.actual_cost),0)
FROM GoogleDisplayAllByGeo gd
JOIN `Date` dt
	ON (dt.date_id = gd.date_id)
JOIN PrismaGooglePlacementJunction pgpj
	ON (gd.placement_id = pgpj.google_placement_id)
LEFT JOIN GoogleCost gc
	ON (gd.id = gc.id)
WHERE iso_year(dt.date) = %s AND iso_week(dt.date) = %s
	AND pgpj.prisma_placement_id IS NOT NULL
GROUP BY iso_year(dt.date), iso_week(dt.date), gd.advertiser_id, gd.campaign_id, gd.site_id,
	pgpj.prisma_placement_id, gd.creative_id, gd.activity_id
ON DUPLICATE KEY UPDATE
	impressions = VALUES(impressions), clicks = VALUES(clicks), click_conversions = VALUES(click_conversions),
	view_conversions = VALUES(view_conversions), click_revenue = VALUES(click_revenue),
	view_revenue = VALUES(view_revenue), cost = VALUES(cost);
"""

def denormalize(week_range):
	try:
		logger.info('%s fill started.' % TABLE_NAME)
		sql = SQL()
		sql.execute_batches(FILL_SQL, week_range)
		sql.commitclose()
		logger.info('%s fill finished.' % TABLE_NAME)
	except Exception as ex:
		logger.exception(ex, 'Critical error in denormalization: %s' % TABLE_NAME)
