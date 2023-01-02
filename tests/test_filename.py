import pytest

from file.filename import MP3FileName


@pytest.mark.parametrize(
    "name, has_each_file_a_disc_number, has_each_file_a_track_number, tag_disc, tag_track, expected_output",
    [
        ["All there", True, True, "1", "01", "101 - "],
        ["All there, long disc", True, True, "01", "01", "0101 - "],
        ["Only track", False, True, None, "01", "01 - "],
        ["Only disc", True, False, None, "01", ""],
        ["None", False, False, None, None, ""],
    ],
)
def test_generate_disc_track_number(name, has_each_file_a_disc_number, has_each_file_a_track_number, tag_disc, tag_track, expected_output):
    assert MP3FileName._generate_disc_track_number(has_each_file_a_disc_number=has_each_file_a_disc_number, has_each_file_a_track_number=has_each_file_a_track_number, tag_disc=tag_disc, tag_track=tag_track) == expected_output, name


@pytest.mark.parametrize(
    "name, tag_artist, tag_title, tag_disc, tag_track, only_single_mp3_file, folder_has_same_artist, has_each_file_a_disc_number, has_each_file_a_track_number, expected_output",
    [
        ["Same artist: All there", "Artist", "Title", "1", "01", False, True, True, True, "[Artist] - 101 - Title.mp3"],
        ["Same artist: All there, single file", "Artist", "Title", "1", "01", True, True, True, True, "[Artist] - Title.mp3"],
        ["Same artist: No disc", "Artist", "Title", None, "01", False, True, False, True, "[Artist] - 01 - Title.mp3"],
        ["Same artist: No track", "Artist", "Title", "1", None, False, True, True, False, "[Artist] - Title.mp3"],
        ["Same artist: No disc, no track", "Artist", "Title", None, None, False, True, False, False, "[Artist] - Title.mp3"],
        ["Different artists: All there", "Artist", "Title", "1", "01", False, False, True, True, "101 - [Artist] - Title.mp3"],
        ["Different artists: No disc", "Artist", "Title", None, "01", False, False, False, True, "01 - [Artist] - Title.mp3"],
        ["Different artists: No track", "Artist", "Title", "1", None, False, False, True, False, "[Artist] - Title.mp3"],
        ["Different artists: No disc, no track", "Artist", "Title", None, None, False, False, False, False, "[Artist] - Title.mp3"],
    ],
)
def test_generate_beautified_filename(name, tag_artist, tag_title, tag_disc, tag_track, only_single_mp3_file, folder_has_same_artist, has_each_file_a_disc_number, has_each_file_a_track_number, expected_output):
    assert (
        MP3FileName.generate_beautified_filename(
            tag_artist=tag_artist,
            tag_title=tag_title,
            tag_disc=tag_disc,
            tag_track=tag_track,
            only_single_mp3_file=only_single_mp3_file,
            folder_has_same_artist=folder_has_same_artist,
            has_each_file_a_disc_number=has_each_file_a_disc_number,
            has_each_file_a_track_number=has_each_file_a_track_number,
        )
        == expected_output
    ), name
