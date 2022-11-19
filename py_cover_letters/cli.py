"""Console script for py_cover_letters."""

import click

from py_cover_letters.config import ConfigurationManager
from py_cover_letters.utils import backup_file
from . import __version__ as current_version


@click.group()
@click.version_option(version=current_version)
def main():
    pass


@click.command(help='Configure the application.')
@click.option('--overwrite', is_flag=True, default=False, help="Overwrite the configuration file.")
def config(overwrite):
    click.echo('Configuration')
    config_manager = ConfigurationManager()
    configuration = config_manager.get_sample_config()
    if config_manager.config_file.exists() and not overwrite:
        click.echo(f'The configuration already exists ({config_manager.config_file}). Use the --overwrite flag.')
        return
    if config_manager.config_file.exists() and overwrite:
        config_backup_folder = config_manager.config_folder / 'backups'
        config_backup_folder.mkdir(exist_ok=True)
        backup_filename = backup_file(config_manager.config_file, config_backup_folder)
        click.echo(f'Backup of the current config file was made {backup_filename}')
        configuration = config_manager.get_configuration()
    new_configuration = configuration.copy()
    for key, key_conf in configuration.items():
        click.echo(f'[{key.upper()}]')
        for sub_key, sub_key_conf in key_conf.items():
            prompt_text = f'{sub_key.replace("_", " ")}'
            new_key = click.prompt(prompt_text, default=sub_key_conf)
            new_configuration[key][sub_key] = new_key
    config_manager.write_configuration(configuration, over_write=True)


@click.command(help='Create cover letters from master Excel file.')
def create():
    click.echo('Creating cover letters')


@click.command(help='Email cover letters.')
@click.option('--all', 'email_all', is_flag=True, default=True, help='Email all the unsent cover letters.')
@click.option('--confirm', is_flag=True, default=True, help='Confirmation before sending the email.')
def email(email_all: bool, confirm: bool):
    click.echo('Email cover letters')


main.add_command(config)
main.add_command(create)

main.add_command(email)

if __name__ == "__main__":
    main()  # pragma: no cover
