# TODO Could this whole bunch of tests be made simpler by using Pytest parameters?


from beautify_single_number import NumberBeautifier


def test_track_number_beautification():
    """
    This tests the main/public method for beautifying track numbers. It contains all the (private) methods related to track numbers.
    """
    assert NumberBeautifier.beautify_track_number(track_number="", helper_length_max=1, minimum_length=1) == ""
    assert NumberBeautifier.beautify_track_number(track_number="1", helper_length_max=1, minimum_length=1) == "1", "Test normal"
    assert NumberBeautifier.beautify_track_number(track_number="1", helper_length_max=2, minimum_length=2) == "01", "Test leading zeros 1"
    assert NumberBeautifier.beautify_track_number(track_number="1", helper_length_max=3, minimum_length=2) == "001", "Test leading zeros 2"
    assert NumberBeautifier.beautify_track_number(track_number="11", helper_length_max=2, minimum_length=2) == "11", "Test leading zeros 3"
    assert NumberBeautifier.beautify_track_number(track_number="11", helper_length_max=3, minimum_length=2) == "011", "Test leading zeros 4"
    assert NumberBeautifier.beautify_track_number(track_number="1/16", helper_length_max=2, minimum_length=2) == "01", "Test track number slash tracks on disc 1"
    assert NumberBeautifier.beautify_track_number(track_number="01/16", helper_length_max=2, minimum_length=2) == "01", "Test track number slash tracks on disc 2"
    assert NumberBeautifier.beautify_track_number(track_number="01", helper_length_max=2, minimum_length=2) == "01", "Test existing leading zero 1"
    assert NumberBeautifier.beautify_track_number(track_number="01", helper_length_max=3, minimum_length=2) == "001", "Test existing leading zero 2"
    assert NumberBeautifier.beautify_track_number(track_number="", helper_length_max=3, minimum_length=2) == "", "Test empty input"
    assert NumberBeautifier.beautify_track_number(track_number="01", helper_length_max=1, minimum_length=1) == "1", "Test removing existing leading zero 1"
    assert NumberBeautifier.beautify_track_number(track_number="001", helper_length_max=2, minimum_length=2) == "01", "Test removing existing leading zeros 2"
    assert NumberBeautifier.beautify_track_number(track_number=" 1", helper_length_max=1, minimum_length=1) == "1", "Test spaces 1"
    assert NumberBeautifier.beautify_track_number(track_number=" 1 ", helper_length_max=1, minimum_length=1) == "1", "Test spaces 2"
    assert NumberBeautifier.beautify_track_number(track_number=None, helper_length_max=1, minimum_length=1) is None, "Test none"


def test_mp3_extract_track_number_from_slash_format():
    """
    Testing the regex that extracts the track number from potential 'slash format'.
    """
    assert NumberBeautifier.extract_number_from_slash_format("") == ""
    assert NumberBeautifier.extract_number_from_slash_format("01") == "01"
    assert NumberBeautifier.extract_number_from_slash_format("01/") == "01"
    assert NumberBeautifier.extract_number_from_slash_format("01/16") == "01"
    assert NumberBeautifier.extract_number_from_slash_format("1") == "1"
    assert NumberBeautifier.extract_number_from_slash_format("1/") == "1"
    assert NumberBeautifier.extract_number_from_slash_format("1/16") == "1"
    assert NumberBeautifier.extract_number_from_slash_format("1/2") == "1"
    assert NumberBeautifier.extract_number_from_slash_format(1) == "1"
    assert NumberBeautifier.extract_number_from_slash_format(None) is None


def test_mp3_tags_has_cd_string_in_folder_name():
    """
    Testing the complex regex realted to strings that hint for multiple CDs in the folder name.
    """
    assert NumberBeautifier.has_cd_string_in_folder_name("") is False
    assert NumberBeautifier.has_cd_string_in_folder_name("cd 1") is True
    assert NumberBeautifier.has_cd_string_in_folder_name("cd3") is True
    assert NumberBeautifier.has_cd_string_in_folder_name("cd  2asd") is False
    assert NumberBeautifier.has_cd_string_in_folder_name("cd  2 asd") is True
    assert NumberBeautifier.has_cd_string_in_folder_name("cd2aasdfsd") is False
    assert NumberBeautifier.has_cd_string_in_folder_name("12_cd2aasdfsd") is False
    assert NumberBeautifier.has_cd_string_in_folder_name("asd cd2") is True
    assert NumberBeautifier.has_cd_string_in_folder_name("2cd") is True
    assert NumberBeautifier.has_cd_string_in_folder_name("2013-2CD-2013-C4") is True
    assert NumberBeautifier.has_cd_string_in_folder_name("_cd2") is True
    assert NumberBeautifier.has_cd_string_in_folder_name(",cd2 ") is True
    assert NumberBeautifier.has_cd_string_in_folder_name("-23") is False
    assert NumberBeautifier.has_cd_string_in_folder_name("192cd2 ") is False
    assert NumberBeautifier.has_cd_string_in_folder_name("-cd23") is True
    assert NumberBeautifier.has_cd_string_in_folder_name("-1cd-") is True
    assert NumberBeautifier.has_cd_string_in_folder_name("- 1 cd -") is True
    assert NumberBeautifier.has_cd_string_in_folder_name(" cd 2 ") is True
    assert NumberBeautifier.has_cd_string_in_folder_name("_1 cd_") is True
    assert NumberBeautifier.has_cd_string_in_folder_name("2cdaasdf") is False
    assert NumberBeautifier.has_cd_string_in_folder_name("cd123455") is False
    assert NumberBeautifier.has_cd_string_in_folder_name("ACDC 2010") is False
    assert NumberBeautifier.has_cd_string_in_folder_name("wcd") is False
    assert NumberBeautifier.has_cd_string_in_folder_name("great cd") is False
    assert NumberBeautifier.has_cd_string_in_folder_name("great cd 2000") is False
    assert NumberBeautifier.has_cd_string_in_folder_name("great cd 20") is True
    assert NumberBeautifier.has_cd_string_in_folder_name("great cd 2") is True
    assert NumberBeautifier.has_cd_string_in_folder_name(None) is False
    assert NumberBeautifier.has_cd_string_in_folder_name(50) is False
