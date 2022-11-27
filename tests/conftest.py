from pathlib import Path

import pytest

from py_cover_letters.db.sqlite import CoverLetterManager
from tests.factories import CoverLetterFactory
from py_cover_letters.utils import is_libreoffice_installed


@pytest.fixture(scope='session')
def output_folder():
    folder = Path(__file__).parent.parent / 'output'
    folder.mkdir(exist_ok=True)
    return folder


@pytest.fixture(scope='session')
def fixtures_folder():
    folder = Path(__file__).parent.parent / 'tests' / 'fixtures'
    return folder


@pytest.fixture(scope='function')
def testing_database_file(output_folder):
    filename = output_folder / 'temp_cover_letters.sqlite'
    yield filename
    filename.unlink(missing_ok=True)


@pytest.fixture(scope='function')
def excel_file(output_folder):
    filename = output_folder / 'test_cover_letters.xlsx'
    yield filename
    # filename.unlink(missing_ok=True)


@pytest.fixture(scope='function')
def cover_letter_manager(testing_database_file) -> CoverLetterManager:
    cover_letters = CoverLetterFactory.create_batch(5, id=None)
    cover_letters.extend(CoverLetterFactory.create_batch(6, new=True))
    cover_letters.extend(CoverLetterFactory.create_batch(2, new=True, delete=True))
    db_manager = CoverLetterManager(testing_database_file)
    for cover_letter in cover_letters:
        db_manager.create(cover_letter)
    return db_manager


libreoffice_required = pytest.mark.skipif(
    is_libreoffice_installed, reason="Libre office is required to run."
)
