from pandas import DataFrame, Series
from utils import read_pandas
import matplotlib.pyplot as plt
import matplotlib.dates
from datetime import datetime, timedelta
from os import path
from math import isnan

PLOT_FAILURES = False

DATE_FMT = "%Y-%m-%d"


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


columns_front = None
columns_back = None


def get_nan(x):
    t = 0
    for i, col in enumerate(columns_front or []):
        if not isnan(x[col]):
            t += 2**i
    print(t)

    print(len(columns))
    # print(columns)
    exit()
    return x


while t < end:
    df = read_pandas(pq_path(t))
    if columns_front is None:
        columns = [x for x in df.columns.values if x.startswith("smart_")]
        i = int(len(columns) / 2)
        columns_front = columns[:i]
        columns_back = columns[i:]
    df["condense"] = df.apply(get_nan, axis=1)
    # print(columns)
    print(df)
    break
    t += timedelta(days=1)
