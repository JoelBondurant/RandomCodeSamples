import aiobj.util.logger as logger
from aiobj.connectors.sql import SQL
import aiobj.model.googledisplaycost as googledisplaycost
import aiobj.model.prismaplacementsummary as prismaplacementsummary
import aiobj.model.placementcostcorrections as placementcostcorrections
import aiobj.model.prismadateplacementstats as prismadateplacementstats
import aiobj.model.placementcost as placementcost
import aiobj.model.sitecost as sitecost
import aiobj.model.campaigncost as campaigncost


def prep():
	"""Preparation steps for cost calculation."""
	try:
		logger.info('Cost compute preparation started.')
		logger.info('Started filling PrismaPlacementSummary.')
		prismaplacementsummary.fill()
		logger.info('Finished filling PrismaPlacementSummary.')
		logger.info('Started filling PrismaDatePlacementStats.')
		prismadateplacementstats.fill()
		logger.info('Finished filling PrismaDatePlacementStats.')
		logger.info('Started PrismaDatePlacementStats corrections.')
		prismadateplacementstats.push_corrections()
		logger.info('Finished PrismaDatePlacementStats corrections.')
		logger.info('Started marking PlacementCostCorrections computed.')
		placementcostcorrections.mark_computed()
		logger.info('Finished marking PlacementCostCorrections computed.')
		logger.info('Cost compute preparation finished.')
	except Exception as ex:
		logger.exception(ex, 'Cost Compute Preparation Critical Error.')
		raise


def compute():
	"""Compute all costs."""
	try:
		logger.info('Cost compute started.')
		logger.info('Started filling GoogleDisplayCosts.')
		googledisplaycost.fill()
		logger.info('Finished filling GoogleDisplayCosts.')
		logger.info('Computing placement costs...')
		placementcost.fill()
		logger.info('Computing site costs...')
		sitecost.fill()
		logger.info('Computing campaign costs...')
		campaigncost.fill()
		logger.info('Started marking PrismaDatePlacementStats computed.')
		prismadateplacementstats.mark_computed()
		logger.info('Finished marking PrismaDatePlacementStats computed.')
		logger.info('Cost compute finished.')
	except Exception as ex:
		logger.exception(ex, 'Cost Compute Critical Error.')
		raise


def score():
	"""Quality score costs."""
	logger.info('Scoring Google costs...')
	googledisplaycost.score()



