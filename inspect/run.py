import pyarrow.parquet as pq
from zipfile import ZipFile
from tqdm import tqdm
import json
from io import BytesIO
from utils import read_pandas
import matplotlib.pyplot as plt
import matplotlib.dates
from datetime import datetime


df = read_pandas("/Users/khang/Downloads/fails.parquet")


def top_n_fails(df, n=10):
    sns = df["model"].value_counts().to_dict()
    sns = [(k, v) for k, v in sns.items()]
    sns.sort(key=lambda v: v[1], reverse=True)
    for x in sns[:n]:
        print(x)


top_n_fails(df)

dates = list(df["date"].unique())
dates.sort()
print(dates)


exit()

df = df[df["model"] == "ST4000DM000"]
df = df.reset_index()

fs = df["date"].value_counts()

fs = [(x, y) for x, y in df["date"].value_counts().to_dict().items()]
print(fs)
fs.sort(key=lambda v: v[0], reverse=True)
exit()
x, y = [], []

for u, v in fs.to_dict().items():
    x.append(u)
    y.append(v)

x = [datetime.strptime(x, "%Y-%m-%d") for x in x]
print(x)

print(matplotlib.dates.date2num(x))
# plt.plot(matplotlib.dates.date2num(x), y)
# plt.show()
print(df)

# y = []

# print(sns[:5])
