from pathlib import Path

import pytest
import tomllib

from folder.foldermain import Folder
from pydantic_models.config_model import Config


def test_album_mixed_artists(tmp_path):  # tmp_path comes from pytest (https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html)

    with open("src/config.toml", "rb") as f:
        config = tomllib.load(f)
    config = Config(**config)

    album_mixed = Folder(folder_full_input=Path("tests/data/album_mixed"), folder_main_input=Path("tests/data/"), folder_main_output=tmp_path, unwanted_files=config.unwanted_files)

    assert album_mixed.name.folderpath_beautified.stem == "[Various Artists] - Testing Normal Album (2022)"

    assert album_mixed.mp3_files[0].name.filepath_beautified.name == "01 - [Artist TPE1] - Title.mp3"
    assert album_mixed.mp3_files[1].name.filepath_beautified.name == "02 - [Artist TPE1] - Title.mp3"
    assert album_mixed.mp3_files[2].name.filepath_beautified.name == "03 - [Another Artist TPE1] - Title.mp3"
    assert album_mixed.mp3_files[3].name.filepath_beautified.name == "04 - [Another Artist TPE1] - Title.mp3"

    assert album_mixed.description.only_single_mp3_file == False
    assert album_mixed.description.folder_has_same_album == True
    assert album_mixed.description.folder_has_same_artist == False
    assert album_mixed.description.folder_has_same_date == True
    assert album_mixed.description.folder_has_same_disc_number == False
    assert album_mixed.description.has_each_file_an_album == True
    assert album_mixed.description.has_each_file_a_date == True
    assert album_mixed.description.has_each_file_a_disc_number == False
    assert album_mixed.description.has_each_file_a_track_number == True
    assert album_mixed.description.is_score_or_soundtrack == False
