import typer

from .users import app as users

app = typer.Typer()
app.add_typer(users, name="users")
