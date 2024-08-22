import os

yqs = []
for year in range(2016, 2025):
    for q in range(1, 5):
        if year == 2024 and q > 2:
            continue
        yqs.append((year, q))

for year, quarter in yqs:
    z = f"done/data_Q{quarter}_{year}.zip"
    if os.path.isfile(z):
        continue
    print(os.path.basename(z))
