from pathlib import Path

import pytest
import tomllib

from folder.foldermain import Folder
from pydantic_models.config_model import Config


def test_missing_required_tags(tmp_path):  # tmp_path comes from pytest (https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html)

    with open("src/config.toml", "rb") as f:
        config = tomllib.load(f)
    config["input_path"] = Path("tests/data/")

    config = Config(**config)

    with pytest.raises(ValueError):
        missing_required_tags = Folder(folder_full_input=Path("tests/data/missing_required_tags"), folder_main_input=config.input_path, folder_main_output=tmp_path, unwanted_files=config.unwanted_files)
