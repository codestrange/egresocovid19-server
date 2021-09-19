HOST = localhost
PORT = 8000

install:
	poetry install

tests: install
	poetry run flake8 . --count --show-source --statistics --max-line-length=88 --extend-ignore=E203
	poetry run black . --check
	poetry run isort . --profile=black
	poetry run pytest --cov=./ --cov-report=xml

export:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

run: install
	poetry run uvicorn egresocovid19.main:app --reload --host ${HOST} --port ${PORT}

deploy:
	docker-compose build && docker-compose up -d

enter_to_api:
	docker exec -t egresocovid19-api /bin/bash

enter_to_db:
	docker exec -t egresocovid19-db /bin/bash
