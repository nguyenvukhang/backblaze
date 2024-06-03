import os
from os import path
from zipfile import ZipFile
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from multiprocessing.pool import ThreadPool
from tqdm import tqdm

SRC_DIR = "/Users/khang/.local/data/backblaze/parquets"

pq_files = os.listdir(SRC_DIR)
pq_files.sort()
pq_files = [x for x in pq_files if x.endswith(".parquet")]


years = list({x.split("-")[0] for x in pq_files})
years.sort()

for pq_file in tqdm(pq_files):
    df = pq.read_table(path.join(SRC_DIR, pq_file)).to_pandas().reset_index()
    # print(df)
    # break
    pq.write_table(pa.Table.from_pandas(df), path.join("output", pq_file))
