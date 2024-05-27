from datetime import date, timedelta

day = timedelta(days=1)
x = date(2016, 1, 1)
end = date(2025, 1, 1)

while x < end:
    print(x)
    x += day
