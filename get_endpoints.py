from datetime import datetime
from multiprocessing.pool import ThreadPool
import requests, json
from os import path

base_url = "https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data"
blaze = lambda v: path.join(base_url, v)


def check_url(urls: list, idx: int):
    """
    Check if the `idx`-th url in the list `urls` is valid. If it's invalid,
    set that value to `None`. This is done so that it is thread-safe.
    """
    with requests.get(urls[idx], stream=True) as r:
        if r.status_code != 200:
            urls[idx] = None


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
