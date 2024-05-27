import zipfile, os
from os import path
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from multiprocessing.pool import ThreadPool
from tqdm import tqdm


def full_run(p: tuple[str, str]):
    fn, member = p
    with zipfile.ZipFile(f"output/.cache/{fn}", "r") as f:
        f.extract(member, path="output")
    csvfile = path.join("output", member)
    tbl = pa.Table.from_pandas(pd.read_csv(csvfile))
    pq.write_table(tbl, path.join("output", path.basename(member) + ".parquet"))
    os.remove(csvfile)


pairs = []

for y in range(2016, 2025):
    for q in range(1, 5):
        if y == 2024 and q != 1:
            continue
        fn = f"data_Q{q}_{y}.zip"
        with zipfile.ZipFile(f"output/.cache/{fn}", "r") as f:
            for member in f.namelist():
                if member.startswith("__MACOSX") or not member.endswith(".csv"):
                    continue
                pairs.append((fn, member))
            print(fn, member)

with ThreadPool(8) as pool:
    total = len(pairs)
    list(tqdm(pool.imap(full_run, pairs), total=total))
