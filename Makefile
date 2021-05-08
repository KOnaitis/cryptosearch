VENV = venv
VEA = . $(VENV)/bin/activate

shell:
	$(VEA); \
	python manage.py shell_plus

venv:
	test -d $(VENV) || python -m venv -p python3.9 $(VENV)

install: venv
	$(VEA); \
	pip install -r requirements

lint: venv
	$(VEA); \
    flake8 project api --statistics --max-line-length=100

test: venv
	$(VEA); \
	pytest

validate: lint test;
