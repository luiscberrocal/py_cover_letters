from pathlib import Path

from .. import CURRENT_CONFIGURATION
from ..constants import EXCEL_FILE, SQLITE_FILE, DEFAULT_OUTPUT_FOLDER, DEFAULT_TEMPLATE
from ..db.excel import ExcelCoverLetterManager
from ..db.sqlite import CoverLetterManager
from ..db.synchronizers import synchronize_to_db
from ..enums import FilterType
from ..generators import build_cover_letter_filename, write_docx_cover_letter
from ..utils import is_libreoffice_installed


def do_generate():
    excel_manager = ExcelCoverLetterManager(EXCEL_FILE)
    db_manager = CoverLetterManager(SQLITE_FILE)
    synchronize_to_db(excel_manager, db_manager)
    not_created = db_manager.filter(FilterType.COVER_LETTER_NOT_CREATED)

    for to_create in not_created:
        ctx = to_create.get_context()
        cover_letter_file = build_cover_letter_filename(DEFAULT_OUTPUT_FOLDER, ctx)
        write_docx_cover_letter(DEFAULT_TEMPLATE, ctx, cover_letter_file)
        if is_libreoffice_installed:
            pass
        else:
            warnings = 'Could not create PDF.'