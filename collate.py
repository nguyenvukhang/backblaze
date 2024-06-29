from sys import argv
import json
from utils import *
import pandas as pd
from os import listdir, path
import gc

# TODO: the artifacts are stored in the directories that are named `asset['id']`
# Iterate over these directories.

data = json.loads(" ".join(argv[1:]))
print(type(data))
print(data)


def file_stem(x: str) -> str:
    return path.basename(x).rsplit(".", maxsplit=1)[0]


def write(df: DataFrame, name: str):
    df.reset_index(inplace=True, drop=True)
    print("----------------")
    print("|", name, "|")
    print(df)
    write_pandas(df, name + ".parquet")
    del df


def assets_iter(key: str) -> Iterable[DataFrame]:
    for asset in data["include"]:
        pqs = filter(lambda v: v.endswith(".parquet"), listdir(asset["id"]))
        pqs = filter(lambda v: file_stem(v) == key, pqs)
        pqs = map(lambda v: path.join(asset["id"], v), pqs)
        for pq_path in pqs:
            yield read_pandas(pq_path)


def __fails__():
    dfs = []
    for df in assets_iter("fails"):
        dfs.append(df)
    write(pd.concat(dfs), "fails")
    del dfs
    gc.collect()


def __models__():
    dfs = []
    for df in assets_iter("models"):
        dfs.append(df)
    write(pd.concat(dfs), "models")
    del dfs
    gc.collect()


__fails__()
__models__()
