.PHONY: build dev dbdump dbload dbnew install lint test

build:
	poetry run python manage.py distill-local --collectstatic --force ./docs
	mv docs/tags docs/TEMP
	mkdir docs/tags/
	mv docs/TEMP docs/tags/index.html
	echo 'toolbox.cezimbra.me' > docs/CNAME

dev:
	poetry run python manage.py runserver

dbload:
	poetry run python manage.py runscript import_from_github

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
