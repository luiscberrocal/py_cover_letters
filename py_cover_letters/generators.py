import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from docxtpl import DocxTemplate

from .utils import run_commands


def convert_docx_to_pdf(docx_file: Path, output_folder: Optional[Path]):
    if output_folder is None:
        output_folder = docx_file.parent

    command = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', f'{output_folder}',
               f'{docx_file}']
    result, errors = run_commands(command)

    return result, errors


def write_docx_cover_letter(template_file: Path, context: Dict[str, Any], output_file: Path) -> None:
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

