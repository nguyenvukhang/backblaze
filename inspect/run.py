from collections.abc import Iterable
from pandas import DataFrame, Series
from utils import read_pandas
import matplotlib.pyplot as plt
import matplotlib.dates
from datetime import datetime, timedelta
from os import path
from math import isnan
from tqdm import tqdm

PLOT_FAILURES = False

DATE_FMT = "%Y-%m-%d"

FIRST_EVER = datetime(2013, 4, 10)
LAST_EVER = datetime(2024, 3, 31)


def day_iter(start=FIRST_EVER, end=LAST_EVER, progress=True) -> Iterable[datetime]:
    t, d = start, timedelta(days=1)
    pbar = tqdm(total=(end - start).days + 1) if progress else None
    while t <= end:
        if pbar is not None:
            pbar.update()
            pbar.set_description(t.strftime(DATE_FMT))
        yield t
        t += d


def generate_bins(years: list[int]) -> list[datetime]:
    bins = []
    for y in years:
        x, y = datetime(y, 1, 1), datetime(y + 1, 1, 1)
        for j in range(4):
            bins.append(x + j * (y - x) / 4)
    return bins


def top_n_fails(df: DataFrame, n=10) -> list[str]:
    """
    Returns the top `n` models sorted by most-failed first.
    """
    sns = [(k, v) for k, v in df["model"].value_counts().to_dict().items()]
    sns.sort(key=lambda v: v[1], reverse=True)
    for model, fails in sns[:n]:
        print(f"{fails: <8} {model}")
    return [x[0] for x in sns[:n]]


def format_axis(ax):
    ax.xaxis.set_major_locator(matplotlib.dates.YearLocator())
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))

    for tick in ax.xaxis.get_majorticklabels():
        tick.set_horizontalalignment("left")


def plot_failures(df: DataFrame, model: str, bins: list[datetime]):
    df = df[df["model"] == model]

    dates = [datetime.strptime(x, DATE_FMT) for x in df["date"].values]
    _, ax = plt.subplots()
    format_axis(ax)
    ax.hist(dates, bins=bins, color="lightblue")
    plt.title(f"{model} failures over the years, by quarter")
    plt.savefig(model.replace(" ", "_") + ".png")


if PLOT_FAILURES:
    df = read_pandas("fails.parquet")
    years = list(set([datetime.strptime(x, DATE_FMT).year for x in df["date"].values]))
    years.sort()
    bins = generate_bins(years)
    top_n = top_n_fails(df)
    for model in top_n:
        plot_failures(df, model, bins)

t = datetime(2016, 1, 1)
end = datetime(2016, 2, 1)


def pq_path(t: datetime):
    base = "/Users/khang/.local/data/backblaze/parquets"
    return path.join(base, t.strftime("%Y-%m-%d") + ".parquet")


u_cols: set[str] = set()
l = 0

col_list: list[list[str]] = []

for i in range(1, 256, 30):
    chunk = lambda: range(i, i + 30)
    col_list.append([f"smart_{i}_normalized" for i in chunk()])
    col_list.append([f"smart_{i}_raw" for i in chunk()])

for t in day_iter():
    df = read_pandas(pq_path(t))
    u_cols = u_cols.union(df.columns)
    if len(u_cols) > l:
        l = len(u_cols)
        print(l)
        print(u_cols)
    # df["condense"] = df.apply(get_nan, axis=1)
    # print(columns)

# I wanna be able to see that for SMART Attr 1, when it was NA for a particular
# model.
#
# So we fix two things: Smart attribute # and model.
