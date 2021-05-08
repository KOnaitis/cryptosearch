VENV = venv
VEA = . $(VENV)/bin/activate

shell:
	$(VEA); \
	python manage.py shell_plus

venv:
	test -d $(VENV) || python3.9 -m venv $(VENV)

install: venv
	$(VEA); \
	pip install -r requirements

lint: venv
	$(VEA); \
    flake8 project api --statistics --max-line-length=127

test: venv
	$(VEA); \
	DJANGO_SETTINGS_MODULE=project.settings pytest

migrate: venv
	$(VEA); \
    ./manage.py makemigrations; \
	./manage.py migrate

static: venv
	$(VEA); \
	./manage.py collectstatic


prepare: static migrate;

validate: lint test;
