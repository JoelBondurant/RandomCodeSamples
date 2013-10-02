/*
Author: Joel Bondurant
Company: REMOVED
Date: 2013-08-28
Summary: REMOVED
*/

/*(1.) Report Query:
	Resultset count: 26,692
*/
SELECT DATEPART(mm, ddd.ReportDate) AS [Month], 
	prop.ProposalId,
	pri.ProposalItemId,
	ddd.SiteId,
	pri.StartDate AS ProposalItemStartDate,
	pri.EndDate AS ProposalItemEndDate,
	SUM(ddd.Impressions) AS TotalImpressions,
	SUM(ddd.Clicks) AS TotalClicks,
	SUM(ddd.Revenue) AS TotalRevenue
FROM DailyDeliveryData ddd
JOIN ProposalItemMediaBuyMapping pimbm
ON (ddd.MediaBuyId = pimbm.MediaBuyId)
JOIN ProposalItem pri
ON (pri.ProposalItemEntityId = pimbm.ProposalItemEntityId AND pri.ParentProposalItemEntityId IS NULL)
JOIN Proposal prop
ON (prop.ProposalId = pri.ProposalId)
JOIN (
	SELECT ProposalId, MAX([Version]) AS MaxVersion
	FROM Proposal
	GROUP BY ProposalId) AS prf
ON (prf.ProposalId = prop.ProposalId AND prf.MaxVersion = prop.[Version])
WHERE DATEPART(yyyy, ddd.ReportDate) = DATEPART(yyyy, GETDATE())
GROUP BY DATEPART(mm, ddd.ReportDate), prop.ProposalId, pri.ProposalItemId, ddd.SiteId, pri.StartDate, pri.EndDate
ORDER BY [Month] DESC, TotalRevenue DESC;

/*(2.) Future Revenue Prediction Ideas:
	Simple linear regression over past 2-12 months of data, segmented by discrete variables.
	Multilinear regression over past 2-12 months of data, with each discrete variable transformed to a "dummy" variable.
	Nonlinear regression over past 2-12 months of data, segmented by discrete variables.
	30-90 Day Moving Average.
	30-90 Day Moving Average Weighted Against Older Data.
	Autoregressive modeling, on discrete variable segmented data.
*/

/*(3.) Super simple estimate for revenue per site category for next month:
*/
SELECT CDSCategoryId, AVG(TotalRevenue) AS RevenueEstimate
FROM (
	SELECT DATEPART(mm, ddd.ReportDate) AS [Month], sc.CDSCategoryId, SUM(ddd.Revenue) AS TotalRevenue
	FROM DailyDeliveryData ddd
	JOIN SiteCategories sc
	ON (ddd.SiteId = sc.SiteId)
	WHERE ddd.ReportDate > DATEADD(dd, -90, GETDATE())
	GROUP BY DATEPART(mm, ddd.ReportDate), sc.CDSCategoryId
	) AS srev
GROUP BY CDSCategoryId
ORDER BY CDSCategoryId ASC;



