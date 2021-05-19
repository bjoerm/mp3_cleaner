from beautify_filepaths import FileBeautifier

import pytest
import pandas as pd

# This uses pytest fixtures. See https://pycon.switowski.com/06-testing/pytest/ for a good intro.


@pytest.fixture
def tags_same_values():
    return pd.Series([
        dict(TPE1="Artist 1", TIT2="Title 1", TALB="Album 1", TPOS="1", TDRC="2000")
        , dict(TPE1="Artist 1", TIT2="Title 2", TALB="Album 1", TPOS="1", TDRC="2000")
        ])


@pytest.fixture
def tags_different_values():
    return pd.Series([
        dict(TPE1="Artist 1", TIT2="Title 1", TALB="Album 1", TDRC="2000")
        , dict(TPE1="Artist 2", TIT2="Title 2", TALB="Album 2", TDRC="2001")
        ])


@pytest.fixture
def tags_partially_missing_values():
    return pd.Series([
        dict(TPE1="Artist 1", TIT2="Title 1", TALB="Album 1", TDRC="2000")
        , dict(TPE1=None, TIT2="Title 2", TALB=None, TDRC=None)
        ])


@pytest.fixture
def tags_fully_missing_values():
    return pd.Series([
        dict(TPE1=None, TIT2="Title 1", TALB=None, TDRC=None)
        , dict(TPE1=None, TIT2="Title 2", TALB=None, TDRC=None)
        ])


def test_check_for_same_artist(tags_same_values, tags_different_values, tags_partially_missing_values, tags_fully_missing_values):
    # Artist
    assert FileBeautifier._check_uniqueness_of_tag(tags=tags_fully_missing_values, id3_field="TPE1") is None
    assert FileBeautifier._check_uniqueness_of_tag(tags=tags_same_values, id3_field="TPE1") is True
    assert FileBeautifier._check_uniqueness_of_tag(tags=tags_different_values, id3_field="TPE1") is False
    assert FileBeautifier._check_uniqueness_of_tag(tags=tags_partially_missing_values, id3_field="TPE1") is False

    # Album
    assert FileBeautifier._check_uniqueness_of_tag(tags=tags_fully_missing_values, id3_field="TALB") is None
    assert FileBeautifier._check_uniqueness_of_tag(tags=tags_same_values, id3_field="TALB") is True
    assert FileBeautifier._check_uniqueness_of_tag(tags=tags_different_values, id3_field="TALB") is False
    assert FileBeautifier._check_uniqueness_of_tag(tags=tags_partially_missing_values, id3_field="TALB") is False

    # Date
    assert FileBeautifier._check_uniqueness_of_tag(tags=tags_fully_missing_values, id3_field="TDRC") is None
    assert FileBeautifier._check_uniqueness_of_tag(tags=tags_same_values, id3_field="TDRC") is True
    assert FileBeautifier._check_uniqueness_of_tag(tags=tags_different_values, id3_field="TDRC") is False
    assert FileBeautifier._check_uniqueness_of_tag(tags=tags_partially_missing_values, id3_field="TDRC") is False


@pytest.fixture
def tags_w_disc_and_w_track_number():
    return pd.Series([
        dict(TRCK="01", TALB="Album 1", TPOS="1")
        , dict(TRCK="02", TALB="Album 1", TPOS="1")
        ])


@pytest.fixture
def tags_w_disc_and_wo_track_number():
    return pd.Series([
        dict(TALB="Album 1", TPOS="1")
        , dict(TALB="Album 1", TPOS="1")
        ])


@pytest.fixture
def tags_wo_disc_and_w_track_number():
    return pd.Series([
        dict(TRCK="01", TALB="Album 1")
        , dict(TRCK="02", TALB="Album 1")
        ])


@pytest.fixture
def tags_wo_disc_and_wo_track_number():
    return pd.Series([
        dict(TALB="Album 1")
        , dict(TALB="Album 1")
        ])


@pytest.fixture
def tags_w_disc_and_partial_track_number():
    return pd.Series([
        dict(TRCK="01", TALB="Album 1", TPOS="1")
        , dict(TALB="Album 1", TPOS="1")
        ])


@pytest.fixture
def tags_wo_disc_and_partial_track_number():
    return pd.Series([
        dict(TRCK="01", TALB="Album 1")
        , dict(TALB="Album 1")
        ])


@pytest.fixture
def tags_partial_disc_and_w_track_number():
    return pd.Series([
        dict(TRCK="01", TALB="Album 1", TPOS="1")
        , dict(TRCK="02", TALB="Album 1")
        ])


@pytest.fixture
def tags_partial_disc_and_wo_track_number():
    return pd.Series([
        dict(TALB="Album 1", TPOS="1")
        , dict(TALB="Album 1")
        ])


