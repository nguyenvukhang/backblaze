import zipfile, os
from os import path
import requests
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa


def rw():
    print("reading...")
    df = pd.read_csv("2024-01-01.csv")
    tbl = pa.Table.from_pandas(df)
    print("read done.")
    pq.write_table(tbl, "example.parquet", write_page_index=False)

    print("writing...")
    df = pq.read_table("example.parquet").to_pandas()
    df.to_csv("dank.csv")


def download(url: str):
    from tqdm import tqdm

    filepath = path.join("output/.cache", path.basename(url))
    if path.isfile(filepath):
        print("Cache hit!", filepath)
        return

    # Streaming, so we can iterate over the response.
    response = requests.get(url, stream=True)

    # Sizes in bytes.
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024

    with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
        with open(filepath, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

    if total_size != 0 and progress_bar.n != total_size:
        raise RuntimeError("Could not download file")


def full_run(fn: str):
    print("start download...")
    download(f"https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/{fn}")
    with zipfile.ZipFile(f"output/.cache/{fn}", "r") as f:
        for member in f.namelist():
            if member.startswith("__MACOSX") or not member.endswith(".csv"):
                continue
            csvfile = path.join("output", member)
            f.extract(member, path="output")
            print("unzip:", csvfile)
            tbl = pa.Table.from_pandas(pd.read_csv(csvfile))
            pq.write_table(tbl, path.join("output", path.basename(member) + ".parquet"))
            os.remove(csvfile)


for y in range(2016, 2025):
    for q in range(1, 5):
        if y == 2024 and q != 1:
            continue
        fn = f"data_Q{q}_{y}.zip"
        print(fn)
full_run("data_Q1_2024.zip")


# df1 = pd.read_csv("2024-01-01.csv")
# print(df1)

# df2 = pq.read_table("example.parquet").to_pandas()
# print(df2)

# s1 = pd.DataFrame(df1, columns=['smart_100_raw'])
# s2 = pd.DataFrame(df2, columns=['smart_100_raw'])
# print(s1[1:10])
# print(s2[1:10])
