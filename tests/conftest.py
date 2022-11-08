import json
from datetime import datetime
from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def output_folder():
    folder = Path(__file__).parent.parent / 'output'
    return folder


@pytest.fixture(scope='session')
def fixtures_folder():
    folder = Path(__file__).parent.parent / 'tests' / 'fixtures'
    return folder