@pytest.fixture
def tags_partial_disc_and_partial_track_number():
    return pd.Series([
        dict(TALB="Album 1", TPOS="1")
        , dict(TRCK="02", TALB="Album 1")
        ])


@pytest.fixture
def tags_w_disc_and_same_track_number():
    return pd.Series([
        dict(TALB="Album 1", TRCK="01", TPOS="1")
        , dict(TALB="Album 1", TRCK="01", TPOS="1")
        ])


@pytest.fixture
def tags_wo_disc_and_same_track_number():
    return pd.Series([
        dict(TALB="Album 1", TRCK="01")
        , dict(TALB="Album 1", TRCK="01")
        ])


def test_check_existance_of_disc_and_track_number(tags_w_disc_and_w_track_number, tags_w_disc_and_wo_track_number, tags_wo_disc_and_w_track_number, tags_wo_disc_and_wo_track_number, tags_w_disc_and_partial_track_number, tags_wo_disc_and_partial_track_number, tags_partial_disc_and_w_track_number, tags_partial_disc_and_wo_track_number, tags_partial_disc_and_partial_track_number, tags_w_disc_and_same_track_number, tags_wo_disc_and_same_track_number):
    assert FileBeautifier._check_existance_of_disc_and_track_number(tags=tags_w_disc_and_w_track_number) == (True, True)  # First element refers to disc number, second track number.
    assert FileBeautifier._check_existance_of_disc_and_track_number(tags=tags_w_disc_and_wo_track_number) == (True, False)
    assert FileBeautifier._check_existance_of_disc_and_track_number(tags=tags_wo_disc_and_w_track_number) == (False, True)
    assert FileBeautifier._check_existance_of_disc_and_track_number(tags=tags_wo_disc_and_wo_track_number) == (False, False)
    assert FileBeautifier._check_existance_of_disc_and_track_number(tags=tags_w_disc_and_partial_track_number) == (True, False)
    assert FileBeautifier._check_existance_of_disc_and_track_number(tags=tags_wo_disc_and_partial_track_number) == (False, False)
    assert FileBeautifier._check_existance_of_disc_and_track_number(tags=tags_partial_disc_and_w_track_number) == (False, True)
    assert FileBeautifier._check_existance_of_disc_and_track_number(tags=tags_partial_disc_and_wo_track_number) == (False, False)
    assert FileBeautifier._check_existance_of_disc_and_track_number(tags=tags_partial_disc_and_partial_track_number) == (False, False)
    assert FileBeautifier._check_existance_of_disc_and_track_number(tags=tags_w_disc_and_same_track_number) == (True, True)
    assert FileBeautifier._check_existance_of_disc_and_track_number(tags=tags_wo_disc_and_same_track_number) == (False, True)

# TODO Use pytest parameters for FileBeautifier._propose_single_filename_from_single_tag


def test_beautify_string_from_tag():
    """
    Testing the regex that enhances strings from tags.
    """
    assert FileBeautifier._beautify_string_from_tag(tag="Test", add_square_brackets=True) == "[Test]"
    assert FileBeautifier._beautify_string_from_tag(tag=7, add_square_brackets=True) == "[7]"
    assert FileBeautifier._beautify_string_from_tag(tag="Test") == "Test"
    assert FileBeautifier._beautify_string_from_tag(tag=7) == "7"
    assert FileBeautifier._beautify_string_from_tag(tag="") == ""
    assert FileBeautifier._beautify_string_from_tag(tag=" ") == ""
    assert FileBeautifier._beautify_string_from_tag(tag=None) == ""


@pytest.fixture
def tags_same_values_score():
    return pd.Series([
        dict(TPE1="Artist 1", TIT2="Title 1", TALB="Album 1 (Score)", TPOS="1", TDRC="2000")
        , dict(TPE1="Artist 1", TIT2="Title 2", TALB="Album 1 (Score)", TPOS="1", TDRC="2000")
        ])


@pytest.fixture
def tags_same_values_soundtrack():
    return pd.Series([
        dict(TPE1="Artist 1", TIT2="Title 1", TALB="Album 1 (Soundtrack)", TPOS="1", TDRC="2000")
        , dict(TPE1="Artist 1", TIT2="Title 2", TALB="Album 1 (Soundtrack)", TPOS="1", TDRC="2000")
        ])


