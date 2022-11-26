from pathlib import Path

from .. import CURRENT_CONFIGURATION
from ..constants import EXCEL_FILE, SQLITE_FILE
from ..db.excel import ExcelCoverLetterManager
from ..db.sqlite import CoverLetterManager
from ..db.synchronizers import synchronize_to_db
from ..enums import FilterType


def do_generate():
    excel_manager = ExcelCoverLetterManager(EXCEL_FILE)
    db_manager = CoverLetterManager(SQLITE_FILE)
    synchronize_to_db(excel_manager, db_manager)
    not_created = db_manager.filter(FilterType.COVER_LETTER_NOT_CREATED)
    for to_create in not_created:
        to_create

