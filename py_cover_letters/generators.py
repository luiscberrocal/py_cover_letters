import datetime
import re
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union, List

from docxtpl import DocxTemplate

from .utils import run_commands


def convert_docx_to_pdf(docx_file: Path,
                        output_folder: Optional[Path] = None) -> Tuple[Union[Path, None], List[Dict[str, Any]]]:
    if output_folder is None:
        output_folder = docx_file.parent

    command = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', f'{output_folder}',
               f'{docx_file}']
    result, errors = run_commands(command)
    convert_regex = re.compile(r"convert\s(?P<docx>[\w\/\s]+\.docx)\s\-\>\s(?P<pdf>[\w\/\s]+\.pdf).+")
    overwrite_regex = re.compile(r"Overwriting\:\s(?P<pdf>[\w\/\s]+\.pdf)")
    errors_regex = re.compile(r'(?P<error_type>Warning|Error)\:(?P<message>.+)')
    errors_list = list()
    pdf = None
    if len(result) == 1:
        match = convert_regex.match(result[0])
        if match:
            pdf = Path(match.group('pdf'))
    elif len(result) == 2:
        match = convert_regex.match(result[0])
        if match:
            pdf = Path(match.group('pdf'))
        match = overwrite_regex.match(result[1])
        if not match:
            errors_list.append({'warning': result[1]})
    else:
        errors_list.append({'error': 'No PDF was created.'})
    for error in errors:
        match = errors_regex.match(error)
        if match:
            error_type = match.group('error_type').lower()
            errors_list.append({error_type: match.group('message')})
    return pdf, errors_list


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
