from collections.abc import Iterable
from pandas import DataFrame, Series
from utils import read_pandas
import matplotlib.pyplot as plt, json
import matplotlib.dates, matplotlib.ticker
from datetime import datetime, timedelta
from os import makedirs, path
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
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))

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


def pq_path(t: datetime):
    base = "/Users/khang/.local/data/backblaze/parquets"
    return path.join(base, t.strftime("%Y-%m-%d") + ".parquet")


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


u_cols: set[str] = set()
l = 0

col_list: list[list[str]] = []

for i in range(1, 256, 30):
    chunk = lambda: range(i, i + 30)
    col_list.append([f"smart_{i}_normalized" for i in chunk()])
    col_list.append([f"smart_{i}_raw" for i in chunk()])


def plot_population(df: DataFrame, model: str):
    df = df[df.index == model]
    # total_entries = int(df[df.index == model]["count"].sum())
    # print(model, total_entries)

    _, ax = plt.subplots()
    format_axis(ax)
    ax.hist(df["date"].values, weights=df["count"].values, bins=20, color="lightblue")
    plt.title(f"{model} failures over the years, by quarter")
    plt.savefig(model.strip().replace(" ", "_") + ".png")
    plt.show()

    print(df)
    exit()


def plot_populations():
    df = read_pandas("models.parquet")
    models = list(map(str, df.index.unique()))
    models.sort()
    for model in models:
        plot_population(df, model)


plot_populations()

# for model in models:
#     records: list[tuple[str, list[int]]] = []
#     print("---", model, "---")
#     for t in day_iter():
#         # read the dataframe
#         df = read_pandas(pq_path(t))
#         df = df[df["model"] == model]
#
#         # print(df)
#         binrep_list = []
#         df_cols = set(df.columns)
#
#         for cols in col_list:
#             b = 0
#             for i, col in filter(lambda v: v[1] in df_cols, enumerate(cols)):
#                 # p=1 means completely NA, p=0 means completely meaningful data
#                 p = df[col].isna().mean()
#                 if p < 0.05:
#                     b += 2**i
#             binrep_list.append(b)
#         records.append((t.strftime(DATE_FMT), binrep_list))
#
#     makedirs("output", exist_ok=True)
#     with open(path.join("output", model + ".json"), "w") as f:
#         json.dump(records, f)
