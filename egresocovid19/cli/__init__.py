import typer

from .code import app as code
from .users import app as users

app = typer.Typer()
app.add_typer(code, name="code")
app.add_typer(users, name="users")
