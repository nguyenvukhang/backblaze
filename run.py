import csv

with open("2024-01-01.csv", "r") as f:
    it = csv.reader(f)
    print(next(it))
    print(next(it))
