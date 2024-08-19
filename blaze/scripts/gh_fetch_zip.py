from sys import argv
from os import path
from subprocess import run
from utils import *
from zipfile import ZipFile
import pandas as pd
from tqdm import tqdm

from blaze.utils import *


OUTPUT_DIR = "output"
BASE_URL = "https://api.github.com/repos/nguyenvukhang/backblaze"
api_github = lambda v: path.join(BASE_URL, v)
TOKEN, ASSET_ID, ASSET_NAME = argv[1:4]
HEADERS = { "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" }  # fmt: skip

if len(argv) < 2:
    print("Please supply a github access token as the first CLI arg.")
    exit(1)


def curl(id: str, target: str):
    cmd = ["curl", "-o", target, "-L", "-H", "Accept: application/octet-stream"]
    cmd += ["-H", f"Authorization: Bearer {TOKEN}"] if TOKEN is not None else []
    cmd += [api_github(f"releases/assets/{id}")]
    run(cmd)


class DataFrameDict:
    def __init__(self):
        self.dfs: dict[str, DataFrame] = {}

    def add(self, key: str, df: DataFrame):
        if self.dfs.get(key, None) is None:
            self.dfs[key] = df
        else:
            self.dfs[key] = pd.concat((self.dfs[key], df))

    def write_all(self):
        for key, df in self.dfs.items():
            write_pandas(df, key + ".parquet")


curl(id=ASSET_ID, target=ASSET_NAME)
dfd = DataFrameDict()
with ZipFile(ASSET_NAME, "r") as z:
    for member in tqdm(z.namelist()):
        df = bytes_to_dataframe(z.read(member))
        date_str = file_stem(member)

        sdf = df[df["failure"] == 1]
        sdf = sdf[["date", "model", "serial_number"]]
        dfd.add("fails", sdf)

        sdf = DataFrame(df["model"].value_counts())
        sdf["date"] = date_str
        sdf = sdf[["date", "count"]]
        dfd.add("models", sdf)

dfd.write_all()
