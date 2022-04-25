# Music Microservice

This microservice manages the music related topics (songs, albums, playlists).

## Local development

To run the application there are two options:

### With Docker

Run `docker-compose up --build` to start the app in port 8000 or `PORT=xxxx docker-compose up --build` to use a specific `xxxx` port.

### With _virtualenv_

#### Run the server

- First of all create a _virtualenv_ (_i.e._ `python3 -m venv venv`) and activate it (`source venv/bin/activate`).
- Upgrade pip and install the dependencies: `pip install --upgrade pip && pip install -r requirements.txt`.
- Update the database structure: `alembic upgrade head`.
- Run the app with:
	```bash
	uvicorn app.main:app --host 0.0.0.0 --port 8000
	```

#### Changes to database models

To create database migrations for changes done in _models_ files, run `alembic revision --autogenerate -m "Title of migration"`. Then, update the database with `alembic upgrade head`.

## Tests

Again, there are two options. Note that the _virtualenv_ option is naturally faster.

### With Docker

Run the command:

```bash
docker-compose run --rm fastapi sh -c "pip install -q -q -r /code/requirements.dev.txt && sh /code/test.sh"
```

### With _virtualenv_

- Be sure to be in the virtual environment, if not, activate it (_i.e._ `source venv/bin/activate`).
- The first time, install the dev dependencies: `pip install -r requirements.dev.txt`.
- Run the linter and tests with `./test.sh`.

## Docs

The documentation is generated automatically by FastAPI. It's available in the server at `/docs` (Swagger) and `/redoc` (ReDoc)
