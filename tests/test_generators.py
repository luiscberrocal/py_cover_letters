import re

from py_cover_letters.generators import get_libreoffice_version


def test_get_libreoffice_version():
    regexp = re.compile(r"(\d\.\d\.\d\.?\d?)\s?(\d*)\(Build:\d+\)")
    version, is_valid = get_libreoffice_version()
    assert regexp.match(version) is not None
    assert is_valid