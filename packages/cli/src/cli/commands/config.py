import typer

from ..utils import printer
from ..utils.config import config_file, load, save

config_app = typer.Typer(help="Manage configuration")


@config_app.command(help="Display all configuration values")
def show() -> None:
    config = load()

    if not config:
        printer.error("No configuration found")
        return

    printer.table([{"Key": k, "Value": v} for k, v in config.items()])


@config_app.command(help="Set a configuration value")
def set(key: str, value: str) -> None:  # noqa: A001
    config = load()
    config[key] = value
    save(config)

    printer.success(f"{key} = {value}")


@config_app.command(help="Reset configuration to defaults")
def reset() -> None:
    path = config_file()

    if path.exists():
        path.unlink()
        printer.success("Configuration reset successfully.")
    else:
        printer.success("No configuration file found.")
