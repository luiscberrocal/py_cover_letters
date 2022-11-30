import datetime
import shutil

from py_cover_letters.db.managers import ExcelManager
from tests.utils import read_excel


def test_update_not_saved(fixtures_folder, output_folder):
    excel_without_id = fixtures_folder / 'test_cover_letters_without_ids.xlsx'
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    timestamp = '001'
    excel_file = output_folder / f'{timestamp}_test_cover_letters_without_ids.xlsx'
    shutil.copy(excel_without_id, excel_file)

    assert len(read_excel(excel_file)) == 50

    manager = ExcelManager(excel_file, backup_folder=output_folder / 'backups')

    assert len(read_excel(excel_file)) == 50

    updated = manager.set_unique_ids()
    assert len(updated) == 50
    assert len(read_excel(excel_file)) == 50

    updated_new = manager.set_unique_ids()
    assert len(updated_new) == 0

    cover_letters = read_excel(excel_file)
    assert len(cover_letters) == 50
