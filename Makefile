current: mig

mig:
	python3 migrate.py

boq:
	python3 build_one_quarter.py https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q1_2016.zip

ci:
	python3 get_endpoints.py
