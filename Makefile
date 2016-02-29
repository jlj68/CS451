
console_chess:
	python3 pychess.py

run_webserver:
	python3 webserver.py

test:
	python3 pychess_test.py

coverage:
	coverage run pychess_test.py
	coverage report -m
	coverage html

clean:
	rm -rf htmlcov
	rm -rf __pycache__
	rm -rf .coverage
	rm -rf *.pyc

