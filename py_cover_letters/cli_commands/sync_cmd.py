from pathlib import Path

import click

from py_cover_letters.db.excel import ExcelCoverLetterManager
from py_cover_letters.db.sqlite import CoverLetterManager
from py_cover_letters.db.synchronizers import synchronize_to_db
from py_cover_letters.exceptions import CoverLetterException


def sync(source: str, target: str, delete_from_db: bool = False):
    source_file = Path(source)
    target_file = Path(target)
    operation = ''
    if source_file.suffix == '.xlsx' and target_file.suffix == '.sqlite':
        excel_file = source_file
        db_file = target_file
        operation = 'sync_to_db'
    else:
        error_message = f'Target and source files need to be either Excel (.xlsx) or SQLite file (.sqlite).' \
                        f' Source: {source_file.name}, Target: {target_file.name}'
        raise CoverLetterException(error_message)

    excel_manager = ExcelCoverLetterManager(excel_file)
    db_manager = CoverLetterManager(db_file)
    if operation == 'sync_to_db':
        created_list, updated_list, deleted_list, errors_list = synchronize_to_db(excel_manager, db_manager,
                                                                                  delete=delete_from_db)
        return operation, created_list, updated_list, deleted_list, errors_list


@click.command('sync', help='Synchronize between database and Excel.')
@click.option('-s', '--source', help='Source file. Either an Excel (.xlsx) or SQLite (.sqlite) file.')
@click.option('-t', '--target', help='Target file. Either an Excel (.xlsx) or SQLite (.sqlite) file.')
def do_sync(source: str, target: str):
    operation, created_list, updated_list, deleted_list, errors_list = sync(source, target)
    if operation == 'sync_to_db':
        click.echo(f'Created: {len(created_list)}')
        click.echo(f'Updated: {len(updated_list)}')
        click.echo(f'Deleted: {len(deleted_list)}')
        click.echo(f'Errors: {len(errors_list)}')
