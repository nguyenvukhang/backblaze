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
zip_file = path.basename(url)


def get_csvs(zip_file: str):
    """
    Gets all the `*.csv` members of the `zip_file`.
    """
    with ZipFile(zip_file, "r") as z:
        l = z.namelist()
        l = filter(lambda v: not v.startswith("__MACOSX"), l)
        l = filter(lambda v: v.endswith(".csv"), l)
        return list(l)


for member in get_csvs(zip_file):
    print("member:", member)
    with ZipFile(zip_file, "r") as z:
        z.extract(member)
        df = pd.read_csv(member, delimiter=",")
        os.remove(member)

        date_str = path.basename(member)[:-4]
        df["date"] = date_str
        pq.write_table(
            pa.Table.from_pandas(df),
            date_str + ".parquet",
        )
