VENV = venv
VEA = . $(VENV)/bin/activate

shell:
	$(VEA); \
	python manage.py shell_plus

venv:
	test -d $(VENV) || python -m virtualenv -p python3.9 $(VENV)

install: venv
	$(VEA); \
	pip install pip setuptools; \
	pip install -r requirements

migrate:
	$(VEA); \
	python manage.py makemigrations; \
	python manage.py migrate
