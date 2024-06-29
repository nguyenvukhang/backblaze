from pandas import DataFrame
from utils import read_pandas
import matplotlib.pyplot as plt
import matplotlib.dates
from datetime import datetime

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


df = read_pandas("fails.parquet")
years = list(set([datetime.strptime(x, DATE_FMT).year for x in df["date"].values]))
years.sort()
bins = generate_bins(years)


top_n = top_n_fails(df)
for model in top_n:
    plot_failures(df, model, bins)
