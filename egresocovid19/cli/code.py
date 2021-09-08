from os import system

import typer

app = typer.Typer()


@app.command()
def run(host: str = "localhost", port: int = 8000):
    install()
    system(
        "poetry run uvicorn egresocovid19.main:app "
        + f"--reload --host {host} --port {port}"
    )


@app.command()
def tests():
    typer.echo("Running tests ...")
    system(
        "poetry run flake8 . --count --show-source "
        + "--statistics --max-line-length=88 --extend-ignore=E203"
    )
    system("poetry run black . --check")
    system("poetry run isort . --profile=black")
    system("poetry run pytest --cov=./ --cov-report=xml")


@app.command()
def export():
    system("poetry export -f requirements.txt -o requirements.txt --without-hashes")


@app.command()
def install():
    typer.echo("Installing dependencies ...")
    system("poetry install")
