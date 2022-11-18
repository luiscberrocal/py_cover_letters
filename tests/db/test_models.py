from py_cover_letters.db.models import CoverLetter


def test_attributes():
    cover_letter = CoverLetter().dict()
    print(CoverLetter.__fields__.keys())

