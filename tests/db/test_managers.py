from py_cover_letters.db.sqlite import CoverLetterManager
from py_cover_letters.enums import FilterType
from tests.factories import CoverLetterFactory


class TestCoverLetterManager:

    def test_create(self, testing_database_file):
        manager = CoverLetterManager(testing_database_file)

        cover_letter = CoverLetterFactory.create(new=True)

        assert cover_letter.id is None

        db_cover_letter = manager.create(cover_letter)

        assert db_cover_letter.id is not None
        assert cover_letter.id is not None

    def test_filter_deleted(self, cover_letter_manager):
        deleted = cover_letter_manager.filter(FilterType.COVER_LETTER_NOT_DELETED)
        all_cover_letters = cover_letter_manager.list()
        assert len(deleted) == 11
        assert len(all_cover_letters) == 13

    def test_filter_not_sent(self, cover_letter_manager):
        not_created = cover_letter_manager.filter(FilterType.COVER_LETTER_NOT_CREATED)
        all_cover_letters = cover_letter_manager.list()
        assert len(not_created) == 8
        assert len(all_cover_letters) == 13
