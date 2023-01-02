from pathlib import Path

import pytest
import tomllib

from folder.foldermain import Folder
from pydantic_models.config_model import Config


def test_album_normal(tmp_path):  # tmp_path comes from pytest (https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html)

    with open("src/config.toml", "rb") as f:
        config = tomllib.load(f)
    config["input_path"] = Path("tests/data/")

    config = Config(**config)

    album_normal = Folder(folder_full_input=Path("tests/data/album_normal"), folder_main_input=config.input_path, folder_main_output=tmp_path, unwanted_files=config.unwanted_files)

    assert album_normal.name.folderpath_beautified.stem == "[Artist TPE1] - Testing Normal Album (2022)"

    assert album_normal.mp3_files[0].name.filepath_beautified.name == "[Artist TPE1] - 01 - Title.mp3"
    assert album_normal.mp3_files[1].name.filepath_beautified.name == "[Artist TPE1] - 02 - Title.mp3"
    assert album_normal.mp3_files[2].name.filepath_beautified.name == "[Artist TPE1] - 03 - Title.mp3"
    assert album_normal.mp3_files[3].name.filepath_beautified.name == "[Artist TPE1] - 04 - Title.mp3"

    assert album_normal.description.only_single_mp3_file == False
    assert album_normal.description.folder_has_same_album == True
    assert album_normal.description.folder_has_same_artist == True
    assert album_normal.description.folder_has_same_date == True
    assert album_normal.description.folder_has_same_disc_number == False
    assert album_normal.description.has_each_file_an_album == True
    assert album_normal.description.has_each_file_a_date == True
    assert album_normal.description.has_each_file_a_disc_number == False
    assert album_normal.description.has_each_file_a_track_number == True
    assert album_normal.description.is_score_or_soundtrack == False
