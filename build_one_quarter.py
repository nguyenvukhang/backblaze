import sys, requests, shutil
from os import path
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from zipfile import ZipFile
import os

if len(sys.argv) < 2:
    print("Please supply download url as first CLI arg.", sys.argv)
    exit(1)

url = sys.argv[1]


def download_file(url) -> str:
    local_filename = path.basename(url)
    with requests.get(url, stream=True) as r:
        if r.status_code == 404:
            return None
        with open(local_filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return local_filename


fp = path.basename(url)


try:
    os.mkdir("output")
except:
    pass

# member is guaranteed to end with ".csv" here.
members = []
with ZipFile(fp, "r") as z:
    for member in z.namelist():
        if member.startswith("__MACOSX") or not member.endswith(".csv"):
            continue
        members.append(member)

for member in members:
    print("member:", member)
    with ZipFile(fp, "r") as z:
        z.extract(member)
        df = pd.read_csv(member, delimiter=",", index_col=0)
        os.remove(member)
        pq.write_table(
            pa.Table.from_pandas(df),
            path.join("output", path.basename(member)[:-4] + ".parquet"),
        )
