from py_cover_letters.db.excel import ExcelCoverLetterManager, COLUMN_MAPPING
from py_cover_letters.db.sqlite import CoverLetterManager
from py_cover_letters.db.synchronizers import synchronize_to_db, synchronize_to_excel
from tests.factories import CoverLetterFactory


def test_synchronize_to_db(output_folder, testing_database_file):
    filename = output_folder / 'sample_cover_letter.xlsx'
    filename.unlink(missing_ok=True)
    excel_manager = ExcelCoverLetterManager(filename, column_mapping=COLUMN_MAPPING)

    excel_manager.write_template()
    assert filename.exists()
    cover_letters = CoverLetterFactory.create_batch(5, new=True)
    excel_manager.add(cover_letters)

    manager = CoverLetterManager(testing_database_file)
    results = synchronize_to_db(excel_manager, manager)

    assert len(results[0]) == 5
    assert len(results[1]) == 0
    assert len(results[2]) == 0


def test_synchronize_to_excel(cover_letter_manager, excel_file):
    excel_manager = ExcelCoverLetterManager(excel_file, column_mapping=COLUMN_MAPPING)
    excel_manager.filename.unlink(missing_ok=True)
    excel_manager.write_template()
    backup_filename, count = synchronize_to_excel(excel_manager, cover_letter_manager)
    assert backup_filename.exists()
    assert count == 11

