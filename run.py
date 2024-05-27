import os
from os import path
from zipfile import ZipFile
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from multiprocessing.pool import ThreadPool
from tqdm import tqdm

DATA_DIR = "output/.cache"


def full_run(p: tuple[str, str]):
    z, member = p
    with ZipFile(path.join(DATA_DIR, z), "r") as f:
        f.extract(member, path="output")
    csvfile = path.join("output", member)
    tbl = pa.Table.from_pandas(pd.read_csv(csvfile))
    os.remove(csvfile)
    pq.write_table(tbl, path.join("output", path.basename(member) + ".parquet"))


pairs = []
for z in filter(lambda v: v.endswith(".zip"), os.listdir(DATA_DIR)):
    with ZipFile(path.join(DATA_DIR, z), "r") as f:
        for member in f.namelist():
            if member.startswith("__MACOSX") or not member.endswith(".csv"):
                continue
            pairs.append((z, member))
            print(z, member)

with ThreadPool(4) as pool:
    total = len(pairs)
    list(tqdm(pool.imap(full_run, pairs), total=total))
