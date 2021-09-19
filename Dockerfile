FROM docker.uclv.cu/tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY poetry.lock .

COPY pyproject.toml .

RUN poetry install

COPY ./egresocovid19 /app/app
