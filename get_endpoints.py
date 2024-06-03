from datetime import datetime
from multiprocessing.pool import ThreadPool
import requests, json


def dl_url(year: int, quarter: int):
    return f"https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q{quarter}_{year}.zip"


potential_urls = []
for year in range(2016, datetime.today().year + 1):
    for quarter in range(1, 5):
        potential_urls.append(dl_url(year, quarter))


def check_url(urls: list[str], idx: int):
    with requests.get(urls[idx], stream=True) as r:
        if r.status_code != 200:
            urls[idx] = None


with ThreadPool(4) as pool:
    jobs = [(potential_urls, i) for i in range(len(potential_urls))]
    pool.starmap(check_url, jobs)

output = {"url": [x for x in potential_urls if x is not None]}
print(json.dumps(output))
