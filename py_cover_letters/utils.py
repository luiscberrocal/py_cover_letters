import datetime
import shutil
import subprocess
from functools import partial
from pathlib import Path
from typing import List, Tuple

from py_cover_letters import CURRENT_CONFIGURATION


def run_commands(commands: List[str], encoding: str = 'utf-8') -> Tuple[List[str], List[str]]:
    """
    :param commands: <list> The command and parameters to run
    :param encoding: <str> Encoding for the shell
    :return: <tuple> Containing 2 lists. First one with results and the Second one with errors if any.
    """
    result = subprocess.run(commands,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    result_lines = result.stdout.decode(encoding).split('\n')[:-1]
    error_lines = result.stderr.decode(encoding).split('\n')[:-1]
    return result_lines, error_lines


def backup_file(filename: Path, backup_folder: Path, add_version: bool = True) -> Path:
    datetime_format = '%Y%m%d_%H%M%S'
    if add_version:
        from . import __version__ as current_version
        version_val = f'v{current_version}_'
    else:
        version_val = ''
    timestamp = datetime.datetime.now().strftime(datetime_format)
    backup_filename = backup_folder / f'{timestamp}_{version_val}{filename.name}'
    shutil.copy(filename, backup_filename)
    return backup_filename


backup_excel = partial(backup_file, Path(CURRENT_CONFIGURATION['database']['backup_folder']))
