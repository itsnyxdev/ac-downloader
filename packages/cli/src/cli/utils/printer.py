from rich.console import Console
from rich.table import Table

console = Console()


def success(message: str) -> None:
    console.print(f"[green]:white_check_mark:[/green] {message}")


def error(message: str) -> None:
    console.print(f"[red]:x:[/red] {message}")


def warning(message: str) -> None:
    console.print(f"[yellow]:warning:[/yellow] {message}")


def info(message: str) -> None:
    console.print(f"[blue]:information:[/blue] {message}")


def table(
    data: list[dict],
    title: str | None = None,
    columns: list[str] | None = None,
) -> None:
    if not data:
        warning("No data to display")
        return

    table = Table(title=title)

    if columns is None:
        columns = list(data[0].keys())

    for col in columns:
        table.add_column(col, style="cyan")

    for row in data:
        table.add_row(*[str(row.get(col, "")) for col in columns])

    console.print(table)
