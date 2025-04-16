init:
	python -m venv venv && source venv/bin/activate && pip install -r requirements-dev.txt

build: init
	./venv/bin/python -m build
