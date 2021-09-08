HOST = localhost
PORT = 8000

install:
	poetry install

tests:
	poetry run flake8 . --count --show-source --statistics --max-line-length=88 --extend-ignore=E203
	poetry run black . --check
	poetry run isort . --profile=black
	poetry run pytest --cov=./ --cov-report=xml

export:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

run: install
	poetry run uvicorn egresocovid19.main:app --reload --host ${HOST} --port ${PORT}
