from sys import argv
import os, subprocess, pandas as pd
from typing import cast
from tqdm import tqdm
from zipfile import ZipFile

from blaze.utils import *

TOKEN, ASSET_ID, ASSET_NAME = argv[1:4]

BASE_URL = "https://api.github.com/repos/nguyenvukhang/backblaze"
api_github = lambda v: os.path.join(BASE_URL, v)
HEADERS = { "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" }  # fmt: skip


def curl(id: str, target: str):
    cmd = ["curl", "-o", target, "-L", "-H", "Accept: application/octet-stream"]
    cmd += ["-H", f"Authorization: Bearer {TOKEN}"] if TOKEN is not None else []
    cmd += [api_github(f"releases/assets/{id}")]
    subprocess.run(cmd)


curl(id=ASSET_ID, target=ASSET_NAME)

with ZipFile(ASSET_NAME, "r") as z:
    DF = cast(DataFrame, None)
    for member in tqdm(z.namelist()):
        df = bytes_to_dataframe(z.read(member))
        date_str = file_stem(member)

        df = df[df["model"] == "ST4000DM000"]
        DF = df if DF is None else pd.concat((DF, df))
    write_pandas(DF, file_stem(ASSET_NAME) + ".ST4000DM000.parquet")
