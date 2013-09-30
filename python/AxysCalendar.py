from datetime import date
#Note that this is not the Julian calendar, not even close.

def getYMD(dayNumber):
    n = int(dayNumber)
    y = n//372 + 1900
    m = (n%372)//31 + 1
    d = n - (y - 1900)*372 - (m - 1)*31 + 1
    return (y, m, d)

def getDate(dayNumber):
    ymd = getYMD(dayNumber)
    return date(ymd[0], ymd[1], ymd[2])

def toAxysDayNumber(aYear, aMonth, aDay):
    y = (aYear - 1900)*372
    m = (aMonth - 1)*31
    d = (aDay - 1)
    return y + m + d