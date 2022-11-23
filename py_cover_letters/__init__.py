"""Top-level package for Py Cover Letters."""

__author__ = """Luis C. Berrocal"""
__email__ = 'luis.berrocal.1942@gmail.com'
__version__ = '0.2.0'

from py_cover_letters.config import ConfigurationManager
print('>>>>>  before current config')
CURRENT_CONFIGURATION = ConfigurationManager().get_current()
print(f'>>>>>  after current config {CURRENT_CONFIGURATION}')
