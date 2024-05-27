current: join-pq

join-pq:
	python3 join-pq.py

verify:
	python3 verify.py

dl:
	-@mkdir -p output/.cache
	python3 run.py
