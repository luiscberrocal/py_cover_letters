class CoverLetterException(Exception):
    pass


class UnsupportedOperationException(CoverLetterException):
    """Raise on operations not supported."""
