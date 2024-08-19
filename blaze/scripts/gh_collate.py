from typing import Iterable, cast
from sys import argv
import json, os, pandas as pd
from blaze.utils import *
from tqdm import tqdm

data = json.loads(" ".join(argv[1:]))


def assets_iter(key: str) -> Iterable[DataFrame]:
    buffer = []
    for asset in data["include"]:
        pqs = filter(lambda v: v.endswith(".parquet"), os.listdir(asset["id"]))
        pqs = filter(lambda v: file_stem(v) == key, pqs)
        pqs = map(lambda v: path.join(asset["id"], v), pqs)
        buffer.extend(pqs)
    for pq_path in tqdm(buffer, desc=key):
        yield read_pandas(pq_path)


DF = cast(DataFrame, None)
for df in assets_iter("ST4000DM000"):
    DF = df if DF is None else pd.concat((DF, df))

print("Sorting...")
DF.sort_values(by=["serial_number", "date"], inplace=True)
print("Reindexing...")
DF.reset_index(drop=True, inplace=True)
print("Writing...")
write_pandas(DF, "ST4000DM000.parquet")
