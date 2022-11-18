from py_cover_letters.db.managers import CoverLetterManager
from tests.factories import CoverLetterFactory


class TestCoverLetterManager:

    def test_create(self, testing_database_file):
        manager = CoverLetterManager(testing_database_file)

        cover_letter = CoverLetterFactory.create(new=True)

        assert cover_letter.id is None

        db_cover_letter = manager.create(cover_letter)

        assert db_cover_letter.id is not None
        assert cover_letter.id is not None

