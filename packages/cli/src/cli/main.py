try:
    from .app import app
except ImportError:
    from cli.app import app


def main() -> None:
    app()


if __name__ == "__main__":
    main()
