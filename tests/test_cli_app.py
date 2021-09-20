from egresocovid19.cli import app
from mimesis import Text
from typer.testing import CliRunner

runner = CliRunner()


def test_cli_users_lists():
    fake_text = Text()
    result = runner.invoke(
        app,
        ["users", "lists"],
        input=f"{fake_text.word()}\n",
    )
    assert result.exit_code == 0
