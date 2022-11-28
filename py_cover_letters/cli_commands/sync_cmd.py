from pathlib import Path


def sync(source: str, target: str):
    source_file = Path(source)
    target_file = Path(target)
