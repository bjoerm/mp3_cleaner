from beautify_string import string_beautification
from beautify_disc_and_track_number import track_number_beautification
from beautify_disc_and_track_number import extract_track_number_from_slash_format
from beautify_disc_and_track_number import has_cd_string_in_folder_name
from beautify_date import extract_year
from tag_management import ProcessMp3

def test_string_beautification():
    assert string_beautification("Test's test's test`s test´s test'S") == "Test's Test's Test's Test's test's", "Test hyphens"
    assert string_beautification("Ac/Dc AC/DC ac/dc guns 'n' roses") == "ACDC ACDC ACDC Guns 'n' Roses", "Test edge cases"
    assert string_beautification(" lost in      space  Lost in Space ") == "Lost In Space Lost In Space", "Test spaces"
    assert string_beautification("where to? what now???") == "Where To What Now", "Question mark"
    assert string_beautification("I'am") == "I'am", "Test connected words"
    #assert string_beautification("data/now data\yesterday", remove_leading_the=False) == "Data-Now Data-Yesterday", "Test slash"
    assert string_beautification("A feat. B C featuring D E feat F") == "A Feat. B C Feat. D E Feat F", "Test Featuring"
    assert string_beautification("New Song Pt. 4 pt. 5 pt 6") == "New Song Part 4 Part 5 Pt 6", "Test Part"
    assert string_beautification("abC dEF ghi j5L") == "abC dEF Ghi j5L", "Test word contains capital letter - but not at beginning"
    assert string_beautification("m&m M&m") == "M+M M+m", "Test &"
    assert string_beautification("baum,stamm 10,5 Gerd,10 10,Gerd") == "Baum, Stamm 10,5 Gerd,10 10, Gerd", "Test comma and space"
    assert string_beautification(" ") == "", "Test empty 1"
    assert string_beautification("") == "", "Test empty 2"
    assert string_beautification("Nice Track REMIX") == "Nice Track Remix", "Test Remix suffix 1"
    assert string_beautification("Nice Track (REMIX)") == "Nice Track (Remix)", "Test Remix suffix 2"
    assert string_beautification("Nice Track LIVE") == "Nice Track Live", "Test Live suffix 1"
    assert string_beautification("Nice Track (LIVE)") == "Nice Track (Live)", "Test Live suffix 2"


def test_string_beautification_leading_the(input=True): # Switch this to True to easily test it also for that case.
    assert string_beautification("The Beatles ", remove_leading_the=input) == "Beatles", "Test Leading The"
    assert string_beautification(" The Beatles ", remove_leading_the=input) == "Beatles", "Test Leading The"
    assert string_beautification("TheBeatles ", remove_leading_the=input) == "TheBeatles", "Test Leading The"
    assert string_beautification("The-Beatles ", remove_leading_the=input) == "The-Beatles", "Test Leading The"



def test_track_number_beautification():
    assert track_number_beautification(track_number="1", helper_length_max=1, minimum_length=1) == "1", "Test normal"
    assert track_number_beautification(track_number="1", helper_length_max=2, minimum_length=2) == "01", "Test leading zeros 1"
    assert track_number_beautification(track_number="1", helper_length_max=3, minimum_length=2) == "001", "Test leading zeros 2"
    assert track_number_beautification(track_number="11", helper_length_max=2, minimum_length=2) == "11", "Test leading zeros 3"
    assert track_number_beautification(track_number="11", helper_length_max=3, minimum_length=2) == "011", "Test leading zeros 4"
    assert track_number_beautification(track_number="1/16", helper_length_max=2, minimum_length=2) == "01", "Test track number slash tracks on disc 1"
    assert track_number_beautification(track_number="01/16", helper_length_max=2, minimum_length=2) == "01", "Test track number slash tracks on disc 2"
    assert track_number_beautification(track_number="01", helper_length_max=2, minimum_length=2) == "01", "Test existing leading zero 1"
    assert track_number_beautification(track_number="01", helper_length_max=3, minimum_length=2) == "001", "Test existing leading zero 2"
    assert track_number_beautification(track_number="", helper_length_max=3, minimum_length=2) == "", "Test empty input"
    assert track_number_beautification(track_number="01", helper_length_max=1) == "1", "Test removing existing leading zero 1"
    assert track_number_beautification(track_number="001", helper_length_max=2) == "01", "Test removing existing leading zeros 2"


def test_mp3_tags_has_cd_string_in_folder_name():
    """Testing the complex regex."""
    
    assert has_cd_string_in_folder_name("cd 1") == True
    assert has_cd_string_in_folder_name("cd3") == True
    assert has_cd_string_in_folder_name("cd  2asd") == False
    assert has_cd_string_in_folder_name("cd  2 asd") == True
    assert has_cd_string_in_folder_name("cd2aasdfsd") == False
    assert has_cd_string_in_folder_name("12_cd2aasdfsd") == False
    assert has_cd_string_in_folder_name("asd cd2") == True
    assert has_cd_string_in_folder_name("2cd") == True
    assert has_cd_string_in_folder_name("2013-2CD-2013-C4") == True
    assert has_cd_string_in_folder_name("_cd2") == True
    assert has_cd_string_in_folder_name(",cd2 ") == True
    assert has_cd_string_in_folder_name("-23") == False
    assert has_cd_string_in_folder_name("192cd2 ") == False
    assert has_cd_string_in_folder_name("-cd23") == True
    assert has_cd_string_in_folder_name("-1cd-") == True
    assert has_cd_string_in_folder_name("- 1 cd -") == True
    assert has_cd_string_in_folder_name(" cd 2 ") == True
    assert has_cd_string_in_folder_name("_1 cd_") == True
    assert has_cd_string_in_folder_name("2cdaasdf") == False
    assert has_cd_string_in_folder_name("cd123455") == False
    assert has_cd_string_in_folder_name(None) == False
    assert has_cd_string_in_folder_name(50) == False


def test_mp3_tags_extract_year():
    """Testing the regex that extract year (YYYY)."""
    
    assert extract_year("1999-12-12") == "1999"
    assert extract_year("1999") == "1999"
    assert extract_year("20-12-1999") == "1999"
    assert extract_year("1999-10") == "1999"
    assert extract_year("1999-October") == "1999"
    assert extract_year("1999-H1") == "1999"
    assert extract_year("11.11.1999") == "1999"
    assert extract_year("2020-12-12") == "2020"
    assert extract_year("2020") == "2020"
    assert extract_year("20-12-2020") == "2020"
    assert extract_year("2020-10") == "2020"
    assert extract_year("2020-October") == "2020"
    assert extract_year("2020-H1") == "2020"
    assert extract_year("11.11.2020") == "2020"
    assert extract_year("11.11.11") == "11.11.11"
    assert extract_year("11-11-11") == "11-11-11"
    assert extract_year(2020) == "2020"
    assert extract_year(1980) == "1980"
    assert extract_year(None) == None


def test_mp3_extract_track_number_from_slash_format():
    """Testing the regex that extracts the track number from potential 'slash format'."""
    
    assert extract_track_number_from_slash_format("01") == "01"
    assert extract_track_number_from_slash_format("01/") == "01"
    assert extract_track_number_from_slash_format("01/16") == "01"
    assert extract_track_number_from_slash_format("1") == "1"
    assert extract_track_number_from_slash_format("1/") == "1"
    assert extract_track_number_from_slash_format("1/16") == "1"
    assert extract_track_number_from_slash_format(1) == "1"
    assert extract_track_number_from_slash_format(None) == None

