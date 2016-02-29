
console_chess:
	python3 pychess.py

run_webserver:
	python3 webserver.py

test:
	python3 -m unittest test.py

coverage:
	coverage run test.py
	coverage report -m
	coverage html

