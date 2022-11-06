import pytest

from file import File


@pytest.mark.parametrize(
    "name, main_field, helper_field, expected_output",
    [
        ["Both", "Track artist", "Album artist", "Track artist"],
        ["Missing Track Artist", None, "Album artist", "Album artist"],
        ["Missing Album Artist", "Track artist", None, "Track artist"],
        ["None", None, None, None],
        ["Both", 2000, 2010, 2000],
        ["Missing Release Year", None, 2010, 2010],
        ["Missing Record Year", 2000, None, 2000],
        ["None", None, None, None],
    ],
)
def test_check_alternative_fields(name, main_field, helper_field, expected_output):
    assert File.check_alternative_fields(main_field, helper_field) == (expected_output, None), name


@pytest.mark.parametrize(
    "name, arist_in, track_in, artist_out, track_out",
    [
        ["Normal", "artist", "track", "artist", "track"],
        ["Normal", "artist", "track (feat. abc)", "artist", "track (feat. abc)"],
        ["Missing artist", None, "track", None, "track"],
        ["Missing track", "artist", None, "artist", None],
        ["None", None, None, None, None],
        ["Feat With Brackets", "artist (feat. abc)", "track", "artist", "track (feat. abc)"],
        ["Feat No Brackets", "artist feat. abc", "track", "artist", "track (feat. abc)"],
    ],
)
def test_check_alternative_fields(name, arist_in, track_in, artist_out, track_out):
    assert File.check_feat_in_artist(arist_in, track_in) == (artist_out, track_out), name
