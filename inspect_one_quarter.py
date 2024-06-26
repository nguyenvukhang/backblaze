from sys import argv
from os import path
from subprocess import run
from utils import *
from io import BytesIO
from zipfile import ZipFile
import pyarrow.parquet as pq


OUTPUT_DIR = "output"
BASE_URL = "https://api.github.com/repos/nguyenvukhang/backblaze"
api_github = lambda v: path.join(BASE_URL, v)


if len(argv) < 2:
    print("Please supply a github access token as the first CLI arg.")
    exit(1)


TOKEN = argv[1]
ASSET_ID = argv[2]
ASSET_NAME = argv[3]

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def curl(id: str, target: str):
    cmd = ["curl", "-o", target, "-L", "-H", "Accept: application/octet-stream"]
    cmd += ["-H", f"Authorization: Bearer {TOKEN}"] if TOKEN is not None else []
    cmd += [api_github(f"releases/assets/{id}")]
    run(cmd)


curl(id=ASSET_ID, target=ASSET_NAME)

with ZipFile(ASSET_NAME, "r") as z:
    for member in z.namelist():
        b = BytesIO(z.read(member))
        df = pq.read_table(b).to_pandas()
        print(df)
        break
