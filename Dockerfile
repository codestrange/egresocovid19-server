FROM docker.uclv.cu/tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY poetry.lock .

COPY pyproject.toml .

RUN apt install curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

RUN poetry config settings.virtualenvs.create false

RUN poetry install

COPY ./egresocovid19 /app/app
