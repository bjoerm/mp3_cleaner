from pathlib import Path

import pytest
import tomllib

from folder.foldermain import Folder
from pydantic_models.config_model import Config


def test_score_normal(tmp_path):  # tmp_path comes from pytest (https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html)

    with open("src/config.toml", "rb") as f:
        config = tomllib.load(f)
    config["input_path"] = Path("tests/data/")

    config = Config(**config)

    score_normal = Folder(folder_full_input=Path("tests/data/score_normal"), folder_main_input=config.input_path, folder_main_output=tmp_path, unwanted_files=config.unwanted_files)

    assert score_normal.name.folderpath_beautified.stem == "[Awesome Movie] - Awesome Movie 1 - First Part (Score) (2022)"

    filenames = []

    for i in range(0, 4):
        filenames.append(score_normal.mp3_files[i].name.filepath_beautified.name)

    filenames.sort()

    assert filenames[0] == "[Artist TPE1] - 01 - Title.mp3"
    assert filenames[1] == "[Artist TPE1] - 02 - Title.mp3"
    assert filenames[2] == "[Artist TPE1] - 03 - Title.mp3"
    assert filenames[3] == "[Artist TPE1] - 04 - Title.mp3"

    assert score_normal.description.only_single_mp3_file == False
    assert score_normal.description.folder_has_same_album == True
    assert score_normal.description.folder_has_same_artist == True
    assert score_normal.description.folder_has_same_date == True
    assert score_normal.description.folder_has_same_disc_number == False
    assert score_normal.description.has_each_file_an_album == True
    assert score_normal.description.has_each_file_a_date == True
    assert score_normal.description.has_each_file_a_disc_number == False
    assert score_normal.description.has_each_file_a_track_number == True
    assert score_normal.description.is_score_or_soundtrack == True
