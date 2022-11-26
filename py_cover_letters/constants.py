from pathlib import Path

from py_cover_letters import CURRENT_CONFIGURATION

BANNER = """
*******************************************************************************
******************************* PY-COVER-LETTERS **************************
*******************************************************************************
"""  # noqa
COLUMN_MAPPING = {
    1: 'id',
    2: 'company_name',
    3: 'position_name',
    4: 'greeting',
    5: 'to_email',
    6: 'cover_template',
    7: 'date_sent_via_email',
    8: 'date_generated',
    9: 'delete'
}
SQLITE_FILENAME = 'cover_letters.sqlite'
SQLITE_FILE = Path(CURRENT_CONFIGURATION['database']['folder']) / SQLITE_FILENAME
EXCEL_FILE = Path(CURRENT_CONFIGURATION['database']['folder']) / CURRENT_CONFIGURATION['database']['file']
