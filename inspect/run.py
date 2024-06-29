import pyarrow.parquet as pq
from zipfile import ZipFile
from tqdm import tqdm
import json
from io import BytesIO
from utils import read_pandas
import matplotlib.pyplot as plt
import matplotlib.dates
from datetime import datetime

DATE_FMT = "%Y-%m-%d"
MODEL = "ST4000DM000"

df = read_pandas("fails.parquet")


def top_n_fails(df, n=10):
    sns = df["model"].value_counts().to_dict()
    sns = [(k, v) for k, v in sns.items()]
    sns.sort(key=lambda v: v[1], reverse=True)
    for x in sns[:n]:
        print(x)


top_n_fails(df)

df = df[df["model"] == "ST4000DM000"]
df = df.reset_index()

years = [datetime(y, 1, 1) for y in range(2013, 2025)]
bins = []
for i in range(len(years) - 1):
    x, y = years[i], years[i + 1]
    for j in range(4):
        bins.append(x + j * (y - x) / 4)

dates = [datetime.strptime(x, DATE_FMT) for x in df["date"].values]
fig, ax = plt.subplots()
plt.axis
ax.hist(dates, bins=bins, color="lightblue")
ax.xaxis.set_major_locator(matplotlib.dates.YearLocator())
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))

for tick in ax.xaxis.get_majorticklabels():
    tick.set_horizontalalignment("left")

plt.title(f"{MODEL} failures over the years, by quarter")
plt.show()

# plt.plot(x, y)
# plt.show()
# print(df)

# y = []

# print(sns[:5])
