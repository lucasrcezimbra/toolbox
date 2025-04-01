.PHONY: build datacollect dataupdate dbdump dbload dbnew dev install lint test

build:
	poetry run python manage.py distill-local --collectstatic --force ./docs
	echo 'toolbox.cezimbra.me' > docs/CNAME

datacollect:
	poetry run github-to-sqlite starred github.sqlite3 $(github)

datafix:
	poetry run python manage.py loaddata data/lists.json 2>&1 1>/dev/null | xargs bin/datafix

dataupdate:
	make datacollect github=$(github)
	make dbnew
	make dbload

dbdump:
	poetry run python manage.py dumpdata core.list --natural-primary --natural-foreign  --indent 4 -o data/lists.json
	poetry run python manage.py runscript dumpnotes

dbload:
	poetry run python manage.py runscript import_from_github
	poetry run python manage.py runscript loadnotes
	poetry run python manage.py loaddata data/lists.json

dbnew:
	rm db.sqlite3
	poetry run python manage.py migrate

dev:
	poetry run python manage.py runserver

install:
	poetry install
	poetry run pre-commit install
	cp contrib/env-sample .env
	poetry run python manage.py migrate

lint:
	poetry run pre-commit run -a

test:
	poetry run pytest
