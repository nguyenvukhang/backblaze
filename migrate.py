import os
from os import path
from zipfile import ZipFile
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
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

for pq_file in tqdm(pq_files):
    df = read_pandas(path.join(SRC_DIR, pq_file))
    if len(df.index) == 0:
        print("EMPTY:", pq_file)
        continue
    dates = df['date'].unique()
    if len(dates) > 1:
        print(dates)
    date = dates[0]
    if '-' not in date:
        print('weird date:', date)
    # if len(df.index) < 10000:
    #     print(df["model"].unique())
    #     ded()
    # print(len(df))
    # print(df)
    # break
    # pq.write_table(pa.Table.from_pandas(df), path.join("output", pq_file))
