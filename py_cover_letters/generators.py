import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from docxtpl import DocxTemplate

from .utils import run_commands


def get_libreoffice_version():
    which_cmd = ['which', 'libreoffice']
    results, errors = run_commands(which_cmd)
    if len(results) == 0:
        return 'Libreoffice not found', False
    if len(errors) > 0:
        return 'Error running which command.', False

    regexp = re.compile(r"LibreOffice\s(?P<version>(\d\.\d\.\d\.?\d?)\s?(\d*)\(Build:\d+\))")
    command = ['libreoffice', '--version']
    results, errors = run_commands(command)
    if len(errors) > 0:
        return 'Errors running command libreoffice --version', False
    match = regexp.match(results[0])
    if match:
        return match.group('version'), True
    else:
        return results[0], False


def convert_docx_to_pdf(docx_file: Path, output_folder: Path):
    command = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', f'{output_folder}',
               f'{docx_file}']
    result, errors = run_commands(command)

    return result, errors


def write_docx_cover_letter(template_file: Path, context: Dict[str, Any], output_file: Path):
    # Open our master template
    doc = DocxTemplate(template_file)
    # Load them up
    doc.render(context)
    # Save the file with personalized filename
    doc.save(output_file)


if __name__ == '__main__':
    root_folder = Path(__file__).parent.parent.parent.parent
    fixtures_folder = root_folder / 'tests' / 'fixtures'
    out_folder = root_folder / 'output'

    template = fixtures_folder / '_experimental' / 'Cover Letter Template.docx'
    today = datetime.today()
    context = {'today': today.strftime('%b %M %Y'), 'position_name': 'Jedi', 'company_name': 'Jedi Order'}

    cover_letter = out_folder / f'{today.strftime("%Y%m%d")}_cover_{context["company_name"]}' \
                                f'_{context["position_name"]}.pdf'
    cover_letter.unlink(missing_ok=True)

    write_docx_cover_letter(template, context, cover_letter)
