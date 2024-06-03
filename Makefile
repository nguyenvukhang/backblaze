current: boq

boq:
	python3 build_one_quarter.py https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q1_2016.zip

ci:
	python3 get_endpoints.py

join-pq:
	python3 join-pq.py

verify:
	python3 verify.py

dl:
	-@mkdir -p output/.cache
	python3 run.py
