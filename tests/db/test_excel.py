from py_cover_letters.db.excel import CoverLetterManager, COLUMN_MAPPING


class TestExcelCoverManager:

    def test_write_template(self, output_folder):
        filename = output_folder / 'sample_cover_letter.xlsx'
        filename.unlink(missing_ok=True)
        manager = CoverLetterManager(filename, column_mapping=COLUMN_MAPPING)

        manager.write_template()
        assert filename.exists()
