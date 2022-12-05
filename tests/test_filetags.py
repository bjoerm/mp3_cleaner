import pytest

from file.tags import MP3FileTags


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
    assert MP3FileTags._check_fallback_tag_fields(main_field=main_field, helper_field=helper_field) == (expected_output, None), name


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
    assert MP3FileTags._check_feat_in_artist(album_artist=arist_in, track=track_in) == (artist_out, track_out), name


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
    assert MP3FileTags._extract_suffixes(track_name=input_track) == (output_track, output_suffix), name


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
    assert MP3FileTags._sort_track_name_suffixes(track_name=input) == expected_output, name


@pytest.mark.parametrize(
    "name, number_current, leading_zeros, expected_output",
    [
        ["General", "1", 1, "1"],
        ["General", "1", 2, "01"],
        ["General", "1", 3, "001"],
        ["General", "2", 1, "2"],
        ["General", "2", 2, "02"],
        ["General", "2", 3, "002"],
        ["General", "10", 2, "10"],
        ["General", "10", 3, "010"],
        ["None", "1", None, None],
        ["Edge Case that shouldn't be possible", "10", 1, "10"],
    ],
)
def test_add_leading_zeros(name, number_current, leading_zeros, expected_output):
    assert MP3FileTags._add_leading_zeros(number_current=number_current, leading_zeros=leading_zeros) == expected_output, name


@pytest.mark.parametrize(
    "name, foldername, expected_output",
    [
        ["No cd number", "No cd Number", None],
        ["A cd number", "Folder name (CD1)", "1"],
        ["A cd number", "Folder name (CD 2)", "2"],
        ["A cd number", "Folder name CD3", "3"],
        ["Underscores", "CD_3", "3"],
        ["Underscores", "_CD_3", "3"],
        ["A cd number", "Folder name CD 4", "4"],
        ["A disc number", "Folder name (Disc1)", "1"],
        ["A disc number", "Folder name (Disc 2)", "2"],
        ["A disc number", "Folder name Disc3", "3"],
        ["A disc number", "Folder name Disc 4", "4"],
        ["No cd number", "The Best CD", None],
        ["No cd number", "The Best CD from 2000", None],
        ["No cd number", "The Best 1 CD from 2000", None],
        ["Possible Edge Case", "ACDC 2", None],
        ["Possible Edge Case", "ACDC 2 CD3", "3"],
        ["Possible Edge Case", "ACDC 2 CD3 (2004)", "3"],
        ["Possible Edge Case", "ACD 2", None],
        ["None", None, None],
    ],
)
def test_find_disc_number_in_foldername(name, foldername, expected_output):
    assert MP3FileTags._find_disc_number_in_foldername(foldername=foldername) == expected_output, name


@pytest.mark.parametrize(
    "name, folder_has_same_disc_number, disc_number, foldername, expected_output",
    [
        ["None", False, None, "Foldername", None],
        ["Disc 1 - Same Tags in Folder", True, "1", "Foldername", None],
        ["Disc 1 - Different Tags in Folder", False, "1", "Foldername", "1"],
        ["Disc 1 - Same Tags in Folder but Foldername", True, "1", "Foldername (CD1)", "1"],
        ["Disc 1 - Same Tags in Folder but Foldername", True, "1", "Foldername CD1", "1"],
        ["Disc 2 - Same Tags in Folder", True, "2", "Foldername", "2"],
        ["Disc 2 - Different Tags in Folder", False, "2", "Foldername", "2"],
        ["Disc in Tag but not Foldername", False, "2", "Foldername", "2"],
        ["Disc in Foldername", False, None, "Foldername (CD1)", "1"],
    ],
)
def test_improve_disc_number(name, folder_has_same_disc_number, disc_number, foldername, expected_output):
    assert MP3FileTags._improve_disc_number(folder_has_same_disc_number=folder_has_same_disc_number, disc_number=disc_number, foldername=foldername) == expected_output, name
