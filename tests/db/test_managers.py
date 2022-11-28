import datetime
import shutil

from py_cover_letters.db.managers import ExcelManager


def test_update_not_saved(fixtures_folder, output_folder):
    excel_withou_id = fixtures_folder / 'test_cover_letters_without_ids.xlsx'
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_folder / f'{timestamp}_test_cover_letters_without_ids.xlsx'
    shutil.copy(excel_withou_id, output_file)

    manager = ExcelManager(output_file, backup_folder=output_folder / 'backups')

    updated = manager.update_not_saved()
    assert len(updated) == 50
