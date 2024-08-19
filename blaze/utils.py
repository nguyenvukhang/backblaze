from io import BytesIO
from os import path
from pandas import DataFrame
import pyarrow.parquet as pq


def file_stem(x: str) -> str:
    return path.basename(x).rsplit(".", maxsplit=1)[0]


def bytes_to_dataframe(b: bytes) -> DataFrame:
    "Parquet Table bytes to a Pandas DataFrame."
    return pq.read_table(BytesIO(b)).to_pandas()
