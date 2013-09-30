classdef DateTime < handle
	
	properties (SetAccess = private, GetAccess = private)
		dateVec;
		YearField = 1;
		MonthField = 2;
		DayField = 3;
		HourField = 4;
		MinuteField = 5;
		SecondField = 6;
	end
	
	methods
		function obj = DateTime(dateObj)
			if (nargin > 0)
				obj.dateVec = datevec(dateObj);
			else
				obj.dateVec = datevec(now);
			end
		end
		
		function year = getYear(obj)
			year = obj.dateVec(obj.YearField);
		end
		
		function month = getMonth(obj)
			month = obj.dateVec(obj.MonthField);
		end
		
		function day = getDay(obj)
			day = obj.dateVec(obj.DayField);
		end
		
		function hour = getHour(obj)
			hour = obj.dateVec(obj.HourField);
		end
		
		function hour = getMinute(obj)
			hour = obj.dateVec(obj.MinuteField);
		end
		
		function hour = getSecond(obj)
			hour = obj.dateVec(obj.SecondField);
		end
		
		function dateNum = toNumber(obj)
			dateNum = datenum(obj.dateVec);
		end
		
		function dateStr = toString(obj)
			dateStr = datestr(obj.dateVec, 'yyyy-mm-dd HH:MM:SS');
		end
		
		function dateVect = toVector(obj)
			dateVect = datevec(obj.toNumber());
		end
		
		function aCopy = copy(obj)
			aCopy = DateTime(obj.toVector());
		end
		
		function dtObj = addYears(obj, numYears)
			dtObj = DateTime(addtodate(obj.toNumber(), numYears, 'year'));
		end
		
		function dtObj = addMonths(obj, numMonths)
			dtObj = DateTime(addtodate(obj.toNumber(), numMonths, 'month'));
		end
		
		function dtObj = addDays(obj, numDays)
			dtObj = DateTime(addtodate(obj.toNumber(), numDays, 'day'));
		end
		
		function dtObj = addHours(obj, numHours)
			dtObj = DateTime(addtodate(obj.toNumber(), numHours, 'hour'));
		end
		
		function dtObj = addMinutes(obj, numMinutes)
			dtObj = DateTime(addtodate(obj.toNumber(), numMinutes, 'minute'));
		end
		
		function dtObj = addSeconds(obj, numSeconds)
			dtObj = DateTime(addtodate(obj.toNumber(), numSeconds, 'second'));
		end
		
		function ageInSecs = ageInSeconds(obj)
			ageInSecs = etime((datevec(now)), obj.dateVec);
		end
		
		function ageInHrs = ageInHours(obj)
			ageInHrs = obj.ageInSeconds() / 3600.0;
		end
	end
	
	
end

