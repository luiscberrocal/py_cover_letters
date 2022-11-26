import re
from datetime import datetime
from pathlib import Path

from py_cover_letters import ConfigurationManager
from py_cover_letters.generators import write_docx_cover_letter, convert_docx_to_pdf
from py_cover_letters.utils import get_libreoffice_version


def test_get_libreoffice_version():
    regexp = re.compile(r"(\d\.\d\.\d\.?\d?)\s?(\d*)\(Build:\d+\)")
    version, is_valid = get_libreoffice_version()
    assert regexp.match(version) is not None
    assert is_valid


def test_write_cover_letter(fixtures_folder, output_folder):
    template = fixtures_folder / 'templates' / 'Cover Letter Template.docx'
    assert template.exists()
    today = datetime.today()
    context = {'date': today.strftime('%b %M %Y'), 'position_name': 'Jedi Knight',
               'company_name': 'Jedi Order Council'}

    docx_filename = f'{today.strftime("%Y%m%d")}_cover_{context["company_name"]}_{context["position_name"]}.docx'
    cover_letter = output_folder / docx_filename
    cover_letter.unlink(missing_ok=True)

    write_docx_cover_letter(template, context, cover_letter)
    assert cover_letter.exists()


def test_convert_docx_to_pdf(fixtures_folder, output_folder):
    config = ConfigurationManager()
    configuration = config.get_configuration()
    template = Path(configuration['cover_letters']['template_folder']) / configuration['cover_letters'][
        'default_template']
    # template = fixtures_folder / '_experimental' / 'Cover Letter Template.docx'
    today = datetime.today()
    context = {'date': today.strftime('%B %-d, %Y'), 'position_name': 'Jedi Knight',
               'company_name': 'Jedi Order Council'}
    naming_context = context  # humps.camelize(context)
    docx_filename = f'{today.strftime("%Y%m%d")}_cover_{naming_context["company_name"]}' \
                    f'_{naming_context["position_name"]}.docx'
    cover_letter = output_folder / docx_filename
    cover_letter.unlink(missing_ok=True)

    write_docx_cover_letter(template, context, cover_letter)
    assert cover_letter.exists()

    pdf = convert_docx_to_pdf(cover_letter, output_folder)
