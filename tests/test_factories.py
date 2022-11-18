from tests.factories import CoverLetterFactory


class TestCoverLetterFactory:

    def test_create(self):
        cover_letter = CoverLetterFactory.create()
        cover_letter_dict = cover_letter.dict()
        expected_fields = {'company_name', 'cover_template', 'date_generated', 'date_sent_via_email', 'description',
                           'greeting', 'id', 'position_name', 'delete', 'to_email'}
        assert set(cover_letter_dict.keys()) == expected_fields
