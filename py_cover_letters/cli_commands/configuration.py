import click

from py_cover_letters.config import ConfigurationManager
from py_cover_letters.utils import backup_file


@click.command(help='Configure the application.')
@click.argument('sub_command', required=False)
@click.option('--overwrite', is_flag=True, default=False, help="Overwrite the configuration file.")
def config(sub_command, overwrite):
    """Configure the application."""
    if sub_command is None:
        click.echo('Configuration')
        config_manager = ConfigurationManager()
        do_configuration(config_manager, overwrite)
    else:
        click.echo(f'sub command {sub_command}')


def do_configuration(config_manager: ConfigurationManager, overwrite: bool):
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


@click.command(help='List the current configuration.')
def show():
    print('Show configuration')
