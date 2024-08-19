# This script fetches all the metadata from BackBlaze itself. This includes
# getting the most up-to-date list of CSV datasets to download.
#
# This script is used on GitHub Actions in the preprocessing stage.

from datetime import datetime
from multiprocessing.pool import ThreadPool
import requests, json, os

BASE_URL = "https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data"


def check_url(urls: list, idx: int):
    """
    Check if the `idx`-th url in the list `urls` is valid. If it's invalid,
    set that value to `None`. This is done so that it is thread-safe.
    """
    with requests.get(urls[idx], stream=True) as r:
        if r.status_code != 200:
            urls[idx] = None


def get_potential_urls() -> list[str]:
    urls = ["data_2013.zip", "data_2014.zip", "data_2015.zip"]
    for year in range(2016, datetime.today().year + 1):
        for quarter in range(1, 5):
            urls.append(f"data_Q{quarter}_{year}.zip")
    return list(map(lambda v: os.path.join(BASE_URL, v), urls))


with ThreadPool(4) as pool:
    potential_urls = get_potential_urls()
    jobs = [(potential_urls, i) for i in range(len(potential_urls))]
    pool.starmap(check_url, jobs)

t = lambda url: {
    # https://f001.backblaze...Data/data_Q1_2024.zip
    "url": url,
    # data_Q1_2024
    "file_stem": os.path.basename(url)[:-4],
}
print(json.dumps({"include": [t(x) for x in potential_urls if x is not None]}))
