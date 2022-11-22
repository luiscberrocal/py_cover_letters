import sys
from platform import python_version

import click


@click.command('about', help='About this application.')
def do_about():
    click.echo(f'Operating System: {sys.platform}')
    click.echo(f'Python : {python_version()}')
