.PHONY: build dev dbdump dbload dbnew install test

build:
	poetry run python manage.py distill-local --collectstatic --force ./docs
	mv docs/tags docs/TEMP
	mkdir docs/tags/
	mv docs/TEMP docs/tags/index.html
	echo 'toolbox.cezimbra.me' > docs/CNAME

dev:
	poetry run python manage.py runserver

dbdump:
	poetry run python manage.py dumpdata core --natural-primary --natural-foreign --indent 4 -o data/github_stars.json
	poetry run python manage.py dumpdata taggit --natural-primary --natural-foreign --indent 4 -o data/tags.json

dbload:
	poetry run python manage.py loaddata data/github_stars.json data/tags.json
	poetry run python data/tool_tags.py

dbnew:
	rm db.sqlite3
	poetry run python manage.py migrate

datagen:
	poetry run github-to-sqlite starred github.sqlite3 lucasrcezimbra
	poetry run sqlite-utils github.sqlite3 \
		"SELECT \
				starred_at AS created_at, \
				starred_at AS updated_at, \
				repos.html_url as url_github, \
				repos.name, \
				'' as notes \
		 FROM \
				stars \
				JOIN repos ON \
						stars.repo = repos.id \
		 ORDER BY starred_at" \
		| sqlite-utils insert db.sqlite3 core_tool -

install:
	poetry install
	poetry run pre-commit install
	cp contrib/env-sample .env
	poetry run python manage.py migrate

test:
	poetry run pytest
