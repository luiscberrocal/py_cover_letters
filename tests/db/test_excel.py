from py_cover_letters.db.excel import ExcelCoverLetterManager, COLUMN_MAPPING
from tests.factories import CoverLetterFactory


class TestExcelCoverManager:

    def test_write_template(self, output_folder):
        filename = output_folder / 'sample_cover_letter.xlsx'
        filename.unlink(missing_ok=True)
        manager = ExcelCoverLetterManager(filename, column_mapping=COLUMN_MAPPING)

        manager.write_template()
        assert filename.exists()
    def test_add(self, output_folder):
        filename = output_folder / 'sample_cover_letter.xlsx'
        filename.unlink(missing_ok=True)
        excel_manager = ExcelCoverLetterManager(filename, column_mapping=COLUMN_MAPPING)

        excel_manager.write_template()
        assert filename.exists()
        cover_letters = CoverLetterFactory.create_batch(5)
        excel_manager.add(cover_letters)

        read_cl = excel_manager.read()
        assert len(read_cl) == 5
        print(read_cl)
