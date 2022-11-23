import pytest

from mp3_file import MP3File

# from mp3_file import MP3File


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
def test_check_fallback_tag_fields(name, main_field, helper_field, expected_output):
    assert MP3File.check_fallback_tag_fields(main_field=main_field, helper_field=helper_field) == (expected_output, None), name


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
def test_check_feat_in_artist(name, arist_in, track_in, artist_out, track_out):
    assert MP3File.check_feat_in_artist(album_artist=arist_in, track=track_in) == (artist_out, track_out), name


@pytest.mark.parametrize(
    "name, input_track, output_track, output_suffix",
    [
        ["No Suffix", "Track", "Track", None],
        ["One Suffix", "Track (Feat. ABC)", "Track (Feat. ABC)", None],
        ["Two Suffixes", "Track (Feat. ABC) (Live)", "Track", "(Feat. ABC) (Live)"],
        ["Two Suffixes", "Track (Live) (Feat. ABC)", "Track", "(Live) (Feat. ABC)"],
        ["Many Suffixes", "Track (Remix) (Acoustic) (Live) (Feat. ABC)", "Track", "(Remix) (Acoustic) (Live) (Feat. ABC)"],
    ],
)
def test_extract_suffixes(name, input_track, output_track, output_suffix):
    assert MP3File._extract_suffixes(track_name=input_track) == (output_track, output_suffix), name


@pytest.mark.parametrize(
    "name, input, expected_output",
    [
        ["No Suffix", "Track", "Track"],
        ["One Suffix", "Track (Feat. ABC)", "Track (Feat. ABC)"],
        ["Two Suffixes", "Track (Feat. ABC) (Live)", "Track (Feat. ABC) (Live)"],
        ["Two Suffixes", "Track (Live) (Feat. ABC)", "Track (Feat. ABC) (Live)"],
        ["Many Suffixes", "Track (Remix) (Acoustic) (Live) (Feat. ABC)", "Track (Remix) (Acoustic) (Feat. ABC) (Live)"],
    ],
)
def test_sort_track_name_suffixes(name, input, expected_output):
    assert MP3File.sort_track_name_suffixes(track_name=input) == expected_output, name


@pytest.mark.parametrize(
    "name, number_current, leading_zeros, expected_output",
    [
        ["General", 1, 1, "1"],
        ["General", 1, 2, "01"],
        ["General", 1, 3, "001"],
        ["General", 2, 1, "2"],
        ["General", 2, 2, "02"],
        ["General", 2, 3, "002"],
        ["General", 10, 2, "10"],
        ["General", 10, 3, "010"],
        ["None", 1, None, None],
        ["Edge Case that shouldn't be possible", 10, 1, "10"],
    ],
)
def test_add_leading_zeros(name, number_current, leading_zeros, expected_output):
    assert MP3File._add_leading_zeros(number_current=number_current, leading_zeros=leading_zeros) == expected_output, name
