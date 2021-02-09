from beautify_multiple_filenames import FileBeautifier

import pytest
import pandas as pd

# This uses pytest fixtures. See https://pycon.switowski.com/06-testing/pytest/ for a good intro.

@pytest.fixture
def tags_same_artist():
    return(
        pd.Series([
            dict(TPE1="Artist 1", TIT2="Title 1")
            , dict(TPE1="Artist 1", TIT2="Title 2")
            ])
        )

@pytest.fixture
def tags_different_artist():
    return(
        pd.Series([
            dict(TPE1="Artist 1", TIT2="Title 1")
            , dict(TPE1="Artist 2", TIT2="Title 2")
            ])
        )

@pytest.fixture
def tags_partially_missing_artist():
    return(
        pd.Series([
            dict(TPE1="Artist 1", TIT2="Title 1")
            , dict(TPE1=None, TIT2="Title 2")
            ])
        )

@pytest.fixture
def tags_fully_missing_artist():
    return(
        pd.Series([
            dict(TPE1=None, TIT2="Title 1")
            , dict(TPE1=None, TIT2="Title 2")
            ])
        )


def test_check_for_same_artist(tags_same_artist, tags_different_artist, tags_partially_missing_artist, tags_fully_missing_artist):
    assert FileBeautifier._check_for_same_artist(tags=tags_fully_missing_artist) == None # BUG Fix this case! Maybe also have tags_partially_missing_artist return None.
    assert FileBeautifier._check_for_same_artist(tags=tags_same_artist) == True
    assert FileBeautifier._check_for_same_artist(tags=tags_different_artist) == False
    assert FileBeautifier._check_for_same_artist(tags=tags_partially_missing_artist) == False


@pytest.fixture
def tags_w_disc_and_w_track_number():
    return(
        pd.Series([
            dict(TRCK="01", TALB="Album 1", TPOS="1")
            , dict(TRCK="02", TALB="Album 1", TPOS="1")
            ])
        )

@pytest.fixture
def tags_w_disc_and_wo_track_number():
    return(
        pd.Series([
            dict(TALB="Album 1", TPOS="1")
            , dict(TALB="Album 1", TPOS="1")
            ])
        )

@pytest.fixture
def tags_wo_disc_and_w_track_number():
    return(
        pd.Series([
            dict(TRCK="01", TALB="Album 1")
            , dict(TRCK="02", TALB="Album 1")
            ])
        )

@pytest.fixture
def tags_wo_disc_and_wo_track_number():
    return(
        pd.Series([
            dict(TALB="Album 1")
            , dict(TALB="Album 1")
            ])
        )

@pytest.fixture
def tags_w_disc_and_partial_track_number():
    return(
        pd.Series([
            dict(TRCK="01", TALB="Album 1", TPOS="1")
            , dict(TALB="Album 1", TPOS="1")
            ])
        )

@pytest.fixture
def tags_wo_disc_and_partial_track_number():
    return(
        pd.Series([
            dict(TRCK="01", TALB="Album 1")
            , dict(TALB="Album 1")
            ])
        )

@pytest.fixture
def tags_partial_disc_and_w_track_number():
    return(
        pd.Series([
            dict(TRCK="01", TALB="Album 1", TPOS="1")
            , dict(TRCK="02", TALB="Album 1")
            ])
        )

@pytest.fixture
def tags_partial_disc_and_wo_track_number():
    return(
        pd.Series([
            dict(TALB="Album 1", TPOS="1")
            , dict(TALB="Album 1")
            ])
        )

@pytest.fixture
def tags_partial_disc_and_partial_track_number():
    return(
        pd.Series([
            dict(TALB="Album 1", TPOS="1")
            , dict(TRCK="02", TALB="Album 1")
            ])
        )

@pytest.fixture
def tags_w_disc_and_same_track_number():
    return(
        pd.Series([
            dict(TALB="Album 1", TRCK="01", TPOS="1")
            , dict(TALB="Album 1", TRCK="01", TPOS="1")
            ])
        )

@pytest.fixture
def tags_wo_disc_and_same_track_number():
    return(
        pd.Series([
            dict(TALB="Album 1", TRCK="01")
            , dict(TALB="Album 1", TRCK="01")
            ])
        )


def test_check_existance_of_disc_and_track_number(tags_w_disc_and_w_track_number, tags_w_disc_and_wo_track_number, tags_wo_disc_and_w_track_number, tags_wo_disc_and_wo_track_number, tags_w_disc_and_partial_track_number, tags_wo_disc_and_partial_track_number, tags_partial_disc_and_w_track_number, tags_partial_disc_and_wo_track_number, tags_partial_disc_and_partial_track_number, tags_w_disc_and_same_track_number, tags_wo_disc_and_same_track_number):
    assert FileBeautifier._check_existance_of_disc_and_track_number(tags=tags_w_disc_and_w_track_number) == (True, True) # First element refers to disc number, second track number.
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
