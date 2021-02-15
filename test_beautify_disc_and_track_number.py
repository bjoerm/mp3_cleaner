
# TODO Could this whole bunch of tests be made simpler by using Pytest parameters? Yes: https://docs.pytest.org/en/reorganize-docs/new-docs/user/parametrize.html


from beautify_single_disc_or_track_number import DiscAndTrackBeautifier


def test_track_number_beautification():
    """
    This tests the main/public method for beautifying track numbers. It contains all the (private) methods related to track numbers.
    """
    assert DiscAndTrackBeautifier.beautify_track_number(track_number="", helper_length_max=1, minimum_length=1) == ""
    assert DiscAndTrackBeautifier.beautify_track_number(track_number="1", helper_length_max=1, minimum_length=1) == "1", "Test normal"
    assert DiscAndTrackBeautifier.beautify_track_number(track_number="1", helper_length_max=2, minimum_length=2) == "01", "Test leading zeros 1"
    assert DiscAndTrackBeautifier.beautify_track_number(track_number="1", helper_length_max=3, minimum_length=2) == "001", "Test leading zeros 2"
    assert DiscAndTrackBeautifier.beautify_track_number(track_number="11", helper_length_max=2, minimum_length=2) == "11", "Test leading zeros 3"
    assert DiscAndTrackBeautifier.beautify_track_number(track_number="11", helper_length_max=3, minimum_length=2) == "011", "Test leading zeros 4"
    assert DiscAndTrackBeautifier.beautify_track_number(track_number="1/16", helper_length_max=2, minimum_length=2) == "01", "Test track number slash tracks on disc 1"
    assert DiscAndTrackBeautifier.beautify_track_number(track_number="01/16", helper_length_max=2, minimum_length=2) == "01", "Test track number slash tracks on disc 2"
    assert DiscAndTrackBeautifier.beautify_track_number(track_number="01", helper_length_max=2, minimum_length=2) == "01", "Test existing leading zero 1"
    assert DiscAndTrackBeautifier.beautify_track_number(track_number="01", helper_length_max=3, minimum_length=2) == "001", "Test existing leading zero 2"
    assert DiscAndTrackBeautifier.beautify_track_number(track_number="", helper_length_max=3, minimum_length=2) == "", "Test empty input"
    assert DiscAndTrackBeautifier.beautify_track_number(track_number="01", helper_length_max=1, minimum_length=1) == "1", "Test removing existing leading zero 1"
    assert DiscAndTrackBeautifier.beautify_track_number(track_number="001", helper_length_max=2, minimum_length=2) == "01", "Test removing existing leading zeros 2"
    assert DiscAndTrackBeautifier.beautify_track_number(track_number=" 1", helper_length_max=1, minimum_length=1) == "1", "Test spaces 1"
    assert DiscAndTrackBeautifier.beautify_track_number(track_number=" 1 ", helper_length_max=1, minimum_length=1) == "1", "Test spaces 2"
    assert DiscAndTrackBeautifier.beautify_track_number(track_number=None, helper_length_max=1, minimum_length=1) == None, "Test none"



def test_mp3_extract_track_number_from_slash_format():
    """
    Testing the regex that extracts the track number from potential 'slash format'.
    """
    assert DiscAndTrackBeautifier.extract_track_number_from_slash_format("") == ""
    assert DiscAndTrackBeautifier.extract_track_number_from_slash_format("01") == "01"
    assert DiscAndTrackBeautifier.extract_track_number_from_slash_format("01/") == "01"
    assert DiscAndTrackBeautifier.extract_track_number_from_slash_format("01/16") == "01"
    assert DiscAndTrackBeautifier.extract_track_number_from_slash_format("1") == "1"
    assert DiscAndTrackBeautifier.extract_track_number_from_slash_format("1/") == "1"
    assert DiscAndTrackBeautifier.extract_track_number_from_slash_format("1/16") == "1"
    assert DiscAndTrackBeautifier.extract_track_number_from_slash_format(1) == "1"
    assert DiscAndTrackBeautifier.extract_track_number_from_slash_format(None) == None




def test_mp3_tags_has_cd_string_in_folder_name():
    """
    Testing the complex regex realted to strings that hint for multiple CDs in the folder name.
    """
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("") == False
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("cd 1") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("cd3") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("cd  2asd") == False
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("cd  2 asd") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("cd2aasdfsd") == False
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("12_cd2aasdfsd") == False
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("asd cd2") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("2cd") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("2013-2CD-2013-C4") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("_cd2") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name(",cd2 ") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("-23") == False
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("192cd2 ") == False
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("-cd23") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("-1cd-") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("- 1 cd -") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name(" cd 2 ") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("_1 cd_") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("2cdaasdf") == False
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("cd123455") == False
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("ACDC 2010") == False
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("wcd") == False
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("great cd") == False
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("great cd 2000") == False
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("great cd 20") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name("great cd 2") == True
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name(None) == False
    assert DiscAndTrackBeautifier.has_cd_string_in_folder_name(50) == False


