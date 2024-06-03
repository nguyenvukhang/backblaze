from datetime import datetime
from multiprocessing.pool import ThreadPool
import requests, shutil
from os import path
from tqdm import tqdm


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
# download_file(dl_url(2024, 2))
# for year in range(2016, datetime.today().year + 1):
#     for quarter in range(1, 5):
#         url = dl_url(year, quarter)
#         with requests.get(url, stream=True) as r:
#             if r.status_code == 200:
#                 print(url)


def print_url_if_valid(url: str):
    with requests.get(url, stream=True) as r:
        if r.status_code == 200:
            print(url)


potential_urls = []
for year in range(2016, datetime.today().year + 1):
    for quarter in range(1, 5):
        potential_urls.append(dl_url(year, quarter))

with ThreadPool(4) as pool:
    total = len(potential_urls)
    list(pool.map(print_url_if_valid, potential_urls))
