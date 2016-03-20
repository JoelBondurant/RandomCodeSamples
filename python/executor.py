"""
A utility to execute concurrent computation.
"""

import multiprocessing
import concurrent.futures

def cpu_count():
	"""Return the number of cpu cores on the local machine."""
	return multiprocessing.cpu_count()


def submit(func, args, thread_count = None):
	"""Submit a function and arguments to execute in parallel threads."""
	thread_count = thread_count or cpu_count()
	results = []
	with concurrent.futures.ThreadPoolExecutor(max_workers = thread_count) as executor:
		futs = {}
		fut_number = 0
		fut_numbers = {}
		for arg in args:
			fut_number += 1
			fut = executor.submit(func, arg)
			futs[arg] = fut
			fut_numbers[fut] = fut_number
		for fut in concurrent.futures.as_completed(futs.values()):
			results.append((fut_numbers[fut], fut.result()))
	return list(zip(*sorted(results))[1])


