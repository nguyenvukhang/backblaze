from os import path
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from zipfile import ZipFile
import os, sys

if len(sys.argv) < 2:
    print("Please supply download url as first CLI arg.", sys.argv)
    exit(1)

url = sys.argv[1]


fp = path.basename(url)


# member is guaranteed to end with ".csv" here.
members = []
with ZipFile(fp, "r") as z:
    for member in z.namelist():
        if member.startswith("__MACOSX") or not member.endswith(".csv"):
            continue
        members.append(member)
print(members)

for member in members:
    print("member:", member)
    with ZipFile(fp, "r") as z:
        z.extract(member)
        df = pd.read_csv(member, delimiter=",")
        os.remove(member)
        pq.write_table(
            pa.Table.from_pandas(df),
            path.basename(member)[:-4] + ".parquet",
        )
