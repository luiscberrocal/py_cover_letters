import datetime
from pathlib import Path
from typing import Dict, Any

from docxtpl import DocxTemplate

from .utils import run_commands


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


def clean_filename(filename: str):
    new_name = filename.replace('.', '').replace(',', '').replace(' ', '_')
    return new_name


def build_cover_letter_filename(output_folder: Path, template_context: Dict[str, Any]) -> Path:
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    company_name = clean_filename(template_context['company_name'])
    position_name = clean_filename(template_context['position_name'])
    base_name = f'{timestamp}_{company_name}_{position_name}.docx'
    cover_letter_file = output_folder / base_name
    return cover_letter_file

# if __name__ == '__main__':
#     root_folder = Path(__file__).parent.parent.parent.parent
#     fixtures_folder = root_folder / 'tests' / 'fixtures'
#     out_folder = root_folder / 'output'
#
#     template = fixtures_folder / '_experimental' / 'Cover Letter Template.docx'
#     today = datetime.today()
#     context = {'today': today.strftime('%b %M %Y'), 'position_name': 'Jedi', 'company_name': 'Jedi Order'}
#
#     cover_letter = out_folder / f'{today.strftime("%Y%m%d")}_cover_{context["company_name"]}' \
#                                 f'_{context["position_name"]}.pdf'
#     cover_letter.unlink(missing_ok=True)
#
#     write_docx_cover_letter(template, context, cover_letter)
