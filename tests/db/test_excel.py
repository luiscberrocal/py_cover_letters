from py_cover_letters.db.excel import ExcelCoverLetterManager, COLUMN_MAPPING


class TestExcelCoverManager:

    def test_write_template(self, output_folder):
        filename = output_folder / 'sample_cover_letter.xlsx'
        filename.unlink(missing_ok=True)
        manager = ExcelCoverLetterManager(filename, column_mapping=COLUMN_MAPPING)

        manager.write_template()
        assert filename.exists()
