from pathlib import Path
from typing import Dict, Any, List

from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook

from .managers import CoverLetterManager
from ..exceptions import CoverLetterException


def simple_write_to_excel(filename: Path, headers: Dict[str, Any], lines: List[Dict[str, Any]]):
    """Writes to excel a List of dictionaries. The headers keys must match the keys of the values to write.
    The headers must contain a dictionary with the title key."""
    wb = Workbook()
    sheet = wb.create_sheet()
    row = 1
    col = 1
    for key, header in headers.items():
        sheet.cell(row=row, column=col, value=header['title'])
        col += 1
    row += 1
    for line in lines:
        col = 1
        for key in headers.keys():
            value = line.get(key)
            if value is not None:
                sheet.cell(row=row, column=col, value=value)
            col += 1
        row += 1

    wb.save(filename)


COLUMN_MAPPING = {
    0: 'company_name',
    1: 'company_name',
    2: 'position_name',
    3: 'greeting',
    4: 'to_email',
    5: 'cover_template',
    6: 'date_sent_via_email',
    7: 'date_generated'
}


class ExcelCoverLetterManager:

    def __init__(self, filename: Path, column_mapping: Dict[int, str], db_manager: CoverLetterManager,
                 sheet_name: str = 'Cover letters'):
        self.filename = filename
        self.column_mapping = column_mapping
        self.columns = [col_name for _, col_name in self.column_mapping.items()]
        self.sheet_name = sheet_name
        self.db_manager = db_manager

    def write_template(self):
        if self.filename.exists():
            error_msg = f'Cannot overwrite template {self.filename}'
            raise CoverLetterException(error_msg)

        wb = Workbook()
        sheet = wb.create_sheet(self.sheet_name, 0)
        row = 1
        col = 1
        for column_name in self.columns:
            sheet.cell(row=row, column=col, value=column_name)
            col += 1
        row += 1

        wb.save(self.filename)

    def read(self):
        wb = load_workbook(self.filename)
        sheet = wb[self.sheet_name]