def test_beautify_folder(tags_same_values, tags_same_values_score, tags_same_values_soundtrack):
    # Normal albums
    assert FileBeautifier._beautify_folder(tags=tags_same_values, has_file_without_tags=False, is_same_artist=True, is_same_album_title=True, is_same_date=True, is_each_track_with_disc_number=True, is_same_disc_number=True) == "[Artist 1] - Album 1 (CD1) (2000)"
    assert FileBeautifier._beautify_folder(tags=tags_same_values, has_file_without_tags=False, is_same_artist=True, is_same_album_title=True, is_same_date=True, is_each_track_with_disc_number=True, is_same_disc_number=False) == "[Artist 1] - Album 1 (2000)"
    assert FileBeautifier._beautify_folder(tags=tags_same_values, has_file_without_tags=True, is_same_artist=True, is_same_album_title=True, is_same_date=True, is_each_track_with_disc_number=True, is_same_disc_number=True) is None
    assert FileBeautifier._beautify_folder(tags=tags_same_values, has_file_without_tags=False, is_same_artist=False, is_same_album_title=True, is_same_date=True, is_each_track_with_disc_number=True, is_same_disc_number=True) is None
    assert FileBeautifier._beautify_folder(tags=tags_same_values, has_file_without_tags=False, is_same_artist=True, is_same_album_title=False, is_same_date=True, is_each_track_with_disc_number=True, is_same_disc_number=True) is None
    assert FileBeautifier._beautify_folder(tags=tags_same_values, has_file_without_tags=False, is_same_artist=True, is_same_album_title=True, is_same_date=False, is_each_track_with_disc_number=True, is_same_disc_number=True) == "[Artist 1] - Album 1 (CD1)"
    assert FileBeautifier._beautify_folder(tags=tags_same_values, has_file_without_tags=False, is_same_artist=True, is_same_album_title=True, is_same_date=True, is_each_track_with_disc_number=False, is_same_disc_number=True) == "[Artist 1] - Album 1 (2000)"
    assert FileBeautifier._beautify_folder(tags=tags_same_values, has_file_without_tags=False, is_same_artist=True, is_same_album_title=True, is_same_date=True, is_each_track_with_disc_number=False, is_same_disc_number=True) == "[Artist 1] - Album 1 (2000)"
    assert FileBeautifier._beautify_folder(tags=tags_same_values, has_file_without_tags=False, is_same_artist=True, is_same_album_title=True, is_same_date=True, is_each_track_with_disc_number=False, is_same_disc_number=False) == "[Artist 1] - Album 1 (2000)"
    assert FileBeautifier._beautify_folder(tags=tags_same_values, has_file_without_tags=False, is_same_artist=True, is_same_album_title=True, is_same_date=True, is_each_track_with_disc_number=False, is_same_disc_number=None) == "[Artist 1] - Album 1 (2000)"
    assert FileBeautifier._beautify_folder(tags=tags_same_values, has_file_without_tags=False, is_same_artist=True, is_same_album_title=True, is_same_date=False, is_each_track_with_disc_number=False, is_same_disc_number=None) == "[Artist 1] - Album 1"
    assert FileBeautifier._beautify_folder(tags=tags_same_values, has_file_without_tags=False, is_same_artist=True, is_same_album_title=True, is_same_date=None, is_each_track_with_disc_number=False, is_same_disc_number=None) == "[Artist 1] - Album 1"

    # Soundtracks and scores
    assert FileBeautifier._beautify_folder(tags=tags_same_values_score, has_file_without_tags=False, is_same_artist=True, is_same_album_title=True, is_same_date=True, is_each_track_with_disc_number=True, is_same_disc_number=True) == "[Album 1] - Album 1 (Score) (CD1) (2000)"
    assert FileBeautifier._beautify_folder(tags=tags_same_values_score, has_file_without_tags=False, is_same_artist=True, is_same_album_title=True, is_same_date=True, is_each_track_with_disc_number=True, is_same_disc_number=False) == "[Album 1] - Album 1 (Score) (2000)"
    assert FileBeautifier._beautify_folder(tags=tags_same_values_soundtrack, has_file_without_tags=False, is_same_artist=True, is_same_album_title=True, is_same_date=True, is_each_track_with_disc_number=True, is_same_disc_number=True) == "[Album 1] - Album 1 (Soundtrack) (CD1) (2000)"
    assert FileBeautifier._beautify_folder(tags=tags_same_values_score, has_file_without_tags=False, is_same_artist=False, is_same_album_title=True, is_same_date=True, is_each_track_with_disc_number=True, is_same_disc_number=True) == "[Album 1] - Album 1 (Score) (CD1) (2000)"
    assert FileBeautifier._beautify_folder(tags=tags_same_values_soundtrack, has_file_without_tags=False, is_same_artist=False, is_same_album_title=True, is_same_date=True, is_each_track_with_disc_number=True, is_same_disc_number=True) == "[Album 1] - Album 1 (Soundtrack) (CD1) (2000)"
