current: dl

verify:
	python3 verify.py

dl:
	-@mkdir -p output/.cache
	python3 run.py
