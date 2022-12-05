from py_cover_letters.db.managers import ExcelManager
from tests.factories import CoverLetterFactory
from tests.utils import read_excel


def test_update_not_saved(excel_file_without_id, output_folder):
    # excel_without_id = fixtures_folder / 'test_cover_letters_without_ids.xlsx'
    # timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    # timestamp = '001'
    # excel_file = output_folder / f'{timestamp}_test_cover_letters_without_ids.xlsx'
    # shutil.copy(excel_without_id, excel_file)

    assert len(read_excel(excel_file_without_id)) == 50

    manager = ExcelManager(excel_file_without_id, backup_folder=output_folder / 'backups')

    assert len(read_excel(excel_file_without_id)) == 50

    updated = manager.set_unique_ids()
    assert len(updated) == 50
    assert len(read_excel(excel_file_without_id)) == 50

    updated_new = manager.set_unique_ids()
    assert len(updated_new) == 0

    cover_letters = read_excel(excel_file_without_id)
    assert len(cover_letters) == 50


class TestExcelManager:

    def test_add(self, excel_file):
        cover_letters = CoverLetterFactory.create_batch(5, new=True)
        manager = ExcelManager(excel_file)
        assert len(manager.cover_letters) == 0
        manager.add(cover_letters)
        assert len(manager.cover_letters) == 5
        for cover_letter in manager.cover_letters:
            assert cover_letter.id is not None

    def test_update(self, excel_file):
        cover_letters = CoverLetterFactory.create_batch(5, new=True)
        manager = ExcelManager(excel_file)
        assert len(manager.cover_letters) == 0
        manager.add(cover_letters)

        cover_letter = manager.cover_letters[3]
        cover_letter.delete = True
        manager.update([cover_letter])

        cover_letter_list = read_excel(excel_file)
        assert len(cover_letter_list) == 5
        assert cover_letter_list[3]['delete']
