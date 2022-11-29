from pprint import pprint

from py_cover_letters.cli_commands.generate_cmd import do_generate


def test_do_generate():
    results = do_generate()
    assert len(results) == 11
    for result in results:
        pprint(result)
