import pyarrow.parquet as pq

# import pandas as pd
# import pyarrow as pa

df = pq.read_table("read.parquet").to_pandas()
print(df)
