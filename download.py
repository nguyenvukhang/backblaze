import requests
import shutil


def download_file(url):
    local_filename = url.split("/")[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return local_filename


download_file(
    "https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q4_2023.zip"
)
