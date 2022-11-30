from pprint import pprint

from py_cover_letters.cli_commands.generate_cmd import do_generate


def test_do_generate(excel_file_without_id, docx_template_file):
    results = do_generate(excel_file_without_id, docx_template_file)
    assert len(results) == 11
    for result in results:
        pprint(result)
