import csv
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa

# pq.read_table
# pd.DataFrame.from_


def rw():
    print("reading...")
    df = pd.read_csv("2024-01-01.csv")
    tbl = pa.Table.from_pandas(df)
    print("read done.")
    pq.write_table(tbl, 'example.parquet', write_page_index=False)

    print("writing...")
    df = pq.read_table("example.parquet").to_pandas()
    df.to_csv("dank.csv")

# rw()

df1 = pd.read_csv("2024-01-01.csv")
# print(df1)

df2 = pq.read_table("example.parquet").to_pandas()
# print(df2)

s1 = pd.DataFrame(df1, columns=['smart_100_raw'])
s2 = pd.DataFrame(df2, columns=['smart_100_raw'])
print(s1[1:10])
print(s2[1:10])
