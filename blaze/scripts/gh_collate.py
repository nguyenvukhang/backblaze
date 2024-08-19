from typing import Iterable, cast
from sys import argv
import json, os, pandas as pd
from blaze.utils import *

data = json.loads(" ".join(argv[1:]))


def assets_iter(key: str) -> Iterable[DataFrame]:
    for asset in data["include"]:
        pqs = filter(lambda v: v.endswith(".parquet"), os.listdir(asset["id"]))
        pqs = filter(lambda v: file_stem(v) == key, pqs)
        pqs = map(lambda v: path.join(asset["id"], v), pqs)
        for pq_path in pqs:
            yield read_pandas(pq_path)


DF = cast(DataFrame, None)
for df in assets_iter("ST4000DM000"):
    DF = df if DF is None else pd.concat((DF, df))

write_pandas(DF, "ST4000DM000.parquet")
