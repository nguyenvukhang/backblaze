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

dfs = {}
for a in data["include"]:
    for pq_file in listdir(a["id"]):
        pq_file = path.join(a["id"], pq_file)
        df = read_pandas(pq_file)
        if a["name"] in dfs:
            dfs[a["name"]].append(df)
        else:
            dfs[a["name"]] = [df]

for name, dfs in dfs.items():
    print("----------------")
    print("|", name, "|")
    print(pd.concat(dfs))
