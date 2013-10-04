package com.sensoranalytics.commons;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

/**
 * A class to manipulate time and dates.
 *
 * @author Joel Bondurant
 * @version 2011.0317
 * @since 1.0
 */
public class TimeUtility {

	private TimeUtility() {} // makes sure that no one tries to instantiate this.

	/**
	 * A regEx for a date-time string.
	 */
	public static final String STANDARD_DATE_REGEX = "20\\d{2}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d{0,3})?";

	/**
	 * A standard date pattern.
	 */
	public static final String STANDARD_DATE_PATTERN = "yyyy-MM-dd'T'HH:mm:ss";

	/**
	 * A date pattern used for file names.
	 */
	public static final String FILENAME_DATE_PATTERN = "yyyyMMdd'T'HHmmss";

	/**
	 * A date formatter object.
	 */
	public static final SimpleDateFormat standardDateFormat = new SimpleDateFormat(STANDARD_DATE_PATTERN);

	/**
	 * A date formatter object.
	 */
	public static final SimpleDateFormat fileNameDateFormat = new SimpleDateFormat(FILENAME_DATE_PATTERN);

	/**
	 * Convenience method to parse a date-time string to a Date object.
	 *
	 * @param dateString A string representing a date time in "yyyy-MM-dd'T'hh:mm:ss" format.
	 * @return The date corresponding to the string.
	 * @throws ParseException Thrown if the string cannot be parsed to a date.
	 */
	public static Date stdString2date(String dateString) throws ParseException {
		return standardDateFormat.parse(dateString);
	}

	/**
	 * Convert a date to a string.
	 *
	 * @param aDate Any date.
	 * @return A string in 'standard' format.
	 */
	public static String date2StdString(Date aDate) {
		return standardDateFormat.format(aDate);
	}

	/**
	 * Convert a date to a string with specified format string.
	 *
	 * Format string examples:
	 * STANDARD_DATE_PATTERN = "yyyy-MM-dd'T'HH:mm:ss";
	 * FILENAME_DATE_PATTERN = "yyyyMMdd'T'HHmmss";
	 *
	 * @param aDate A date to format.
	 * @param dateFormatString A date formatting string.
	 * @return A String of the result.
	 */
	public static String date2FmtString(Date aDate, String dateFormatString) {
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat(dateFormatString);
		return simpleDateFormat.format(aDate);
	}

	/**
	 * Convert file name date string to Date.
	 *
	 * @param dateString A file name date string.
	 * @return The corresponding date.
	 * @throws ParseException
	 */
	public static Date fileNameString2date(String dateString) throws ParseException {
		return fileNameDateFormat.parse(dateString);
	}

	/**
	 * Convert a date to a filename date.
	 *
	 * @param aDate Any date.
	 * @return String file name representation.
	 */
	public static String date2FileNameString(Date aDate) {
		return fileNameDateFormat.format(aDate);
	}

	/**
	 * Return the time difference in seconds between two dates.
	 *
	 * @param startDate Start date.
	 * @param endDate End date.
	 * @return Time difference in seconds.
	 */
	public static Long timeDifferenceInSeconds(Date startDate, Date endDate) {
		if (startDate == null || endDate == null) {
			return null;
		}
		return (endDate.getTime() - startDate.getTime()) / (1000L) ;
	}

	/**
	 * Add hours to a date by value.
	 *
	 * @param aDate Pass date by value.
	 * @param hours Number of hours to add.
	 * @return A new date object with the hours added.
	 */
	public static Date addHours(Date aDate, int hours) {
		Calendar cal = GregorianCalendar.getInstance();
		cal.setTime(aDate);
		cal.add(Calendar.HOUR, hours);
		return cal.getTime();
	}

	/**
	 * Add seconds to a date by value.
	 * @param aDate Pass date by value.
	 * @param seconds Number of seconds to add.
	 * @return A new date object with the seconds added.
	 */
	public static Date addSeconds(Date aDate, int seconds) {
		Calendar cal = GregorianCalendar.getInstance();
		cal.setTime(aDate);
		cal.add(Calendar.SECOND, seconds);
		return cal.getTime();
	}

	/**
	 * Compute the number of hours between two dates.
	 *
	 * @param startDate Earlier date.
	 * @param endDate Later date.
	 * @return number of hours between dates.
	 */
	public static long hoursBetween(Calendar startDate, Calendar endDate) {
		Calendar date = (Calendar) startDate.clone();
		long hoursBetween = -1;
		while (date.before(endDate) || date.equals(endDate)) {
			date.add(Calendar.HOUR, 1);
			hoursBetween++;
		}
		return hoursBetween;
	}

	/**
	 * Compare two dates for equivalence to the day.
	 *
	 * @param d1 Date one.
	 * @param d2 Date two.
	 * @return true if the dates are in the same day, false ow.
	 */
	public static boolean dateCompare(Date d1, Date d2) {
		Calendar c1 = GregorianCalendar.getInstance();
		Calendar c2 = GregorianCalendar.getInstance();
		c1.setTime(d1);
		c2.setTime(d2);
		boolean sameDate = c1.get(Calendar.YEAR) == c2.get(Calendar.YEAR);
		sameDate = sameDate && c1.get(Calendar.DAY_OF_YEAR) == c2.get(Calendar.DAY_OF_YEAR);
		return sameDate;
	}

	/**
	 * Compute midnight of the date provided.
	 *
	 * @param aDate
	 * @return Midnight of the date provided.
	 */
	public static Date endOfDay(Date aDate) {
		Calendar cal = GregorianCalendar.getInstance();
		cal.setTime(aDate);
		cal.set(Calendar.MILLISECOND, 0);
		cal.set(Calendar.SECOND, 0);
		cal.set(Calendar.MINUTE, 0);
		cal.set(Calendar.HOUR_OF_DAY, 24);
		Date midnight = cal.getTime();
		return midnight;
	}

	/**
	 * Compute the seconds from a date to the end of day.
	 *
	 * @param aDate Any date.
	 * @return The number of seconds from the given date until midnight.
	 */
	public static Long secondsToEndOfDay(Date aDate) {
		Date midnight = endOfDay(aDate);
		return timeDifferenceInSeconds(aDate, midnight);
	}

	/**
	 * Compute day break of the date provided.
	 *
	 * @param aDate A date with time.
	 * @return Day break of the date provided. The dawn of a new day.
	 */
	public static Date startOfDay(Date aDate) {
		Calendar cal = GregorianCalendar.getInstance();
		cal.setTime(aDate);
		cal.set(Calendar.MILLISECOND, 0);
		cal.set(Calendar.SECOND, 0);
		cal.set(Calendar.MINUTE, 0);
		cal.set(Calendar.HOUR_OF_DAY, 0);
		Date dayBreak = cal.getTime();
		return dayBreak;
	}

	/**
	 * Compute the number of seconds from the start of the day to a date.
	 *
	 * @param aDate Any date.
	 * @return The number of seconds from the start of the day for the date given.
	 */
	public static Long secondsFromStartOfDay(Date aDate) {
		Date dayBreak = startOfDay(aDate);
		return timeDifferenceInSeconds(dayBreak, aDate);
	}

	/**
	 * Get the GregorianCalendar.Calendar.HOUR_OF_DAY for a date.
	 *
	 * @param aDate Any date.
	 * @return The 24 hour hour of the day.
	 */
	public static int hourOfDay(Date aDate) {
		Calendar cal = GregorianCalendar.getInstance();
		cal.setTime(aDate);
		return cal.get(Calendar.HOUR_OF_DAY);
	}
}
