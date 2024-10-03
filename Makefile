.PHONY: dbdump dbload dbnew

dbdump:
		poetry run python manage.py dumpdata core --natural-primary --natural-foreign --indent 4 -o data/github_stars.json
		poetry run python manage.py dumpdata taggit --natural-primary --natural-foreign  --indent 4 -o data/tags.json

dbload:
		poetry run python manage.py loaddata data/github_stars.json data/tags.json

dbnew:
		rm db.sqlite3
		poetry run python manage.py migrate
