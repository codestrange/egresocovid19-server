import typer
from beanie import init_beanie
from beanie.operators import RegEx

from ..database import UserEntity, client, entities
from ..services.auth_service import AuthService
from ..settings import get_settings
from ..utils.run_sync import run_sync

app = typer.Typer()

auth_service = AuthService(settings=get_settings())


@app.command()
def create(
    name: str = typer.Option(..., prompt=True),
    email: str = typer.Option(..., prompt=True),
    phone: str = typer.Option(..., prompt=True),
    password: str = typer.Option(
        ...,
        prompt=True,
        confirmation_prompt=True,
        hide_input=True,
    ),
    email_confirmed: bool = typer.Option(False, prompt=True),
    phone_confirmed: bool = typer.Option(False, prompt=True),
    disabled: bool = typer.Option(False, prompt=True),
):
    run_sync(
        init_beanie(
            database=client.egresocovid19,
            document_models=entities,  # type: ignore
        )
    )
    hashed_password = auth_service.get_password_hash(password)
    user = UserEntity(
        name=name,
        email=email,
        phone=phone,
        hashed_password=hashed_password,
        email_confirmed=email_confirmed,
        phone_confirmed=phone_confirmed,
        disabled=disabled,
    )
    run_sync(user.save())
    typer.echo(user)


@app.command()
def lists(
    query: str = typer.Option(..., prompt=True),
):
    run_sync(
        init_beanie(
            database=client.egresocovid19,
            document_models=entities,  # type: ignore
        )
    )
    users = run_sync(UserEntity.find(RegEx(UserEntity.email, query)).to_list())
    typer.echo(users)
