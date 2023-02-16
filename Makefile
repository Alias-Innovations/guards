install:
	pip install .

format:
	black .
	flake8 .

test:
	python -m pytest
