from pathlib import Path

from sqlmodel import create_engine, SQLModel, Session, select

from .excel import ExcelCoverLetterManager
from .models import CoverLetter


class CoverLetterManager:

    def __init__(self, sql_file: Path):
        self.engine = create_engine(f'sqlite:///{sql_file}')
        SQLModel.metadata.create_all(self.engine)  # , tables=[CoverLetter])

    def _exec(self, statement):
        with Session(self.engine) as session:
            project_result = session.exec(statement)

            return project_result

    def get(self, cover_letter_id: int) -> CoverLetter:
        with Session(self.engine) as session:
            statement = select(CoverLetter).where(CoverLetter.id == cover_letter_id)
            results = session.exec(statement)
            db_project = results.one()
        return db_project

    def create(self, cover_letter: CoverLetter):
        with Session(self.engine) as session:
            session.add(cover_letter)
            session.commit()
            session.refresh(cover_letter)
        return cover_letter

    def delete(self, cover_letter: CoverLetter):
        with Session(self.engine) as session:
            statement = select(CoverLetter).where(CoverLetter.id == cover_letter.id)
            results = session.exec(statement)
            db_project = results.one()
            session.delete(db_project)
            session.commit()
        return cover_letter

    def update(self, project: CoverLetter):
        with Session(self.engine) as session:
            statement = select(CoverLetter).where(CoverLetter.id == project.id)
            results = session.exec(statement)
            db_project = results.one()
            exclude = ['id', 'created']
            project_dict = project.dict()
            for key, value in project_dict.items():
                if key not in exclude:
                    setattr(db_project, key, value)
            # db_project.jira = 'RRR'
            session.add(db_project)
            session.commit()
            session.refresh(db_project)

    def list(self):
        with Session(self.engine) as session:
            statement = select(CoverLetter)
            projects = session.exec(statement).all()
            return projects


def synchronize_to_db(excel_manager: ExcelCoverLetterManager, db_manager: CoverLetterManager,
                      delete: bool = False):
    excel_cover_letters = excel_manager.read()
    updated_list = list()
    deleted_list = list()
    created_list = list()
    for cover_letter in excel_cover_letters:
        if cover_letter.id is None:
            db_manager.create(cover_letter)
            created_list.append(cover_letter)
        else:
            db_cover_letter = db_manager.get(cover_letter.id)
            if db_cover_letter != cover_letter:
                if delete and db_cover_letter.delete:
                    db_manager.delete(cover_letter)
                    deleted_list.append(cover_letter)
                else:
                    db_manager.update(cover_letter)
                    updated_list.append(cover_letter)
    return created_list, updated_list, deleted_list
