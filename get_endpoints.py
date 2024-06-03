from datetime import datetime
from multiprocessing.pool import ThreadPool
import requests, shutil, json
from os import path


def dl_url(year: int, quarter: int):
    return f"https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q{quarter}_{year}.zip"


def download_file(url) -> str:
    local_filename = path.basename(url)
    with requests.get(url, stream=True) as r:
        if r.status_code == 404:
            return None
        with open(local_filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename


datetime.today()

potential_urls = []
for year in range(2016, datetime.today().year + 1):
    for quarter in range(1, 5):
        potential_urls.append(dl_url(year, quarter))


def check_url(urls: list[str], idx: int):
    url = urls[idx]
    with requests.get(url, stream=True) as r:
        if r.status_code != 200:
            urls[idx] = None


with ThreadPool(4) as pool:
    total = len(potential_urls)
    jobs = [(potential_urls, i) for i in range(len(potential_urls))]
    pool.starmap(check_url, jobs)

output = {"urls": [x for x in potential_urls if x is not None]}
print(json.dumps(output))
