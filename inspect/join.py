import json
from os import walk, path
from tqdm import tqdm

db = {}


def update(db, model, capacity, serial_numbers):
    if db.get(model, None) is None:
        db[model] = {}
    if db[model].get(capacity, None) is None:
        db[model][capacity] = set(serial_numbers)
    else:
        for sn in serial_numbers:
            db[model][capacity].add(sn)


jsons = []

for root, _, files in walk("."):
    for file in files:
        if not (file.startswith("summary") and file.endswith(".json")):
            continue
        jsons.append(path.join(root, file))

for f in tqdm(jsons):
    with open(f, "r") as f:
        data = json.load(f)
        for model, v in data.items():
            for capacity, serial_numbers in v.items():
                update(db, model, capacity, serial_numbers)

for model, v in db.items():
    for capacity in v.keys():
        db[model][capacity] = list(db[model][capacity])

with open("summary.json", "w") as f:
    json.dump(db, f)
