#!/usr/bin/python3

from multiprocessing import Pool
import sys, requests

def request(line):
	user = line.strip()
	status = requests.get(f"https://github.com/{user}").status_code
	result = {"user": user, "data": status}
	if status == 404: print(user)
	return result

# Set how many threads u want lol
pool = Pool(processes=100)

try:
	lines = sys.stdin.readlines()
	results = pool.map(request, lines)
except KeyboardInterrupt:
	sys.exit() # OH SHIT CTRL+C

# Can also print them out again
# for res in results:
# 	print(res)