from pathlib import Path
from shutil import rmtree

import pytest


@pytest.fixture(autouse=True)
def tmp_module():
    tmp_module = Path("tests") / "tmp_module"

    tmp_module.mkdir()
    (tmp_module / "__init__.py").touch()

    yield tmp_module

    rmtree(tmp_module, ignore_errors=True)
