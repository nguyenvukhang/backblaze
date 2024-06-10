import pyarrow.parquet as pq
from zipfile import ZipFile
from pyarrow.util import sys
from tqdm import tqdm
import json
from io import BytesIO

ht: dict[tuple[str, str], set[str]] = {}


def insert(ht, model, serial_number, capacity):
    x = ht.get((model, capacity), None)
    if x is None:
        x = set()
    x.add(serial_number)
    ht[(model, capacity)] = x


name = sys.argv[1]

with ZipFile(name + ".zip", "r") as z:
    for member in tqdm(z.namelist()):
        df = pq.read_table(BytesIO(z.read(member))).to_pandas()
        df = df[["model", "serial_number", "capacity_bytes"]]
        for _, (model, serial_number, capacity) in df.iterrows():
            capacity = int(capacity)
            model = str(model)
            serial_number = str(serial_number)
            insert(ht, model, serial_number, capacity)

output = {}
for (model, capacity), serial_numbers in ht.items():
    if output.get(model, None) is None:
        output[model] = {}
    output[model][capacity] = list(serial_numbers)


with open(f"summary-{name}.json", "w") as f:
    json.dump(output, f)
