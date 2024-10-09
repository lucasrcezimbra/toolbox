.PHONY: build dev dbdump dbload dbnew install lint test

build:
	poetry run python manage.py distill-local --collectstatic --force ./docs
	echo 'toolbox.cezimbra.me' > docs/CNAME

dev:
	poetry run python manage.py runserver

dbdump:
	poetry run python manage.py dumpdata core.list --natural-primary --natural-foreign  --indent 4 -o data/lists.json

dbload:
	poetry run python manage.py runscript import_from_github
	poetry run python manage.py loaddata data/lists.json

dbnew:
	rm db.sqlite3
	poetry run python manage.py migrate

collectdata:
	poetry run github-to-sqlite starred github.sqlite3 $(github)

install:
	poetry install
	poetry run pre-commit install
	cp contrib/env-sample .env
	poetry run python manage.py migrate

lint:
	poetry run pre-commit run -a

test:
	poetry run pytest
