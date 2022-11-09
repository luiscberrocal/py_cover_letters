from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class CoverLetter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_name: str
    position_name: str
    description: Optional[str]
    greeting: Optional[str]
    to_email: Optional[str]
    cover_template: Optional[str]
    date_sent_via_email: Optional[datetime]
    date_generated: Optional[datetime]
