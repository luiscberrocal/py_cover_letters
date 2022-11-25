from pathlib import Path

from .. import CURRENT_CONFIGURATION
from ..db.excel import ExcelCoverLetterManager
from ..db.synchronizers import synchronize_to_db

def do_generate():
    excel_file = Path(CURRENT_CONFIGURATION['database']['folder']) / CURRENT_CONFIGURATION['file']
    excel_manager = ExcelCoverLetterManager
    pass
