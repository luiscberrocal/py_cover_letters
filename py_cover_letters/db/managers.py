from pathlib import Path
from typing import Protocol, List, Optional, Dict

from py_cover_letters.config import CoverLetter
from py_cover_letters.constants import COLUMN_MAPPING
from py_cover_letters.enums import FilterType


class CoverLetterManager(Protocol):

    def get(self, cover_letter_id: int) -> CoverLetter:
        ...

    def create(self, cover_letter: CoverLetter) -> CoverLetter:
        ...

    def delete(self, cover_letter: CoverLetter) -> bool:
        ...

    def update(self, project: CoverLetter) -> CoverLetter:
        ...

    def list(self) -> List[CoverLetter]:
        ...

    def filter(self, filter_type: FilterType) -> List[CoverLetter]:
        ...

class ExcelManager:
    def __init__(self, filename: Path, column_mapping: Optional[Dict[int, str]] = None,
                 sheet_name: str = 'Cover letters'):
        self.filename = filename
        if column_mapping is None:
            self.column_mapping = COLUMN_MAPPING
        else:
            self.column_mapping = column_mapping
        self.columns = [col_name for _, col_name in self.column_mapping.items()]
        self.sheet_name = sheet_name
