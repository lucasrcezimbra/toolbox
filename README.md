# Toolbox

![](./contrib/screenshot.png)

## Installation
```bash
git clone git@github.com:lucasrcezimbra/toolbox.git
cd toolbox
poetry install
poetry run pre-commit install
cp contrib/env-sample .env
poetry run python manage.py migrate
```

### Test
```bash
poetry run pytest
```

### Run
```bash
poetry run manage.py runserver
```

### Generate the database
```bash
poetry run python manage.py migrate
pipx install github-to-sqlite
github-to-sqlite starred github.db lucasrcezimbra
pipx install sqlite-utils
sqlite-utils github.db "select starred_at as created_at, starred_at as updated_at, repos.html_url as url_github, repos.name from stars join repos on stars.repo = repos.id order by starred_at" | sqlite-utils insert db.sqlite3 core_tool -
```
