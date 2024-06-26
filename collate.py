from sys import argv
import json
from utils import *
import pandas as pd

# TODO: the artifacts are stored in the directories that are named `asset['id']`
# Iterate over these directories.

data = json.loads(" ".join(argv[1:]))
print(type(data))
print(data)

dfs = []
for a in data["include"]:
    df = read_pandas(a["id"])
    dfs.append(df)
    print(df)
    print('------------')

df = pd.concat(dfs)
print(df)
