pre-commit:
	pre-commit run --all-files

test:
	pytest tests

clean:
	rm -rf dist build _build __pycache__ *.egg-info

build:
	make clean
	python setup.py sdist

publish:
	twine upload dist/*
