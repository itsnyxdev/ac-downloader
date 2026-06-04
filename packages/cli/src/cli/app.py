import typer

from .commands.config import config_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(config_app, name="config")
