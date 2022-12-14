import re

from py_cover_letters.constants import COLUMN_MAPPING
from py_cover_letters.db.managers import ExcelManager
from py_cover_letters.utils import backup_file


def test_backup(output_folder):
    filename = output_folder / 'sample_cover_letter.xlsx'
    filename.unlink(missing_ok=True)
    ExcelManager(filename, column_mapping=COLUMN_MAPPING)

    backup_filename = backup_file(filename, output_folder)
    assert backup_filename.exists()
    regex = re.compile(r'\d{8}_\d{6}_v\d\.\d\.\d_sample_cover_letter\.xlsx')
    match = regex.match(backup_filename.name)
    assert match is not None, f'Filename {backup_filename.name} did not match regexp'
    backup_filename.unlink()
