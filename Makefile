check:
	pylint3 --errors-only --output-format=parseable *.py


test:
	python3 test.py
