from typing import cast
import pandas as pd, pyarrow.parquet as pq, pyarrow as pa, sys
from os import path
from zipfile import ZipFile
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


def generate_parquets(members: list[str]):
    Df = cast(pd.DataFrame, None)
    with ZipFile(zip_file, "r") as z:
        for member in members:
            print("member:", member, flush=True)
            df = pd.read_csv(BytesIO(z.read(member)), delimiter=",")
            date_str = path.basename(member).removesuffix(".csv")
            df["date"] = date_str
            Df = df if Df is None else pd.concat((Df, df))
            pq.write_table(pa.Table.from_pandas(df), date_str + ".parquet")
    Df.reset_index(drop=True, inplace=True)
    tbl = pa.Table.from_pandas(Df)
    pq.write_table(tbl, zip_file.removesuffix(".zip") + ".parquet")


members = get_csvs(zip_file)
generate_parquets(members)
