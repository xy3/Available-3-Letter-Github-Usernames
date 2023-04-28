#!/usr/bin/python3

from multiprocessing import Pool
import sys, requests
import threading
from datetime import datetime
import tqdm

def check(username):
    status = request(username)
    if status == 500:
        return {"status": "unchecked", "username": username}

    if status == 404:
        return {"status": "available", "username": username}

    return {"status": "taken", "username": username}


def request(line):
    user = line.strip()
    try:
        result = requests.get(f"https://github.com/{user}", timeout=10)
        return result.status_code
    except Exception:
        return 500


def main():
    inputList = [s.strip() for s in sys.stdin.readlines()] 
    unchecked = set(inputList)
    available = []
    taken = []

    pool = Pool(processes=50)

    try:
        for result in tqdm.tqdm(pool.imap_unordered(check, inputList), total=len(inputList)):
            status = result["status"]
            if status != "unchecked":
                unchecked.remove(result["username"])
            if status == "available":
                available.append(result["username"])
            else:
               taken.append(result["username"])


        now = datetime.now()
        dl_string = now.strftime("%d_%m_%Y_%H:%M:%S")
        with open(f"unchecked_{dl_string}.txt", "x") as f:
            f.write("\n".join(list(unchecked)))
            f.write("\n")

        with open(f"available_{dl_string}.txt", "x") as f:
            f.write("\n".join(available))
            f.write("\n")
 
        with open(f"taken_{dl_string}.txt", "x") as f:
            f.write("\n".join(taken))       
            f.write("\n")

        print(f"\nAvailable: {len(available)} | Taken: {len(taken)} | Unchecked/failed: {len(unchecked)}\n")

    except KeyboardInterrupt:
        sys.exit() # ctrl c 


if __name__ == "__main__":
    main()
