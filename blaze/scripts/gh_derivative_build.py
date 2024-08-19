from sys import argv
import os, subprocess, pandas as pd
from typing import Iterable, cast
from tqdm import tqdm
from zipfile import ZipFile

from blaze.utils import *

TOKEN, ASSET_ID, ASSET_NAME = argv[1:4]

BASE_URL = "https://api.github.com/repos/nguyenvukhang/backblaze"
api_github = lambda v: os.path.join(BASE_URL, v)
HEADERS = { "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" }  # fmt: skip


def run_cmd(cmd: list[str], retries: int):
    try:
        subprocess.run(cmd)
    except:
        run_cmd(cmd, retries - 1)


def curl(id: str, target: str):
    cmd = ["curl", "-o", target, "-L", "-H", "Accept: application/octet-stream"]
    cmd += ["-H", f"Authorization: Bearer {TOKEN}"] if TOKEN is not None else []
    cmd += [api_github(f"releases/assets/{id}")]
    run_cmd(cmd, retries=3)


def dataframes() -> Iterable[DataFrame]:
    with ZipFile(ASSET_NAME, "r") as z:
        for member in tqdm(z.namelist()):
            yield bytes_to_dataframe(z.read(member))


curl(id=ASSET_ID, target=ASSET_NAME)

DF = cast(DataFrame, None)
for df in dataframes():
    df = df[df["model"] == "ST4000DM000"]
    # df = df[["date", "serial_number", "model", "capacity_bytes", "failure"]]
    DF = df if DF is None else pd.concat((DF, df))

DF.sort_values(by=["serial_number"], kind="stable", inplace=True)
DF.reset_index(drop=True, inplace=True)
write_pandas(DF, "ST4000DM000.parquet")
