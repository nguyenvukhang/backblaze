from sys import argv
import json
from utils import *
import pandas as pd
from os import listdir, path

# TODO: the artifacts are stored in the directories that are named `asset['id']`
# Iterate over these directories.

data = json.loads(" ".join(argv[1:]))
print(type(data))
print(data)


def file_stem(x: str) -> str:
    return path.basename(x).rsplit(".", maxsplit=1)[0]


dfls: dict[str, list[DataFrame]] = {}
for a in data["include"]:
    for pq_file in listdir(a["id"]):
        if not pq_file.endswith(".parquet"):
            continue
        pq_file = path.join(a["id"], pq_file)
        df = read_pandas(pq_file)
        key = file_stem(pq_file)
        if key in dfls:
            dfls[key].append(df)
        else:
            dfls[key] = [df]

dfs: dict[str, DataFrame] = {}

for name, df_list in dfls.items():
    dfs[name] = pd.concat(df_list)
    dfs[name].reset_index(inplace=True)

for name, df in dfs.items():
    print("----------------")
    print("|", name, "|")
    print(df)
    write_pandas(df, name + ".parquet")
