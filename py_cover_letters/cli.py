"""Console script for py_cover_letters."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("py-cover-letters")
    click.echo("=" * len("py-cover-letters"))
    click.echo("Project to create, manage and email cover letters.")


if __name__ == "__main__":
    main()  # pragma: no cover
