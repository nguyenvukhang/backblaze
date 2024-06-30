import numpy as np, pyarrow.parquet as pq, pyarrow as pa
from pandas import DataFrame
from tqdm import tqdm
from datetime import datetime, timedelta
from typing import Iterable
from dateutil import tz
from os import makedirs
from shutil import rmtree


def read_pandas(path: str) -> DataFrame:
    return pq.read_table(path).to_pandas()

def write_pandas(df: DataFrame, path: str):
    pq.write_table(pa.Table.from_pandas(df), path)


def unsqueeze(x: np.ndarray) -> np.ndarray:
    return np.expand_dims(x, axis=0)


def std_date(date: datetime) -> str:
    """
    Uses `%Y-%m-%d` to format the date. Standard project-wide.
    """
    return date.strftime("%Y-%m-%d")


def day_iter(start: datetime, end: datetime) -> Iterable[datetime]:
    """
    An (inclusive) iterator from `start` to `end`, incrementing in days.
    """
    day = timedelta(days=1)
    while start <= end:
        yield start
        start += day


def day_iter_tqdm(start: datetime, end: datetime) -> Iterable[datetime]:
    """
    An (inclusive) iterator from `start` to `end`, incrementing in days.
    """
    day = timedelta(days=1)
    bar = tqdm(total=(end - start).days + 1)
    while start <= end:
        bar.set_description(std_date(start))
        yield start
        bar.update()
        start += day
    bar.close()


def day_iter_n(start: datetime, n: int) -> Iterable[datetime]:
    """
    An iterator of length `n`, starting from `start`.
    """
    day = timedelta(days=1)
    for _ in range(n):
        yield start
        start += day


def today() -> datetime:
    """
    Get today's datetime (Singapore TZ)
    """
    return datetime.now(tz.gettz("Asia/Singapore"))


def clear_dir(path: str):
    """
    Annihilates a directory and re-creates it empty.
    """
    try:
        rmtree(path)
    except FileNotFoundError:
        pass
    makedirs(path, exist_ok=True)
