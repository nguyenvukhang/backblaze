import sys, requests, shutil
from os import path
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from zipfile import ZipFile
import os

if len(sys.argv) < 2:
    print("Please supply download url as first CLI arg.", sys.argv)
    exit(1)

url = sys.argv[1]


def download_file(url) -> str:
    local_filename = path.basename(url)
    with requests.get(url, stream=True) as r:
        if r.status_code == 404:
            return None
        with open(local_filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return local_filename


fp = path.basename(url)


with ZipFile(fp, "r") as z:
    # dfs = []
    for member in z.namelist():
        if member.startswith("__MACOSX") or not member.endswith(".csv"):
            continue
        # member is guaranteed to end with ".csv" here.
        print("member:", member)
        b: bytes = z.read(member)
        z.extract(member)
        df = pd.read_csv(member, delimiter=",", index_col=0)
        os.remove(member)
        pq.write_table(pa.Table.from_pandas(df), member[:-4] + ".parquet")

        # dfs.append(df)
    # df = pd.concat(dfs)
    # tbl = pa.Table.from_pandas(df)
    # pq.write_table(tbl, fp[:-4] + ".parquet")
