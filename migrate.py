import os
from os import path
from zipfile import ZipFile
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from pyarrow.parquet.core import json
from tqdm import tqdm
from utils import *

ded = lambda: exit(0)

SRC_DIR = "/Users/khang/.local/data/backblaze/parquets"

pq_files = os.listdir(SRC_DIR)
pq_files = [x for x in pq_files if x.endswith(".parquet")]
pq_files.sort()
n = len(pq_files)

start_date = datetime.strptime(pq_files[0].split(".")[0], "%Y-%m-%d")

# check that all files are in order.
for t, pq_file in zip(day_iter_n(start_date, n), pq_files):
    assert t.strftime("%Y-%m-%d") == pq_file.split(".")[0]

# (date, serial_number)
fails: dict[str, list[str]] = {}
f_date: list[str] = []
f_sn: list[str] = []

makedirs("output", exist_ok=True)

for pq_file in tqdm(pq_files):
    date_str = path.basename(pq_file).removesuffix(".parquet")
    df = read_pandas(path.join(SRC_DIR, pq_file))
    if len(df.index) == 0:
        continue
    df["date"] = date_str
    df = df[df["failure"] == 1]
    for sn in df["serial_number"].values:
        f_date.append(date_str)
        f_sn.append(sn)

df = DataFrame(list(zip(f_date, f_sn)), columns=["date", "serial_number"])
write_pandas(df, 'fails.parquet')

#     print(df)
#
# with open("fails.json", "w") as f:
#     json.dump(fails, f)
