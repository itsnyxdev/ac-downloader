import typer

from .commands.config import config_app
from .commands.convert import convert


def _get_version() -> str:
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version("cli")
    except PackageNotFoundError:
        return "0.1.0"


app = typer.Typer(no_args_is_help=True)


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        False, "--version", "-v", help="Show version and exit"
    ),
) -> None:
    if version:
        typer.echo(f"ac-downloader {_get_version()}")
        raise typer.Exit()


app.add_typer(config_app, name="config")
app.command(help="Convert an Adobe Connect XML export to MP4")(convert)
