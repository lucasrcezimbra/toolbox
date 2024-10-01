# Toolbox


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
