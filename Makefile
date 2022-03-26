PYTHON ?= python
ROOT = $(dir $(realpath $(firstword $(MAKEFILE_LIST))))


clean:
	find . -name '__pycache__' | xargs rm -rf
	rm -rf htmlcov .coverage


coverage:
	$(PYTHON) -m pytest --cov="." --cov-report html


format:
	$(PYTHON) -m black fastproject tests
	$(PYTHON) -m isort .


run:
	$(PYTHON) -m uvicorn --reload --host 0.0.0.0 --port 8000 fastproject.main:app


test:
	$(PYTHON) -m pytest