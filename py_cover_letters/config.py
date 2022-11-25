import json
import os
from pathlib import Path
from typing import Dict, Any

import toml
from pydantic import BaseModel, ValidationError

from .exceptions import ConfigurationError
from .utils import backup_file


class CoverLetter(BaseModel):
    template_folder: str
    default_template: str
    default_output_folder: str


class Gmail(BaseModel):
    email: str
    token: str


class Database(BaseModel):
    folder: str
    file: str
    backup_folder: str


class Configuration(BaseModel):
    cover_letters: CoverLetter
    gmail: Gmail
    database: Database


class ConfigurationManager:

    def __init__(self, config_folder: Path | None = None):
        if config_folder is None:
            self.config_folder = Path().home() / '.py_cover_letters'
            self.config_folder.mkdir(exist_ok=True)
        else:
            self.config_folder = config_folder

        self.config_file = self.config_folder / 'configuration.toml'
        self.username = os.getlogin()

    def get_sample_config(self) -> Dict[str, Any]:
        data = {'cover_letters': {'template_folder': str(self.config_folder / 'templates'),
                                  'default_template': 'Cover Letter Template.docx',
                                  'default_output_folder': str(Path(os.getcwd()) / 'output')},
                'gmail': {'email': f'{self.username}@gmail.com',
                          'token': 'SECRET'},
                'database': {'folder': str(Path(os.getcwd()) / 'data'),
                             'file': 'cover_letters.xlsx',
                             'backup_folder': str(Path(os.getcwd()) / 'data' / 'backups')}
                }
        return data

    def write_configuration(self, config_data: Dict[str, Any], over_write=False):
        if self.config_file.exists() and not over_write:
            raise Exception('Cannot overwrite config file.')
        with open(self.config_file, 'w') as f:
            toml.dump(config_data, f)

    def get_configuration(self):
        if not self.config_folder.exists():
            error_message = 'No configuration file found. Run py-cover-letters config.'
            raise ConfigurationError(error_message)

        with open(self.config_file, 'r') as f:
            configuration = toml.load(f)
        return configuration

    def get_configuration_obj(self):
        config = self.get_configuration()
        config_obj = Configuration(**config)
        return config_obj

    def export_to_json(self, export_file: Path):
        config = self.get_configuration()
        with open(export_file, 'w') as f:
            json.dump(config, f)

    def is_valid(self, raise_error: bool = False) -> bool:
        try:
            self.get_configuration_obj()
            return True
        except ValidationError as e:
            error_msg = f'Configuration error. Type: {e.__class__.__name__} Error: {e}'
            if raise_error:
                raise ConfigurationError(error_msg)
            return False

    def backup(self):
        config_backup_folder = self.config_folder / 'backups'
        config_backup_folder.mkdir(exist_ok=True)
        backup_filename = backup_file(self.config_file, config_backup_folder)


    @classmethod
    def get_current(cls):
        config = cls()
        return config.get_configuration()
