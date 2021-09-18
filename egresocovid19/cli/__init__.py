import typer

from .code import app as code
from .db import app as db
from .users import app as users

app = typer.Typer()
app.add_typer(code, name="code")
app.add_typer(db, name="db")
app.add_typer(users, name="users")
