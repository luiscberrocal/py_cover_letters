from pathlib import Path
from typing import Any, List, Dict

from ..constants import EXCEL_FILE, DEFAULT_OUTPUT_FOLDER, DEFAULT_TEMPLATE
from ..db.managers import ExcelManager
from ..enums import FilterType
from ..generators import build_cover_letter_filename, write_docx_cover_letter, convert_docx_to_pdf
from ..utils import is_libreoffice_installed


def do_generate(excel_file: Path) -> List[Dict[str, Any]]:
    excel_manager = ExcelManager(excel_file)
    not_created = excel_manager.filter(FilterType.COVER_LETTER_NOT_CREATED)
    generated = list()
    for cover_letter in not_created:
        data = {'cover_letter': cover_letter.dict()}
        ctx = cover_letter.get_context()
        cover_letter_file = build_cover_letter_filename(DEFAULT_OUTPUT_FOLDER, ctx)
        write_docx_cover_letter(DEFAULT_TEMPLATE, ctx, cover_letter_file)
        data['docx'] = cover_letter_file
        if is_libreoffice_installed():
            convert_docx_to_pdf(cover_letter_file)
        generated.append(data)
    return generated
