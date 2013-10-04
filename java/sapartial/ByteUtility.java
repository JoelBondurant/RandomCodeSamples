package com.sensoranalytics.commons;

import java.util.ArrayList;
import java.util.List;

/**
 * A utility class for manipulation of byte arrays.
 *
 * @author Joel Bondurant
 * @version 2011.0317
 * @since 1.0
 */
public class ByteUtility {

	private ByteUtility() {} // makes sure that no one tries to instantiate this.
	
	/**
	 * Hex characters for use producing human readable strings.
	 */
	public static final String hexChars = "0123456789ABCDEF";

	/**
	 * Converts a byte array to hex string with leading 0x.
	 *
	 * @param byteArray A byte array to convert to a hex string.
	 * @return A string representing the hex representation of the input.
	 */
	public static String toHexString(byte [] byteArray) {
		if (byteArray == null) {
			return null;
		}
		final StringBuilder sb = new StringBuilder(2 + 2 * byteArray.length);
		sb.append("0x");
		for (final byte b: byteArray) {
			sb.append(hexChars.charAt((b & 0xF0) >> 4)).append(hexChars.charAt((b & 0x0F)));
		}
		return sb.toString();
	}

	/**
	 * Parse a string delimited list of integers into an integer list. 
	 * @param intStrList A list of integers delimited by ...
	 * @param delimiter ... delimited by this.
	 * @return A list of the integers.
	 */
	public static List<Integer> intStrList2intList(String intStrList, String delimiter) {
		List<Integer> intList = new ArrayList<Integer>();
		String[] intStrArr = intStrList.split(delimiter);
		for(String intStr: intStrArr) {
			intList.add(Integer.parseInt(intStr));
		}
		return intList;
	}

	/**
	 * Bit packs a list of integers into a long. Note that for this to work, all integers must be
	 * less than (Long.SIZE - 1) = 63.
	 * TODO: move to lot or wafer class.
	 * @param slotList List of slot numbers.
	 * @return A long representing the bit packed list of slot numbers.
	 */
	public static long slots2long(List<Integer> slotList) {
		long slotLong = 0L;
		for (Integer slotNum: slotList) {
			if (slotNum >= Long.SIZE) {
				//TODO: throw exception.
			}
			slotLong += Math.pow(2, slotNum - 1);
		}
		return slotLong;
	}

	/**
	 * 
	 * Bit unpacks a long into a list of integers in range [1, Long.SIZE - 1].
	 * @param n long
	 * @return A list of integers in the bit packed list of slot numbers.
	 */
	public static List<Integer> long2slots(long n) {
		List<Integer> slots = new ArrayList<Integer>();
		for (int i = 0; i < Long.SIZE; i++) {
			long x = (long) Math.pow(2, i);
			if ((x & n) == x) {
				slots.add(i + 1);
			}
		}
		return slots;
	}

}
