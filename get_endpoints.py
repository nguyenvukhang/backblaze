from datetime import datetime
from multiprocessing.pool import ThreadPool
import requests, json, sys
from os import makedirs, path
import requests

# This file serves as a preprocessing step for GitHub Actions. It gets all the
# valid urls that we can download BackBlaze data from, and returns a JSON table
# that will be the input to the matrix of the next CI task.

base_url = "https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data"
blaze = lambda v: path.join(base_url, v)

github_base_url = "https://api.github.com/repos/nguyenvukhang/backblaze"
api_github = lambda v: path.join(github_base_url, v)


def check_url(urls: list, idx: int):
    """
    Check if the `idx`-th url in the list `urls` is valid. If it's invalid,
    set that value to `None`. This is done so that it is thread-safe.
    """
    with requests.get(urls[idx], stream=True) as r:
        if r.status_code != 200:
            urls[idx] = None


def backblaze_csvs():
    potential_urls = [
        blaze("data_2013.zip"),
        blaze("data_2014.zip"),
        blaze("data_2015.zip"),
    ]
    for year in range(2016, datetime.today().year + 1):
        for quarter in range(1, 5):
            potential_urls.append(blaze(f"data_Q{quarter}_{year}.zip"))

    with ThreadPool(4) as pool:
        jobs = [(potential_urls, i) for i in range(len(potential_urls))]
        pool.starmap(check_url, jobs)

    t = lambda x: {
        # https://f001.backblaze...Data/data_Q1_2024.zip
        "url": x,
        # data_Q1_2024
        "file_stem": path.basename(x)[:-4],
    }
    print(json.dumps({"include": [t(x) for x in potential_urls if x is not None]}))


def github_parquets():
    HEADERS = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    TAG = "v0.4"
    OUTPUT_DIR = "output"
    makedirs(OUTPUT_DIR, exist_ok=True)
    res = requests.get(api_github(f"releases/tags/{TAG}"), headers=HEADERS).json()
    assets = filter(lambda a: a["name"].endswith(".zip"), res["assets"])
    incl = [{"id": str(a["id"]), "name": str(a["name"])} for a in assets]
    print(json.dumps({"include": incl}))


if len(sys.argv) < 2:
    print("Please supply an action argument.")
    exit(1)

if sys.argv[1] == "backblaze-csv":
    backblaze_csvs()
elif sys.argv[1] == "github-parquets":
    github_parquets()
else:
    print("Unrecognized argument.")
    exit(1)
