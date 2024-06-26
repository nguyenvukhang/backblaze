from collections.abc import Iterable
import pandas as pd, pyarrow.parquet as pq, pyarrow as pa, os, sys
from os import path
from zipfile import ZipFile
from pandas import DataFrame
from io import BytesIO

if len(sys.argv) < 2:
    print("Please supply download url as first CLI arg.", sys.argv)
    exit(1)

url = sys.argv[1]
zip_file = path.basename(url)


def get_csvs(zip_file: str) -> list[str]:
    """
    Gets all the `*.csv` members of the `zip_file`.
    """
    with ZipFile(zip_file, "r") as z:
        l = z.namelist()
        l = filter(lambda v: not v.startswith("__MACOSX"), l)
        l = filter(lambda v: v.endswith(".csv"), l)
        csvs = list(l)
        csvs.sort()
        return csvs


def file_stem(x: str) -> str:
    return path.basename(x).rsplit(".", maxsplit=1)[0]


def generate_parquets(members: list[str]):
    with ZipFile(zip_file, "r") as z:
        for member in members:
            print("member:", member, flush=True)
            df = pd.read_csv(BytesIO(z.read(member)), delimiter=",")
            date_str = file_stem(member)
            df["date"] = date_str
            pq.write_table(pa.Table.from_pandas(df), date_str + ".parquet")


def inspect_parquets(pq_files: list[str]):
    print(pq_files)


members = get_csvs(zip_file)
generate_parquets(members)
inspect_parquets([file_stem(x) + ".parquet" for x in members])
