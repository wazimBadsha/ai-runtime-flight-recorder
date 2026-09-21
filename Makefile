PYTHON ?= python3

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -p 'test_*.py'

demo:
	PYTHONPATH=src $(PYTHON) examples/full_demo.py

server:
	PYTHONPATH=src uvicorn aibpe.serve:app --reload

clean:
	rm -rf .aibpe .pytest_cache
