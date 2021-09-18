import typer
from beanie import init_beanie

from ..database import client, entities
from ..seedbed import initialize_provinces_data
from ..utils.run_sync import run_sync

app = typer.Typer()


@app.command()
def add_initial_data():
    run_sync(
        init_beanie(
            database=client.egresocovid19,
            document_models=entities,  # type: ignore
        )
    )
    run_sync(initialize_provinces_data())
    typer.echo("Data initialized")
