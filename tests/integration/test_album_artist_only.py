from pathlib import Path

import pytest
import tomllib

from folder.foldermain import Folder
from pydantic_models.config_model import Config


def test_album_artist_only(tmp_path):  # tmp_path comes from pytest (https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html)
    """Case where instead of a artist only an album artist is found. This is then used as artist."""

    with open("src/config.toml", "rb") as f:
        config = tomllib.load(f)
    config["input_path"] = Path("tests/data/")

    config = Config(**config)

    album_artist_only = Folder(folder_full_input=Path("tests/data/album_artist_only"), folder_main_input=config.input_path, folder_main_output=tmp_path, unwanted_files=config.unwanted_files)

    assert album_artist_only.name.folderpath_beautified.stem == "album_artist_only"

    assert album_artist_only.mp3_files[0].name.filepath_beautified.name == "[Albumartist TPE1] - Title.mp3"

    assert album_artist_only.description.only_single_mp3_file == True
    assert album_artist_only.description.folder_has_same_album == False
    assert album_artist_only.description.folder_has_same_artist == True
    assert album_artist_only.description.folder_has_same_date == False
    assert album_artist_only.description.folder_has_same_disc_number == False
    assert album_artist_only.description.has_each_file_an_album == False
    assert album_artist_only.description.has_each_file_a_date == False
    assert album_artist_only.description.has_each_file_a_disc_number == False
    assert album_artist_only.description.has_each_file_a_track_number == False
    assert album_artist_only.description.is_score_or_soundtrack == False
