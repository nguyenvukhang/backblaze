from collections.abc import Iterable
from pandas import DataFrame, Series
from utils import read_pandas, write_pandas
import matplotlib.pyplot as plt, json
import matplotlib.dates, matplotlib.ticker
from datetime import datetime, timedelta
from os import makedirs, path
from math import isnan
from tqdm import tqdm

PLOT_FAILURES = False
PLOT_POPULATION = False
GATHER_ATTRIBUTES = True
DATE_FMT = "%Y-%m-%d"
FIRST_EVER = datetime(2013, 4, 10)
LAST_EVER = datetime(2024, 3, 31)
OUTPUT_DIR = "output"
makedirs(path.join(OUTPUT_DIR), exist_ok=True)


def day_iter(start=FIRST_EVER, end=LAST_EVER, progress=True) -> Iterable[datetime]:
    t, d = start, timedelta(days=1)
    pbar = tqdm(total=(end - start).days + 1) if progress else None
    while t <= end:
        if pbar is not None:
            pbar.update()
            pbar.set_description(t.strftime(DATE_FMT))
        yield t
        t += d


def generate_quarter_bins(years: list[int]) -> list[datetime]:
    bins = []
    for y in years:
        x, y = datetime(y, 1, 1), datetime(y + 1, 1, 1)
        for j in range(4):
            bins.append(x + j * (y - x) / 4)
    return bins


def generate_week_bins(years: list[int]) -> list[datetime]:
    bins = []
    t = datetime(years[0], 1, 1)
    day, week = timedelta(days=1), timedelta(days=7)
    while t.weekday() > 0:
        t -= day
    end = datetime(years[-1], 12, 31)
    while t <= end:
        bins.append(t)
        t += week
    return bins


def top_n_fails(df: DataFrame, n=1e10, silent=False) -> list[str]:
    """
    Returns the top `n` models sorted by most-failed first.
    """
    sns = [(k, v) for k, v in df["model"].value_counts().to_dict().items()]
    sns.sort(key=lambda v: v[1], reverse=True)
    if n < len(sns):
        sns = sns[:n]
    if not silent:
        for model, fails in sns:
            print(f"{fails: <8} {model}")
    return [x[0] for x in sns]


def format_axis(ax):
    ax.xaxis.set_major_locator(matplotlib.dates.YearLocator())
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))

    for tick in ax.xaxis.get_majorticklabels():
        tick.set_horizontalalignment("left")


def sanitize_model(model: str) -> str:
    return model.strip().replace(" ", "_")


def plot_failures(df: DataFrame, model: str, bins: list[datetime]):
    df = df[df["model"] == model]

    dates = [datetime.strptime(x, DATE_FMT) for x in df["date"].values]
    _, ax = plt.subplots()
    format_axis(ax)
    ax.hist(dates, bins=bins, color="lightblue")
    plt.title(f"{model} failures over the years, by quarter")
    filename = model.strip().replace(" ", "_") + ".png"
    makedirs(path.join(OUTPUT_DIR, "failures"), exist_ok=True)
    plt.savefig(path.join(OUTPUT_DIR, "failures", filename))
    plt.close()


def pq_path(t: datetime):
    base = "/Users/khang/.local/data/backblaze/parquets"
    return path.join(base, t.strftime("%Y-%m-%d") + ".parquet")


def df_iter(
    start=FIRST_EVER, end=LAST_EVER, progress=False
) -> Iterable[tuple[datetime, DataFrame]]:
    for t in day_iter(start, end, progress=progress):
        yield t, read_pandas(pq_path(t))


def plot_population(df: DataFrame, model: str):
    df = df[df.index == model]

    _, ax = plt.subplots()
    format_axis(ax)
    dates = [datetime.strptime(x, DATE_FMT) for x in df["date"].values]
    ax.hist(dates, weights=df["count"].values, bins=30, color="lightblue")
    plt.title(f"{model} population over the years")
    filename = model.strip().replace(" ", "_") + ".png"
    makedirs(path.join(OUTPUT_DIR, "populations"), exist_ok=True)
    plt.savefig(path.join(OUTPUT_DIR, "populations", filename))
    plt.close()


def plot_populations():
    df = read_pandas("models.parquet")
    models = list(map(str, df.index.unique()))
    models.sort()
    for model in tqdm(models):
        plot_population(df, model)


def get_binrep(df: DataFrame, cols: list[str], threshold=0.05) -> int:
    b = 0
    for i, col in filter(lambda v: v[1] in df.columns, enumerate(cols)):
        # p=1 means completely NA, p=0 means completely meaningful data
        p = df[col].isna().mean()
        if p < threshold:
            b += 2**i
    return b


def gather_attributes():
    all_cols: list[str] = []
    for i in range(1, 256):
        all_cols.append(f"smart_{i}_normalized")
        all_cols.append(f"smart_{i}_raw")
    for model in top_n_fails(read_pandas("fails.parquet"), n=5):
        print(model)
        data = {c: [] for c in all_cols}
        data["date"] = []
        for t in day_iter(start=datetime(2017, 2, 1), end=datetime(2020, 12, 31)):
            date_str = t.strftime(DATE_FMT)
            df = read_pandas(pq_path(t))
            df = df[df["model"] == model]
            dfc = set(df.columns)
            data["date"].append(date_str)
            for col in all_cols:
                data[col].append(col in dfc and df[col].isna().mean() < 0.05)
            # if t == FIRST_EVER + timedelta(days=100):
            #     break
        df = DataFrame(data)
        df["model"] = model
        df = df[
            ["model", "date", *[x for x in df.columns if x not in ("model", "date")]]
        ]
        makedirs(path.join(OUTPUT_DIR, "attrs"), exist_ok=True)
        write_pandas(
            df, path.join(OUTPUT_DIR, "attrs", sanitize_model(model) + ".parquet")
        )


MODEL = "ST8000DM002"

for t, df in df_iter(datetime(2017, 3, 2), datetime(2017, 3, 2)):
    df = df[df["model"] == "ST8000DM002"]
    print(df["failure"].value_counts())
    print(t, len(df.index) > 0)
    # if len(df.index) == 0:
    #     continue
    # print(df)
    # break


# exit()
# _, ax = plt.subplots()
# format_axis(ax)
# dates = [datetime.strptime(x, DATE_FMT) for x in absent["date"].values]
# ax.hist(dates, bins=30, color="lightblue")
# # plt.title(f"{model} failures over the years, by quarter")
# # filename = model.strip().replace(" ", "_") + ".png"
# makedirs(path.join(OUTPUT_DIR, "failures"), exist_ok=True)
# # plt.savefig(path.join(OUTPUT_DIR, "failures", filename))
# plt.show()
# plt.close()
# exit()
# print(df)


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
#     with open(path.join(OUTPUT_DIR, model + ".json"), "w") as f:
#         json.dump(records, f)

if PLOT_FAILURES:
    df = read_pandas("fails.parquet")
    years = list(set([datetime.strptime(x, DATE_FMT).year for x in df["date"].values]))
    years.sort()
    bins = generate_quarter_bins(years)
    p = [(k, v) for k, v in df["model"].value_counts().to_dict().items()]
    p.sort(key=lambda v: v[1], reverse=True)
    for model in tqdm([sn for sn, _ in p]):
        plot_failures(df, model, bins)
if PLOT_POPULATION:
    plot_populations()
if GATHER_ATTRIBUTES:
    gather_attributes()
