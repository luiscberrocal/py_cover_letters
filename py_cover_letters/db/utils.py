import datetime
import shutil
from pathlib import Path


def backup_file(filename: Path, backup_folder: Path) -> Path:
    datetime_format = '%Y%m%d_%H%M%S'
    timestamp = datetime.datetime.now().strftime(datetime_format)
    backup_filename = backup_folder / f'{timestamp}_{filename.name}'
    shutil.copy(filename, backup_filename)
    return backup_filename
