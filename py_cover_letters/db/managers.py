from pathlib import Path

from sqlmodel import create_engine, SQLModel, Session, select

from py_cover_letters.db.models import CoverLetter


class CoverLetterManager:

    def __init__(self, sql_file: Path):
        self.engine = create_engine(f'sqlite:///{sql_file}')
        SQLModel.metadata.create_all(self.engine)  # , tables=[CoverLetter])

    def _exec(self, statement):
        with Session(self.engine) as session:
            project_result = session.exec(statement)

            return project_result

    def create(self, project: CoverLetter):
        with Session(self.engine) as session:
            session.add(project)
            session.commit()

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
